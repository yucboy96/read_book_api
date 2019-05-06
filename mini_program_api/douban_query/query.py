import requests
import re
import json
from dbTables.models import Bookshelf

URL = "https://www.douban.com/search"


def search_list(search_string, search_words):
    params = {
        "cat": 1001,
        "q": search_string
    }
    header = {
        "Content-Type": "application/json; charset=UTF-8"}
    r = requests.get(URL, params=params, headers=header)
    detail_pattern = re.compile(
        r"<a class=\"nbg\" href=\"(?:\S*)\"[^\n]*sid: (\d*),.*title=\"(.*)\" ><img src=\"(.*)\"></a>")
    wtpy_pattern = re.compile(r"<span class=\"subject-cast\">([^\n]*)</span>\s*</div>\s*</div>\s*(?:<p>(.*)</p>)*")
    rating_pattern = re.compile(
        r"(?:<span class=\"rating_nums\">(\d.\d)</span>)|(?:<span>\(目前无人评价\)</span>)")
    print("success get response from" + search_string)
    it1 = detail_pattern.finditer(r.text)
    it2 = wtpy_pattern.finditer(r.text)
    it3 = rating_pattern.finditer(r.text)
    book_list = book_list_constructor(it1, it2, it3, search_string, search_words)
    sorted_list = sorted(book_list, key=lambda kv: kv['confidence'])
    return sorted_list


def book_list_constructor(it1, it2, it3, search_string, search_words):
    list = []
    while True:
        try:
            x = next(it1)
            y = next(it2)
            z = next(it3)
            dic = {"search_string": search_string}
            confidence = gen_confidence(x.group(2) + y.group(1).replace('/', ''), search_words)
            if confidence == 0:
                continue
            else:
                dic["confidence"] = confidence
            if y.group(2) is None:
                dic["intro"] = "暂无简介"
            else:
                dic["intro"] = y.group(2)
            # wtpy = y.group(1).split('/')
            # dic["writer"] = wtpy[0]
            # dic["publisher"] = "暂无"
            # dic["pubTime"] = "暂无"
            # pubTime_pattern = re.compile(r"\s*\d\d\d\d\s*")
            # if len(wtpy) == 4:
            #     dic["publisher"] = wtpy[2]
            #     dic["writer"] = wtpy[0] + '/' + wtpy[1]
            # if len(wtpy) == 3:
            #     dic["publisher"] = wtpy[1]
            #     dic["writer"] = wtpy[0]
            # if pubTime_pattern.match(wtpy[-1]) is not None:
            #     dic["pubTime"] = wtpy[-1]
            # else:
            #     dic["publisher"] = wtpy[-1]
            webUrl = str(x.group(1))
            dic["webUrl"] = webUrl
            dic["title"] = x.group(2)
            dic["imgUrl"] = x.group(3)
            dic["shortIntro"] = y.group(1)

            if z.group(1) is None:
                dic["rating"] = "暂无评分"
            else:
                dic["rating"] = z.group(1)
            list.append(dic)
        except StopIteration:
            break
    return list


def dp_function(dp, i, j, target, word):
    if i < 0 or j < 0:
        dp[i][j] = 0
        return 0
    if dp[i][j] >= 0:
        return dp[i][j]
    if target[i] == word[j]:
        dp[i][j] = dp_function(dp, i - 1, j - 1, target, word) + 1
    else:
        dp[i][j] = max(dp_function(dp, i - 1, j, target, word), dp_function(dp, i, j - 1, target, word))
    dp[i][j] = True
    return dp[i][j]


def gen_confidence(target, search_words):
    sum = 0
    print(target)
    for word in search_words:
        dp = [[-1 for j in range(len(word))] for i in range(len(target))]
        sum = sum + dp_function(dp, len(target) - 1, len(word) - 1, target, word)
    return sum


def search_book_intro(webUrl):
    r = requests.get(webUrl)
    intro_pattern = re.compile(r"<p data-clamp=\"3\">(.*)</p>")
    tag_pattern = re.compile(r"")
    its = intro_pattern.finditer(r.text)
    list = []
    for it in its:
        for paragraph in it.group(1).split("<br/>"):
            list.append(paragraph)
    return list


def search_more_detail(webUrl, shortIntro):
    webUrl = "https://m.douban.com/rexxar/api/v2/elessar/subject/" + webUrl
    r = json.loads(requests.get(webUrl).text)
    attributes = ['作者', '出版社']
    myAttributes = ['writer', 'publisher']
    dic = {'writer': '暂无', 'publisher': '暂无', 'tags': '暂无', 'pubTime': '暂无'}
    if r['extra']['info']:
        for item in r['extra']['info']:
            try:
                index = attributes.index(item[0])
                dic[myAttributes[index]] = item[1]
            except ValueError:
                continue
    shortIntro = shortIntro.replace(dic['writer'], '').replace(dic['publisher'], '')
    pubTime_pattern = re.compile(r".*(\d\d\d\d).*")
    it = pubTime_pattern.match(shortIntro)
    if it is not None:
        dic['pubTime'] = it.group(1)
    if r['tags']:
        tags = ''
        for item in r['tags']:
            tags = tags + item['name'] + ','
        if len(tags):
            tags = tags[:-1]
        dic['tags'] = tags
    return dic


if __name__ == '__main__':
    search_list("see")
