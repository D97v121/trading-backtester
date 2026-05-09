from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'

    from app.routes import register_routes
    register_routes(app)

    return app