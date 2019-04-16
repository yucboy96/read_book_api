import requests
import re
from dbTables.models import Bookshelf

URL = "https://www.douban.com/search"


def search(keyword_string, sessionId):
    params = {
        "cat": 1001,
        "q": keyword_string
    }
    header = {
        "Content-Type": "application/json; charset=UTF-8"}
    r = requests.get(URL, params=params, headers=header)
    detail_pattern = re.compile(r"<a class=\"nbg\" href=\"(\S*)\"[^\n]*title=\"(.*)\" ><img src=\"(.*)\"></a>")
    wtpy_pattern = re.compile(r"<span class=\"subject-cast\">([^\n]*)</span>")

    it1 = detail_pattern.finditer(r.text)
    it2 = wtpy_pattern.finditer(r.text)

    book_list = book_list_constructor(it1, it2, sessionId)
    return book_list[0], book_list


def book_list_constructor(it1, it2, sessionId):
    list = []
    while True:
        try:
            x = next(it1)
            y = next(it2)
            dic = {"sessionId": sessionId}
            wtpy = y.group(1).split('/')
            if len(wtpy) == 4:
                dic["publisher"] = wtpy[-2]
                dic["writer"] = wtpy[0] + '/' + wtpy[1]
            if len(wtpy) == 3:
                dic["publisher"] = wtpy[-2]
                dic["writer"] = wtpy[0]
            dic["webUrl"] = x.group(1)
            dic["title"] = x.group(2)
            dic["imgUrl"] = x.group(3)
            list.append(dic)
        except StopIteration:
            break
    return list


if __name__ == '__main__':
    search("see")
