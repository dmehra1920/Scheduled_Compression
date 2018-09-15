from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.homepage.as_view()),
    url(r'^display/',views.display.as_view()),
    url(r'^result$',views.save),
]