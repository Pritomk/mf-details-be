from flask import Flask
from routes.routes import register_routes
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['DEBUG'] = True

register_routes(app)

if __name__ == "__main__":
    app.run()