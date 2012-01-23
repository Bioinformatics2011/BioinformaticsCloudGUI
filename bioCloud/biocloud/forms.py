'''
Created on Jan 23, 2012
@author: m1
'''
from django import forms

class UploadForm(forms.Form):
    userFile = forms.FileField(
        label='Select a file',
    )
