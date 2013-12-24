from django.shortcuts import render
from django_simple_response.decorators import serialization
from datetime import date

def home(request):
    return 401, "Not authorized"
