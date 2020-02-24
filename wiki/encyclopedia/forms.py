from django import forms

class searchForm(forms.Form):
    search = forms.CharField(label="Page Search", max_length=128)

class newPageForm(forms.Form):
    title = forms.CharField(label="Page Title",initial="page", max_length=128)
    #title = forms.Textarea
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":20}))