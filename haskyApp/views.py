from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

# Create your views here.

def pages(request, type):
    paginator = Paginator(type, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content

def index(request):
    content = pages(request, questions)
    return render(request, "index.html", {'questions': content})

def hot(request):
    content = pages(request, questions)
    return render(request, "hot.html", {'questions': content})

def question(request):
    content = pages(request, answers)
    return render(request, "question.html", {'answers': content})
    

def signup(request):
    return render(request, "signup.html", {})
    
def login(request):
    return render(request, "login.html", {})

def ask(request):
    return render(request, "ask.html", {})

questions = [
    {
        "title": f"Question number {i+1}",
        "body": "A very curious question" + " a very curious question"*30,
        "likes": f"{(i%2 + 1) + abs(i%5)}"
    } for i in range (100)
]

answers = [
    {
        "body": f"A witty answer number {i+1}" + " here you can see a witty answer"*30,
        "likes": f"{(i%2 + 1) + abs(i%5)}"
    } for i in range (100)
]