from django.shortcuts import render

from . models import TestData, TestDataCat
def index(request):

    TestDataCat.data_export('excel')


    return