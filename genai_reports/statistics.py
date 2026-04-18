"""
Statistics generation module for receipt data analysis
"""

import statistics
from typing import List, Dict, Any, Optional
from collections import Counter
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StatisticsGenerator:
    """Generate statistical insights from receipt data"""
    
    def __init__(self):
        self.stats = {}
    
    def generate_all_statistics(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive statistics from receipts"""
        self.stats = {
            'timestamp': datetime.now().isoformat(),
            'total_receipts': len(receipts),
            'financial_stats': self._calculate_financial_stats(receipts),
            'company_stats': self._calculate_company_stats(receipts),
            'text_box_stats': self._calculate_text_box_stats(receipts),
            'data_quality': self._assess_data_quality(receipts),
        }
        return self.stats
    
    def _calculate_financial_stats(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate financial statistics"""
        totals = []
        
        for receipt in receipts:
            key_info = receipt.get('key_info', {})
            try:
                total = float(key_info.get('total', 0))
                if total > 0:
                    totals.append(total)
            except (ValueError, TypeError):
                pass
        
        if not totals:
            return {
                'count': 0,
                'sum': 0,
                'average': 0,
                'median': 0,
                'min': 0,
                'max': 0,
                'std_dev': 0,
            }
        
        return {
            'count': len(totals),
            'sum': round(sum(totals), 2),
            'average': round(sum(totals) / len(totals), 2),
            'median': round(statistics.median(totals), 2),
            'min': round(min(totals), 2),
            'max': round(max(totals), 2),
            'std_dev': round(statistics.stdev(totals), 2) if len(totals) > 1 else 0,
        }
    
    def _calculate_company_stats(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate company-related statistics"""
        companies = Counter()
        addresses = Counter()
        
        for receipt in receipts:
            key_info = receipt.get('key_info', {})
            company = key_info.get('company', 'Unknown').strip()
            address = key_info.get('address', 'Unknown').strip()
            
            if company:
                companies[company] += 1
            if address:
                addresses[address] += 1
        
        top_companies = companies.most_common(10)
        
        return {
            'total_unique_companies': len(companies),
            'total_unique_addresses': len(addresses),
            'top_companies': [{'name': name, 'count': count} for name, count in top_companies],
            'receipts_with_company_info': sum(companies.values()),
            'receipts_with_address_info': sum(addresses.values()),
        }
    
    def _calculate_text_box_stats(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate text box statistics"""
        box_counts = []
        
        for receipt in receipts:
            num_boxes = receipt.get('num_boxes', 0)
            box_counts.append(num_boxes)
        
        if not box_counts:
            return {'avg_boxes': 0, 'total_boxes': 0, 'min_boxes': 0, 'max_boxes': 0}
        
        return {
            'avg_boxes': round(sum(box_counts) / len(box_counts), 2),
            'total_boxes': sum(box_counts),
            'min_boxes': min(box_counts),
            'max_boxes': max(box_counts),
            'median_boxes': statistics.median(box_counts),
        }
    
    def _assess_data_quality(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess data quality and completeness"""
        completeness = {
            'company': 0,
            'address': 0,
            'date': 0,
            'total': 0,
        }
        
        for receipt in receipts:
            key_info = receipt.get('key_info', {})
            if key_info.get('company', '').strip():
                completeness['company'] += 1
            if key_info.get('address', '').strip():
                completeness['address'] += 1
            if key_info.get('date', '').strip():
                completeness['date'] += 1
            if key_info.get('total', '').strip():
                completeness['total'] += 1
        
        total = len(receipts) if receipts else 1
        
        return {
            'total_records': total,
            'field_completion_rates': {
                field: round((count / total * 100), 2)
                for field, count in completeness.items()
            },
            'fully_complete_records': sum(
                1 for receipt in receipts
                if all([
                    receipt.get('key_info', {}).get(field, '').strip()
                    for field in ['company', 'address', 'date', 'total']
                ])
            ),
        }
    
    def get_summary_text(self) -> str:
        """Generate a text summary of statistics"""
        if not self.stats:
            return "No statistics generated yet."
        
        financial = self.stats.get('financial_stats', {})
        company = self.stats.get('company_stats', {})
        textbox = self.stats.get('text_box_stats', {})
        quality = self.stats.get('data_quality', {})
        
        summary = f"""
RECEIPT DATA STATISTICS SUMMARY
{'='*50}

Dataset Overview:
- Total Receipts: {self.stats.get('total_receipts', 0)}
- Generated: {self.stats.get('timestamp', 'N/A')}

Financial Summary:
- Total Amount: ${financial.get('sum', 0):,.2f}
- Average Per Receipt: ${financial.get('average', 0):,.2f}
- Median: ${financial.get('median', 0):,.2f}
- Range: ${financial.get('min', 0):,.2f} - ${financial.get('max', 0):,.2f}

Company Information:
- Unique Companies: {company.get('total_unique_companies', 0)}
- Unique Addresses: {company.get('total_unique_addresses', 0)}
- Top Company: {company.get('top_companies', [{}])[0].get('name', 'N/A') if company.get('top_companies') else 'N/A'}

Data Quality:
- Fully Complete Records: {quality.get('fully_complete_records', 0)}
- Company Info: {quality.get('field_completion_rates', {}).get('company', 0)}%
- Address Info: {quality.get('field_completion_rates', {}).get('address', 0)}%
- Date Info: {quality.get('field_completion_rates', {}).get('date', 0)}%
- Total Info: {quality.get('field_completion_rates', {}).get('total', 0)}%
"""
        return summary
