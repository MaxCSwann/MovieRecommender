import os
import datetime
from django.db import models
from django.contrib.auth.models import User
import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

""" 
---------------------
where I left off 
---------------------
currently the primary key of a movie is its title
these are unique but it makes things difficult 
when i got rid of the primary key attribute django complained
it gets confused when it tries to reassign ids 
https://stackoverflow.com/questions/32991965/you-are-trying-to-add-a-non-nullable-field-id-to-contact-info-without-a-defaul
this stack overflow explains the problem perfectly
i tried resetting my db but apparently this didnt do anything and the problem persists
so now we have no movies in our db 
will need to re add them all in the populate db.ipynb file

update:
FIIIIIIIXXXXXEEEEEED
"""
#this will be populated either by converting csv to model including only necessary attributes
#-->or by converting pandas dataframe defined in populate.ipynb to django models <--
class Movie(models.Model):
    Title = models.CharField(max_length=100) #string, Title is the unique Index
    Genre = models.CharField(max_length=100) #string, can be multiple genres e.g 'Crime, Drama'
    Director = models.CharField(max_length=100) #string, can be multiple genres e.g 'Sam Wood, Edmund Goulding'
    Actors = models.TextField()#string, can be multiple genres e.g 'Ewan McGregor, Albert Finney, Billy Crudup, Jessica Lange'
    Plot = models.TextField() #long string
    tomatoURL = models.URLField() #url to rotten tomatoes page on the movie
    #bag_of_words = models.TextField() #will need to generate (not in csv initially) space seperated string
    #Key_words = models.TextField() #is the keyword extraction of the plot using rake 
    Poster = models.URLField()#img url 
    #Reviews = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True) #reviews for a given movie
    #slug for heroku compatibility

    #TODO:create a method that computes simlarity score to all other movies returns
    #returns an ordered list of movies most similar to least similar
    #TODO:maake this save as a list as a movie attribute
    #try catch when trying to return movie list, if is set return
    #else compute, save, return

    #TODO: create a function that returns list of similar movies
    #returns a queryset of movie objects
    def getSimilarMovies(self):   

        if os.path.isfile('./cosine_sim.npy'):
            cosine_sim = np.load('cosine_sim.npy')
        else:
            cosine_sim = computeSimilarityMatrix()

        # gettin the index of the movie, -1 as django counts from 1
        idx = (self.id-1)

        # creating a Series with the similarity scores in descending order
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

        # getting the indexes of the 10 most similar movies
        top_10_indexes = list(score_series.iloc[1:11].index)
        
        #this is to match the returned ids to djangos ids
        for i,idx in enumerate(top_10_indexes):
            top_10_indexes[i] = idx + 1

        #queryset is all movies with matching ids
        return Movie.objects.filter(id__in=top_10_indexes)
        #return recommended_movies

        #pseudo code
        """      
                if iset file.cosine_simlarity
                    mat = load(cosine_simlarity)
                else
                    computeSimilarityMatrix()
                    mat = load(cosine_similarity)

            # creating a Series for the movie titles so they are associated to an ordered numerical
            # list I will use later to match the indexes
            indices = pd.Series(df.index)
            indices[:5]
                similarities = mat[self.id]
                orderedIDs = similarties.order()
                queryset = []
                foreach id in orderedIds
                    movie = Movie.objects.get(id= id)
                    queryset.add(movie)

                return queryset """
    
class Member(User):
    name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to='usrImages', null=True)
    likes = models.ForeignKey(Movie, related_name = "liked", on_delete=models.CASCADE, blank = True, null=True)#user likes

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE, blank = True, null=True) #reviews for a given movie
    author = models.ForeignKey(Member, related_name='author', on_delete=models.CASCADE, blank = True, null=True)
    text = models.TextField()
    created_date = models.DateField(default = datetime.date.today)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('created_date',)

#computes a similarity matrix for all movies
#returns cosine similarity matrix
#save similarity matrix to storage as binary file
#accessed from movie manager 
def computeSimilarityMatrix():
    data = list(Movie.objects.all().values()) #want dictionary of all movies in db
    df = pd.DataFrame(data, columns=['Title', 'Genre', 'Director', 'Actors', 'Plot'])

    # discarding the commas between the actors' full names and getting only the first three names
    df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])

    # putting the genres in a list of words
    df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))

    df['Director'] = df['Director'].map(lambda x: x.split(' '))

    # merging together first and last name for each actor and director, so it's considered as one word 
    # and there is no mix up between people sharing a first name
    for index, row in df.iterrows():
        row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]
        row['Director'] = ''.join(row['Director']).lower()
        row['Title'] = ''.join(row['Title']).lower()

    # initializing the new column
    df['Key_words'] = ""

    for index, row in df.iterrows():
        plot = row['Plot']

        # instantiating Rake, by default is uses english stopwords from NLTK
        # and discard all puntuation characters
        r = Rake()

        # extracting the words by passing the text
        r.extract_keywords_from_text(plot)

        # getting the dictionary whith key words and their scores
        key_words_dict_scores = r.get_word_degrees()
        
        # assigning the key words to the new column
        row['Key_words'] = list(key_words_dict_scores.keys())

    # dropping the Plot column as it turns into Key_words
    df.drop(columns = ['Plot'], inplace = True)

    df['bag_of_words'] = ''
    columns = df.columns
    for index, row in df.iterrows():
        words = ''
        for col in columns:
            if col != 'Director' or col != 'Title':
                words = words + ' '.join(row[col])+ ' '
            else:
                words = words + row[col]+ ' '
        row['bag_of_words'] = words
        
    df.drop(columns = [col for col in df.columns if col!= 'bag_of_words'], inplace = True)

    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])
    # generating the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    #save numpy array as .npy binary file for permanent storage
    np.save('cosine_sim.npy', cosine_sim)
    return cosine_sim