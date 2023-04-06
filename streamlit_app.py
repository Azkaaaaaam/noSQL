import streamlit as st
import pymongo
#client = pymongo.MongoClient("mongodb+srv://kamounazzap:Hello123.@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
#db = client.test
#mongodb://_:<API-KEY>@global.aws.realm.mongodb.com:27020/?authMechanism=PLAIN&authSource=%24external&ssl=true&appName=data-mnfje:Cluster0:api-key


client = pymongo.MongoClient("mongodb+srv://kamounazzap:Hello123.@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority")
db = client.test
#db = client.test
movies_collection = db["moviesds"]

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


def delete_movie():
    movie_titles = [movie["title"] for movie in movies_collection.find()]
    selected_movie_title = st.selectbox("Select a movie", movie_titles)
    selected_movie_info = movies_collection.find_one({"title": selected_movie_title})
    movies_collection.delete_one({"_id": selected_movie_info["_id"]})
    st.success(f"{selected_movie_info['title']} has been deleted from the database.")


def display_comments(selected_movie_info):
    st.write("Comments:")
    comments = selected_movie_info.get("comments", [])
    for comment in comments:
        if "nickname" in comment and "comment" in comment:
            st.write(f"{comment['nickname']}: {comment['comment']}")

def main():
    st.set_page_config(page_title="Movie Database", page_icon=":movie_camera:")

    st.title("Movie Database")

    menu = ["Home", "Add New Movie", "View Movie Info", "Delete Movie"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Connect to the database
    conn = sqlite3.connect('movie_database.db')
    c = conn.cursor()

    if choice == "Home":
        st.write("Welcome to the Movie Database! Use the menu on the left to navigate.")

    elif choice == "Add New Movie":
        add_new_movie(c, conn)

    elif choice == "View Movie Info":
        # Retrieve the list of movie titles from the database
        movie_titles = get_movie_titles(c)

        selected_movie_title = st.selectbox("Select a movie", movie_titles)
        selected_movie_info = get_movie_info(c, selected_movie_title)
        display_movie_info(selected_movie_info)
        add_comment(selected_movie_info, c, conn)
        display_comments(selected_movie_info)
        rate_movie(selected_movie_info, c, conn)

    elif choice == "Delete Movie":
        # Retrieve the list of movie titles from the database
        movie_titles = get_movie_titles(c)

        selected_movie_title = st.selectbox("Select a movie", movie_titles)
        selected_movie_info = get_movie_info(c, selected_movie_title)
        delete_movie(selected_movie_info, c, conn)

    st.sidebar.write("Movie List")
    # Retrieve the list of movies from the database
    movies = get_all_movies(c)
    for movie in movies:
        st.sidebar.write(movie[0])

    # Close the database connection
    conn.close()

main()

main()

    
