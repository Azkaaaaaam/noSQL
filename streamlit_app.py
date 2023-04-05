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
    new_movie = {"title": title, "released_year": released_year, "kind": kind, "nationality": nationality, "average_ranking": 0, "comments": []}
    movies.append(new_movie)
    st.sidebar.success(f"{title} has been added to the database.")

# List of example movies
movies = [
    {"title": "The Shawshank Redemption", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.7, "comments": ["Great movie!", "One of my all-time favorites."]},
    {"title": "The Godfather", "released_year": 1972, "kind": "Crime", "nationality": "USA", "average_ranking": 4.8, "comments": ["A classic!", "Marlon Brando was amazing."]},
    {"title": "The Dark Knight", "released_year": 2008, "kind": "Action", "nationality": "USA", "average_ranking": 4.5, "comments": ["Heath Ledger's Joker was iconic.", "The action scenes were breathtaking."]},
    {"title": "Pulp Fiction", "released_year": 1994, "kind": "Crime", "nationality": "USA", "average_ranking": 4.4, "comments": []},
    {"title": "Forrest Gump", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.6, "comments": []},
]

# Add example movies to the dropdown list
movie_list = [movie["title"] for movie in movies]
selected_movie = st.selectbox("Select a movie", movie_list)
selected_movie_info = next((movie for movie in movies if movie["title"] == selected_movie), None)
if selected_movie_info is not None:
    # Add a list of nicknames to the selected movie info dictionary
    if "nicknames" not in selected_movie_info:
        selected_movie_info["nicknames"] = []
    
    st.write(f"Title: {selected_movie_info['title']}")
    st.write(f"Released year: {selected_movie_info['released_year']}")
    st.write(f"Kind: {selected_movie_info['kind']}")
    st.write(f"Nationality: {selected_movie_info['nationality']}")
    st.write(f"Average ranking: {selected_movie_info['average_ranking']}")
    
    # Add a comments section
    comment_expander = st.beta_expander("Comments", expanded=True)
    with comment_expander:
        # Display the comments for the selected movie
        if selected_movie_info["comments"]:
            for i in range(len(selected_movie_info["comments"])):
                st.write(f"{selected_movie_info['nicknames'][i]}: {selected_movie_info['comments'][i]}")
        else:
            st.write("No comments yet. Be the first to add a comment!")

        # Add a "Add Comment" button to add a comment to the selected movie
        with st.beta_container():
            comment = st.text_input("Enter your comment")
            nickname = st.text_input("Enter your nickname")
            if st.button("Add Comment"):
                if comment and nickname:
                    selected_movie_info["comments"].append(comment)
                    selected_movie_info["nicknames"].append(nickname)
                    st.success(f"Comment added to {selected_movie}.")

    
    # Add a "Add Comment" button to add a comment to the selected movie
    if st.button("Add Comment"):
        comment = st.text_input("Enter your comment")
        nickname = st.text_input("Enter your nickname")
        if comment and nickname:
            selected_movie_info["comments"].append(comment)
            selected_movie_info["nicknames"].append(nickname)
            st.success(f"Comment added to {selected_movie}.")
        
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
