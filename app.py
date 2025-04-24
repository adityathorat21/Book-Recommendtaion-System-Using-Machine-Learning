from flask import Flask,render_template,request
import pickle
import numpy as np

popular_books = pickle.load(open('popular_books.pkl','rb'))
data_table = pickle.load(open('data_table.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_books['Book-Title'].values),
                           author=list(popular_books['Book-Author'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           votes=list(popular_books['rating-Count'].values),
                           rating=list(popular_books['avg-rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(data_table.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == data_table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

@app.route('/contact')
def contact():
    students = [
        {
            'name': 'Aditya Thorat',
            'email': 'adityathorat206@gmail.com',
            'branch': 'Computer Science and Engineering',
            'college': 'Govt. Collage of Engineering, Amravati'
        },
        {
            'name': 'Tejas Gaurkhade',
            'email': 'tejasgaurkhede3000@gmail.com',
            'branch': 'Computer Science and Engineering',
            'college': 'Govt. Collage of Engineering, Amravati'
        }
    ]
    return render_template('contact.html', students=students)



if __name__ == '__main__':
    app.run(debug=True)