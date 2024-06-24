from django import forms
from core.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    # names model vale use krne
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model=ProductReview
        fields = ['review', 'rating']