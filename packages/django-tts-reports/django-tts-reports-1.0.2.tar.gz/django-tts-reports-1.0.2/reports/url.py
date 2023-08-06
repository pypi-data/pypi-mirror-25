from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import HelloPDFView

urlpatterns = [
    url(r'^deal-buyer-report/(?P<uuid>[-\w]+)/', login_required(HelloPDFView.as_view()), name='deal-buyer-report'),
]