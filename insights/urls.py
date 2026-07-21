from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.insights_page,
        name='insights'
    ),

    path(
        'download-report/',
        views.download_report,
        name='download_report'
    ),

]