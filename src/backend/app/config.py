"""
Configuration management for PublicPulse AI
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Database Configuration
    database_url: str = "sqlite:///./publicpulse.db"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:4321"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Crawler Configuration
    max_crawl_depth: int = 3
    max_pages_per_scan: int = 50
    crawler_timeout: int = 30000  # milliseconds
    crawler_user_agent: str = "PublicPulseAI/1.0 (Website Auditing Bot)"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    # Background Tasks
    background_task_timeout: int = 300  # seconds
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI Configuration
    watsonx_api_key: str = ""
    watsonx_project_id: str = ""
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_model_id: str = "meta-llama/llama-2-70b-chat"
    
    # Alternative AI
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    
    # Feature Flags
    enable_ai_recommendations: bool = True
    enable_auto_fix_preview: bool = True
    enable_batch_processing: bool = True
    
    # Performance
    cache_enabled: bool = True
    cache_ttl: int = 3600  # seconds
    
    # Development
    debug: bool = False
    testing: bool = False


# Global settings instance
settings = Settings()

# Made with Bob
