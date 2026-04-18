"""
Configuration module for GenAI Report Generation System
"""

import os
from pathlib import Path
from typing import Optional

class Config:
    """Configuration for the report generation system"""
    
    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    # Data is in ICDAR-2019-SROIE subdirectory
    DATA_DIR = PROJECT_ROOT / "ICDAR-2019-SROIE" / "data"
    BOX_DIR = DATA_DIR / "box"
    KEY_DIR = DATA_DIR / "key"
    IMG_DIR = DATA_DIR / "img"
    REPORTS_DIR = PROJECT_ROOT / "generated_reports"
    
    # LLM Configuration
    # Options: "openai", "anthropic", "ollama", "local"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Anthropic Configuration
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
    
    # Ollama Configuration (local)
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    
    # Report Configuration
    REPORT_FORMAT = "pdf"  # or "html", "markdown"
    REPORT_LANGUAGE = "english"
    
    # Scheduling
    SCHEDULE_WEEKLY = "monday"  # Day for weekly reports
    SCHEDULE_WEEKLY_TIME = "09:00"  # Time in HH:MM format
    SCHEDULE_MONTHLY_DAY = 1  # Day of month for monthly reports
    SCHEDULE_MONTHLY_TIME = "09:00"
    
    # Statistics Configuration
    INCLUDE_CHARTS = True
    CHART_TYPE = "matplotlib"  # or "plotly"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = PROJECT_ROOT / "logs" / "genai_reports.log"
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.BOX_DIR.exists():
            raise FileNotFoundError(f"Box data directory not found: {cls.BOX_DIR}")
        if not cls.KEY_DIR.exists():
            raise FileNotFoundError(f"Key data directory not found: {cls.KEY_DIR}")
        
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required for OpenAI provider")
        
        if cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required for Anthropic provider")
        
        return True
