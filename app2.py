from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from flask_session import Session
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, UserMixin, logout_user
import datetime
import re
import bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secrete_key"
app.config[
    "MONGO_URI"
] = "Your_mongo_URI"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)

TrendingGames = [
    {
        "name": "War Frame",
        "image_url": "/static/images/trending-01.jpg",
        "price": 28,
        "disc_price": 20,
    },
    {
        "name": "Towar of Fantasy",
        "image_url": "/static/images/trending-02.jpg",
        "price": 44,
        "disc_price": 0,
    },
    {
        "name": "Super People",
        "image_url": "/static/images/trending-03.jpg",
        "price": 64,
        "disc_price": 44,
    },
    {
        "name": "Master Duel",
        "image_url": "/static/images/trending-04.jpg",
        "price": 32,
        "disc_price": 0,
    },
    
]

TopGames = [
    {"name": "War Frame", "image_url": "/static/images/top-game-01.jpg"},
    {"name": "PUBG", "image_url": "/static/images/top-game-02.jpg"},
    {"name": "Apex Legends", "image_url": "/static/images/top-game-03.jpg"},
    {"name": "The Simsa", "image_url": "/static/images/top-game-04.jpg"},
    {"name": "Lostark", "image_url": "/static/images/top-game-05.jpg"},
    {"name": "Destiny 2", "image_url": "/static/images/top-game-06.jpg"},
]

TopCategories = [
    {"name": "Brawlhalla", "image_url": "/static/images/categories-01.jpg"},
    {"name": "Dota 2", "image_url": "/static/images/categories-02.jpg"},
    {"name": "Tower of Fantasy", "image_url": "/static/images/categories-03.jpg"},
    {"name": "Super People", "image_url": "/static/images/categories-04.jpg"},
    {"name": "War Frame", "image_url": "/static/images/categories-05.jpg"},
]

AllGames = [
    {
        "name": "War Frame",
        "cat": "adv",
        "image_url": "/static/images/trending-01.jpg",
        "price": 28,
        "disc_price": 20,
    },
    {
        "name": "Towar of Fantasy",
        "cat": "adv",
        "image_url": "/static/images/trending-02.jpg",
        "price": 44,
        "disc_price": 0,
    },
    {
        "name": "Super People",
        "cat": "adv",
        "image_url": "/static/images/trending-03.jpg",
        "price": 64,
        "disc_price": 44,
    },
    {
        "name": "Master Duel",
        "cat": "rac",
        "image_url": "/static/images/trending-04.jpg",
        "price": 32,
        "disc_price": 0,
    },
    {
        "name": "PUBG",
        "cat": "str",
        "image_url": "/static/images/top-game-02.jpg",
        "price": 24,
        "disc_price": 20,
    },
    {
        "name": "Apex Legends",
        "cat": "rac",
        "image_url": "/static/images/top-game-03.jpg",
        "price": 55,
        "disc_price": 45,
    },
    {
        "name": "The Simsa",
        "cat": "str",
        "image_url": "/static/images/top-game-04.jpg",
        "price": 40,
        "disc_price": 35,
    },
    {
        "name": "Lostark",
        "cat": "adv",
        "image_url": "/static/images/top-game-05.jpg",
        "price": 25,
        "disc_price": 19,
    },
    {
        "name": "Destiny 2",
        "cat": "str",
        "image_url": "/static/images/top-game-06.jpg",
        "price": 65,
        "disc_price": 59,
    },
    {
        "name": "Brawlhalla",
        "cat": "str",
        "image_url": "/static/images/categories-01.jpg",
        "price": 15,
        "disc_price": 10,
    },
    {
        "name": "Dota 2",
        "cat": "rac",
        "image_url": "/static/images/categories-02.jpg",
        "price": 85,
        "disc_price": 65,
    },
]


@app.route("/")
def index():
    
    if "email" in session:
        print("Authanticate")
        return render_template(
            "index2.html",
            TrendingGames=TrendingGames,
            TopGames=TopGames,
            TopCategories=TopCategories,
        )
    else:
        return render_template(
            "index2.html",
            TrendingGames=TrendingGames,
            TopGames=TopGames,
            TopCategories=TopCategories,
        )


@app.route("/shop")
def shop():
    return render_template("shop.html", AllGames=AllGames)


@app.route("/products/<string:category>/<string:game_name>")
@app.route("/products/<string:game_name>")
@app.route("/products")
def product(category=None, game_name=None):
    games = AllGames
    if category is None:
        category = "All-Product"

    if category == "trending":
        games = TrendingGames
    elif category == "most-played":
        games = TopGames
    elif category == "top-category":
        games = TopCategories

    if game_name:
        game_details = next((game for game in games if game["name"] == game_name), None)
        if not game_details:
            return "Product not fount", 404
        return render_template(
            "product-details.html",
            category=category,
            game=game_details,
            TopCategories=TopCategories,
        )
    else:
        return render_template(
            "product-details.html",
            category=category,
            game=game_name,
            TopCategories=TopCategories,
        )


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._-]+@gmail\.com$"
    return re.match(pattern, email)


@app.route("/contact", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        data = {
            "name": name,
            "surname": surname,
            "email": email,
            "subject": subject,
            "message": message,
            "date": datetime.datetime.utcnow(),
        }
        if is_valid_email(email):
            print("valid email")
            if "email" in session:
                print("in session")
                mongo.db.response.insert_one(data)
                return jsonify({"success": True})
            else:
                print("Not in session")
                return jsonify({"result": True})
        else:
            message = "Email is Invalid"
            print(message)
            return jsonify({"error": message})
    return render_template("contact.html")


@app.route("/search/<string:game_name>", methods=["GET", "POST"])
def search(game_name):
    query = None  # Initialize the query variable

    if request.method == "POST":  # Change "get" to "POST"
        query = request.form["query"]
        if query:
            game_details = next(
                (game for game in AllGames if game["name"] == query), None
            )
            print(game_details)
            print(game_name)
            if game_details:
                return render_template(
                    "search.html",
                    query=query,
                    game_name=query,
                    search_result=game_details,
                )

    return render_template(
        "search.html", query=query, game_name=query, search_result=None
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["emails"]
        name = request.form["name"]
        password = request.form["passwords"]
        confirm_password = request.form["confrim-passwords"]

        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        hash_confirm_password = bcrypt.hashpw(
            confirm_password.encode("utf-8"), bcrypt.gensalt()
        )

        if is_valid_email(email):
            if password == confirm_password:
                print("password check")
                UserEmail = mongo.db.UserData.find_one({"email": email})
                if UserEmail is None:
                    print("email check")
                    SignupData = {
                        "email": email,
                        "name": name,
                        "password": hash_password,
                        "c-password": hash_confirm_password,
                        "date": datetime.datetime.utcnow(),
                    }
                    session["email"] = email
                    mongo.db.UserData.insert_one(SignupData)
                    return jsonify({"result": True})
                    
                else:
                    message = "The email is already taken."
                    print(message)
                    return jsonify({"error": message, "type": "email"})
                    
            else:
                message = "Passwords must be same"
                print(message)
                return jsonify({"error": message, "type": "password"})
                
        else:
            message = "The Email in not valid"
            print(message)
            return jsonify({"error": message, "type": "email"})
            

    return render_template("signup.html")


class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": user_id})
    return User(user_id) if user_data else None


@app.route("/signin", methods=["GET", "POST"])
def signin():
    message = "Please enter your credential "
    if request.method == "POST":
        email = request.form["email"]
        print(email)
        password = request.form["password"]
        userfound = mongo.db.UserData.find_one({"email": email})
        print(userfound)

        if userfound:
            email_val = userfound["email"]
            passwordcheck = userfound["password"]
            print(email_val, passwordcheck)
            if bcrypt.checkpw(password.encode("utf-8"), passwordcheck):
                session["email"] = email_val
                print(password, passwordcheck)

                return jsonify({"result": True})

            else:
                if "email" in session:
                    return jsonify({"result": True})

                message = "wrong password"
                print(message)
                return jsonify({"error": message, "type": "password"})
        else:
            message = "email not found"
            print(message)
            return jsonify({"error": message, "type": "email"})

    print(message)
    return render_template("signin.html")


@app.route("/subscribe")
def subscribe():
    return redirect(url_for("shop"))


@app.route("/logout")
def logout():
    session.pop("email", None)
    logout_user()
    return redirect(url_for("signin"))


if __name__ == "__main__":
    app.run()
