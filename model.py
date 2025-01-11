import json
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
df = pd.read_csv('Songs.csv')
df = df.sample(50)

# Select relevant features for recommendations
features = ['artist_name', 'release_date', 'genre', 'topic']

# Define weights for each feature (you can adjust these weights)
weights = {
    'artist_name': 1.5,  # higher weight means more importance
    'release_date': 0.5, 
    'genre': 1.0, 
    'topic': 1.2
}

# One-hot encode categorical features
encoder = OneHotEncoder()
encoded_features = encoder.fit_transform(df[features]).toarray()

# Apply weights to the encoded features
weighted_features = encoded_features.copy()

# Applying different weights to each feature group
start = 0
for feature, weight in zip(features, weights.values()):
    end = start + len(encoder.categories_[features.index(feature)])
    weighted_features[:, start:end] *= weight
    start = end


similarity_matrix = cosine_similarity(weighted_features)
def recommend_songs_with_priorities(song_index, num_recommendations=5):
    # Get similarity scores for the input song
    song_similarities = similarity_matrix[song_index]
    
    # Get indices of the most similar songs, excluding the input song itself
    similar_songs_indices = song_similarities.argsort()[::-1][1:num_recommendations+1]
    
    # Return details of the most similar songs
    return df.iloc[similar_songs_indices][['artist_name', 'track_name', 'release_date', 'genre', 'topic']]
recommended_songs = recommend_songs_with_priorities(0, num_recommendations=20)

dict_data = recommended_songs.transpose().to_dict()
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(dict_data, f, ensure_ascii=False, indent=4)
