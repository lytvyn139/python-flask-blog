from flask import Flask
app = Flask (__name__) #__name__ is name of the module


#two routes leads to home
@app.route('/') # <-- flask decorators
@app.route('/home')
def home():
  return "<h1>Welcome home %USERNAME%</h1>"

@app.route('/about')
def about():
  return "<h1>About this page</h1>"

# hot reload/debugger is active
if __name__ == '__main__':
  app.run(debug=True)
