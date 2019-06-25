import re


def link_filter(item):
    link_pattern = re.compile(r"<a.*?>\s*(.*)\s*(.*)</a>")
    its = link_pattern.finditer(item)
    mutiItem = ""
    for it in its:
        mutiItem = mutiItem + it.group(1) + it.group(2) + ','
    mutiItem = mutiItem[:-1]
    if mutiItem != "":
        return mutiItem
    else:
        return item


def item(info):
    dic = {}
    item_pattern1 = re.compile(r"<span class=\"pl\">(.*):</span>((.|\n)*?)<br/?>")
    item_pattern2 = re.compile(r"<span>\s*<span class=\"pl\">(.*)</span>:((.|\n)*?)</span><br/>")
    it1 = item_pattern1.finditer(info)
    it2 = item_pattern2.finditer(info)
    for it in it1:
        dic[it.group(1).replace(' ', '')] = link_filter(it.group(2))
    for it in it2:
        dic[it.group(1).replace(' ', '')] = link_filter(it.group(2))
    return dic


def get_tags(text):
    tags_pattern = re.compile(r"<a class=\"  tag\" href=\".*\">(.*)</a>")
    its = tags_pattern.finditer(text)
    tags = ""
    for it in its:
        tags = tags + it.group(1) + ','
    if tags == "":
        tags = "暂无"
    return tags


def re_detail(text):
    info_pattern = re.compile(r"<div id=\"info\" class=\"\">(.*?)</div>", re.DOTALL)
    its = info_pattern.search(text)
    infoDic = item(its.group(1))
    infoDic["tags"] = get_tags(text)
    return infoDic
