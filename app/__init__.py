from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from sqlalchemy import MetaData
from datetime import datetime

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__, static_folder='static', template_folder='templates')

    from app.config import DevelopmentConfig, TestingConfig, ProductionConfig

    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }

    app.config.from_object(configs.get(config_name, DevelopmentConfig))

    if not app.config.get("TESTING"):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(app.instance_path, 'data.sqlite')

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'

    from app.users.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    from .main_views import main_bp
    from .users.views import users_bp
    from .products.views import products_bp
    from .posts import post_bp

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
