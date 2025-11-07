from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os 

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='static', template_folder='templates')

    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig
    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    app.config.from_object(configs.get(config_name, DevelopmentConfig))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'data.sqlite')


    db.init_app(app)
    
    from app.posts import models

    migrate.init_app(app, db)

    from .main_views import main_bp
    from .users.views import users_bp
    from .products.views import products_bp
    from .posts import post_bp
    from app.posts import views 

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(post_bp, url_prefix='/post')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404
    
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    return app
