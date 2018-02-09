# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 09:56:29 2018

@author: alexkreamas
"""

from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))
    
