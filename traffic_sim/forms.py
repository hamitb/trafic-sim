from django import forms

from .models import Post

class Map(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('Map_id',)
