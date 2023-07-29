import streamlit as st
import pandas as pd
import requests
import webbrowser

# Load the movie list and similarity matrix
movies = pd.read_pickle('movie_list.pkl')
similarity = pd.read_pickle('similarity.pkl')

# API configuration
API_KEY = "8265bd1679663a7ea12ac168da84d2e8&language=en-US"
IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Function to get movie poster URL
def get_poster_url(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data['poster_path']
        return IMG_BASE_URL + poster_path
    else:
        return None

# Function to get movie homepage URL
def get_movie_homepage(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        homepage = data['homepage']
        return homepage
    else:
        return None

# Main page for search options
st.title("Movie Recommender")

# Search options
search_type = st.selectbox("Search Type", ["Title","Genres", "Cast", "Crew"])
search_term = st.text_input(f"Enter {search_type.lower()}")

# Search button
if st.button("Search"):
    # Filter movies based on search type and term
    if search_type == "Title":
        matching_movies = movies[movies['title'].str.contains(search_term, case=False)]
    elif search_type == "Genres":
        matching_movies = movies[movies['genres'].str.contains(search_term, case=False)]
    elif search_type == "Cast":
        matching_movies = movies[movies['cast'].str.contains(search_term, case=False)]
    elif search_type == "Crew":
        matching_movies = movies[movies['crew'].str.contains(search_term, case=False)]

    # Show search results
    if matching_movies.empty:
        st.warning("No movies found matching the search term.")
    else:
        st.subheader("Search Results")
        for index, row in matching_movies.iterrows():
            # Show movie details
            st.write(row['title'])
            st.write("Overview:", row['overview'])
            st.write("Genres:", row['genres'])
            st.write("Cast:", row['cast'])
            st.write("---")

            # Get movie poster URL
            poster_url = get_poster_url(row['movie_id'])
            if poster_url:
                st.image(poster_url, use_column_width=True)

        # Get top 5 recommended movies
        index = matching_movies.index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_homepages =[]
        for i in distances[1:6]:
            recommended_movie = movies.iloc[i[0]]
            recommended_movie_names.append(recommended_movie['title'])
            recommended_movie_posters.append(get_poster_url(recommended_movie['movie_id']))
            recommended_movie_homepages.append(get_movie_homepage(recommended_movie['movie_id']))

        st.subheader("Recommended Movies")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            if recommended_movie_posters[0]:
                st.image(recommended_movie_posters[0], use_column_width=True)
        with col2:
            st.text(recommended_movie_names[1])
            if recommended_movie_posters[1]:
                st.image(recommended_movie_posters[1], use_column_width=True)
        with col3:
            st.text(recommended_movie_names[2])
            if recommended_movie_posters[2]:
                st.image(recommended_movie_posters[2], use_column_width=True)
        with col4:
            st.text(recommended_movie_names[3])
            if recommended_movie_posters[3]:
                st.image(recommended_movie_posters[3], use_column_width=True)
        with col5:
            st.text(recommended_movie_names[4])
            if recommended_movie_posters[4]:
                st.image(recommended_movie_posters[4], use_column_width=True)
