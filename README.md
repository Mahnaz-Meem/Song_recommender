# Spotify Song Recommender
- 📊 Bootcamp Project
- 🗓 Date: 26 August 2022
- 👩🏽‍💻 Created by: Mahnaz Sarker Meem, Mary Angélica Ramírez Pinzón, Yadong Du👋🏼
- 👉🏼  [Check it out here](https://www.canva.com/design/DAFKWV42R_k/SWV8DI44veDQ5Zw4cdnxQg/edit?utm_content=DAFKWV42R_k&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) 👈🏼

## Table of Contents
- [About](#about)
- [Technologies used](#technologies-used)
- [Data](#dataset)
- [Visualization](#visualization)

## About
A Canva presentation displaying the project presentation and a notebook for displaying the demo has been created. The hot songs data was collected from [here](https://www.billboard.com/charts/hot-100/) and the not hot songs data has been obtained from [here](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs).

Here, based on the audio-features collected from Spotify,the model recommends similar song from the similar type of songs. Based on the user's choice whether it is from Hot songs or Not Hot songs, the model recommends another song from corresponding datasets.

In the python codes, three different clustering models: K-Means, Gaussian and Agglomerative, have been created to find the optimum clustering model and K-Means(11) have been chosen. Based on this clustering, the model identifies the song cluster and recommends another hot song, if the user is looking for a hot song or recommends a not hot song, if the user is open to other songs.

In future, with machine learning models this could be developed and more user specific recommendation could be suggested. 

## Technologies used
* Python (pandas, numpy, matplotlib, seaborn, plotly, sklearn, statistic, pickle, spotipy, json, sys)
* Canva

## Data
- https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs

## Visualization

Please click on the link to open and visualize the Canva presentation.

[Link](https://www.canva.com/design/DAFKWV42R_k/SWV8DI44veDQ5Zw4cdnxQg/edit?utm_content=DAFKWV42R_k&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

However, to visualize how the model works, and to get a recommendation of a song of your choice, you may need to run the codes :wink:
