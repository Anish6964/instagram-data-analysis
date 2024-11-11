import instaloader
import json
import re

# Function to extract hashtags from captions
def extract_hashtags(caption):
    return re.findall(r'#\w+', caption) if caption else []

# Initialize Instaloader
L = instaloader.Instaloader()

# Optional: Login for better access (required for private profiles or more requests)
# L.login("your_username", "your_password")

def download_instagram_data(username, max_posts=10):
    """Download captions, likes, and hashtags from a user's Instagram posts."""
    profile = instaloader.Profile.from_username(L.context, username)
    
    posts_data = []
    for post in profile.get_posts():
        if len(posts_data) >= max_posts:
            break
        post_data = {
            'caption': post.caption,
            'likes': post.likes,
            'hashtags': extract_hashtags(post.caption)
        }
        posts_data.append(post_data)
    
    # Save the data to a JSON file
    with open('instagram_data.json', 'w') as f:
        json.dump(posts_data, f, indent=4)
    
    print(f"Downloaded {len(posts_data)} posts for user '{username}'")

# Replace 'brand_username' with the Instagram handle of your chosen brand
download_instagram_data('ferrari')
