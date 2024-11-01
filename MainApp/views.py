from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.models import Snippet
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm, UserRegistrationForm,CommentForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required(login_url="HomePage")
def add_snippet_page(request):
    #создаем пустую форму при запросе методом GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'form': form,
            'pagename': 'Добавление нового сниппета'
            }
        return render(request, 'pages/add_snippet.html', context)
    #если форма заполнена, то получаем данные из формы и создаем новый сниппет в БД
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit = False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("SnippetsList")
        return render(request, "pages/add_snippet.html", {"form": form})


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {"pagename": 'Просмотр сниппетов',
               "snippets": snippets,
               "count": snippets.count()
               }
    return render(request, 'pages/view_snippets.html', context)

@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {'pagename': 'Мои сниппеты',
               'snippets': snippets,
               'count':snippets.count()}
    return render(request, 'pages/view_snippets.html', context)



def snippet_details(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        context = {
            "pagename": 'Просмотр сниппета',
            "ErrorText":f'Сниппет с id {snippet_id} не существует.'
        }
        return render(request, "pages/error_page.html", context)
    else:
        comment_form = CommentForm()
        snippet = Snippet.objects.get(id=snippet_id)
        context = {
            "pagename": 'Просмотр сниппета',
            "snippet": snippet
                   }
        context["type"] = "view"
        context["comment_form"] = comment_form
        return render(request,'pages/snippet_details.html',context)


@login_required
def snippet_edit(request, snippet_id):
    context ={
        "pagename":"Редактирование сниппета"
    }
    try:
        snippet = Snippet.objects.filter(user=request.user).get(id=snippet_id)
    except ObjectDoesNotExist:
        return Http404
    # #Variant 1
    # # получение данных сниппета с помощью SnippetForm
    # if request.method == "GET":
    #     form = SnippetForm(instance=snippet)
    #     return render(request, "pages/add_snippet.html", {"form":form})
    #Variant 2
    #хотим получить страницу с данными сниппета
    if request.method == "GET":
        context = {
            'snippet': snippet,
            'type': 'edit',
            }
        return render(request, 'pages/snippet_details.html', context)
    #если форма заполнена, то получаем данные из формы и создаем новый сниппет в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.public = data_form.get("public",False)
        snippet.save()
        return redirect("SnippetsList")    

@login_required
def snippet_delete(request, snippet_id):
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=snippet_id)
        snippet.delete()
    return redirect("SnippetsList")

@login_required
def comments_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit = False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect("SnippetDetails",snippet_id=snippet_id)
    return HttpResponseNotAllowed(['POST'])




def create_user(request):
    context = {
        'pagename': 'регистрация нового пользователя'
        }
    if request.method == "GET":
        form = UserRegistrationForm()
        context["form"] = form
        return render(request,'pages/registration.html',context)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("HomePage")
        context["form"] = form
        return render(request, "pages/registration.html", context)







def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("username =", username)
        print("password =", password)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            context = {
                "pagename": "PythonBin",
                "errors": ["Wrong username or password"],
            }
            return render(request,"pages/index.html", context)
    return redirect('HomePage')


def logout(request):
    auth.logout(request)
    return redirect("HomePage")