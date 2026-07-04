import re
from flask import Flask, request, render_template, redirect, url_for, flash
import datetime
from collections import Counter
from typing import List, Dict, Any, Optional

from config import Config
from providers import get_provider

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/u/<user_input>', methods=['GET'])
def get_data(user_input: str):
    # Sanitize and validate username input
    if not re.match(r'^[a-zA-Z0-9._]+$', user_input):
        flash("Invalid username format. Usernames can only contain letters, numbers, periods, and underscores.")
        return redirect(url_for("home"))

    provider = get_provider()

    # Fetch user search results
    users = provider.search_users(user_input)
    if not users:
        flash("Error loading profile. Make sure profile is public and exists.")
        return redirect(url_for("home"))

    user_id = closest_match(users, user_input)
    if not user_id:
        flash("Error loading profile. Make sure profile is public and exists.")
        return redirect(url_for("home"))

    user_info = provider.get_user_info(user_id)
    if user_info is None:
        flash("Error loading profile. Make sure profile is public and exists.")
        return redirect(url_for("home"))

    media_data = provider.get_recent_media(user_id)
    if not media_data:
        flash("Error. User has no media.")
        return redirect(url_for("home"))

    processed_data = process_media_data(media_data)

    all_data = {
        'basic': user_info,
        'likes': list(reversed(processed_data['likes'])),
        'comments': list(reversed(processed_data['comments'])),
        'days': processed_data['days_pos'],
        'hours': processed_data['hours_pos'],
        'filters': processed_data['filters_arr'],
        'locations': processed_data['locations'],
        'tags': set(processed_data['tags']),
        'tag_positions': processed_data['tag_positions'],
        'date_range': processed_data['date_range'],
    }

    return render_template('chart.html', all_data=all_data)

def closest_match(data: List[Dict[str, Any]], match: str) -> Optional[str]:
    """Finds the closest matching username in data."""
    for user in data:
        if user['username'].lower() == match.lower():
            return user['id']
    return None

def process_media_data(media_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process media data to extract useful information."""
    likes, comments, days, hours, filters, locations, tags, tag_positions = [], [], [], [], [], [], [], []
    date_range = []

    if media_data:
        date_range.append(format_timestamp(media_data[0]['created_time']))
        date_range.append(format_timestamp(media_data[-1]['created_time']))

    for post in media_data:
        try:
            likes.append(post['likes']['count'])
            comments.append(post['comments']['count'])
            days.append(format_timestamp(post['created_time'], '%a'))
            hours.append(format_timestamp(post['created_time'], '%H'))
            filters.append(post.get('filter', 'Unknown'))
            if 'location' in post and post['location']:
                locations.append([post['location']['latitude'], post['location']['longitude']])
            for user_tag in post.get('users_in_photo', []):
                tags.append(user_tag['user']['username'])
                tag_positions.append([user_tag['position']['x'], user_tag['position']['y']])
        except (KeyError, TypeError, IndexError):
            continue

    days_pos = count_occurrences(days, ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    hours_pos = count_occurrences(hours, [f"{i:02}" for i in range(24)])
    filters_arr = [[filter_, count] for filter_, count in Counter(filters).items()]

    return {
        'likes': likes,
        'comments': comments,
        'days_pos': days_pos,
        'hours_pos': hours_pos,
        'filters_arr': filters_arr,
        'locations': locations,
        'tags': tags,
        'tag_positions': tag_positions,
        'date_range': date_range
    }

def format_timestamp(timestamp: str, fmt: str = '%b %e/%y') -> str:
    """Convert timestamp to formatted string."""
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime(fmt)

def count_occurrences(items: List[str], categories: List[str]) -> List[List[str]]:
    """Count occurrences of items and map them to predefined categories."""
    counts = Counter(items)
    return [[category, counts.get(category, 0)] for category in categories]

if __name__ == "__main__":
    app.debug = Config.DEBUG
    app.run(host='0.0.0.0', port=Config.PORT)
