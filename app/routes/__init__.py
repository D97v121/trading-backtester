def register_routes(app):
    from .main_routes import main_bp
    app.register_blueprint(main_bp)