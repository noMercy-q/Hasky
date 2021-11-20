from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Question, Answer, Tag, Profile, QuestionManager

# Create your views here.

def pages(request, type):
    paginator = Paginator(type, 5)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content

def index(request):
    new_questions = Question.objects.new()
    tags = Tag.objects.top_tags()
    top_users = Profile.objects.top()
    content = pages(request, new_questions)
    context = {
        'questions': content,
        'tags': tags,
        'top_users': top_users
    }
    return render(request, "index.html", context)

def hot(request):
    top_questions = Question.objects.top()
    tags = Tag.objects.top_tags()
    top_users = Profile.objects.top()
    content = pages(request, top_questions)
    context = {
        'questions': content,
        'tags': tags,
        'top_users': top_users
    }
    return render(request, "hot.html", context)

def question(request, pk):
    question = Question.objects.get(id = pk)
    tags = Tag.objects.top_tags()
    top_answers = Answer.objects.top(pk)
    top_users = Profile.objects.top()
    content = pages(request, top_answers)
    context = {
        'question': question,
        'answers': content,
        'tags': tags,
        'top_users': top_users
    }
    return render(request, "question.html", context)

def tag(request, pk):
    tag_questions = Question.objects.tag(pk)
    cur_tag = Tag.objects.get(id = pk)
    tags = Tag.objects.top_tags()
    top_users = Profile.objects.top()
    content = pages(request, tag_questions)
    context = {
        'questions': content,
        'tags': tags,
        'tag': cur_tag,
        'top_users': top_users
    }
    return render(request, "tag.html", context)

#class one_question(DetailView):
#   model = Question
#template_name = "question.html"
#    context_name = "question"
#    
   # extra_context = {'answers': answers}

    

def signup(request):
    return render(request, "signup.html", {})
    
def login(request):
    return render(request, "login.html", {})

def ask(request):
    return render(request, "ask.html", {})

#questions = [
#  {
#       "title": f"Question number {i+1}",
#        "body": "A very curious question" + " a very curious question"*30,
#        "likes": f"{(i%2 + 1) + abs(i%5)}"
#    } for i in range (100)
#]
#questions = Question.objects.all()

#top_questions = Question.objects.top()


#top_answers = Answer.objects.top()


#cur_question = 

#answers = [
#    {
#        "body": f"A witty answer number {i+1}" + " here you can see a witty answer"*30,
#        "likes": f"{(i%2 + 1) + abs(i%5)}"
#    } for i in range (100)
#]