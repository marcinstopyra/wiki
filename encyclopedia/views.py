from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from . import util
from django import forms
from random import randrange

class newEntryForm(forms.Form):
    title = forms.CharField(label="New Entry Title")
    entry_content = forms.CharField(label="New Entry", widget=forms.Textarea)

class editEntryForm(forms.Form):
    edit_content = forms.CharField(label="Edit Entry", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    contentMD = util.get_entry(entry_title)

    if contentMD == None:
        return render(request,"encyclopedia/error.html", {
            "message": "<h1>Page not found :(</h1>"
        })

    markdowner = Markdown()
    contentHTML = markdowner.convert(contentMD)
    return render(request, "encyclopedia/entry.html", {
        "title": entry_title,
        "content": contentHTML
    })

def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    if query in entries:
        return redirect("wiki/" + query)
    else:
        print("smuteczeg")
        #find entries that match the search query
        search_entries = util.search_entries(entries, query)
        return render(request, "encyclopedia/search.html", {
        "q": query,
        "search_entries": search_entries
        })

def newPage(request):
    if request.method == "POST":
        entries = util.list_entries()
        form = newEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry_content"]
            if title in entries:
                print("JUSZ JEST")
                return render(request, "encyclopedia/newPage.html",{
                            "form": form,
                            "alert": True
                            })
            else:
                print("ADDED")
                with open("./entries/" + title + ".md", 'w') as file:
                    file.write("#" + title + '\n')
                    file.write(content)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tasks/add.html",{
                "form": form
            })
    return render(request, "encyclopedia/newPage.html", {
    "form": newEntryForm()
    })

def editPage(request, title):
    if request.method == "POST":
        form = editEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["edit_content"]
            with open("./entries/" + title + ".md", 'w') as file:
                file.truncate(0)
                file.write(content)
        return HttpResponseRedirect(reverse("index"))
    else:
        with open("./entries/" + title + ".md") as file:
            entry_content = file.read()
        # Preocupying form with existing content
        form = editEntryForm({"edit_content": entry_content})
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "form": form
        })

def randomPage(request):
    entries = util.list_entries()
    index = randrange(len(entries))
    return HttpResponseRedirect("/wiki/" + entries[index])
