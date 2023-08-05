from django.shortcuts import render

# Create your views here.
from flask import Blueprint, request, render_template

testapp = Blueprint("auth", __name__, url_prefix="/auth")

@testapp.route("/hello")
def hello():
    return render_template("testapp/hello.html")

# Fibonacci numbers module

def fibPrint(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while b < n:
        print(b)
        a, b = b, a+b

def fibReturn(n):   # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result

def LogPrint(strMsg):    # write Fibonacci series up to n
        print('msg from lib yooooooo: ',strMsg)