from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseInstagramProvider(ABC):
    @abstractmethod
    def search_users(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for users matching the query string.
        Returns a list of dicts, each containing at least:
        - 'username': str
        - 'id': str
        """
        pass

    @abstractmethod
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get profile details for a given user ID.
        Returns a dict containing:
        - 'username': str
        - 'profile_picture': str
        - 'counts': {
            'followed_by': int,
            'follows': int
          }
        """
        pass

    @abstractmethod
    def get_recent_media(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get recent media items for a given user ID.
        Returns a list of media dicts, each containing:
        - 'likes': {'count': int}
        - 'comments': {'count': int}
        - 'created_time': str (UNIX timestamp as string)
        - 'filter': str
        - 'location': {'latitude': float, 'longitude': float} (optional)
        - 'users_in_photo': [
            {
              'user': {'username': str},
              'position': {'x': float, 'y': float}
            }
          ] (optional)
        """
        pass
