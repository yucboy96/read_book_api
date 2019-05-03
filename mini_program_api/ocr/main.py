import requests
import json
import base64
import time
from dbTables.models import Variable
import datetime

AK = "XUOonTSYCPuppXpa1o7FdyZ8"
SK = "gYfWM3SsYHGYnElcmodY0CuCtjnuyrsi"
ACCESSTOKENURL = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"
OCRURL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


def get_access_token():
    Variable.objects.get_or_create(name="baidu_access_token")
    access_token = Variable.objects.get(name="baidu_access_token")
    now = datetime.datetime.now()
    if access_token.lifeTime != '':
        if (now - datetime.timedelta(0,int(access_token.lifeTime))) < access_token.lastModify:
            return access_token.value
    params = {
        "client_id": AK,
        "client_secret": SK
    }
    header = {
        "Content-Type": "application/json; charset=UTF-8"}
    r = requests.post(ACCESSTOKENURL, params=params, headers=header)
    r = json.loads(r.text)
    access_token.lifeTime = str(r["expires_in"])
    access_token.lastModify = now
    access_token.value = r["access_token"]
    access_token.save()
    return r["access_token"]


def ocr(pic):
    access_token = get_access_token()
    params = {
        "access_token": access_token
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    data = {
        "image": base64.b64encode(pic).decode("utf-8"),
        "probability": "true"
    }
    r = requests.post(OCRURL, params=params, headers=header, data=data)
    return json.loads(r.text)


if __name__ == '__main__':
    with open("./examples/cut/img1_cut/cut_3.png", 'rb') as pic:
        pic = pic.read()
        ocr(pic)
