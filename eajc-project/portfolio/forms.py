from django import forms

class ContactPortfolioForm(forms.Form):
    
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','name':'name','placeholder':'Noms *','required':True}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','email':'email','placeholder':'Email *','required':True}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','message':'message','placeholder':'Tapez votre message *', 'rows':5, 'required':True}))



