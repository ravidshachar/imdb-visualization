import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


st.title('MovieMiner')

# Add a slider to the sidebar:
year_slider = st.slider(
    'Select a range of values',
    2000, 2020, (2007, 2008)
)
st.title("Between years: " + str(year_slider[0]) + " and " + str(year_slider[1]))

st.title('Stat1')

#legendary_df = df[df['is_legendary'] == 1]
fig1 = plt.figure()
#ax = sns.countplot(data=legendary_df , x = 'type1',order=legendary_df['type1'].value_counts().index)
plt.xticks(rotation=45)
st.pyplot(fig1)


st.title('Stat2')

#legendary_df = df[df['is_legendary'] == 1]
fig1 = plt.figure()
#ax = sns.countplot(data=legendary_df , x = 'type1',order=legendary_df['type1'].value_counts().index)
plt.xticks(rotation=45)
st.pyplot(fig1)



st.title('Stat3')

#legendary_df = df[df['is_legendary'] == 1]
fig1 = plt.figure()
#ax = sns.countplot(data=legendary_df , x = 'type1',order=legendary_df['type1'].value_counts().index)
plt.xticks(rotation=45)
st.pyplot(fig1)




st.title('Stat4')

#legendary_df = df[df['is_legendary'] == 1]
fig1 = plt.figure()
#ax = sns.countplot(data=legendary_df , x = 'type1',order=legendary_df['type1'].value_counts().index)
plt.xticks(rotation=45)
st.pyplot(fig1)




st.title('Stat5')

#legendary_df = df[df['is_legendary'] == 1]
fig1 = plt.figure()
#ax = sns.countplot(data=legendary_df , x = 'type1',order=legendary_df['type1'].value_counts().index)
plt.xticks(rotation=45)
st.pyplot(fig1)