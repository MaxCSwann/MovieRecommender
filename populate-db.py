#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from recommender.models import Movie

pd.set_option('display.max_columns', 100)
df = pd.read_csv('https://query.data.world/s/uikepcpffyo2nhig52xxeevdialfl7')
df.head()


# In[2]:


df = df[['Title','Genre','Director','Actors','Plot', 'tomatoURL', 'Poster']]
df.head()


# In[3]:


db_as_dict = df.to_dict('index')

print(db_as_dict)

# In[5]:


for index in db_as_dict:
    mov = Movie(**db_as_dict[index])
    mov.save()



