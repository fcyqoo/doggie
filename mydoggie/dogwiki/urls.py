from django.conf.urls import url
from django.contrib import admin
from dogwiki import views

admin.autodiscover()

urlpatterns = [
    # Project lifecycle
    url(r'^all/', views.wiki_index)
]
