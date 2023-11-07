import pandas as pd
import random
df=pd.read_csv("F:/spotify.csv",encoding='latin1')

df1=df[['track_name','released_year']]
# print(df1.head())
a=['SongName','ReleaseYear']
df1.columns=a
b=df['artist(s)_name']
df['artist(s)_name']= b.str.split(',').str[0].str.strip()
df['artist(s)_name']=pd.DataFrame(df['artist(s)_name'])
df1=pd.DataFrame(df1)
df1['Artist']=df['artist(s)_name']
pd.set_option('display.max_columns', None)
rating=[3.4,3.5,3.6,3.7,3.8,3.9,4.0,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8]
Rating = [random.choice(rating) for _ in range(953)]
 
df1['Rating']=Rating
music_genres = ['Pop', 'Rock', 'Hip Hop', 'Rap', 'Country', 'Jazz', 'Blues', 'Electronic', 'Classical', 'Folk', 'Funk', 'Dance']
g=[random.choice(music_genres)for _ in range(953)]
df1['Genre']=g
# print(df1.head())

# print(df1)
# df1.concat([df['artist(s)_name']])
# print(df2.head())