"""Environment-driven configuration. No secrets in code (NFR-6)."""
from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    database_url: str = "postgresql+psycopg://tayari:tayari@localhost:5432/tayari"

    # Upstream real data sources (public)
    hdx_base: str = "https://data.humdata.org/api/3/action"
    hdx_org: str = "igad-climate-prediction-and-application-center"
    stac_base: str = (
        "https://raw.githubusercontent.com/icpac-igad/stac-api/"
        "refs/heads/main/ibf_catalog"
    )
    geonode_base: str = "https://geoportal.icpac.net/api/v2"

    # LLM
    llm_provider: str = "template"  # bedrock | openai | template
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    aws_region: str = "us-east-1"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    # SMS (Africa's Talking sandbox)
    at_username: str | None = None
    at_api_key: str | None = None
    at_sender: str = "TAYARI"

    # App
    frontend_origin: str = "http://localhost:5173"
    cache_ttl_seconds: int = 3600
    request_timeout: float = 25.0

    # Analysis dekad (YYYY-MM-DD). Default = a real 2021 Horn of Africa drought peak
    # (CDI shows Alert in Garissa/Isiolo, Warning in Marsabit/Samburu). Change to
    # analyse any real dekad; "latest" uses the most recent available CDI raster.
    cdi_as_of: str = "2021-05-01"


settings = Settings()
