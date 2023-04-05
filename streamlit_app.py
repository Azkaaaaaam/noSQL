import streamlit as st
from neo4j import GraphDatabase, basic_auth

# Connect to Neo4j database
driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "password"))

# Define Neo4j queries
GET_ALL_MOVIES = "MATCH (m:Movie) RETURN m ORDER BY m.title ASC"
GET_MOVIE_INFO = "MATCH (m:Movie {title: $title}) RETURN m.title, m.released_year, m.kind, m.nationality, m.average_ranking"
ADD_MOVIE = "CREATE (m:Movie {title: $title, released_year: $released_year, kind: $kind, nationality: $nationality})"
RATE_MOVIE = "MATCH (m:Movie {title: $title}) SET m.average_ranking = ($average_ranking + m.average_ranking) / 2"

# Streamlit app layout
st.title("Movie Database")
st.header("Select a movie from the dropdown list to view its details, rate it, or delete it.")
st.sidebar.header("Add a new movie")
title = st.sidebar.text_input("Title")
released_year = st.sidebar.number_input("Released year", min_value=1800, max_value=2100)
kind = st.sidebar.text_input("Kind")
nationality = st.sidebar.text_input("Nationality")
if st.sidebar.button("Add movie"):
    with driver.session() as session:
        session.run(ADD_MOVIE, title=title, released_year=released_year, kind=kind, nationality=nationality)
        st.sidebar.success(f"{title} has been added to the database.")

with driver.session() as session:
    # Get all movies from database and add them to the dropdown list
    movies = session.run(GET_ALL_MOVIES)
    movie_list = [movie["m"]["title"] for movie in movies]
    selected_movie = st.selectbox("Select a movie", movie_list)

    # Get the selected movie's information and display it
    movie_info = session.run(GET_MOVIE_INFO, title=selected_movie).single()
    st.write(f"Title: {movie_info['m.title']}")
    st.write(f"Released year: {movie_info['m.released_year']}")
    st.write(f"Kind: {movie_info['m.kind']}")
    st.write(f"Nationality: {movie_info['m.nationality']}")
    st.write(f"Average ranking: {movie_info['m.average_ranking']}")

    # Add a "Rate" button to rate the selected movie
    if st.button("Rate"):
        rating = st.number_input("Enter your rating (0-5)", min_value=0, max_value=5)
        session.run(RATE_MOVIE, title=selected_movie, average_ranking=rating)
        st.success(f"You rated {selected_movie} {rating} stars.")

    # Add a "Delete" button to delete the selected movie
    if st.button("Delete"):
        session.run(f"MATCH (m:Movie {{title: '{selected_movie}'}}) DETACH DELETE m")
        st.success(f"{selected_movie} has been deleted from the database.")

