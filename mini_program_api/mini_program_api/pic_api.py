from django.http import JsonResponse

from . import util
from ocr.main import ocr
from douban_query.main import search
from ocr.segmentation import segment
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_POST
def upload_pic(request):
    sessionId = request.POST.get("sessionId")
    pic = request.FILES.get("pic")
    # pic = ImageFile(pic)
    pics = segment(pic.read(), DEBUG=1)
    book_list_recommond = []
    for pic in pics:
        result = ocr(pic)
        search_string = ""
        print (result)
        if "words_result" in result:
            for keyword in result["words_result"]:
                search_string = search_string + keyword["words"] + "+"
            search_string = search_string[:-1]
            print(search_string)
            if search_string == "":
                continue
            book_list_recommond.append(search(search_string, sessionId)[0])
            print(book_list_recommond)
    return JsonResponse(util.get_json_dict(message='analyse success', data=book_list_recommond))
