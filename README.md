
# NoSQL - MongoDB + Streamlit

A brief description of what this project does and who it's for


## Documentation

[1- How to link GIthub and MongoDB](https://drive.google.com/file/d/1flTM8Mqby30gAXSRSWzf9EiVP9h_DiJw/view?usp=sharing)

[2- JSON- Configuration of MongoDB](https://github.com/Azkaaaaaam/noSQL/blob/588efa1fb60bfd776c7ad0d3da6685199959cd12/realm_config.json)

[3- Demo Running The App](https://drive.google.com/file/d/1c1g6Eb4JpOIZ1vcUAixlx7bX6qMdU7zl/view?usp=sharing)

[4- Want to Try it Yourself?](https://azkaaaaaam-nosql-streamlit-app-fqbmi0.streamlit.app/)
## Installing Libraries

To install the required libraries :
```javascript
$ pip install -r requirements.txt
```

## The main frontend app 

This [streamlit.py](https://github.com/Azkaaaaaam/noSQL/blob/588efa1fb60bfd776c7ad0d3da6685199959cd12/streamlit_app.py) is an implementation a web app using the Streamlit framework, aiming to manage a movie database that we previously stored in a MongoDB database [see next section].

In our app, we connect to the MongoDB database using the PyMongo library, and it uses the "moviesds" database and "moviesds" collection to store the movie data. The movie data includes fields such as title, year, genre, nationality, average rating, comments, and ratings.

### main() function

--> The main function of the script is defined by the Streamlit app, which displays a sidebar with four options: **"View All Movies"**, **"Add Movie"**, **"Delete Movie"**, and **"Rate Movie"**. 

- **The "View All Movies"** option retrieves all movies from the MongoDB collection and displays their information using the "display_movie_info" and "display_comments" functions. 
- **The "Add Movie"** option allows the user to add a new movie to the database using the "add_new_movie" function. 
- **The "Delete Movie"** option allows the user to delete a movie from the database using the "delete_movie" function. 
- Finally, **the "Rate Movie"** option allows the user to rate a movie and add comments to it using the "add_comment" and "update_rating" functions.

--> **The "display_movie_info"** function displays the title, year, genre, nationality, and average rating of a selected movie. The "display_comments" function displays the comments of a selected movie.

--> **The "add_comment"** function allows the user to add a comment to a selected movie. The "update_rating" function allows the user to update the average rating of a selected movie.

### Connection to DB 
In our python code, we define several  functions to connect to the MongoDB database, retrieve movie data, and manipulate movie data, EG: "connect_to_mongodb", "get_movies_data", and "update_movie_data".

```javascript
client = pymongo.MongoClient("mongodb+srv://<user>:<psw>@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority")

# Access the "moviesds" database.
db = client["moviesds"]

# Access the "moviesds" collection.
movies_collection = db["moviesds"]
```


## The Backend: MongoDB in Cloud -- [link](https://cloud.mongodb.com/)

The database contains movie data, including the title, genre, year, nationality, average rating, comments, and ratings. The data is stored in a collection called "movies". The following is a breakdown of the fields for each movie document:

- Title (string): The title of the movie.
- Genre (string): The genre of the movie.
- Year (long): The year the movie was released.
- Nationality (string): The nationality of the movie.
- Average Rating (string or double): The average rating of the movie based on user ratings.
- Comments (array of objects): An array of comments made by users who have watched the movie. Each comment object contains a nickname (string) and comment (string).
- Ratings (array of integers): An array of integers representing the user ratings for the movie.

Exemple:
```javascript
{"_id":{"$oid":"642dc4607d99ed0ce91ba527"},"title":"Avengers: Endgame","genre":"Action","year":{"$numberLong":"2019"},"nationality":"American","average_rating":"4.8","comments":[{"nickname":"marvel_fan","comment":"This movie was amazing!"},{"nickname":"avenger_lover","comment":"Best movie ever!"}]}
```
