from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from graphene_django.views import GraphQLView
from .schema import api_schema
from .views import FormManager, DownloadFormSubmissions


urlpatterns = [
    url(r'builder/', FormManager.as_view()),
    url(r'download/', DownloadFormSubmissions.as_view()),
    url(r'graphql', GraphQLView.as_view(graphiql=True, schema=api_schema)),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()