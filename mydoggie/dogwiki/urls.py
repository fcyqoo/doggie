from django.conf.urls import url
from django.contrib import admin
from dogwiki import views

admin.autodiscover()

urlpatterns = [
    # Project lifecycle
    url(r'^all/', views.wiki_index),
    url(r'^update_base/', views.update_dog_base),
    url(r'^update_info/', views.update_dog_info)
]
