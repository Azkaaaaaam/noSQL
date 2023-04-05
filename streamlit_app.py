import streamlit as st

# Define movie class to store movie information and comments
class Movie:
    def __init__(self, title, released_year, kind, nationality, comments=None):
        self.title = title
        self.released_year = released_year
        self.kind = kind
        self.nationality = nationality
        self.comments = comments or []

    def add_comment(self, commenter, comment):
        self.comments.append((commenter, comment))

    def __str__(self):
        return f"{self.title} ({self.released_year}), {self.kind}, {self.nationality}, {len(self.comments)} comments"


# Define function to add a new movie to the movie list
def add_movie(movie_list):
    title = st.sidebar.text_input("Title")
    released_year = st.sidebar.number_input("Released year", min_value=1800, max_value=2100)
    kind = st.sidebar.text_input("Kind")
    nationality = st.sidebar.text_input("Nationality")
    movie = Movie(title, released_year, kind, nationality)
    movie_list.append(movie)
    st.sidebar.success(f"{title} has been added to the database.")


# Define function to rate a movie
def rate_movie(movie, rating):
    if rating is not None:
        if movie.average_ranking is None:
            movie.average_ranking = rating
        else:
            movie.average_ranking = (movie.average_ranking + rating) / 2


# Define function to add a comment to a movie
def add_comment(movie):
    commenter = st.text_input("Your name")
    comment = st.text_input("Your comment")
    if commenter and comment:
        movie.add_comment(commenter, comment)
        st.success("Comment added.")


# Define some sample movies
movie_list = [
    Movie("The Godfather", 1972, "Crime, Drama", "USA", [("John", "Great movie!"), ("Jane", "I loved it!")]),
    Movie("The Shawshank Redemption", 1994, "Drama", "USA"),
    Movie("The Dark Knight", 2008, "Action, Crime, Drama", "USA", [("Mary", "Amazing film"), ("Bob", "The best superhero movie ever!")]),
    Movie("The Godfather: Part II", 1974, "Crime, Drama", "USA", [("Alice", "Even better than the first one")])
]

# Streamlit app layout
st.title("Movie Database")
st.header("Select a movie from the dropdown list to view its details, rate it, add a comment or delete it.")
st.sidebar.header("Add a new movie")
add_movie(movie_list)

selected_movie = st.selectbox("Select a movie", [str(movie) for movie in movie_list])
selected_movie = next((movie for movie in movie_list if str(movie) == selected_movie), None)

if selected_movie is not None:
    st.write(f"Title: {selected_movie.title}")
    st.write(f"Released year: {selected_movie.released_year}")
    st.write(f"Kind: {selected_movie.kind}")
    st.write(f"Nationality: {selected_movie.nationality}")
    st.write(f"Average ranking: {selected_movie.average_ranking}")

    # Add a "Rate" button to rate the selected movie
    rating = st.number_input("Enter your rating (0-5)", min_value=0, max_value=5)
    rate_movie(selected_movie, rating)
    if rating is not None:
        st.success(f"You rated {selected_movie.title}
