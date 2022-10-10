from glob import glob
from turtle import title
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django import forms
import random

#global variable
entries = util.list_entries()
actualEntry = ""

#class use in views edit and new page
class newEncyclopedia(forms.Form):
    title = forms.CharField(label ="TITLE")
    content = forms.CharField(label = "content")
    
class editEncyclopedia(forms.Form):
    content = forms.CharField(label = "content")

#home views with all encyclopedia
def index(request):
    global entries
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })
#views of 1 encyclopedia
def entry(request,title): 
    if "actualEntry" not in request.session:
        global actualEntry
        actualEntry = title
    return render(request, "encyclopedia/entry.html", {
        "entries": util.convertToHtml(title)
    } ) 

#views to create a new encyclopedia
def newPage(request):       
    if request.method == "POST": 
        form = newEncyclopedia(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:index"))
        else: 
            return HttpResponseRedirect(reverse("wiki:index"))
    return render(request, "encyclopedia/createNewPage.html", {
        "form" : newEncyclopedia()
    })
#views to edit a current encyclopedia
def edit(request):
    global actualEntry
    if request.method == "POST": 
        form = editEncyclopedia(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(actualEntry, content)
            return render(request, "encyclopedia/entry.html", {
        "entries": util.convertToHtml(actualEntry)
    } )
        else: 
            return HttpResponseRedirect(reverse("wiki:index"))
    else:
        form = editEncyclopedia({'content' : util.get_entry(actualEntry)})
    return render(request, "encyclopedia/edit.html", {
        'form' : form
    })
#view to display a random encyclopedia
def randomPage(request): 
    global entries
    entry = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "entries": util.get_entry(entry)
    } )
