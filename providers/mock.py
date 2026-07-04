import hashlib
import random
import time
from typing import List, Dict, Any, Optional
from providers.base import BaseInstagramProvider

class MockInstagramProvider(BaseInstagramProvider):
    def _set_deterministic_seed(self, username: str) -> None:
        """Sets a deterministic random seed based on the username md5 hash."""
        hash_val = hashlib.md5(username.lower().encode('utf-8')).hexdigest()
        # Convert hex string to a large integer seed
        seed = int(hash_val, 16) % (2**32)
        random.seed(seed)

    def search_users(self, query: str) -> List[Dict[str, Any]]:
        """Mock searching for users. Returns a list with the user and similar usernames."""
        self._set_deterministic_seed(query)
        
        # Always return the queried username as the primary result
        results = [
            {'username': query.lower(), 'id': f"mock_id_{hashlib.md5(query.lower().encode()).hexdigest()[:8]}"}
        ]
        
        # Add a couple of similar usernames for realism
        suffixes = ["_trends", "_official", "_fan", "gallery"]
        for suffix in random.sample(suffixes, 2):
            sibling = f"{query.lower()}{suffix}"
            results.append({
                'username': sibling,
                'id': f"mock_id_{hashlib.md5(sibling.encode()).hexdigest()[:8]}"
            })
            
        return results

    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Mock profile detailed stats."""
        # Extract a seed identifier from the user ID to maintain consistency
        self._set_deterministic_seed(user_id)
        
        # Reconstruct or invent username
        username_part = user_id.replace("mock_id_", "")
        username = f"user_{username_part[:4]}"
        
        # engagement & size tiers
        tier = random.choice(['small', 'medium', 'large'])
        if tier == 'small':
            followed_by = random.randint(150, 4500)
            follows = random.randint(100, 1200)
        elif tier == 'medium':
            followed_by = random.randint(12000, 85000)
            follows = random.randint(400, 2500)
        else:  # large
            followed_by = random.randint(250000, 5600000)
            follows = random.randint(150, 600)
            
        return {
            'username': username,
            'profile_picture': f"https://api.dicebear.com/7.x/identicon/svg?seed={username}",
            'counts': {
                'followed_by': followed_by,
                'follows': follows
            }
        }

    def get_recent_media(self, user_id: str) -> List[Dict[str, Any]]:
        """Generates 33 high-fidelity mock posts with realistic distributions."""
        self._set_deterministic_seed(user_id)
        
        # Determine follower scale for engagement math
        tier_roll = random.random()
        if tier_roll < 0.5:
            followers = random.randint(500, 5000)
        elif tier_roll < 0.85:
            followers = random.randint(15000, 100000)
        else:
            followers = random.randint(300000, 3000000)
            
        # Instagram standard filters
        filters = ['Normal', 'Clarendon', 'Juno', 'Lark', 'Ludwig', 'Gingham', 'Valencia', 'X-Pro II', 'Sierra', 'Lo-fi', 'Amaro', 'Hefe']
        
        # Predefined mock locations
        mock_cities = [
            {'name': 'New York', 'lat': 40.7128, 'lng': -74.0060},
            {'name': 'Paris', 'lat': 48.8566, 'lng': 2.3522},
            {'name': 'Tokyo', 'lat': 35.6762, 'lng': 139.6503},
            {'name': 'San Francisco', 'lat': 37.7749, 'lng': -122.4194},
            {'name': 'London', 'lat': 51.5074, 'lng': -0.1278},
            {'name': 'Sydney', 'lat': -33.8688, 'lng': 151.2093}
        ]
        
        mock_tags = ['photographer', 'travel', 'vibes', 'daily', 'explore', 'creative', 'friends', 'nature']
        
        media_list = []
        now = int(time.time())
        # Generate 33 posts spaced over the last 90 days
        for i in range(33):
            # Backwards timestamp step (e.g., posting every 1.5 to 5 days)
            post_time = now - (i * random.randint(129600, 432000))
            
            # Engagement calculations
            engagement_rate = random.uniform(0.015, 0.09)
            likes_mean = int(followers * engagement_rate)
            likes = int(random.gauss(likes_mean, likes_mean * 0.2))
            likes = max(random.randint(5, 50), likes) # Floor limit
            
            comments_mean = int(likes * random.uniform(0.02, 0.08))
            comments = int(random.gauss(comments_mean, comments_mean * 0.3))
            comments = max(random.randint(1, 15), comments) # Floor limit
            
            # Filter selection (Normal filter is most common)
            fltr = 'Normal' if random.random() < 0.4 else random.choice(filters)
            
            post = {
                'likes': {'count': likes},
                'comments': {'count': comments},
                'created_time': str(post_time),
                'filter': fltr
            }
            
            # 40% of posts have location
            if random.random() < 0.4:
                city = random.choice(mock_cities)
                # Add a tiny random offset to city coords for spread
                post['location'] = {
                    'latitude': city['lat'] + random.uniform(-0.05, 0.05),
                    'longitude': city['lng'] + random.uniform(-0.05, 0.05)
                }
                
            # 50% of posts have user tags
            if random.random() < 0.5:
                users_in_photo = []
                # Tag 1 to 3 users
                num_tags = random.randint(1, 3)
                tagged_names = random.sample(mock_tags, num_tags)
                for name in tagged_names:
                    users_in_photo.append({
                        'user': {'username': f"mock_{name}"},
                        'position': {
                            'x': round(random.uniform(0.1, 0.9), 4),
                            'y': round(random.uniform(0.1, 0.9), 4)
                        }
                    })
                post['users_in_photo'] = users_in_photo
                
            media_list.append(post)
            
        return media_list
