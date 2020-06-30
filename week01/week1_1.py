import os
# import re
import requests
from bs4 import BeautifulSoup as bs
# import pandas as pd
import csv

def get_html_from_network(url, headers=None):
    rsp = requests.get(url, headers=headers)
    if rsp.content != 200:
        raise Exception(f"请求失败, 状态码:{rsp.status_code}\n\n{rsp.text}")
    rsp.encoding = 'utf-8'
    return rsp.text

def get_html_from_local_file(file_path):
    if not os.path.isfile(file_path):
        raise Exception(f"文件:{file_path}不存在")
    with open(file_path) as f:
        html = f.read()
    return html

def get_movie_summary(html, shared_start=0, shared_stop=10, path="."):
    bs_info = bs(html, "html.parser")
    movies = []
    for movie in bs_info.find_all("div", attrs={"class": "movie-hover-info"})[slice(shared_start, shared_stop)]:
        tmp = {}
        raw_title, raw_type, _, raw_release = movie.find_all("div", attrs={"class", "movie-hover-title"})
        tmp["title"] = raw_title.span.text
        tmp["type"] = raw_type.contents[-1].strip()
        tmp["release"] = raw_release.contents[-1].strip()
        movies.append(tmp)

    headers = ["title", "type", "release"]
    path = f"{path.rstrip('/')}/question1.csv"
    with open(path, "w", encoding="utf-8") as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(movies)
    return path

if __name__ == "__main__":
    file_path = "/tmp/maoyan.html"
    url = "http://maoyan.com/films?showType=3"
    headers = {
        "user-agent": "",
        "cookie": ""
    }
    # html = get_html_from_network(url ,headers)
    html = get_html_from_local_file(file_path)
    path = get_movie_summary(html, path="/Users/ang.li/Downloads")
    print(path)


