from flask import Flask
from config import Config
from routes.main import main_routes
from routes.auth import auth
# from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)

# Initialize session
# Session(app)

# Register Blueprints
app.register_blueprint(main_routes)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)




# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':

#     app.run()
