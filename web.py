wimport streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import networkx as nx
from imdb_visualization.neo4j_wrapper import get_nodes_by_years,get_top_actors,get_top_directors
from imdb_visualization import nx_wrapper

CATEGORIES = ("Actor","Director","Genre","Votes","Metascore","Certificate","Length","Couples","All")
TOTAL_ACTORS_IN_DB = 15000
TOTAL_DIRECTORS_IN_DB = 3000

def get_genre_against(df,name_against):
	"""
	genre organized in lists
	this function separate them
	"""
	new_genre_df = []
	counter = 0
	for list_of_movie_genres in genre_vs_metascore_df["genre"]:
		for each_genre in list_of_movie_genres:
			new_genre_df.append([each_genre.strip(),genre_vs_metascore_df[name_against].iloc[counter]])
		counter += 1
	new_genre_df = pd.DataFrame(new_genre_df,columns=["genre",name_against])
	return new_genre_df

st.title('MovieMiner')
category = st.sidebar.radio('Which stats you want to see', CATEGORIES , index=2)

if(category != "Couples"):
	# Add a slider to the sidebar:
	year_slider = st.slider(
		'Select a range of values',
		2000, 2020, (2007, 2008)
	)
	st.title("Between years: " + str(year_slider[0]) + " and " + str(year_slider[1]))
	years_df = get_nodes_by_years(year_slider[0],year_slider[1])


if(category in ["Couples"]):
	with st.spinner('Loading...'):
		couples_df = nx_wrapper.get_actor_couples()
		st.title("Top 10 Couples between 2000 and 2020")
		st.write("#acted_together shows the times they acted togeter")
		st.write("#acted_connection present the times they acted with somebody else(second agree)")
		st.write("Here's top 10 couples.")
		st.write(couples_df)


if(category in ["Actor","Rating","All"]):
	
	st.title('Movies Actor acted in against Rating')
	actors = get_top_actors(year_slider[0],year_slider[1],top_num=TOTAL_ACTORS_IN_DB)
	fig1 = plt.figure()
	ax = sns.boxplot(data=actors , x = 'movies_num' , y = 'avg_movie_rating')
	st.pyplot(fig1)

if(category in ["Actor","Metascore","All"]):
	
	st.title('Movies Actor acted in against Metascore')
	actors = get_top_actors(year_slider[0],year_slider[1],top_num=TOTAL_ACTORS_IN_DB)
	fig2 = plt.figure()
	ax = sns.boxplot(data=actors , x = 'movies_num' , y = 'avg_metascore')
	st.pyplot(fig2)

if(category in ["Director","Rating","All"]):
	
	st.title('Movies Director Directed against Rating')
	directors = get_top_directors(year_slider[0],year_slider[1],top_num=TOTAL_DIRECTORS_IN_DB)
	fig3 = plt.figure()
	ax = sns.boxplot(data=directors , x = 'movies_num' , y = 'avg_movie_rating')
	st.pyplot(fig3)

if(category in ["Director","Metascore","All"]):
	
	st.title('Movies Director Directed against Metascore')
	directors = get_top_directors(year_slider[0],year_slider[1],top_num=TOTAL_DIRECTORS_IN_DB)
	fig4 = plt.figure()
	ax = sns.boxplot(data=directors , x = 'movies_num' , y = 'avg_metascore')
	st.pyplot(fig4)

if(category in ["Rating","Length","All"]):
	st.title('rating against length')
	rating_vs_length_df = years_df[['rating','length']]
	fig5 = plt.figure()
	ax = sns.scatterplot(data=rating_vs_length_df , x = 'length' , y = 'rating')
	st.pyplot(fig5)

if(category in ["Metascore","Rating","All"]):
	st.title('rating against metascore')
	rating_vs_metascore_df = years_df[['rating','metascore']]
	fig6 = plt.figure()
	ax = sns.scatterplot(data=rating_vs_metascore_df , x = 'metascore' , y = 'rating')
	st.pyplot(fig6)


if(category in ["Length","All"]):
	st.title('Length histogram')
	lengths_df = years_df[['length']]
	fig7 = plt.figure()
	ax = sns.histplot(data=lengths_df , x = 'length')
	st.pyplot(fig7)



if(category in ["Certificate","Metascore","All"]):
	st.title('Certificate against metascore')
	certificate_vs_metascore_df = years_df[['certificate','metascore']]
	fig8 = plt.figure()
	ax = sns.boxplot(data=certificate_vs_metascore_df , x = 'certificate' , y = 'metascore')
	st.pyplot(fig8)

if(category in ["Certificate","Votes","All"]):
	st.title('Certificate against votes')
	certificate_vs_votes_df = years_df[['certificate','votes']]
	fig9 = plt.figure()
	ax = sns.boxplot(data=certificate_vs_votes_df , x = 'certificate' , y = 'votes')
	st.pyplot(fig9)

if(category in ["Genre","Metascore"]):
	st.title('Genre against Metascore')
	genre_vs_metascore_df = years_df[['genre','metascore']]
	
	new_genre_df = get_genre_against(genre_vs_metascore_df,"metascore")
	
	fig10 = plt.figure(figsize=(17, 6))
	ax = sns.boxplot(data=new_genre_df , x = 'genre' , y = 'metascore')
	st.pyplot(fig10)

if(category in ["Genre","Votes"]):
	st.title('Genre against Votes')
	genre_vs_metascore_df = years_df[['genre','votes']]
	
	new_genre_df = get_genre_against(genre_vs_metascore_df,"votes")
	
	fig11 = plt.figure(figsize=(17, 6))
	ax = sns.boxplot(data=new_genre_df , x = 'genre' , y = 'votes')
	st.pyplot(fig11)
