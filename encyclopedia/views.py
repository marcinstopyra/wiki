from django.shortcuts import render, redirect
from django.http import HttpResponse
from markdown2 import Markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    contentMD = util.get_entry(entry_title)

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
