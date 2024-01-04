from flask import Flask, render_template, request
import joblib
import pandas

app = Flask(__name__)

movies = joblib.load(open('movie_list.pkl', 'rb'))
similarity = joblib.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

@app.route('/')
def index():
    return render_template('index.html', movie_list=movie_list)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input from the form
    user_input = request.form.get('selected_movie')
    movie_index = movies[movies['title'] == user_input].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    movie_names = []
    for i in movie_list:
        movie_names.append(movies.iloc[i[0]].title)
    recommendations = movie_names

    return render_template('recommendations.html', selected_movie=user_input, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
