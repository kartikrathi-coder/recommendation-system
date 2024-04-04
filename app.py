import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify API credentials
client_credentials_manager = SpotifyClientCredentials(client_id='70a9fb89662f4dac8d07321b259eaad7', client_secret='4d6710460d764fbbb8d8753dc094d131')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load the pickled files
with open('./notebooks/musicrec.pkl', 'rb') as f:
    musicrec = pickle.load(f)

with open('./notebooks/similarities.pkl', 'rb') as f:
    similarities = pickle.load(f)

# Streamlit UI
st.title('Music Recommendation System')

# Load the pickled file
with open('./notebooks/musicrec.pkl', 'rb') as f:
    new_df = pickle.load(f)
    
# Dropdown for selecting a song
selected_song = st.selectbox("Select a song:", new_df['title'])

# Function to recommend music
def recommend_music(music):
    music_index = new_df[new_df['title'] == music].index
    if len(music_index) == 0:
        st.write("Song not found in the database. Please try another one.")
    else:
        music_index = music_index[0]
        distances = similarities[music_index]
        music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]  # Display 6 songs
        recommended_songs = []  # Collect recommended songs to display together
        for i in range(len(music_list)):
            song_name = new_df.iloc[music_list[i][0]]['title']
            # Search for the song on Spotify
            results = sp.search(q='track:' + song_name, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                if track['album']['images']:
                    image_url = track['album']['images'][0]['url']
                    recommended_songs.append((song_name, image_url))
                else:
                    st.write("No image available for:", song_name)
            else:
                st.write("No information available for:", song_name)

        # Display recommended songs
        cols = st.columns(5)  # Arrange the posters in 3 columns
        for i, col in enumerate(cols):
            if i < len(recommended_songs):
                song_name, image_url = recommended_songs[i]
                col.image(image_url, caption=song_name, use_column_width=True)



# User input for song name
#user_input = st.text_input("Enter a song name:")

# Button to trigger recommendation
if st.button("Recommend"):
    recommend_music(selected_song)
