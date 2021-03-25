from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import random
from . import util
from markdown2 import Markdown
from .forms import CreatForm, EditForm

def index(request):
    """
    Lists all entries in the encyclopedia.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def visit_entry(request, title):
    """
    Goes to the specific entry details.
    """
    return render(request,"encyclopedia/visit_entry.html",{
        "entry": util.get_entry(title),
        "title": title
    })


def create_page(request):
    """
    Shows a form that allows the user to create a new encyclopedia entry.
    """
    entries=util.list_entries()
    if request.method == "POST":
        form = CreatForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = form.cleaned_data["title"]
            
            for entry in entries:
                if title == entry:
                    return render(request,"encyclopedia/create_page.html",{
                        "form": form,
                        "isexist": True,
                        "message": "This Title already exist."
                    })
                else:
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("encyclopedia:index"))
        
        else:
            return render(request,"encyclopedia/create_page.html",{
                "form": form
            })
    return render(request, "encyclopedia/create_page.html",{
        "form": CreatForm()
    } )


def random_page(request):
    """
    Picks a random article from the encyclopedia and shows it to the user.
    """
    entries = util.list_entries()
    title = random.choice(entries)
    return render(request,"encyclopedia/visit_entry.html",{
        "entry": util.get_entry(title),
        "title": title
    })


def search_page(request):
    """
    - If the user write the correct name of the article in the search form, he will
        be taken to the content of this article.
    - Otherwise, a list of all the entries' name that match the query string will
        be shown.  
    """
    if request.method ==  "GET":
        page = request.GET.get('q')
        entries = util.list_entries()
        entries_set=set(entries)

        if page in entries_set:
            return render(request, "encyclopedia/visit_entry.html",{
                "entry": util.get_entry(page),
                "title": page
            })
        
        else:
            results = list(filter(lambda x: page in x, entries))
            return render(request, "encyclopedia/search_page.html",{
                "results": results
            })

        

def edit(request, pageName):
    """
    Shows a form that allows the user to edit the content of selected article.
    """
    
    if request.method == "POST":
        form = EditForm(request.POST)
    
        if form.is_valid():    
            content = form.cleaned_data["content"]
            title = form.cleaned_data["title"]
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:visit_entry", args=(title, )))
                    
        else:

            form = EditForm({'title': pageName, 'content': util.get_entry(pageName) })
            return render(request, "encyclopedia/edit_page.html", {
                "form": EditForm(),
                "pageName": pageName
            })
    
    
    return render(request, "encyclopedia/edit_page.html", {
        "form":  EditForm({'title': pageName, 'content': util.get_entry(pageName) }),
        "pageName": pageName
    })

def about(request):
    """
    Shows information about the project.
    """
    return render(request,"encyclopedia/about.html")
