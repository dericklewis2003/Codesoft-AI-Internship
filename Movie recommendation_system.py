import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style

# Data Import
movies_data = pd.read_csv('https://raw.githubusercontent.com/Pistonamey/Movie-Recommendation/main/movies.csv')

# Feature Selection
selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']

# Data Preprocessing
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')

# Combining all the selected features
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + \
    movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director']

# Converting the text data to feature vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

# Getting the similarity scores using cosine similarity
similarity = cosine_similarity(feature_vectors)

# Creating a list with all the movie names given in the dataset
list_of_all_titles = movies_data['title'].tolist()

def get_recommendations():
    movie_name = movie_entry.get()
    if not movie_name:
        messagebox.showerror("Error", "Please enter a movie name")
        return

    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    if not find_close_match:
        messagebox.showerror("Error", "No close matches found. Please try another movie.")
        return

    close_match = find_close_match[0]
    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    recommendations.delete(*recommendations.get_children())
    for i, movie in enumerate(sorted_similar_movies[1:11], 1):
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['title'].values[0]
        recommendations.insert("", "end", values=(i, title_from_index))

# Create the main window with a modern style
root = tk.Tk()
style = Style(theme="flatly")
root.title("Movie Recommender")
root.geometry("500x600")

# Create a main frame
main_frame = ttk.Frame(root, padding="20 20 20 20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create and pack widgets with improved layout
ttk.Label(main_frame, text="Enter your favorite movie:", font=("Helvetica", 14)).pack(pady=(0, 10))

movie_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 12))
movie_entry.pack(pady=(0, 20), ipady=5)

ttk.Button(main_frame, text="Get Recommendations", command=get_recommendations, style="Accent.TButton").pack(pady=(0, 20))

ttk.Label(main_frame, text="Recommended Movies:", font=("Helvetica", 14)).pack(pady=(0, 10))

# Use a Treeview instead of Listbox for a more modern look
columns = ("Rank", "Movie Title")
recommendations = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
recommendations.heading("Rank", text="Rank")
recommendations.heading("Movie Title", text="Movie Title")
recommendations.column("Rank", width=50, anchor="center")
recommendations.column("Movie Title", width=400)
recommendations.pack(pady=(0, 20), fill=tk.BOTH, expand=True)

# Start the GUI event loop
root.mainloop()