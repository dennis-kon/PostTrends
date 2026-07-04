import pytest
from app import closest_match, format_timestamp, count_occurrences, process_media_data

def test_closest_match():
    users = [
        {'username': 'john_doe', 'id': '123'},
        {'username': 'jane_doe', 'id': '456'},
    ]
    # Exact match case-insensitive
    assert closest_match(users, 'JOHN_DOE') == '123'
    # No match case
    assert closest_match(users, 'jack_doe') is None

def test_format_timestamp():
    # Test converting a timestamp to various formats
    timestamp = "1483228800" # 2017-01-01 00:00:00 UTC (or local)
    # The result may depend slightly on test environment timezone, so we verify structure/regex or stable format parts
    formatted = format_timestamp(timestamp, '%Y-%m-%d')
    assert formatted == '2017-01-01'

def test_count_occurrences():
    items = ['Mon', 'Mon', 'Tue', 'Fri']
    categories = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    counts = count_occurrences(items, categories)
    
    assert counts == [
        ['Mon', 2],
        ['Tue', 1],
        ['Wed', 0],
        ['Thu', 0],
        ['Fri', 1],
        ['Sat', 0],
        ['Sun', 0]
    ]

def test_process_media_data():
    mock_raw_media = [
        {
            'likes': {'count': 100},
            'comments': {'count': 10},
            'created_time': '1483228800',
            'filter': 'Clarendon',
            'location': {'latitude': 40.7128, 'longitude': -74.0060},
            'users_in_photo': [
                {
                    'user': {'username': 'buddy'},
                    'position': {'x': 0.5, 'y': 0.5}
                }
            ]
        },
        {
            'likes': {'count': 200},
            'comments': {'count': 20},
            'created_time': '1483315200',
            'filter': 'Normal',
            # No location or user tags
        }
    ]
    
    result = process_media_data(mock_raw_media)
    
    assert result['likes'] == [100, 200]
    assert result['comments'] == [10, 20]
    assert len(result['locations']) == 1
    assert result['locations'][0] == [40.7128, -74.0060]
    assert 'buddy' in result['tags']
    assert result['tag_positions'][0] == [0.5, 0.5]
    assert len(result['filters_arr']) == 2
    # Ensure filters are aggregated correctly
    filter_dict = dict(result['filters_arr'])
    assert filter_dict['Clarendon'] == 1
    assert filter_dict['Normal'] == 1
