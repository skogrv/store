from django import forms
from .models import Listing, Comment
from django_starfield import Stars



class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('main_image',)




class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(widget=Stars)
    class Meta:
        model = Comment
        fields = ('comment', 'rating')

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),

        }
