import requests
import csv
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, send_file

app = Flask('Thirteen')

db = {}


# 웹 캐시(cache)때문에 한 번 csv 파일을 다운로드 했던 파일을 다시 다운로드 하려고하면
# 리로드하더라도 다운로드 관련 코드 변경사항이 적용되지 않는 문제가 발생.
# 아래는 웹 캐시를 사용하지 않게 하는 코드.
# IE 나 Chrome 에서만 작동.
@app.after_request
def add_header(rqst):
    rqst.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    rqst.headers["Pragma"] = "no-cache"
    rqst.headers["Expires"] = "0"
    rqst.headers['Cache-Control'] = 'public, max-age=0'
    return rqst


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    job = request.args.get('job_name').lower()
    url_list = [f'https://stackoverflow.com/jobs?r=true&q={job}',
                f'https://weworkremotely.com/remote-jobs/search?term={job}',
                f'https://remoteok.io/remote-dev+{job}-jobs']

    if db.get(job):
        job_list = db.get(job)
    else:
        job_list = extract(url_list)
        db[job] = job_list

    return render_template('search.html', job_list=job_list, length=len(job_list), name=job)


@app.route('/export')
def export():
    job_name = request.args.get('job_name').lower()
    jobs = db[job_name]
    save_to_file(jobs, job_name)
    return send_file(f'{job_name}.csv', as_attachment=True)


def save_to_file(jobs, job_name):
    file = open(f'{job_name}.csv', mode='w', encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(['title', 'link', 'company'])
    for job in jobs:
        writer.writerow(job.values())
    return


def extract(url_list):
    temp_list = []
    result = requests.get(url_list[0]).text
    soup = BeautifulSoup(result, 'html.parser')
    jobs = soup.find('div', {'class': 'listResults'}).find_all('div', {'class': 'grid--cell fl1'})

    for job in jobs:
        title = job.find('a')['title']
        link = "https://stackoverflow.com" + job.find("a")["href"]
        company = job.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).find("span").text.strip()
        temp_list.append({'title': title, 'link': link, 'company': company})

    result = requests.get(url_list[1]).text
    soup = BeautifulSoup(result, 'html.parser')
    jobs = soup.find("section", {"class": "jobs"}).find("ul").find_all("li")

    for job in jobs:
        link = "https://weworkremotely.com" + job.find("a")["href"]
        title = job.find("span", {"class": "title"})
        if title is not None:
            title = title.text
        company = job.find("span", {"class": "company"})
        if company is not None:
            company = company.text
        temp_list.append({'title': title, 'link': link, 'company': company})

    result = requests.get(url_list[2]).text
    soup = BeautifulSoup(result, "html.parser")
    jobs = soup.find("table", {"id": "jobsboard"}).find_all("tr", {"class": "job"})
    for job in jobs:
        company = job.find("td", {"class": "company position company_and_position"}). \
            find("a", {"itemprop": "hiringOrganization"}).find("h3").text
        title = job.find("td", {"class": "company position company_and_position"}). \
            find("h2", {"itemprop": "title"}).text
        link = "https://remoteok.io" + job["data-href"]
        temp_list.append({'title': title, 'link': link, 'company': company})

    return temp_list


app.run(host='0.0.0.0')
