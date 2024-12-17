# from flask import Flask
# from models.database import db
# from routes.user_routes import user_routes
# from models.models import users_bp
# from models import db

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object("config.Config")

#     # Initialize database
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()  # Creates database tables if they don't exist

#     # Register blueprints
#     app.register_blueprint(user_routes, url_prefix="/api")

#     # Enregistrement des routes
#     app.register_blueprint(users_bp)


#     return app



# if __name__ == "__main__":
#     app = create_app()
#     app.run(host="0.0.0.0", port=3000)

from flask import Flask
from models.database import db  # Instance SQLAlchemy
from routes.user_routes import user_routes  # Blueprint des routes utilisateurs

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Importer les configurations

    # Initialisation de la base de données
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas

    # Enregistrement des routes utilisateurs
    app.register_blueprint(user_routes, url_prefix="/api")


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
