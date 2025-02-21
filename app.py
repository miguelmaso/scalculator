from flask import Flask
from config import Config
from routes.csection import csection
from routes.auth import auth
# from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)

# Initialize session
# Session(app)

# Register Blueprints
app.register_blueprint(csection)
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)



