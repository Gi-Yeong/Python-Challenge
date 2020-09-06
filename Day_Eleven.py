import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

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

app = Flask("DayEleven")


@app.route('/')
def home():
    return render_template('day_11_home.html', subreddits=subreddits)


@app.route('/read')
def read():
    search_list = list(request.args)
    print(search_list)
    read_list = search(search_list)
    return render_template('day_11_read.html', search_list=search_list, result_list=read_list)


def search(list):
    result = []
    for subreddit in list:
        url = f'https://www.reddit.com/r/{subreddit}/top/?t=month'
        reddit = requests.get(url, headers=headers)
        soup = BeautifulSoup(reddit.text, 'html.parser')
        post_list = soup.find_all('div', {'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
        for post in post_list:
            title = post.find('h3', {'class': '_eYtD2XCVieq6emjKBH3m'}).text
            votes = post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text
            print(votes)
            if 'k' in votes:
                int_votes = int(float(votes.strip('k')) * 1000)
            else:
                int_votes = int(votes)
            href = post.find('a')['href']
            keyword = f"r/{subreddit}"
            post_tuple = (int_votes, title, href, keyword)
            result.append(post_tuple)
    return sorted(result, reverse=True)


app.run(host="0.0.0.0")
