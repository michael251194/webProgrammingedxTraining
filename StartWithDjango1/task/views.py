from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms


# Create your views here.
#tasks = []
# define the tasks inside the index view to manage the session
class newTaskForm(forms.Form):
    task = forms.CharField(label ="new task")
    #priority = forms.IntegerField(label="priority", min_value=1, max_value=10)

def index(request):
    if "tasks" not in request.session:
            request.session["tasks"] = []

    return render(request, "task/index.html", {
        "tasks" : request.session["tasks"] 
    })

def add(request): 
    if request.method == "POST": 
        form = newTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else: 
            return render(request, "task/add.html", {
                "form": form
            })
    return render(request, "task/add.html", {
        "form":newTaskForm()
    })