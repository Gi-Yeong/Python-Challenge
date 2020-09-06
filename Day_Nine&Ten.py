import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine")


@app.route("/")
def index():
    order_by = request.args.get('order_by')
    if order_by == 'new':
        if 'new' in db:
            new_list = db['new']
        else:
            new_list = get_list(new)
            db['new'] = new_list
        return render_template('day_9_10_index.html', order='new', list=new_list)
    else:
        if 'popular' in db:
            popular_list = db['popular']
        else:
            popular_list = get_list(popular)
            db['popular'] = popular_list
        return render_template('day_9_10_index.html', order='popular', list=popular_list)


@app.route("/<objected_id>")
def detail(objected_id):
    url = make_detail_url(objected_id)
    comment = requests.get(url).json()
    return render_template("day_9_10_detail.html", comment=comment)


def get_list(url):
    result = requests.get(url).json()
    result_list = []
    for item in result['hits']:
        title = item['title']
        url = item['url']
        points = item['points']
        author = item['author']
        num_comments = item['num_comments']
        object_id = item['objectID']
        item_dict = {
            'title'       : title,
            'url'         : url,
            'points'      : points,
            'author'      : author,
            'num_comments': num_comments,
            'object_id'   : object_id
        }
        result_list.append(item_dict)
    return result_list


app.run(host="0.0.0.0")
