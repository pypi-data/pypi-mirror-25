
from django.conf.urls import url

from poll.views import VoteView


urlpatterns = [

    url(r'^vote/$', VoteView.as_view(), name='vote')

]