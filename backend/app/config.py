import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Autonomous Compliance & RFP Due Diligence Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Storage directories
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    SAMPLE_DIR: str = os.path.join(BASE_DIR, "sample_data")
    
    # LLM Settings (supports OpenAI, Gemini, or Autonomous Local Mode)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = "gpt-4o-mini"
    
    # Enterprise thresholds
    HIGH_RISK_LIABILITY_THRESHOLD_USD: float = 250000.0  # Flag any penalty > $250k
    MIN_SLA_UPTIME_THRESHOLD: float = 99.9               # Standard enterprise SLA cap
    
    class Config:
        case_sensitive = True

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
