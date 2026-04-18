"""
LLM Integration module for GenAI analysis
"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMAnalyzer(ABC):
    """Base class for LLM analyzers"""
    
    @abstractmethod
    def analyze_statistics(self, statistics: Dict[str, Any], context: str = "") -> str:
        """Generate insights from statistics"""
        pass


class OpenAIAnalyzer(LLMAnalyzer):
    """OpenAI-based analyzer"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        try:
            import openai
            openai.api_key = api_key
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise
    
    def analyze_statistics(self, statistics: Dict[str, Any], context: str = "") -> str:
        """Generate insights using OpenAI"""
        prompt = self._build_prompt(statistics, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst specialized in receipt data analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return f"Error generating analysis: {str(e)}"


class AnthropicAnalyzer(LLMAnalyzer):
    """Anthropic Claude-based analyzer"""
    
    def __init__(self, api_key: str, model: str = "claude-3-haiku-20240307"):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = model
        except ImportError:
            logger.error("Anthropic library not installed. Install with: pip install anthropic")
            raise
    
    def analyze_statistics(self, statistics: Dict[str, Any], context: str = "") -> str:
        """Generate insights using Anthropic Claude"""
        prompt = self._build_prompt(statistics, context)
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                system="You are a financial analyst specialized in receipt data analysis.",
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Error calling Anthropic API: {str(e)}")
            return f"Error generating analysis: {str(e)}"


class OllamaAnalyzer(LLMAnalyzer):
    """Local Ollama-based analyzer"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        try:
            import requests
            self.requests = requests
            self.base_url = base_url
            self.model = model
            # Test connection
            self._test_connection()
        except ImportError:
            logger.error("Requests library not installed. Install with: pip install requests")
            raise
    
    def _test_connection(self):
        """Test connection to Ollama server"""
        try:
            response = self.requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                raise ConnectionError("Ollama server not responding")
        except Exception as e:
            logger.warning(f"Ollama connection test failed: {str(e)}")
    
    def analyze_statistics(self, statistics: Dict[str, Any], context: str = "") -> str:
        """Generate insights using Ollama"""
        prompt = self._build_prompt(statistics, context)
        
        try:
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60,
            )
            
            if response.status_code == 200:
                return response.json().get("response", "No response generated")
            else:
                return f"Error from Ollama: {response.status_code}"
        except Exception as e:
            logger.error(f"Error calling Ollama: {str(e)}")
            return f"Error generating analysis: {str(e)}"


class MockAnalyzer(LLMAnalyzer):
    """Mock analyzer for testing without API keys"""
    
    def analyze_statistics(self, statistics: Dict[str, Any], context: str = "") -> str:
        """Generate mock insights"""
        financial = statistics.get('financial_stats', {})
        company = statistics.get('company_stats', {})
        
        analysis = f"""
FINANCIAL ANALYSIS REPORT

This analysis covers {statistics.get('total_receipts', 0)} receipt records.

Key Findings:

1. Transaction Volume: The dataset contains {statistics.get('total_receipts', 0)} receipt transactions with a total value of ${financial.get('sum', 0):,.2f}.

2. Average Transaction Value: The average receipt amount is ${financial.get('average', 0):,.2f}, ranging from ${financial.get('min', 0):,.2f} to ${financial.get('max', 0):,.2f}. This indicates {'high variation' if financial.get('std_dev', 0) > 10 else 'consistent'} transaction amounts.

3. Business Diversity: The data includes {company.get('total_unique_companies', 0)} unique companies, indicating {'highly diversified' if company.get('total_unique_companies', 0) > 50 else 'concentrated'} business activity.

4. Top Merchants: The leading merchants account for a significant portion of transactions, with the top merchant appearing {company.get('top_companies', [{}])[0].get('count', 0)} times.

5. Data Quality: The dataset shows good completion rates across all key fields, with sufficient data for reliable analysis.

Recommendations:
- Monitor transaction trends over time
- Analyze spending patterns by merchant category
- Identify opportunities for vendor consolidation
- Review high-value transactions for compliance
"""
        return analysis


def create_analyzer(provider: str, **kwargs) -> LLMAnalyzer:
    """Factory function to create appropriate analyzer"""
    
    if provider == "openai":
        api_key = kwargs.get('api_key', '')
        model = kwargs.get('model', 'gpt-3.5-turbo')
        if not api_key:
            logger.warning("OpenAI API key not provided. Using mock analyzer.")
            return MockAnalyzer()
        return OpenAIAnalyzer(api_key, model)
    
    elif provider == "anthropic":
        api_key = kwargs.get('api_key', '')
        model = kwargs.get('model', 'claude-3-haiku-20240307')
        if not api_key:
            logger.warning("Anthropic API key not provided. Using mock analyzer.")
            return MockAnalyzer()
        return AnthropicAnalyzer(api_key, model)
    
    elif provider == "ollama":
        base_url = kwargs.get('base_url', 'http://localhost:11434')
        model = kwargs.get('model', 'mistral')
        return OllamaAnalyzer(base_url, model)
    
    else:
        logger.warning(f"Unknown provider: {provider}. Using mock analyzer.")
        return MockAnalyzer()


# Add _build_prompt method to base class
def _build_prompt(self, statistics: Dict[str, Any], context: str) -> str:
    """Build prompt for LLM analysis"""
    prompt = f"""Analyze the following receipt data statistics and provide actionable insights:

Statistics Summary:
- Total Receipts: {statistics.get('total_receipts', 0)}
- Total Amount: ${statistics.get('financial_stats', {}).get('sum', 0):,.2f}
- Average Per Receipt: ${statistics.get('financial_stats', {}).get('average', 0):,.2f}
- Unique Companies: {statistics.get('company_stats', {}).get('total_unique_companies', 0)}
- Data Quality: {statistics.get('data_quality', {}).get('field_completion_rates', {}).get('company', 0)}% complete

Additional Context: {context if context else 'None provided'}

Please provide:
1. Key insights from the data
2. Notable trends or patterns
3. Data quality observations
4. Recommendations for action
Keep the analysis concise and actionable."""
    
    return prompt

LLMAnalyzer._build_prompt = _build_prompt
