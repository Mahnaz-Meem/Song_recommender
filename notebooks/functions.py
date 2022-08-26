
def inputSong():
    """ Prompt the user for a song and an artist"""
    
    user_song = ''
    artist_song = ''
    
    while True:
        user_song = input('Please enter the song: ')
        user_song = user_song.replace("'",'').title()
        
        user_artist = input('Please enter the artist: ')
        user_artist = user_artist.replace("'",'').title()
        
        print()
        print('Your song is: %s' %(user_song))
        print('The artist of the song is: %s' %(user_artist))
        
        command = input('\nIf the song and artist ARE correct, please press ENTER to continue. \n\
If they are NOT correct , press ANY KEY to enter them again.')
        
        if len(command) == 0:
            break
        else:
            continue
            
    return user_song, user_artist

def querySong(song = user_song, artist = user_artist):
    """ search the ids and audio features of a song"""
    
    print('Loading...')

    user_song_id = {'song': [], 'artist': [], 'album': [], 'href':[],'id':[],'uri':[]}
    #song_validation = pd.DataFrame()

    result = sp.search(q=r"track:{} artist:{}".format(song,artist), limit=5)


    if result['tracks']['total']>0:        
        tracks = result['tracks']['total']

        if tracks > 5:
            tracks = 5

        
        # Querying ids
        for x in range(tracks):
            user_song_id['href'].append(result['tracks']['items'][x]['href'])
            user_song_id['id'].append(result['tracks']['items'][x]['id'])
            user_song_id['uri'].append(result['tracks']['items'][x]['uri'])
            user_song_id['album'].append(result['tracks']['items'][x]['album']['name'])
            user_song_id['artist'].append(result['tracks']['items'][x]['artists'][0]['name'])
            user_song_id['song'].append(result['tracks']['items'][x]['name'])
            
            
        song_validation = pd.DataFrame(user_song_id)
            
        print('Loading...Done.')
        
        # Song Validation
        
        while True:
            display(song_validation) #[['song','artist','album']])
        
            idx = input('Please confirm the version of your song by choosing (0-4):')
            
            try:
                idx = int(idx)
            except:
                print('Please use numeric digits.')
                continue
            
            if idx < 0 or idx > 4:
                print('Please enter an integer number in [0,4].')
                continue
            break
        
        # display(song_validation.iloc[idx])
        
        user_song_id = pd.DataFrame(song_validation.iloc[idx]).T.reset_index(drop=True) 
        # display(user_song_id)
        
        # Quering audio features
        
        #Get Audio Features
        audio_feat = sp.audio_features(user_song_id['uri'])[0]
        print('processing...Done.')
        
        #Define the empty dictionary
        audio_dict = { key : [] for key in list(audio_feat.keys()) }
        
        # Create the dictionary for the dataframe
        audio_dict = { key : audio_dict[key] + [audio_feat[key]] for key in list(audio_dict.keys())}
        # pprint.pprint(audio_dict)

        
    else:
        print('The song is not found. Please try again.')
    

    
    # Process output 
    # That output processing is returning error when no song is found.
    #user_song_id = pd.DataFrame(user_song_id)    
    
    user_song_audio = pd.DataFrame(audio_dict)
    user_song_features = pd.concat([user_song_id,user_song_audio], axis=1)
    
    
    return user_song_features

def predictCluster(user_df):
    """It predicts the cluster for the user song"""
    
    # Load the scaler
    with open('scaler.pickle', "rb") as file:
        scaler = pickle.load(file)
        
    # Load the model
    with open('kmeans_11.pickle', "rb") as file:
        best_clustering = pickle.load(file)
        
    
    # Scale audio features
    X = user_df.loc[:,'danceability':'time_signature'].drop(['mode', 'type', 'uri', 'track_href', 'analysis_url', 'instrumentalness', 'time_signature', 'duration_ms','id'], axis = 1)
    display(X)
    X_scaled = scaler.transform(X)
    # Save X_scaled as dataframe
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    display(X_scaled)
    
    # Predict cluster
    cluster = best_clustering.predict(X_scaled)
    
    
    # Process output
    user_df['cluster'] = cluster
    
    return user_df

def songRecommender(user_df):
    """ Recommends a song based on the input song"""
    
    # Load the songs' dataframe
    full = pd.read_csv('full_new.csv')
    
    # User song's cluster
    user_cluster = user_df.cluster[0]
    print('user cluster is: %s' %(user_cluster))
    
    # Check if it is in Hot data base
    if full.song[full.hot == 'Yes'].isin(user_df.song).sum() > 0:
        recommendation = full[(full.hot == 'Yes') & (full.Kmeans_11 == user_cluster)].sample()
    else:
        recommendation = full[(full.hot == 'No') & (full.Kmeans_11 == user_cluster)].sample()
        
    # Print the result
    print('The recommended song is:')
    print(recommendation.iloc[0,2]) #song)
    print(recommendation.iloc[0,3]) #singer)
    print(recommendation.iloc[0,12]) #full.loc[0,"url"]
    
    return recommendation #[['song','singer','url']]

def recommend():
    """ Ask the user to input a song and then recommends a similar one"""
    
    recommended_songs = pd.DataFrame()
    
    next_recommend = True
    
    while next_recommend:
        # Prompt user input
        user_song, user_artist = inputSong()

        #Initialize SpotiPy with user credentias
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                               client_secret= client_secret))


        # Get user's song's features
        try:
            user_song_features = querySong(user_song, user_artist)
        except:
            print('The song is not found. Please try again.')
            continue


        # Predict user's song's cluster
        user_song_features = predictCluster(user_song_features)

        # Get a recommended song
        recommendation = songRecommender(user_song_features)
        
        display(recommendation[['song','artist','uri']])
        
        # Process output
        recommended_songs = pd.concat([recommended_songs,recommendation], axis=0)
        
        # Ask for another recommendation:
        while True:
            another = input('Want another recommendation? (Y - Yes, N - No)')
            
            if another.lower() in ['y', 'yes']:
                break
            elif another.lower() in ['n', 'no']:
                next_recommend = False
                break
            else:
                continue
    
    return recommended_songs

def recommend():
    """ Ask the user to input a song and then recommends a similar one"""
    
    recommended_songs = pd.DataFrame()
    
    next_recommend = True
    
    while next_recommend:
        # Prompt user input
        user_song, user_artist = inputSong()

        #Initialize SpotiPy with user credentias
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                               client_secret= client_secret))


        # Get user's song's features
        try:
            user_song_features = querySong(user_song, user_artist)
        except:
            print('The song is not found. Please try again.')
            continue


        # Predict user's song's cluster
        user_song_features = predictCluster(user_song_features)

        # Get a recommended song
        recommendation = songRecommender(user_song_features)
        
        display(recommendation[['song','artist','uri']])
        
        # Process output
        recommended_songs = pd.concat([recommended_songs,recommendation], axis=0)
        
        # Ask for another recommendation:
        while True:
            another = input('Want another recommendation? (Y - Yes, N - No)')
            
            if another.lower() in ['y', 'yes']:
                break
            elif another.lower() in ['n', 'no']:
                next_recommend = False
                break
            else:
                continue
    
    return recommended_songs

def recommend():
    """ Ask the user to input a song and then recommends a similar one"""
    
    recommended_songs = pd.DataFrame()
    
    next_recommend = True
    
    while next_recommend:
        # Prompt user input
        user_song, user_artist = inputSong()

        #Initialize SpotiPy with user credentias
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                               client_secret= client_secret))


        # Get user's song's features
        try:
            user_song_features = querySong(user_song, user_artist)
        except:
            print('The song is not found. Please try again.')
            continue


        # Predict user's song's cluster
        user_song_features = predictCluster(user_song_features)

        # Get a recommended song
        recommendation = songRecommender(user_song_features)
        
        display(recommendation[['song','artist','uri']])
        
        # Process output
        recommended_songs = pd.concat([recommended_songs,recommendation], axis=0)
        
        # Ask for another recommendation:
        while True:
            another = input('Want another recommendation? (Y - Yes, N - No)')
            
            if another.lower() in ['y', 'yes']:
                break
            elif another.lower() in ['n', 'no']:
                next_recommend = False
                break
            else:
                continue
    
    return recommended_songs

def inputSong():
    """ Prompt the user for a song and an artist"""
    
    user_song = ''
    artist_song = ''
    
    while True:
        user_song = input('Please enter the song: ')
        user_song = user_song.replace("'",'').title()
        
        user_artist = input('Please enter the artist: ')
        user_artist = user_artist.replace("'",'').title()
        
        print()
        print('Your song is: %s' %(user_song))
        print('The artist of the song is: %s' %(user_artist))
        
        command = input('\nIf the song and artist ARE correct, please press ENTER to continue. \n\
If they are NOT correct , press ANY KEY to enter them again.')
        
        if len(command) == 0:
            break
        else:
            continue
            
    return user_song, user_artist

def querySong(song = user_song, artist = user_artist):
    """ search the ids and audio features of a song"""
    
    print('Loading...')

    user_song_id = {'song': [], 'artist': [], 'album': [], 'href':[],'id':[],'uri':[]}
    #song_validation = pd.DataFrame()

    result = sp.search(q=r"track:{} artist:{}".format(song,artist), limit=5)


    if result['tracks']['total']>0:        
        tracks = result['tracks']['total']

        if tracks > 5:
            tracks = 5

        
        # Querying ids
        for x in range(tracks):
            user_song_id['href'].append(result['tracks']['items'][x]['href'])
            user_song_id['id'].append(result['tracks']['items'][x]['id'])
            user_song_id['uri'].append(result['tracks']['items'][x]['uri'])
            user_song_id['album'].append(result['tracks']['items'][x]['album']['name'])
            user_song_id['artist'].append(result['tracks']['items'][x]['artists'][0]['name'])
            user_song_id['song'].append(result['tracks']['items'][x]['name'])
            
            
        song_validation = pd.DataFrame(user_song_id)
            
        print('Loading...Done.')
        
        # Song Validation
        
        while True:
            display(song_validation) #[['song','artist','album']])
        
            idx = input('Please confirm the version of your song by choosing (0-4):')
            
            try:
                idx = int(idx)
            except:
                print('Please use numeric digits.')
                continue
            
            if idx < 0 or idx > 4:
                print('Please enter an integer number in [0,4].')
                continue
            break
        
        # display(song_validation.iloc[idx])
        
        user_song_id = pd.DataFrame(song_validation.iloc[idx]).T.reset_index(drop=True) 
        # display(user_song_id)
        
        # Quering audio features
        
        #Get Audio Features
        audio_feat = sp.audio_features(user_song_id['uri'])[0]
        print('processing...Done.')
        
        #Define the empty dictionary
        audio_dict = { key : [] for key in list(audio_feat.keys()) }
        
        # Create the dictionary for the dataframe
        audio_dict = { key : audio_dict[key] + [audio_feat[key]] for key in list(audio_dict.keys())}
        # pprint.pprint(audio_dict)

        
    else:
        print('The song is not found. Please try again.')
    

    
    # Process output 
    # That output processing is returning error when no song is found.
    #user_song_id = pd.DataFrame(user_song_id)    
    
    user_song_audio = pd.DataFrame(audio_dict)
    user_song_features = pd.concat([user_song_id,user_song_audio], axis=1)
    
    
    return user_song_features

def predictCluster(user_df):
    """It predicts the cluster for the user song"""
    
    # Load the scaler
    with open('scaler.pickle', "rb") as file:
        scaler = pickle.load(file)
        
    # Load the model
    with open('kmeans_11.pickle', "rb") as file:
        best_clustering = pickle.load(file)
        
    
    # Scale audio features
    X = user_df.loc[:,'danceability':'time_signature'].drop(['mode', 'type', 'uri', 'track_href', 'analysis_url', 'instrumentalness', 'time_signature', 'duration_ms','id'], axis = 1)
    display(X)
    X_scaled = scaler.transform(X)
    # Save X_scaled as dataframe
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    display(X_scaled)
    
    # Predict cluster
    cluster = best_clustering.predict(X_scaled)
    
    
    # Process output
    user_df['cluster'] = cluster
    
    return user_df

def songRecommender(user_df):
    """ Recommends a song based on the input song"""
    
    # Load the songs' dataframe
    full = pd.read_csv('full_new.csv')
    
    # User song's cluster
    user_cluster = user_df.cluster[0]
    print('user cluster is: %s' %(user_cluster))
    
    # Check if it is in Hot data base
    if full.song[full.hot == 'Yes'].isin(user_df.song).sum() > 0:
        recommendation = full[(full.hot == 'Yes') & (full.Kmeans_11 == user_cluster)].sample()
    else:
        recommendation = full[(full.hot == 'No') & (full.Kmeans_11 == user_cluster)].sample()
        
    # Print the result
    print('The recommended song is:')
    print(recommendation.iloc[0,2]) #song)
    print(recommendation.iloc[0,3]) #singer)
    print(recommendation.iloc[0,12]) #full.loc[0,"url"]
    
    return recommendation #[['song','singer','url']]

def recommend():
    """ Ask the user to input a song and then recommends a similar one"""
    
    recommended_songs = pd.DataFrame()
    
    next_recommend = True
    
    while next_recommend:
        # Prompt user input
        user_song, user_artist = inputSong()

        #Initialize SpotiPy with user credentias
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                               client_secret= client_secret))


        # Get user's song's features
        try:
            user_song_features = querySong(user_song, user_artist)
        except:
            print('The song is not found. Please try again.')
            continue


        # Predict user's song's cluster
        user_song_features = predictCluster(user_song_features)

        # Get a recommended song
        recommendation = songRecommender(user_song_features)
        
        display(recommendation[['song','artist','uri']])
        
        # Process output
        recommended_songs = pd.concat([recommended_songs,recommendation], axis=0)
        
        # Ask for another recommendation:
        while True:
            another = input('Want another recommendation? (Y - Yes, N - No)')
            
            if another.lower() in ['y', 'yes']:
                break
            elif another.lower() in ['n', 'no']:
                next_recommend = False
                break
            else:
                continue
    
    return recommended_songs
