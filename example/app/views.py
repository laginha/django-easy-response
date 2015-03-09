from django.shortcuts import render
from easy_response.decorators import serialization
from datetime import date

def home(request):
    return 401, "Not authorized"
