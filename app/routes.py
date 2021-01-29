from app import app

@app.route('/')
@app.route('/index')
def index():
    return "<h1>you made it to <h3>bloggler!</h1></h3>"
