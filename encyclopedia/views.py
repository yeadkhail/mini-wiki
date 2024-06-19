from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown
from django.utils.safestring import mark_safe
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random

class Searchform(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class Createnewform(forms.Form):
    newtitle = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}),label="Title:")
    newcontent = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter the markdown content','rows':8,'cols':80}),label="Content:")

class Editentryform(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), label="Title:")
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'cols': 80}), label="Content:")

def index(request):
    if request.method == "POST":
        form = Searchform(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            queryr = form.cleaned_data["query"]
            content = util.get_entry(queryr.lower())
            if content is not None:
                return HttpResponseRedirect(reverse("title", args=[queryr.lower()]))

            else:
                all_entries = util.list_entries()
                entries = [entry for entry in all_entries if queryr.lower() in entry.lower()]
                if len(entries) == 0:
                    print(len(entries))
                    entries.append("Sorry,No matches found")
                return render(request,"encyclopedia/index.html",{
                    "entries":entries,"form":Searchform()
                })
        else:
            print(len(entries))
            return render(request,"encyclopedia/index.html",{
                    "entries":entries,"form":Searchform()
                })



    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "form": Searchform()
    })

def title(request,name):
    content = util.get_entry(name.lower())
    if content is not None:
        content = markdown.markdown(content)
        content = mark_safe(content)
    else:
        content = "Sorry, the content doesn't exists"

    return render(request,"encyclopedia/title.html",{
        "name":name, "content": content,"form": Searchform()
    })


def new(request):
    if request.method == "POST":
        form = Createnewform(request.POST)
        if form.is_valid():
            newtitle = form.cleaned_data["newtitle"]
            newcontent = form.cleaned_data["newcontent"]
            content = util.get_entry(newtitle.lower())
            if content is not None:
                valid = False
                return render(request,"encyclopedia/new.html",{
                    "form2": form , "valid":valid,
                })
            else:
                valid = True
                util.save_entry(newtitle,newcontent)
                return HttpResponseRedirect(reverse("title", args=[newtitle.lower()]))
    else:
        return render(request,"encyclopedia/new.html",{
            "form":Searchform(), "form2":Createnewform(), "valid":True,
        })
    

def edit(request,name):
    if request.method == "POST":
        form3 = Editentryform(request.POST)
        if form3.is_valid():
            title = form3.cleaned_data["title"]
            content = form3.cleaned_data["content"]
            util.save_entry(title.lower(),content)
            return HttpResponseRedirect(reverse("title",args=[title.lower()]))
    else:
            entry = util.get_entry(name.lower())
            form3 = Editentryform(initial={'title': name,"content":entry})
    return render(request,"encyclopedia/edit.html",{
        "form3":form3,"title":name
    })

def randcontent(request):
    entries = util.list_entries()
    length = len(entries)
    randnum = random.randint(0,length-1)
    return HttpResponseRedirect(reverse("title",args=[entries[randnum].lower()]))
    
