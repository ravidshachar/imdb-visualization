import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from imdb_visualization.neo4j_wrapper import get_nodes_by_years


def get_genre_against(df,name_against):
	new_genre_df = []
	counter = 0
	for list_of_movie_genres in genre_vs_metascore_df["genre"]:
		for each_genre in list_of_movie_genres:
			new_genre_df.append([each_genre.strip(),genre_vs_metascore_df[name_against].iloc[counter]])
		counter += 1
	new_genre_df = pd.DataFrame(new_genre_df,columns=["genre",name_against])
	return new_genre_df

st.title('MovieMiner')

# Add a slider to the sidebar:
year_slider = st.slider(
    'Select a range of values',
    2000, 2020, (2007, 2008)
)
category = st.sidebar.radio('Which stats you want to see', ("Length","Metascore","Certificate","Votes","All"))

st.title("Between years: " + str(year_slider[0]) + " and " + str(year_slider[1]))

years_df = get_nodes_by_years(year_slider[0],year_slider[1])
st.write(years_df)


if(category in ["Rating","Length","All"]):
	st.title('rating against length')
	rating_vs_length_df = years_df[['rating','length']]
	fig1 = plt.figure()
	ax = sns.scatterplot(data=rating_vs_length_df , x = 'length' , y = 'rating')
	st.pyplot(fig1)

if(category in ["Metascore","Rating","All"]):
	st.title('rating against metascore')
	rating_vs_metascore_df = years_df[['rating','metascore']]
	fig2 = plt.figure()
	ax = sns.scatterplot(data=rating_vs_metascore_df , x = 'metascore' , y = 'rating')
	st.pyplot(fig2)


if(category in ["Length","All"]):
	st.title('Length histogram')
	lengths_df = years_df[['length']]
	fig3 = plt.figure()
	ax = sns.histplot(data=lengths_df , x = 'length')
	st.pyplot(fig3)



if(category in ["Certificate","Metascore","All"]):
	st.title('Certificate against metascore')
	certificate_vs_metascore_df = years_df[['certificate','metascore']]
	fig4 = plt.figure()
	ax = sns.boxplot(data=certificate_vs_metascore_df , x = 'certificate' , y = 'metascore')
	st.pyplot(fig4)

if(category in ["Certificate","Votes","All"]):
	st.title('Certificate against votes')
	certificate_vs_votes_df = years_df[['certificate','votes']]
	fig5 = plt.figure()
	ax = sns.boxplot(data=certificate_vs_votes_df , x = 'certificate' , y = 'votes')
	st.pyplot(fig5)

if(category in ["Genre","Metascore"]):
	st.title('Certificate against votes')
	
	genre_vs_metascore_df = years_df[['genre','metascore']]
	new_genre_df = get_genre_against(genre_vs_metascore_df,"metascore")
	fig6 = plt.figure(figsize=(17, 6))
	ax = sns.boxplot(data=new_genre_df , x = 'genre' , y = 'metascore')
	st.pyplot(fig6)