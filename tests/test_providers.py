import pytest
from config import Config
from providers import get_provider
from providers.mock import MockInstagramProvider
from providers.graph import InstagramGraphProvider

def test_provider_factory(monkeypatch):
    # Test factory returns mock provider by default or if specified
    monkeypatch.setattr(Config, "PROVIDER", "mock")
    prov = get_provider()
    assert isinstance(prov, MockInstagramProvider)

    # Test factory returns graph provider when configured
    monkeypatch.setattr(Config, "PROVIDER", "graph")
    monkeypatch.setattr(Config, "ACCESS_TOKEN", "test_token")
    prov2 = get_provider()
    assert isinstance(prov2, InstagramGraphProvider)
    assert prov2.access_token == "test_token"

def test_mock_provider_determinism():
    prov = MockInstagramProvider()
    
    # Check search_users
    res1 = prov.search_users("testuser")
    res2 = prov.search_users("testuser")
    assert res1 == res2
    assert len(res1) > 0
    assert res1[0]['username'] == 'testuser'
    assert 'id' in res1[0]

    # Check get_user_info
    info1 = prov.get_user_info("mock_id_testuser")
    info2 = prov.get_user_info("mock_id_testuser")
    assert info1 == info2
    assert 'username' in info1
    assert 'profile_picture' in info1
    assert 'counts' in info1
    assert 'followed_by' in info1['counts']

    # Check get_recent_media
    media1 = prov.get_recent_media("mock_id_testuser")
    media2 = prov.get_recent_media("mock_id_testuser")
    assert media1 == media2
    assert len(media1) == 33
    
    # Check fields in media item
    item = media1[0]
    assert 'likes' in item
    assert 'count' in item['likes']
    assert 'comments' in item
    assert 'count' in item['comments']
    assert 'created_time' in item
    assert 'filter' in item
