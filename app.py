from flask import Flask
from models.database import db
from routes.user_routes import user_routes
from routes.bus_routes import bus_routes
from routes.driver_routes import driver_routes
from models.user import User



def seed_data(app):
    with app.app_context():
        # Vérifie si la table est vide
        if User.query.count() == 0:
            # Liste d'utilisateurs par défaut
            users = [
                User(name="Alice Doe", email="alice@example.com"),
                User(name="Bob Smith", email="bob@example.com"),
                User(name="Charlie Brown", email="charlie@example.com")
            ]
            # Ajoute les utilisateurs dans la base de données
            db.session.bulk_save_objects(users)
            db.session.commit()
            print("Base de données remplie avec des utilisateurs par défaut.")
        else:
            print("La base de données contient déjà des utilisateurs.")


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Creates database tables if they don't exist
        #seed_data(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    

    # Register blueprints
    app.register_blueprint(user_routes, url_prefix="/api/user")
    app.register_blueprint(bus_routes, url_prefix="/api/bus")
    app.register_blueprint(driver_routes, url_prefix="/api/driver")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)

