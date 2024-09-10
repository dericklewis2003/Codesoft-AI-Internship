# Codesoft-AI-Internship

# TASK 1
# Tic-Tac-Toe with AI

## Project Description

This project is an implementation of the classic Tic-Tac-Toe game using Python and Pygame. It features a graphical user interface and an AI opponent with adjustable difficulty levels.

### Key Features:

- **Graphical User Interface**: Clean and intuitive design using Pygame.
- **AI Opponent**: Play against a computer opponent with three difficulty levels:
  - Easy: Makes random moves.
  - Medium: Alternates between random and strategic moves.
  - Hard: Uses the Minimax algorithm for optimal play.
- **Best of 5 Series**: Games are played in a series, with the first to win 3 games declared the overall winner.
- **Score Tracking**: Keeps track of wins for both the human player and the AI.
- **Customizable**: Easy to modify colors and game parameters.

### Technologies Used:

- Python
- Pygame

### How to Play:

1. Choose a difficulty level from the main menu.
2. Click on the game board to make your move.
3. Try to get three in a row to win a game.
4. Win 3 games to win the series!

Enjoy playing against an AI opponent that adapts to your skill level!


# TASK 2

# Movie Recommendation System

## Project Description

This Movie Recommendation System is a Python-based application that suggests movies to users based on their preferences. It utilizes machine learning techniques to analyze movie features and provide personalized recommendations through a user-friendly graphical interface.

## Features

- **Data-Driven Recommendations**: Utilizes a dataset of movies with various features such as genres, keywords, taglines, cast, and directors.
- **Machine Learning Algorithm**: Implements TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity to find movies similar to the user's input.
- **Graphical User Interface**: Provides an intuitive GUI built with Tkinter for easy interaction.
- **Real-time Recommendations**: Generates and displays top 10 movie recommendations based on user input.

## Technologies Used

- Python 3.x
- Libraries:
  - Pandas: For data manipulation and analysis
  - NumPy: For numerical operations
  - Scikit-learn: For implementing machine learning algorithms (TfidfVectorizer and cosine_similarity)
  - Tkinter: For creating the graphical user interface

## How It Works

1. **Data Preprocessing**: The system loads and preprocesses movie data, combining relevant features into a single text representation for each movie.

2. **Feature Extraction**: TF-IDF vectorization is applied to convert the text data into numerical feature vectors.

3. **Similarity Calculation**: Cosine similarity is computed between all pairs of movies based on their feature vectors.

4. **User Input**: The user enters the name of a movie they like through the GUI.

5. **Recommendation Generation**: The system finds the closest match to the user's input, then identifies and ranks similar movies based on the pre-computed similarity scores.

6. **Display**: The top 10 recommended movies are displayed in the GUI.





