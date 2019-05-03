from django.http import JsonResponse
import json
import datetime

from . import util
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from dbTables.models import ReadTracker


@csrf_exempt
@require_POST
def start_read(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    return JsonResponse(util.get_json_dict(message="start_read success",
                                           data={"ReadTrackerId": ReadTracker.objects.create(**request.POST).id}))


@csrf_exempt
@require_POST
def read_success(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    readTracker = ReadTracker.objects.get(id=request.POST["ReadTrackerId"])
    readTracker.isSuccess = True
    readTracker.save()
    return JsonResponse(util.get_json_dict(message="read success success"))


@csrf_exempt
@require_POST
def get_week_track(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    sessionId = request.POST["sessionId"]
    today = datetime.date.today()
    d = today.isoweekday()
    start = datetime.date.today() - datetime.timedelta(days=(d - 1))
    end = start - datetime.timedelta(days=-7)
    endTitle = start - datetime.timedelta(days=-6)
    title = str(start.year) + '年' + str(start.month) + '月' + str(start.day) + '日至' + str(endTitle.month) + '月' + str(
        endTitle.day) + '日'
    readTracker = ReadTracker.objects.filter(modify__range=(start, end), sessionId=sessionId)
    readSuccess = [0 for i in range(7)]
    readFailed = [0 for i in range(7)]
    successTimes = 0
    failedTimes = 0
    for tracker in readTracker:
        if tracker.isSuccess:
            readSuccess[tracker.modify.weekday()] = readSuccess[tracker.modify.weekday()] + tracker.readTime
            successTimes = successTimes + 1
        else:
            readFailed[tracker.modify.weekday()] = readFailed[tracker.modify.weekday()] + tracker.readTime
            failedTimes = failedTimes + 1
    return JsonResponse(util.get_json_dict(
        data={"title": title, "readSuccess": readSuccess, "readFailed": readFailed, "successTimes": successTimes,
              "failedTimes": failedTimes}))


@csrf_exempt
@require_POST
def get_month_track(request):
    request.POST = json.loads(request.body.decode('utf-8'))
    sessionId = request.POST["sessionId"]
    month = request.POST["month"]
    year = datetime.date.today().year
    start = datetime.datetime(year=year, month=month, day=1)
    if month == 12:
        year = year + 1
        month = 0
    end = datetime.datetime(year=year, month=month + 1, day=1)
    readTracker = ReadTracker.objects.filter(modify__range=(start, end), sessionId=sessionId)
    readSuccess = []
    successTimes = 0
    failedTimes = 0
    for tracker in readTracker:
        if tracker.isSuccess:
            readSuccess.append([(tracker.modify - start).days / 7, tracker.modify.weekday(), tracker.readTime])
            successTimes = successTimes + 1
        else:
            failedTimes = failedTimes + 1
    return JsonResponse(
        util.get_json_dict({"readSuccess": readSuccess, "successTimes": successTimes, "failedTimes": failedTimes}))
