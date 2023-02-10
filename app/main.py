from flask import Flask, render_template, request
from Fortuna import percent_true
from app.bot import chat_bot
from app.database import MongoDB

APP = Flask(__name__)
APP.db = MongoDB()
pre_prompt = """You are now acting as an AI ChatBot in a chatroom environment. 
You should not add your name or format your response in any way. Plain text is good.
Your goal is to engage in friendly banter and conversations with users, 
responding in a sarcastic and human-like manner. Here is a recap of the conversation so far:"""


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
        if percent_true(66) or "ChatBot" in text:
            history = APP.db.find_all().sort("id", -1).limit(4)
            prompt = "\n".join(
                f"{obj['Name']}: {obj['Text']}" for obj in history
            )
            APP.db.insert_one({
                "Name": "ChatBot",
                "Text": chat_bot(f"{pre_prompt} ```{prompt}```"),
            })
        return render_template("post.html", record=record, user=user)
    else:
        return render_template("post.html")


@APP.route("/delete/<_id>")
def delete(_id: str):
    APP.db.collection.delete_one({"id": int(_id)})
    return feed()


if __name__ == '__main__':
    APP.run()
