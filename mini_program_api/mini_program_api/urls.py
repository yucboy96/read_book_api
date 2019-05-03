"""mini_program_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.urls import path

from . import view
from . import account_api, book_api,tracker_api


urlpatterns = [
    path('code2id', account_api.code2id),
    path('update_user', account_api.update_user),
    path('check_with_session_key', account_api.check_with_session_key),
    path('upload_pic', book_api.upload_pic),
    path('book_intro', book_api.book_intro),
    path('bookshelf_add', book_api.bookshelf_add),
    path('get_bookshelf', book_api.get_bookshelf),
    path('delete_book', book_api.delete_book),
    path("start_read", tracker_api.start_read),
    path('read_success', tracker_api.read_success),
    path('get_week_track',tracker_api.get_week_track),
    path('get_month_track',tracker_api.get_month_track),
    path('get_wxcode', account_api.get_wxcode)
]
