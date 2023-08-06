from django.conf.urls import url

from . import views

app_name = 'appodeal'

urlpatterns = [
    url(r'^reward/$', views.RewardCreateAPIView.as_view(), name='reward-create'),
]
