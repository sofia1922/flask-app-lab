from flask import Flask

def create_app():
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    from .main_views import main_bp
    from .users.views import users_bp
    from .products.views import products_bp

    app.register_blueprint(main_bp)                 
    app.register_blueprint(users_bp, url_prefix='/users')   
    app.register_blueprint(products_bp, url_prefix='/products')

    return app

app = create_app()
