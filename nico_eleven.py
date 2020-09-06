from flask import Flask, render_template, request
from nico_scrapper import aggregate_subreddits

app = Flask("RedditNews")

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


@app.route("/")
def home():
    return render_template("nico_eleven_home.html", subreddits=subreddits)


@app.route("/read")
def read():
    selected = []
    for subreddit in subreddits:
        if subreddit in request.args:
            selected.append(subreddit)
    posts = aggregate_subreddits(selected)
    posts.sort(key=lambda post: post['votes'], reverse=True)
    return render_template("nico_eleven_read.html", selected=selected, posts=posts)


app.run(host="0.0.0.0")