from config import Config
from providers.base import BaseInstagramProvider
from providers.mock import MockInstagramProvider
from providers.graph import InstagramGraphProvider

def get_provider() -> BaseInstagramProvider:
    """
    Factory function to retrieve the configured Instagram provider.
    """
    if Config.PROVIDER == "graph":
        return InstagramGraphProvider(access_token=Config.ACCESS_TOKEN)
    # Default to mock provider
    return MockInstagramProvider()
