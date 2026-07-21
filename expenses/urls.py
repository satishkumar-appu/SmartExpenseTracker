from django.urls import path
from . import views


urlpatterns = [

    path(
        'add/',
        views.add_transaction,
        name='add_transaction'
    ),


    path(
        'list/',
        views.transaction_list,
        name='transaction_list'
    ),


    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),


    path(
        'edit/<int:id>/',
        views.edit_transaction,
        name='edit_transaction'
    ),


    path(
        'delete/<int:id>/',
        views.delete_transaction,
        name='delete_transaction'
    ),


    path(
        'export-csv/',
        views.export_csv,
        name='export_csv'
    ),

]