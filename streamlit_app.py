import streamlit as st


def add_new_movie(movies):
    title = st.sidebar.text_input("Title")
    released_year = st.sidebar.number_input("Released year", min_value=1800, max_value=2100)
    kind = st.sidebar.text_input("Kind")
    nationality = st.sidebar.text_input("Nationality")
    if st.sidebar.button("Add movie"):
        new_movie = {"title": title, "released_year": released_year, "kind": kind, "nationality": nationality, "average_ranking": 0, "comments": []}
        movies.append(new_movie)
        st.sidebar.success(f"{title} has been added to the database.")
    return movies


def display_movie_info(selected_movie_info):
    st.write(f"Title: {selected_movie_info['title']}")
    st.write(f"Released year: {selected_movie_info['released_year']}")
    st.write(f"Kind: {selected_movie_info['kind']}")
    st.write(f"Nationality: {selected_movie_info['nationality']}")
    st.write(f"Average ranking: {selected_movie_info['average_ranking']}")
    

def add_comment(selected_movie_info):
    comment = st.text_input("Enter your comment")
    nickname = st.text_input("Enter your nickname")
    if st.button("Add Comment"):
        if comment and nickname:
            selected_movie_info["comments"].append(comment)
            selected_movie_info["nicknames"].append(nickname)
            st.success(f"Comment added to {selected_movie_info['title']}.")


def display_comments(selected_movie_info):
    st.write("Comments:")
    if "nicknames" in selected_movie_info:
        for i, comment in enumerate(selected_movie_info["comments"]):
            if i < len(selected_movie_info["nicknames"]):
                st.write(f"{selected_movie_info['nicknames'][i]}: {comment}")
            else:
                st.write(f"Anonymous: {comment}")
    else:
        for comment in selected_movie_info["comments"]:
            st.write(f"Anonymous: {comment}")


def rate_movie(selected_movie_info):
    rating = st.number_input("Enter your rating (0-5)", min_value=0, max_value=5)
    selected_movie_info["average_ranking"] = (rating + selected_movie_info["average_ranking"]) / 2
    st.success(f"You rated {selected_movie_info['title']} {rating} stars.")


def delete_movie(movies, selected_movie_info):
    movies.remove(selected_movie_info)
    st.success(f"{selected_movie_info['title']} has been deleted from the database.")
    return movies


def main():
    st.title("Movie Database")
    st.header("Select a movie from the dropdown list to view its details, rate it, or delete it.")
    
    # List of example movies
    movies = [
        {"title": "The Shawshank Redemption", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.7, "comments": ["Great movie!", "One of my all-time favorites."]},
        {"title": "The Godfather", "released_year": 1972, "kind": "Crime", "nationality": "USA", "average_ranking": 4.8, "comments": ["A classic!", "Marlon Brando was amazing."]},
        {"title": "The Dark Knight", "released_year": 2008, "kind": "Action", "nationality": "USA", "average_ranking": 4.6, "comments": ["Heath Ledger's performance was outstanding.", "Great soundtrack."]},
        {"title": "The Lord of the Rings: The Fellowship of the Ring", "released_year": 2001, "kind": "Adventure", "nationality": "USA", "average_ranking": 4.5, "comments": ["Epic story!", "The special effects were amazing."]},
        {"title": "Forrest Gump", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.4, "comments": ["Tom Hanks was perfect for this role.", "Heartwarming story."]}
        ]
    # Create a list of movie titles for the dropdown menu
    movie_titles = [movie["title"] for movie in movies]

    # Create a dropdown menu to select a movie
    selected_movie_title = st.selectbox("Select a movie", movie_titles)

    # Find the selected movie in the list of movies
    selected_movie_info = None
    for movie in movies:
        if movie["title"] == selected_movie_title:
            selected_movie_info = movie
            break

    # Display the details of the selected movie
    if selected_movie_info:
        display_movie_info(selected_movie_info)
        rate_movie(selected_movie_info)
        add_comment(selected_movie_info)
        display_comments(selected_movie_info)
        if st.button("Delete movie"):
            movies = delete_movie(movies, selected_movie_info)

    # Add a new movie to the database
    movies = add_new_movie(movies)
if name == "main":
main()

    
