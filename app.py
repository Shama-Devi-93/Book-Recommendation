from flask import Flask, render_template, request
import pickle
import gzip

import numpy as np
app = Flask(__name__)
popular_df = pickle.load(open('popular.pkl', 'rb'))
result = pickle.load(open('result.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
# with gzip.open('books.pkl.gz', 'rb') as f:
#     # Read the compressed data
#     books = f.read()
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

@app.route('/')


def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['number_of_ratings'].values),
                           rating=list(popular_df['avg-rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html',)

@app.route('/recommend_books',methods=['post'])


def recommend():
    user_input = request.form.get('user_input')
    if user_input not in result.index:
        return render_template('Book_Not_Found.html')
    index = np.where(result.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == result.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    print(data)
    return render_template('recommend.html',data=data)

@app.route('/contact')
def contact_ui():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)

