from flask import Flask, render_template, request
import pandas as pd
from preproc import df1
from sklearn.neighbors import NearestNeighbors
import random
app = Flask(__name__)

# data = {
#     'SongName': ['song1', 'song2', 'song3', 'song4', 'song5', 'song6', 'song7', 'song8', 'song9', 'song10'],
#     'Genre': ['Pop', 'Pop', 'Rock', 'Rock', 'Pop', 'Jazz', 'Jazz', 'Rock', 'Pop', 'Rock'],
#     'Artist': ['Artist1', 'Artist2', 'Artist3', 'Artist4', 'Artist5', 'Artist6', 'Artist7', 'Artist8', 'Artist9', 'Artist10'],
#     'Rating': [4.5, 4.8, 4.6, 4.7, 4.9, 4.2, 4.3, 4.6, 4.7, 4.5],
#     'ReleaseYear': [2019, 2020, 2021, 2019, 2020, 2018, 2019, 2021, 2018, 2022]
# }             

df = pd.DataFrame(df1)
df_encoded = pd.get_dummies(df[['Genre', 'Artist']])
df_features = pd.concat([df_encoded, df['ReleaseYear']], axis=1)

knn_model = NearestNeighbors(n_neighbors=100 , metric='euclidean')
knn_model.fit(df_features)

def get_song_details(song_name):
    song_details = df[df['SongName'] == song_name]
    if song_details.empty:
        return None
    return song_details[['Artist', 'Genre', 'ReleaseYear']].iloc[0] 

def recommend_similar_songs(song_name):
    song_details = get_song_details(song_name)
    if song_details is None:
        return None, None

    input_data = pd.DataFrame({
        'Genre': [song_details['Genre']],
        'Artist': [song_details['Artist']],
        'ReleaseYear': [song_details['ReleaseYear']]
    })

    input_encoded = pd.get_dummies(input_data[['Genre', 'Artist']])
    input_features = pd.concat([input_encoded, input_data['ReleaseYear']], axis=1)
    # print(input_features)
    for col in df_features.columns:
        if col not in input_features.columns:
            input_features[col] = 0

    input_features = input_features[df_features.columns]

    _, indices = knn_model.kneighbors(input_features)

    recommended_songs = df.iloc[indices[0]]
    genre_recommendations = recommended_songs[recommended_songs['Genre'] == song_details['Genre']].sort_values(by='Rating', ascending=False)
    artist_recommendations = recommended_songs[recommended_songs['Artist'] == song_details['Artist']].sort_values(by='Rating', ascending=False)

    return genre_recommendations[['SongName', 'Rating', 'Genre']], artist_recommendations[['SongName', 'Rating', 'Genre']]

@app.route('/', methods=['GET', 'POST'])
def index():
    genre_recommendations = None
    artist_recommendations = None

    top_10_rated_songs = df.sort_values(by='Rating', ascending=False).head(20)
    print(top_10_rated_songs[:10])
    if request.method == 'POST':
        song_name = request.form['song_name']
        genre_recommendations, artist_recommendations = recommend_similar_songs(song_name)

    return render_template('index.html', genre_recommendations=genre_recommendations,
                           artist_recommendations=artist_recommendations, top_rated_songs=top_10_rated_songs)

audio_filenames = ["Alone.mp3", "Believer.mp3", "Darkside.mp3", "faded.mp3"]
@app.route('/your_route')
def your_route():
    # Choose a random audio filename
    random_audio_filename = random.choice(audio_filenames)

    return render_template('details.html', raf=random_audio_filename)






@app.route('/details')
def details():
    return render_template('details.html')
from flask import send_from_directory
@app.route('/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static', filename)

app.config['STATIC_FOLDER'] = 'static'
if __name__ == '__main__':
    app.run(debug=True)
