from flask import Flask
from routes.routes import register_routes

app = Flask(__name__)

app.config['DEBUG'] = True

register_routes(app)

if __name__ == "__main__":
    app.run()