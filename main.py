import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import ast
def recommend(movie):
    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv') 
    movies = movies.merge(credits,on='title')
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    def convert(text):
        L = []
        for i in ast.literal_eval(text):
            L.append(i['name']) 
        return L 

    movies.dropna(inplace=True)
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    def convert3(text):
        L = []
        counter = 0
        for i in ast.literal_eval(text):
            if counter < 3:
                L.append(i['name'])
            counter+=1
        return L 

    movies['cast'] = movies['cast'].apply(convert)

    movies['cast'] = movies['cast'].apply(lambda x:x[0:3])

    def fetch_director(text):
        L = []
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
        return L 

    movies['crew'] = movies['crew'].apply(fetch_director)

    #movies['overview'] = movies['overview'].apply(lambda x:x.split())


    def collapse(L):
        L1 = []
        for i in L:
            L1.append(i.replace(" ",""))
        return L1

    movies['cast'] = movies['cast'].apply(collapse)
    movies['crew'] = movies['crew'].apply(collapse)
    movies['genres'] = movies['genres'].apply(collapse)
    movies['keywords'] = movies['keywords'].apply(collapse)

    movies['overview'] = movies['overview'].apply(lambda x:x.split()) # it convert all in lower case
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew'] # it add all the column
    new = movies.drop(columns=['overview','genres','keywords','cast','crew'])

    new['tags'] = new['tags'].apply(lambda x: " ".join(x))
    # new.head()

    # new['tags'] 

    import nltk
    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()
    def steam(text):
        y = []
        for i in text.split():
            ps.stem(i)
            y.append(ps.stem(i))
        return " ".join(y)
    new['tags'] =  new['tags'].apply(steam)

    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=5000,stop_words='english')
        

    vector = cv.fit_transform(new['tags']).toarray()

    # vector
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(vector)
    sorted(list(enumerate(similarity[0])),reverse=True,key = lambda x: x[1])[1:6]
    new[new['title'] == 'The Lego Movie'].index[0]

    # movie = 'Avatar'
    # def recommend(movie):
    movie_index = new[new['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key = lambda x: x[1])[1:6]
    recomanded_movie = []
    for i in movie_list:
        recomanded_movie.append(new.iloc[i[0]].title)
        # print(new.iloc[i[0]].title)
        # return (new.iloc[i[0]].title)
    return(recomanded_movie)
    
# recommend('Avatar')


