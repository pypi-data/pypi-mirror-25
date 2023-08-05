from flask import Blueprint, request, render_template

module_add = Blueprint("auth", __name__, url_prefix="/auth")

@module_add.route("/hello")
def hello():
    return render_template("module_add/hello.html")


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
   