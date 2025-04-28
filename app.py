# from flask import Flask,render_template,request
# import pickle
# import numpy as np
#
# popular_books = pickle.load(open('popular_books.pkl','rb'))
# data_table = pickle.load(open('data_table.pkl','rb'))
# books = pickle.load(open('books.pkl','rb'))
# similarity_score = pickle.load(open('similarity_score.pkl','rb'))
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return render_template('index.html',
#                            book_name = list(popular_books['Book-Title'].values),
#                            author=list(popular_books['Book-Author'].values),
#                            image=list(popular_books['Image-URL-M'].values),
#                            votes=list(popular_books['rating-Count'].values),
#                            rating=list(popular_books['avg-rating'].round(1).values)
#                            )
#
# @app.route('/recommend')
# def recommend_ui():
#     return render_template('recommend.html')
#
# @app.route('/recommend_books', methods=['post'])
# def recommend():
#     user_input = request.form.get('user_input')
#     index = np.where(data_table.index == user_input)[0][0]
#     similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]
#
#     data = []
#     for i in similar_items:
#         item = []
#         temp_df = books[books['Book-Title'] == data_table.index[i[0]]]
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
#         item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
#
#         data.append(item)
#
#     print(data)
#
#     # Pass user_input to the template
#     return render_template('recommend.html', data=data, user_input=user_input)
#
# @app.route('/contact')
# def contact():
#     students = [
#         {
#             'name': 'Aditya Thorat',
#             'email': 'adityathorat@gmail.com',
#             'mobile': '9513415225',
#             'college': 'Govt. Collage of Engineering, Amravati'
#         },
#         {
#             'name': 'Tejas Gaurkhede',
#             'email': 'tejasgaurkhede@gmail.com',
#             'mobile': '9623235232',
#             'college': 'Govt. Collage of Engineering, Amravati'
#         }
#     ]
#     return render_template('contact.html', students=students)
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import numpy as np

popular_books = pickle.load(open('popular_books.pkl', 'rb'))
data_table = pickle.load(open('data_table.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for flashing messages

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_books['Book-Title'].values),
                           author=list(popular_books['Book-Author'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           votes=list(popular_books['rating-Count'].values),
                           rating=list(popular_books['avg-rating'].round(1).values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if not user_input:
        flash('Please enter a book name!')
        return redirect(url_for('recommend_ui'))

    # Convert all titles to lowercase for checking
    all_titles = data_table.index.str.lower()

    if user_input.lower() not in all_titles.values:
        flash('Book not found or spelling mistake! Please try again.')
        return redirect(url_for('recommend_ui'))

    # If book is found
    index = np.where(data_table.index.str.lower() == user_input.lower())[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == data_table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html', data=data, user_input=user_input)

@app.route('/contact')
def contact():
    students = [
        {
            'name': 'Aditya Thorat',
            'email': 'adityathorat@gmail.com',
            'mobile': '9513415225',
            'college': 'Govt. College of Engineering, Amravati'
        },
        {
            'name': 'Tejas Gaurkhede',
            'email': 'tejasgaurkhede@gmail.com',
            'mobile': '9623235232',
            'college': 'Govt. College of Engineering, Amravati'
        }
    ]
    return render_template('contact.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
