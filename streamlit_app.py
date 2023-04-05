import streamlit as st

# Streamlit app layout
st.title("Movie Database")
st.header("Select a movie from the dropdown list to view its details, rate it, or delete it.")
st.sidebar.header("Add a new movie")
title = st.sidebar.text_input("Title")
released_year = st.sidebar.number_input("Released year", min_value=1800, max_value=2100)
kind = st.sidebar.text_input("Kind")
nationality = st.sidebar.text_input("Nationality")
if st.sidebar.button("Add movie"):
    st.sidebar.success(f"{title} has been added to the database.")

# List of example movies
movies = [
    {"title": "The Shawshank Redemption", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.7},
    {"title": "The Godfather", "released_year": 1972, "kind": "Crime", "nationality": "USA", "average_ranking": 4.8},
    {"title": "The Dark Knight", "released_year": 2008, "kind": "Action", "nationality": "USA", "average_ranking": 4.5},
    {"title": "Pulp Fiction", "released_year": 1994, "kind": "Crime", "nationality": "USA", "average_ranking": 4.4},
    {"title": "Forrest Gump", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.6},
]

# Add example movies to the dropdown list
movie_list = [movie["title"] for movie in movies]
selected_movie = st.selectbox("Select a movie", movie_list)

# Get the selected movie's information and display it
selected_movie_info = next((movie for movie in movies if movie["title"] == selected_movie), None)
if selected_movie_info is not None:
    st.write(f"Title: {selected_movie_info['title']}")
    st.write(f"Released year: {selected_movie_info['released_year']}")
    st.write(f"Kind: {selected_movie_info['kind']}")
    st.write(f"Nationality: {selected_movie_info['nationality']}")
    st.write(f"Average ranking: {selected_movie_info['average_ranking']}")

    # Add a "Rate" button to rate the selected movie
    if st.button("Rate"):
        rating = st.number_input("Enter your rating (0-5)", min_value=0, max_value=5)
        selected_movie_info["average_ranking"] = (rating + selected_movie_info["average_ranking"]) / 2
        st.success(f"You rated {selected_movie} {rating} stars.")

    # Add a "Delete" button to delete the selected movie
    if st.button("Delete"):
        movies.remove(selected_movie_info)
        st.success(f"{selected_movie} has been deleted from the database.")
else:
    st.write("No movie selected.")
