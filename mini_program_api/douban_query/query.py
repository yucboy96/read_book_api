import requests
import re
from dbTables.models import Bookshelf

URL = "https://www.douban.com/search"


def search_list(search_string):
    params = {
        "cat": 1001,
        "q": search_string
    }
    header = {
        "Content-Type": "application/json; charset=UTF-8"}
    r = requests.get(URL, params=params, headers=header)
    detail_pattern = re.compile(
        r"<a class=\"nbg\" href=\"(?:\S*)\"[^\n]*sid: (\d*),.*title=\"(.*)\" ><img src=\"(.*)\"></a>")
    wtpy_pattern = re.compile(r"<span class=\"subject-cast\">([^\n]*)</span>")
    rating_pattern = re.compile(r"(?:<span class=\"rating_nums\">(\d.\d)</span>)|(?:<span>\(目前无人评价\)</span>)")
    print(r.text)
    it1 = detail_pattern.finditer(r.text)
    it2 = wtpy_pattern.finditer(r.text)
    it3 = rating_pattern.finditer(r.text)

    book_list = book_list_constructor(it1, it2, it3, search_string)
    return book_list


def book_list_constructor(it1, it2, it3, search_string):
    list = []
    while True:
        try:
            x = next(it1)
            y = next(it2)
            z = next(it3)
            dic = {"search_string": search_string, "isSearchList": True}
            wtpy = y.group(1).split('/')
            dic["writer"] = wtpy[0]
            dic["publisher"] = "暂无"
            dic["pubTime"] = "暂无"
            pubTime_pattern = re.compile(r"\s*\d\d\d\d\s*")
            if len(wtpy) == 4:
                dic["publisher"] = wtpy[2]
                dic["writer"] = wtpy[0] + '/' + wtpy[1]
            if len(wtpy) == 3:
                dic["publisher"] = wtpy[1]
                dic["writer"] = wtpy[0]
            if pubTime_pattern.match(wtpy[-1]) is not None:
                dic["pubTime"] = wtpy[-1]
            else:
                dic["publisher"] = wtpy[-1]
            webUrl = str(x.group(1))
            dic["webUrl"] = webUrl
            dic["title"] = x.group(2)
            dic["imgUrl"] = x.group(3)
            print(z.groups())
            if z.group(1) is None:
                dic["rating"] = "暂无评分"
            else:
                dic["rating"] = z.group(1)
            list.append(dic)
        except StopIteration:
            break
    return list


def search_book_intro(webUrl):
    r = requests.get(webUrl)
    intro_pattern = re.compile(r"<p data-clamp=\"3\">(.*)</p>")
    its = intro_pattern.finditer(r.text)
    list = []
    for it in its:
        for paragraph in it.group(1).split("<br/>"):
            list.append(paragraph)
    return list


if __name__ == '__main__':
    search_list("see")
