import click
from blog.database import mongo
from flask_simplelogin import SimpleLogin
from werkzeug.security import check_password_hash, generate_password_hash


def create_user(**data):
    """Creates user with encrupted password."""
    try:
        if "username" not in data and "password" not in data:
            raise ValueError("username and password are required.")

        data["password"] = generate_password_hash(
            data.pop("password"), method="pbkdf2:sha256"
        )
        if mongo.db.users.find_one({"username": data["username"]}):
            print("User not created! This user already exists")
        else:
            mongo.db.users.insert_one(data)
            return data
    except Exception as e:
        print(e)


def validate_login(user):
    """Validates user login."""
    if "username" not in user and "password" not in user:
        raise ValueError("username and password are required.")

    db_user = mongo.db.users.find_one({"username": user["username"]})
    if db_user and check_password_hash(db_user["password"], user["password"]):
        return True
    return False


def configure(app):
    SimpleLogin(app, login_checker=validate_login)

    @app.cli.command()
    @click.argument("username")
    @click.password_option()
    def add_user(username, password):
        """Creates a new user"""
        user = create_user(username=username, password=password)
        click.echo(f"user created {user['username']}")
