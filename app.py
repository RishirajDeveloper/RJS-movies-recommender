from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import requests

app = Flask(__name__)

# 1. Datasets Load (Memory mein ek hi baar load hoga)
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 2.Poster Fetcher Function
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7cf1c9fb46a8f18f024fed30d0fdcd6f'
        response = requests.get(url, timeout=1.5) # Timeout 1.5s rakha hai taaki site lag na kare
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    # Fallback placeholder image agar poster na mile ya API network slow ho
    return "https://via.placeholder.com/500x750.png?text=Poster+Not+Found"

# 3. Home Route (Dropdown options ke liye)
@app.route('/')
def home():
    movie_list = movies['title'].values.tolist()
    return render_template('index.html', movie_list=movie_list)

# 4. Recommendation API Endpoint (Bina page refresh kiye details bhejega)
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    selected_movie = data.get('movie')
    
    if selected_movie not in movies['title'].values:
        return jsonify({'error': 'Movie not found'}), 400
        
    # Movie ka index aur similarities nikaalein
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = similarity[movie_index]
    
    # Top 5 similar movies collect karna
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_details = []
    
    for i in movie_list:
        match_index = i[0]
        
        # Title aur Movie ID safely extraction
        movie_title = movies.loc[match_index, 'title']
        movie_id = int(movies.loc[match_index, 'movie_id'])
        
        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_id))
        
        # Local data se details parse karna (Lists ko normal string sentence banana)
        raw_overview = movies.loc[match_index, 'overview']
        raw_genres = movies.loc[match_index, 'genres']
        raw_cast = movies.loc[match_index, 'cast']
        raw_crew = movies.loc[match_index, 'crew']
        
        recommended_details.append({
            'overview': " ".join(raw_overview) if isinstance(raw_overview, list) else str(raw_overview),
            'genres': ", ".join(raw_genres) if isinstance(raw_genres, list) else str(raw_genres),
            'cast': ", ".join(raw_cast) if isinstance(raw_cast, list) else str(raw_cast),
            'crew': ", ".join(raw_crew) if isinstance(raw_crew, list) else str(raw_crew)
        })
        
    return jsonify({
        'names': recommended_movies,
        'posters': recommended_posters,
        'details': recommended_details
    })

if __name__ == '__main__':
    app.run(debug=True)