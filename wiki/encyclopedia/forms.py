from django import forms


class CreatForm(forms.Form):
    """
    This form allows the user to create a new article in the wiki.    
    """ 
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)
  
class EditForm(forms.Form):
    """
    This form allows the user to update an existing article. 
    The user can update the content of the article but not the title.
    """ 
    title = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    content = forms.CharField(widget=forms.Textarea)