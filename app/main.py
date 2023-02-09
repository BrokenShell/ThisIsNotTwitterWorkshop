from flask import Flask, render_template, request

from app.database import MongoDB

APP = Flask(__name__)
APP.db = MongoDB()


@APP.route("/")
def home():
    return render_template("home.html")


@APP.route("/feed")
def feed():
    payload = APP.db.find_all().sort("id", -1).limit(100)
    return render_template("feed.html", payload=payload)


@APP.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        user = request.values.get("Name")
        text = request.values.get("Text")
        record = {
            "Name": user,
            "Text": text,
        }
        APP.db.insert_one(record)
        return render_template("post.html", record=record, user=user)
    else:
        return render_template("post.html")


@APP.route("/delete/<_id>")
def delete(_id: str):
    APP.db.collection.delete_one({"id": int(_id)})
    return feed()


if __name__ == '__main__':
    APP.run()
