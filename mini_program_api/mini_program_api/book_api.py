from django.http import JsonResponse
import json
import re


from . import util
from ocr.main import ocr
from douban_query.query import search_list, search_book_intro, search_more_detail
from ocr.segmentation import segment
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from dbTables.models import Bookshelf


def word_filter(word):
    result = []
    for char in word:
        if re.search("[\u4e00-\u9fff]",char) is not None:
            result.append(char)
    return ''.join(result)


@csrf_exempt
@require_POST
def upload_pic(request):
    #global GLOBALINDEX
    sessionId = request.POST.get("sessionId")
    pic = request.FILES.get("pic")
    # pic = ImageFile(pic)
    pics = segment(pic.read(), DEBUG=0)
    ocr_result_list = []
    # dir_name = "./output/{0}".format(GLOBALINDEX)
    # fo = open(dir_name + "/seachString.txt", "w")
    #GLOBALINDEX = GLOBALINDEX + 1
    for pic_group in pics:
        search_string = ""
        search_words = []
        for pic in pic_group[:-1]:
            result = ocr(pic)
            print("this is text_cut img")
            print(result)
            if "words_result" in result:
                for keyword in result["words_result"]:
                    word = word_filter(keyword["words"])
                    if len(word)>0:
                        search_string = search_string + word + "+"
                        search_words.append(word)
        search_string = search_string[:-1]
            # print(search_string)
        if search_string == "":
            result = ocr(pic_group[-1])
            print("this is cut img")
            print(result)
            if "words_result" in result:
                for keyword in result["words_result"]:
                    word = word_filter(keyword["words"])
                    if len(word)>0:
                        search_string = search_string + word + "+"
                        search_words.append(word)
        search_string = search_string[:-1]
        print("search_string")
        print(search_string)

        # fo.write(search_string+"\n")

        if search_string != "":
            ocr_result_list.append({"search_string": search_string, "search_words": search_words})
    # fo.close()
    return JsonResponse(util.get_json_dict(message='analyse success', data=ocr_result_list))


def book_candidate(searchList, n):
    book_list_candidate = []
    for i in range(1, min(len(searchList), n)):
        searchList[i]["isFirst"] = False
        book_list_candidate.append(searchList[i])
    return book_list_candidate


@csrf_exempt
@require_POST
def update_infoDic(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    infoDic = search_more_detail(request.POST.get("webUrl"), request.POST.get("shortIntro"))
    print(infoDic)
    Bookshelf.objects.filter(webUrl=request.POST.get("webUrl")).update(**infoDic)
    return JsonResponse(util.get_json_dict(data={'infoDic': infoDic}))


@csrf_exempt
@require_POST
def book_intro(request):  # to get more detail info such as the tags and intro and split wrtier publisher
    request.POST = json.loads(request.body.decode('utf-8'))
    webUrl = request.POST.get("webUrl")
    data = search_book_intro(webUrl)
    print("book_intro data:")
    print(data)
    if data:
        return JsonResponse(util.get_json_dict(data={"intro": data}))
    else:
        return JsonResponse(util.get_json_dict(data={"intro": "暂无简介"}))


@csrf_exempt
@require_POST
def bookshelf_add(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    chosen_books = request.POST.get("chosen_books")
    for book in chosen_books:
        if Bookshelf.objects.filter(sessionId = book["sessionId"],imgUrl = book["imgUrl"]).first() is None:
            Bookshelf.objects.create(**book)
    return JsonResponse(util.get_json_dict(message="bookshelf_add success"))


@csrf_exempt
@require_POST
def get_bookshelf(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    sessionId = request.POST.get("sessionId")
    print("User login:")
    print(sessionId)
    bookList = list(Bookshelf.objects.filter(sessionId=sessionId).values())
    for book in bookList:
        book["lastRead"] = book["lastRead"].date()
    return JsonResponse(util.get_json_dict(message="get bookshelf success", data=bookList))


@csrf_exempt
@require_POST
def delete_book(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    sessionId = request.POST.get("sessionId")
    webUrl = request.POST.get("webUrl")
    try:
        Bookshelf.objects.filter(sessionId=sessionId, webUrl=webUrl).delete()
    finally:
        return JsonResponse(util.get_json_dict(message="delete book success"))
