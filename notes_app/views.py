from django.shortcuts import render, redirect
from django.http import HttpResponse
from notes_app.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout, login
from django.contrib.auth.decorators import login_required


def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get('password')


        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid username')
            return redirect('/login/')

        # checks user authentication
        user = authenticate(username=username, password=password)
        
        if user is None:
            messages.error(request, "Invalid password")
            return redirect("/login/")

        else:
            login(request,user)  # session of user
            return redirect("/home/")

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        username = data.get("username")

        user = User.objects.filter(username=username)


        if user.exists():
            messages.info(request, "Username already exits!")
            return redirect("/register/")

        user = User.objects.create(
            first_name=first_name, last_name=last_name, username=username
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account created successfully!")
        return redirect("/register/")

    return render(request, "register.html")



@login_required(login_url='/login/')
def home_page(request):
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        description = data.get("description")

        Tasks.objects.create(name=name, description=description)
        return redirect("/home/")

    queryset = Tasks.objects.all()

    if request.GET.get("search"):
        queryset = queryset.filter(name__icontains=request.GET.get("search"))

    context = {"tasks": queryset}
    return render(request, "home.html", context)


def edit_task(request, id):
    queryset = Tasks.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        description = data.get("description")

        queryset.name = name
        queryset.description = description
        queryset.save()

        return redirect("/home/")

    context = {"tasks": queryset}
    return render(request, "edit.html", context)


def done_task(request, id):
    queryset = Tasks.objects.get(id=id)
    queryset.delete()

    return redirect("/home/")


# Create your views here.
