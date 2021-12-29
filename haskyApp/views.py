from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .models import Question, Answer, Tag, Profile, QuestionManager, Like
from .forms import LoginForm, QuestionForm, SignupForm, AnswerForm, EditProfileForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django import forms
from django.views.decorators.http import require_GET, require_POST


from django.http import HttpResponseRedirect, request
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

    if request.method == "GET":
        form = AnswerForm()
    else:
        form = AnswerForm(data = request.POST)
        if form.is_valid():
            new_ans = Answer(body = form.cleaned_data['body'], question_id = pk, author_id = request.user.profile.id)
            new_ans.save()
            #form = AnswerForm()
            #return redirect(reverse("?page=1")) ???????????????????
            return redirect("questions", pk = question.id)
            #return redirect("/questions/" + pk})

    context = {
        'question': question,
        'answers': content,
        'tags': tags,
        'top_users': top_users,
        'form': form, 
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
    tags = Tag.objects.top_tags()
    top_users = Profile.objects.top()
    if request.method == "GET":
        form = SignupForm()
    elif request.method == "POST":
        next = request.GET.get('next', '/')
        form = SignupForm(data = request.POST, files = request.FILES)
        if form.is_valid():
            name = form.cleaned_data['username']
            passw = form.cleaned_data['password']

            new_user = User.objects.create_user(username = name, password = passw)
            new_user.save()
            photo = form.files.get('avatar', False)

            if photo:
                #photo = form.files['avatar']   
                new_profile = Profile(user = new_user, avatar = photo)
            else:
                new_profile = Profile(user = new_user)

            new_profile.save()
            user = auth.authenticate(username = name, password = passw)
            if user:
                auth.login(request, user)
                #return redirect(reverse('new'))
                return HttpResponseRedirect(next)
            
    context = {
        'tags': tags,
        'top_users': top_users,
        'form': form
    }
    return render(request, "signup.html", context)

@login_required
def edit(request):
    #return render(request, "edit.html")
    tags = Tag.objects.top_tags()
    top_users = Profile.objects.top()

    if request.method == "GET":
        initial_data = model_to_dict(request.user)
        if request.user.profile.avatar:
            initial_data['avatar'] = request.user.profile.avatar
        form = EditProfileForm(initial=initial_data)
    elif request.method == "POST":
        form = EditProfileForm(data = request.POST, files = request.FILES, instance=request.user)
        if form.is_valid():
           form.save()
           return redirect(reverse('edit'))
            
    context = {
        'tags': tags,
        'top_users': top_users,
        'form': form
    }
    return render(request, "edit.html", context)
    

    
def login(request):
    tags = Tag.objects.top_tags()
    top_users = Profile.objects.top()

    if request.method == "GET":
        form = LoginForm()
    elif request.method == "POST":
        next = request.GET.get('next', '/')
        form = LoginForm(data = request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, "Something went wrong! Please check if Caps Lock is off and try again!")
            else:
                auth.login(request, user)
                #return redirect("/new")
                return HttpResponseRedirect(next)

    context = {
        'tags': tags,
        'top_users': top_users,
        'form': form
        }
    return render(request, "login.html", context)

 

@login_required
def ask(request):
    tags = Tag.objects.top_tags()
    top_users = Profile.objects.top()

    q_form = QuestionForm()
    if request.method == "POST":
        q_form = QuestionForm(data = request.POST)
        if q_form.is_valid():

            new_question = Question(head = q_form.cleaned_data['head'], body = q_form.cleaned_data['body'], author_id = request.user.profile.id)
            new_question.save()

            arr = q_form.data['tags'].split(' ')
            if len(arr) > 3:
                q_form.add_error(None, "Not more than 3 tags!!")
            else:
                arrTags = []
                for str in arr:
                    improved = improveTag(str)
                    if improved:
                        tag, res = Tag.objects.get_or_create(name = improved)
                        arrTags.append(tag)

                tagsQuestions = []
                for tag in arrTags:
                    tagsQuestions.append(Question.tags.through(tag_id=tag.id, question_id=new_question.id))
                #for tag in arrTags:
                Question.tags.through.objects.bulk_create(tagsQuestions)

                return redirect("questions", pk = new_question.id)
    return render(request, "ask.html", {'tags': tags, 'top_users': top_users, 'form': q_form})

def logout(request):
    auth.logout(request)
    return redirect(reverse('new'))

@login_required
@require_POST
def vote(request):
    print(request.POST)
    content = request.POST['content']
    if (content == "question"):
        print ("I AM QUESTION LIKE")
        q_id = request.POST['id']
        q = Question.objects.get(id = q_id)
        like = Like(user = request.user.profile, content_object = q, vote = 1)
        like.save()
    elif (content == "answer"):
        print ("I AM ANSWER LIKE")

        a_id = request.POST['id']
        a = Answer.objects.get(id = a_id)
        like = Like(user = request.user.profile, content_object = a, vote = 1)
        like.save()
    return JsonResponse({})





def improveTag(str):
    marks = ''' !()-[]{};?@#$%:'"\,./^&;*'''
    improved = str
    for x in str:  
        if x in marks:  
            improved = improved.replace(x, "")  
    return improved
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