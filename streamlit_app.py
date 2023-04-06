import streamlit as st
import pymongo
import sqlite3

#client = pymongo.MongoClient("mongodb+srv://kamounazzap:Hello123.@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
#db = client.test
#mongodb://_:<API-KEY>@global.aws.realm.mongodb.com:27020/?authMechanism=PLAIN&authSource=%24external&ssl=true&appName=data-mnfje:Cluster0:api-key


client = pymongo.MongoClient("mongodb+srv://streamlit:streamlit@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority")

# Access the "moviesds" database.
db = client["moviesds"]

# Access the "moviesds" collection.
movies_collection = db["moviesds"]

def display_movie_info(selected_movie_info):
    if selected_movie_info is not None:
        st.write(f"Title: {selected_movie_info['title']}")
        st.write(f"year: {selected_movie_info['year']}")
        st.write(f"genre: {selected_movie_info['genre']}")
        st.write(f"Nationality: {selected_movie_info['nationality']}")
        st.write(f"average rating: {selected_movie_info['average_rating']}")
    else:
        st.write("No movie selected.")

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
            ratings = selected_movie_info.get("average_rating", [])
            ratings.append(rating)
            movies_collection.update_one({"_id": selected_movie_info["_id"]}, {"$set": {"average_rating": average_rating}})
            st.success("Rating added.")
        else:
            st.error("Invalid rating. Please choose a rating between 1 and 5.")

def delete_movie(selected_movie_info, movies_collection):
    if selected_movie_info is not None:
        title = selected_movie_info["title"]
        dropdown_options = [title] # Add the movie title to the dropdown options
        st.write(f"Select '{title}' to delete from the database:")
        selected_movie_title = st.selectbox("Movies", dropdown_options)
        if st.button("Delete"):
            movies_collection.delete_one({"_id": selected_movie_info["_id"]})
            st.success(f"{selected_movie_title} has been deleted from the database.")
    else:
        st.write("No movie selected.")

def add_new_movie():
    title = st.text_input("Title")
    year = st.number_input("year", min_value=1800, max_value=2100)
    genre = st.text_input("genre")
    nationality = st.text_input("Nationality")
    if st.button("Add movie"):
        new_movie = {"title": title, "year": year, "genre": genre, "nationality": nationality,
                     "average_rating": 0, "comments": [], "ratings": []}
        movies_collection.insert_one(new_movie)
        st.success(f"{title} has been added to the database.")




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
            st.write(f"Released year: {movie['year']}")
            st.write(f"genre: {movie['genre']}")
            st.write(f"Nationality: {movie['nationality']}")
            st.write(f"Average rating: {movie['average_rating']}")
            display_comments(movie)
            st.write("\n")

    # Search movies
    elif choice == "Search Movies":
        st.header("Search Movies")
        search_term = st.text_input("Enter a search term")
        movies = movies_collection.find({"$or": [{"title": {"$regex": search_term, "$options": "-i"}},
                                                  {"genre": {"$regex": search_term, "$options": "-i"}},
                                                  {"nationality": {"$regex": search_term, "$options": "-i"}}]})
        for movie in movies:
            st.write(f"Title: {movie['title']}")
            st.write(f"Released year: {movie['year']}")
            st.write(f"genre: {movie['genre']}")
            st.write(f"Nationality: {movie['nationality']}")
            st.write(f"Average rating: {movie['average_rating']}")
            display_comments(movie)
            st.write("\n")

    # Add movie
    elif choice == "Add Movie":
        st.header("Add Movie")
        add_new_movie()

    # Delete movie
    elif choice == "Delete Movie":
        st.header("Delete Movie")
        delete_movie(selected_movie_info, movies_collection)

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
    
