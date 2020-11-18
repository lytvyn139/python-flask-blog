from flask import Flask, render_template

app = Flask (__name__) #__name__ is name of the module

posts = [
  {
    'author': 'Iurii Lytvyn',
    'title': 'Blog Post 1',
    'content': 'You day of the year',
    'date_posted': 'April 1, 2020'
  },
  {
    'author': 'Johm Smith',
    'title': 'Blog Post 2',
    'content': 'I don\'t know what I\'m doing',
    'date_posted': 'May 2, 2019'
  },
]

#two routes leads to home
@app.route('/') # <-- flask decorators
@app.route('/home')
def home():
  return render_template('home.html', posts=posts) #passing posts dict 

@app.route('/about')
def about():
  return render_template('about.html', title='About')

# hot reload/debugger is active
if __name__ == '__main__':
  app.run(debug=True)
