import json
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

# Load custom stopwords from file
def load_stopwords(file_path='stopwords.txt'):
    with open(file_path, 'r') as file:
        stopwords = set(word.strip().lower() for word in file.readlines())
    return stopwords

stop_words = load_stopwords()

# Load the data from the JSON file
with open('instagram_data.json', 'r') as f:
    data = json.load(f)

# Convert data to a DataFrame
df = pd.DataFrame(data)

# Function to clean and tokenize text using custom stopwords
def clean_and_tokenize(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s#]', '', text)  # Remove special characters
    words = text.lower().split()
    words = [word for word in words if word not in stop_words and len(word) > 1]
    return words

# Analyze captions
df['tokens'] = df['caption'].apply(lambda x: clean_and_tokenize(x) if x else [])
df['word_count'] = df['tokens'].apply(len)

# Extract hashtags
df['hashtags'] = df['caption'].apply(lambda x: re.findall(r'#\w+', x) if x else [])

# Calculate average likes for each word
word_likes = Counter()
word_count = Counter()

for _, row in df.iterrows():
    for word in row['tokens']:
        word_likes[word] += row['likes']
        word_count[word] += 1

# Compute average likes for words
avg_word_likes = {word: word_likes[word] / word_count[word] for word in word_count}

# Print top 10 words by average likes
top_words = sorted(avg_word_likes.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 Words with Highest Average Likes:")
for word, avg_likes in top_words:
    print(f"{word}: {avg_likes:.2f}")

# Calculate average likes for hashtags
hashtag_likes = Counter()
hashtag_count = Counter()

for _, row in df.iterrows():
    for hashtag in row['hashtags']:
        hashtag_likes[hashtag] += row['likes']
        hashtag_count[hashtag] += 1

avg_hashtag_likes = {tag: hashtag_likes[tag] / hashtag_count[tag] for tag in hashtag_count}

# Print top 10 hashtags by average likes
top_hashtags = sorted(avg_hashtag_likes.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Hashtags with Highest Average Likes:")
for hashtag, avg_likes in top_hashtags:
    print(f"{hashtag}: {avg_likes:.2f}")

# Visualization: Top 10 words and hashtags by average likes
top_words_df = pd.DataFrame(top_words, columns=['Word', 'Avg Likes'])
top_hashtags_df = pd.DataFrame(top_hashtags, columns=['Hashtag', 'Avg Likes'])

# Plotting
plt.figure(figsize=(10, 5))
plt.barh(top_words_df['Word'], top_words_df['Avg Likes'])
plt.title('Top 10 Words by Average Likes')
plt.xlabel('Average Likes')
plt.ylabel('Words')
plt.gca().invert_yaxis()
plt.show()

plt.figure(figsize=(10, 5))
plt.barh(top_hashtags_df['Hashtag'], top_hashtags_df['Avg Likes'])
plt.title('Top 10 Hashtags by Average Likes')
plt.xlabel('Average Likes')
plt.ylabel('Hashtags')
plt.gca().invert_yaxis()
plt.show()
