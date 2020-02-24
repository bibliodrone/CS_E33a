from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from . import util
from .forms import newPageForm
import re
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def randomPage(request):
    entry_list = util.list_entries()
    entry_len = len(entry_list)
    entry_rand = random.randint(1,entry_len)
    rand_entry = entry_list[entry_rand-1]
    
    return redirect("/wiki/" + rand_entry)

def entry(request, title):
    if request.method == "POST":
        form=newPageForm(request.POST)
        
        if form.is_valid():
            pageTitle=form.cleaned_data["title"]
            pageContent=form.cleaned_data["content"]
            util.save_entry(pageTitle, pageContent)
            return redirect("/wiki/"+ pageTitle)
    else:
        page_content=util.get_entry(title)
        if page_content:
            final_content=processContent(page_content)
            return render(request, "encyclopedia/entry.html", {
                "content":final_content,
                "title":title
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "title" : title, 
                "entries": util.list_entries()
            })

def newpage(request):
    form = newPageForm(initial={
        "title": "New Page", 
        "content": ""
        })
    return render(request, "encyclopedia/newpage.html",{
        "form":form,
        "title":"New Page",
        "content":" "
    })

def edit(request):
    title=request.GET['edit']
    content=util.get_entry(title)

    form = newPageForm({"title": title, "content":content})
    
    return render(request, "encyclopedia/edit.html", {
        "form":form,
        "title":title,
        "content":content
        })
        
def search(request):
    title=request.GET['search']
    
    try:
        content = util.get_entry(title)
        content = processContent(content)
        return render(request, "encyclopedia/entry.html", {
            "content":content,
            "title":title
        })
    
    except:
        results = util.list_entries()
        match_list = []
        l_title = title.lower()
        for r in results:
            rl = r.lower()
            if rl.startswith(l_title):
                match_list.append(r)

        return render(request, "encyclopedia/searchresults.html", {
            "title" : title,
            "match_list" : match_list
        })

def searchresults(request, title, match_list):
    return render(request, "encyclopedia/searchresults.html", {
        "title":title,
        "match_list":match_list
    })

# I don't know how well this approach would scale for large files...
def processContent(content):
    
    #paragraphs
    content = re.sub('(^[A-Za-z].+$)', r'<p>\1</p>', content, flags=re.MULTILINE)
    #headings
    content = re.sub('(##)(.+)',r'<h2>\2</h2>', content)
    content = re.sub('(#[^#])(.+)', r'<h1>\2</h1>', content) 
    #strong
    content = re.sub('(\*\*)([^*]+)(\*\*)', r'<strong>\2</strong>', content)
    #href
    content = re.sub('(\[)([^]]+)(\])(\()([^)]*)(\))', r'<a href="\5">\2</a>', content)
    #ul
    spl=content.splitlines()
    srange = len(spl)
        
    for line in range(srange):
        spl[line] = spl[line].strip()
        if spl[line].startswith("* "):
            spl[line] = "<li>" + spl[line].replace("* ", "") + "</li>"

    for line in range(srange):
        
        if spl[line].startswith("<li>"):
            if not(spl[line-1].startswith ("<li>")):
                if not(spl[line-1].startswith("<ul>")):
                    spl[line] = "<ul>" + spl[line]
            # If last line of file is list element, add closing </ul>
            if line == srange-1:
                spl[line] += "</ul>"
            elif not(spl[line+1].endswith("</li>")):
                if not(spl[line+1].endswith("</ul>")):
                    spl[line] = spl[line] + "</ul>"
    
    content = ("")
    for line in spl:
        content+=line
    
    return(content)
