import streamlit as st
import pymongo
import sqlite3

#client = pymongo.MongoClient("mongodb+srv://kamounazzap:Hello123.@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
#db = client.test
#mongodb://_:<API-KEY>@global.aws.realm.mongodb.com:27020/?authMechanism=PLAIN&authSource=%24external&ssl=true&appName=data-mnfje:Cluster0:api-key


client = pymongo.MongoClient("mongodb+srv://streamlit:streamlit@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority")
db = client.test
movies_collection = db["moviesds.moviesds"]


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
            comments = selected_movie_info.get("comments", [])
            comments.append({"nickname": nickname, "comment": comment})
            movies_collection.update_one({"_id": selected_movie_info["_id"]}, {"$set": {"comments": comments}})
            st.success("Comment added.")
            
def rate_movie(selected_movie_info):
    rating = st.slider("Rate the movie (1-5)", 1, 5, 1)
    if st.button("Submit Review"):
        if rating >= 1 and rating <= 5:
            ratings = selected_movie_info.get("ratings", [])
            ratings.append(rating)
            movies_collection.update_one({"_id": selected_movie_info["_id"]}, {"$set": {"ratings": ratings}})
            st.success("Rating added.")
        else:
            st.error("Invalid rating. Please choose a rating between 1 and 5.")


def add_new_movie():
    title = st.text_input("Title")
    released_year = st.number_input("Released year", min_value=1800, max_value=2100)
    kind = st.text_input("Kind")
    nationality = st.text_input("Nationality")
    if st.button("Add movie"):
        new_movie = {"title": title, "released_year": released_year, "kind": kind, "nationality": nationality,
                     "average_ranking": 0, "comments": [], "ratings": []}
        movies_collection.insert_one(new_movie)
        st.success(f"{title} has been added to the database.")


def display_movie_info(selected_movie_info):
    if selected_movie_info is not None:
        st.write(f"Title: {selected_movie_info['title']}")
        st.write(f"Year: {selected_movie_info['year']}")
        st.write(f"Genre: {selected_movie_info['genre']}")
        st.write(f"Director: {selected_movie_info['director']}")
    else:
        st.write("No movie selected.")


def display_comments(selected_movie_info):
    st.write("Comments:")
    comments = selected_movie_info.get("comments", [])
    for comment in comments:
        if "nickname" in comment and "comment" in comment:
            st.write(f"{comment['nickname']}: {comment['comment']}")


def main():
    st.set_page_config(page_title="Movie Database", page_icon=":movie_camera:")

    # Sidebar options
    options = ["View All Movies", "Search Movies", "Add Movie", "Delete Movie"]
    choice = st.sidebar.selectbox("Select an option", options)

    # View all movies
    if choice == "View All Movies":
        st.header("All Movies")
        movies = movies_collection.find()
        for movie in movies:
            st.write(f"Title: {movie['title']}")
            st.write(f"Released year: {movie['released_year']}")
            st.write(f"Kind: {movie['kind']}")
            st.write(f"Nationality: {movie['nationality']}")
            st.write(f"Average ranking: {movie['average_ranking']:.1f}")
            display_comments(movie)
            st.write("\n")

    # Search movies
    elif choice == "Search Movies":
        st.header("Search Movies")
        search_term = st.text_input("Enter a search term")
        movies = movies_collection.find({"$or": [{"title": {"$regex": search_term, "$options": "-i"}},
                                                  {"kind": {"$regex": search_term, "$options": "-i"}},
                                                  {"nationality": {"$regex": search_term, "$options": "-i"}}]})
        for movie in movies:
            st.write(f"Title: {movie['title']}")
            st.write(f"Released year: {movie['released_year']}")
            st.write(f"Kind: {movie['kind']}")
            st.write(f"Nationality: {movie['nationality']}")
            st.write(f"Average ranking: {movie['average_ranking']:.1f}")
            display_comments(movie)
            st.write("\n")

    # Add movie
    elif choice == "Add Movie":
        st.header("Add Movie")
        add_new_movie()

    # Delete movie
    elif choice == "Delete Movie":
        st.header("Delete Movie")
        delete_movie()

    # View movie details
    st.sidebar.write("\n")
    movie_titles = [movie["title"] for movie in movies_collection.find()]
    selected_movie_title = st.sidebar.selectbox("Select a movie", movie_titles)
    selected_movie_info = movies_collection.find_one({"title": selected_movie_title})
    st.sidebar.write("\n")
    display_movie_info(selected_movie_info)
    st.sidebar.write("\n")
    rate_movie(selected_movie_info)
    st.sidebar.write("\n")
    add_comment(selected_movie_info)


main()
    
