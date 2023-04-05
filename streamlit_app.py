import streamlit as st
import pymongo
#client = pymongo.MongoClient("mongodb+srv://kamounazzap:Hello123.@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
#db = client.test
import requests
import json
url = "https://data.mongodb-api.com/app/data-mnfje/endpoint/data/v1/action/findOne"

payload = json.dumps({
    "collection": "moviesds",
    "database": "moviesds",
    "dataSource": "Cluster0",
    "projection": {
        "_id": 1
    }
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': gKkfz9siabHfG8cXbJeCfz55m1qyka5AYMdS9yyZMXkXANd6iUZrUD9tZUClqONs, 
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)





def display_movie_info(selected_movie_info):
    st.write(f"Title: {selected_movie_info['title']}")
    st.write(f"Released year: {selected_movie_info['released_year']}")
    st.write(f"Kind: {selected_movie_info['kind']}")
    st.write(f"Nationality: {selected_movie_info['nationality']}")
    st.write(f"Average ranking: {selected_movie_info['average_ranking']:.1f}")


def add_comment(selected_movie_info):
    nickname = st.text_input("Enter your nickname", value="Anonymous")
    comment = st.text_input("Enter your comment")
    if st.button("Add Comment"):
        if nickname != "Anonymous" and not comment:
            st.error("You must write a comment.")
        elif comment:
            selected_movie_info["comments"].append({"nickname": nickname, "comment": comment})
            st.success("Comment added.")
            
def rate_movie(selected_movie_info):
    rating = st.slider("Rate the movie (1-5)", 1, 5, 1)
    if st.button("Submit Review"):
        if rating >= 1 and rating <= 5:
            if "ratings" in selected_movie_info:
                selected_movie_info["ratings"].append(rating)
            else:
                selected_movie_info["ratings"] = [rating]
            st.success("Rating added.")
        else:
            st.error("Invalid rating. Please choose a rating between 1 and 5.")


def add_new_movie(movies):
    title = st.text_input("Title")
    released_year = st.number_input("Released year", min_value=1800, max_value=2100)
    kind = st.text_input("Kind")
    nationality = st.text_input("Nationality")
    if st.button("Add movie"):
        new_movie = {"title": title, "released_year": released_year, "kind": kind, "nationality": nationality,
                     "average_ranking": 0, "comments": [], "ratings": []}
        movies.append(new_movie)
        st.success(f"{title} has been added to the database.")
    return movies


def delete_movie(movies, selected_movie_info):
    movies.remove(selected_movie_info)
    st.success(f"{selected_movie_info['title']} has been deleted from the database.")
    return movies

def display_comments(selected_movie_info):
    st.write("Comments:")
    for comment in selected_movie_info["comments"]:
        if "nickname" in comment and "comment" in comment:
            st.write(f"{comment['nickname']}: {comment['comment']}")

def main():
    st.set_page_config(page_title="Movie Database", page_icon=":movie_camera:")

    st.title("Movie Database")

    menu = ["Home", "Add New Movie", "View Movie Info", "Delete Movie"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # List of example movies
    movies = [
        {"title": "The Shawshank Redemption", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.7, "comments": ["Great movie!", "One of my all-time favorites."]},
        {"title": "The Godfather", "released_year": 1972, "kind": "Crime", "nationality": "USA", "average_ranking": 4.8, "comments": ["A classic!", "Marlon Brando was amazing."]},
        {"title": "The Dark Knight", "released_year": 2008, "kind": "Action", "nationality": "USA", "average_ranking": 4.6, "comments": ["Heath Ledger's performance was outstanding.", "Great soundtrack."]},
        {"title": "The Lord of the Rings: The Fellowship of the Ring", "released_year": 2001, "kind": "Adventure", "nationality": "USA", "average_ranking": 4.5, "comments": ["Epic story!", "The special effects were amazing."]},
        {"title": "Forrest Gump", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.4, "comments": ["Tom Hanks was perfect for this role.", "Heartwarming story."]}
        ]
    
    if choice == "Home":
        st.write("Welcome to the Movie Database! Use the menu on the left to navigate.")

    elif choice == "Add New Movie":
        movies = add_new_movie(movies)

    elif choice == "View Movie Info":
        selected_movie_title = st.selectbox("Select a movie", [movie["title"] for movie in movies])
        selected_movie_info = [movie for movie in movies if movie["title"] == selected_movie_title][0]
        display_movie_info(selected_movie_info)
        add_comment(selected_movie_info)
        display_comments(selected_movie_info)
        rate_movie(selected_movie_info)

    elif choice == "Delete Movie":
        selected_movie_title = st.selectbox("Select a movie", [movie["title"] for movie in movies])
        selected_movie_info = [movie for movie in movies if movie["title"] == selected_movie_title][0]
        movies = delete_movie(movies, selected_movie_info)

    st.sidebar.write("Movie List")
    for movie in movies:
        st.sidebar.write(movie["title"])            
main()

    
