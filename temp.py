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
db_comment = {}
app = Flask("DayNine")


def get_post_list(url):
    res = requests.get(url).json()
    temp_list = []
    for item in res['hits']:
        title = item['title']
        url = item['url']
        points = item['points']
        author = item['author']
        num_comments = item['num_comments']
        objectID = item['objectID']
        post_dict = {
            'title'       : title,
            'url'         : url,
            'points'      : points,
            'author'      : author,
            'num_comments': num_comments,
            'objectid'    : objectID,
        }
        temp_list.append(post_dict)
    return temp_list


def children_check(children_list, comment_list):
    for children in children_list:
        temp_dict = {'author': children['author'], 'text': children['text']}
        comment_list.append(temp_dict)
        if children['children']:
            children_check(children['children'], comment_list)


def get_comment(objectid):
    url = make_detail_url(objectid)
    try:
        res = requests.get(url).json()
    except:
        print(f"Error: {url}")
    post_dict = {
        'title' : res['title'],
        'points': res['points'],
        'author': res['author'],
        'url'   : res['url']
    }
    comment_list = []
    children_check(res['children'], comment_list)
    return post_dict, comment_list


@app.route('/')
def popular_func():
    order_by = request.args.get('order_by')
    if order_by == 'popular' or order_by is None:
        if 'popular' in db:
            popular_list = db['popular']
        else:
            popular_list = get_post_list(popular)
            db['popular'] = popular_list
        return render_template(
            'index_1.html', order="popular", post_list=popular_list)
    elif order_by == 'new':
        if 'new' in db:
            new_list = db['new']
        else:
            new_list = get_post_list(new)
            db['new'] = new_list
        return render_template('index_1.html', order="new", post_list=new_list)
    else:
        return


@app.route('/<objectid>')
def detail_func(objectid):
    if objectid == "favicon.ico":
        return
    if objectid in db_comment:
        post_dict = db_comment[objectid]['post_dict']
        comment_list = db_comment[objectid]['comment_list']
    else:
        post_dict, comment_list = get_comment(objectid)
        db_comment[objectid] = {
            'post_dict'   : post_dict,
            'comment_list': comment_list
        }
    return render_template(
        'detail_1.html', post_dict=post_dict, comment_list=comment_list)


app.run(host="0.0.0.0")

"""
해커뉴스 API와 Flask를 활용하여 해커뉴스 웹사이트 클론코딩을 진행합니다.

웹 사이트에는 다음 경로가 있어야합니다:
/
/?order_by=new
/?order_by=popular

# 조건
Fake DB를 구현하여 '신규'와 '인기'가 더 빠르게 로드 할 수 있어야 합니다.

Templete는 현재 order_by 선택 사항을 반영해야합니다.

기본 페이지 "/"는 order_by popular 입니다.

의견을 보러 갈 각 이야기에 대한 링크가 있어야합니다.

# 힌트
주석에 작성자가 없으면 삭제되었음을 의미합니다.

주석 텍스트를 렌더링하려면 Flask의 safe 태그를 사용하십시오.

CSS에 대해 걱정하지 마십시오. 기본 HTML 요소의 스타일을 지정하는 상용구에 .css 파일이 포함되어 있으며 <header> <section> <div> <h1> 등을 사용하면 자동으로 멋지게 보입니다.

API는 시간당 10,000 개의 요청으로 제한이 있습니다.
"""

"""
# templates/detail_1.html
<!DOCTYPE html>
<html>

<head>
  <link href="https://andybrewer.github.io/mvp/mvp.css" rel="stylesheet"></link>
</head>

<body>
</body>

</html>


# templates/index_1.html
<!DOCTYPE html>
<html>

<head>
  <link href="https://andybrewer.github.io/mvp/mvp.css" rel="stylesheet"></link>
</head>

<body>
  
</body>

</html>
"""