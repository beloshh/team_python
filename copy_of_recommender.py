# -*- coding: utf-8 -*-

#import libraries
import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#read the posts table from the JSON file
l_posts = pd.read_json('json_data/lucid_table_posts.json',orient='columns')

#read the notifications table from the JSON file
l_nots = pd.read_json('json_data/lucid_table_notifications.json',orient='columns')

#read the following table from the JSON file
l_follow =  pd.read_json('json_data/lucid_table_following.json',orient='columns')

#read the thoughts table from the JSON file
l_thoughts =  pd.read_json('json_data/lucid_table_thoughts.json',orient='columns')

#read the users table from the JSON file
l_users =  pd.read_json('json_data/lucid_table_users.json',orient='columns')

#printing 3 rows in the contents of the posts table
l_posts.head(3)

#selecting only 'id', 'user_id', and 'title' in the posts table as that is what we would be using
posts = l_posts[['id','user_id','title']]
#printing the selected columns
posts.head()

#printing 3 rows in the contents of the notifications table
l_nots.head(3)

#selecting only 'id', 'user_id', and 'action' in the notifications table as that is what we would be using
notifs = l_nots[['id', 'user_id', 'action']]
#printing the selected columns
notifs.head()

"""# MOST POPULAR ARTICLES"""

#merging posts and notifications table on user_id
pop_articles = posts.merge(notifs, on='user_id')
#arranging the titles and the amount of actions performed on the titles in descending order
pop_articles = pop_articles.groupby('title')['action'].count().sort_values(ascending=False)
print("TOP 10 RECOMMENDATIONS BASED ON MOST POPULAR ARTICLES\n")
print(pop_articles.head(10))

"""#CONTENT BASED RECOMMENDER"""

#printing 10 rows in the title column in the posts table
posts['title'].head(10)

#Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

#Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(posts['title'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#Construct a reverse map of indices and post titles
indices = pd.Series(posts.index, index=posts['title']).drop_duplicates()

# function that takes in a post title as an input
# this is when a user clicks on an article

def get_recommendations(title, cosine_sim=cosine_sim):
  
  try:
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the posts based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar posts
    sim_scores = sim_scores[1:11]

    # Get the post indices
    post_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar posts
    print("RECOMMENDATIONS BASED ON YOUR READING PATTERN\n")
    return posts['title'].iloc[post_indices]
  
  except KeyError:
    print("We Have No Recommendations For You!")

#calling function for recommendation
get_recommendations('First HTML Project')