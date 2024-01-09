import numpy as np
import pandas as pd
import datetime

#1 Read file
print ("0. Read files and clean data")
anime_data =pd.read_csv("Anime_Data.txt")
print(anime_data)

#2 Check info about the data
# print(anime_data.info())

#3 Convert @start and @finish into datetime type and recheck
anime_data['start'] =pd.to_datetime(anime_data['start'])
anime_data['finish'] = pd.to_datetime(anime_data['finish'])


#4 Clean data
#4.1 Null data
anime_data.dropna(inplace=True)


#4.2 Wrong data: episodes = 0
for x in anime_data.index:
    if anime_data.loc[x,"episodes"] == 0:
        anime_data.drop(x, inplace = True)


#4.4 Wrong data: duration_min = 0
anime_data = anime_data[anime_data['duration_min'] != 0]

print(anime_data.info())

#5 Display #anime for each year
print ("1. Exploratory Analysis")
anime_year = anime_data['start'].dt.year.unique()
anime_year.sort()
print ("+ Number of anime by year")
for year in anime_year:
  print(year, ": ", anime_data[anime_data.start.dt.year == year].shape[0])

#6 Add "Decade" into data and count #anime by decade
  
def name_decade(year):
  if year <= 1949:
    return '1940s'
  elif 1949 < year <= 1959:
    return '1950s'
  elif 1959 < year <= 1969:
    return '1960s'
  elif 1969 < year <= 1979:
    return '1970s'
  elif 1979 < year <= 1989:
    return '1980s'
  elif 1989 < year <= 1999:
    return '1990s'
  elif 1999 < year <= 2009:
    return '2000s'
  else:
    return '2010s'
anime_data = anime_data.assign(
    decade = anime_data.start.dt.year.apply(name_decade)
)
anime_decade = anime_data.decade.unique()
anime_decade.sort()
print("+ Number of anime by decade")
for each_decade in anime_decade:  
  print(each_decade, ": ", anime_data[anime_data.decade == each_decade].shape[0])

#7 Add "Season" into data and count #anime by season
  
def name_season(month):
  if month <=3:
    return "Winter-Spring"
  elif 3 < month <= 6:
    return "Sring"
  elif 6 < month <= 9:
    return "Summer"
  else:
    return "Fall"  
anime_data = anime_data.assign(season = anime_data.start.dt.month.apply(name_season))
anime_season = anime_data.season.unique()
anime_season_list = []


print ("+ Number of anime by season")
for each_season in anime_season:
  anime_season_data = anime_data[anime_data.season == each_season].shape[0]
  anime_season_list.append(anime_season_data)
table_anime_season = pd.DataFrame()
table_anime_season = table_anime_season.assign(
  season = anime_season,
  anime = anime_season_list)
print (table_anime_season)


#8 Summarize data on anime of TV type
print ("2. Explanatory Analysis")
TV_anime = anime_data[anime_data.type == "TV"]
print ("+ Total number of anime: ", TV_anime.shape[0])
print ("+ Anime with the most episodes: ", TV_anime.sort_values(by = 'episodes').iloc[-1].title)
print ("+ Total number of episodes: ", TV_anime.episodes.sum())
print ("+ Total duration in minutes and days respectively: ", round((TV_anime.duration_min.sum() / 60), 2), " and ", round(TV_anime.duration_min.sum() / 60 / 24,2))
print ("+ Average time for each episode: ", round(TV_anime.duration_min.sum()/TV_anime.shape[0],2))

print ("+ Average score by decade: ")
for decade in anime_decade:
  score_decade_data = TV_anime[TV_anime.decade == decade]
  if score_decade_data.empty == True:
    print("\t", decade, "Not available")
  else:
    print("\t",decade, round(score_decade_data.score.sum()/score_decade_data.shape[0],2))


anime_source = TV_anime.source.unique()
new_datas = pd.DataFrame(index = anime_source)
for each_season in anime_season:
  index_data = []
  data_season = TV_anime[TV_anime.season == each_season]
  for each_source in anime_source:
    data_by_source = data_season[data_season.source == each_source]
    datas = round(data_by_source.score.sum()/data_by_source.shape[0],2)
    index_data.append(datas)
  new_datas[each_season] = index_data
print ("+ Average score by season and source: ")
print (new_datas)


#9. Filter anime with type movie and decompose movie genre
movie = anime_data[anime_data.type == "Movie"].drop(columns = ['type' ,'episodes', 'duration_min', 'start', 'finish'])
movie = movie.assign(genre = movie.genre.str.split(', '))
movie = movie.explode('genre')

#10 Number of anime and score by genre
print ("+ Number of anime and average score by genre: ")
genre_table = pd.DataFrame()
genre_data_list = []
score_genre_list = []
for each_genre in movie.genre.unique():
    genre_data = movie[movie.genre == each_genre].shape[0]
    genre_data_list.append(genre_data)
    score_genre = round(movie[movie.genre == each_genre].score.sum()/movie[movie.genre == each_genre].shape[0],2)
    score_genre_list.append(score_genre)
genre_table = genre_table.assign(
  Genre = movie.genre.unique(),
  Number = genre_data_list,
  Score = score_genre_list
)
print (genre_table)

#11 Average score by genre and studio

studio_table = pd.DataFrame()
studio_genre_list = []
score_list = []
for each_studio in movie.studio.unique():
  studio_data = movie[movie.studio == each_studio]
  for each_genre in movie.genre.unique():
    studio_genre_list.append(each_studio + " | " + each_genre)
    score_list.append(round(studio_data[studio_data.genre == each_genre].score.sum()/studio_data[studio_data.genre == each_genre].shape[0],2))
studio_table = studio_table.assign(
  Studio_Genre = studio_genre_list,
  Score = score_list
)
studio_table = studio_table.dropna(axis=0)
print("+ Average score by genre and studio: ")
print(studio_table)