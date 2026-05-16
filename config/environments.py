from typing import Dict, Any

ENV_CONFIG: Dict[str, Dict[str, str]] = {
    "dev": {
        "base_url": "https://dev.example.com",
        "api_url": "https://api.dev.example.com",
    },
    "qa": {
        "base_url": "https://qa.example.com",
        "api_url": "https://api.qa.example.com",
    },
    "staging": {
        "base_url": "https://staging.example.com",
        "api_url": "https://api.staging.example.com",
    },
    "prod": {
        "base_url": "https://example.com",
        "api_url": "https://api.example.com",
    },
}
