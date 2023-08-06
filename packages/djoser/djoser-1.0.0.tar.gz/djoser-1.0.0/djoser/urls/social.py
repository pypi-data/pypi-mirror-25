from django.conf.urls import url

from rest_framework_jwt import views


urlpatterns = [
    url(r'^social-auth/', views.obtain_jwt_token, name='social-auth'),
]
