
from django import forms

from posts.models import Post


class PostAdminForm(forms.ModelForm):
    tytle_ru = forms.CharField()
    text_ru = forms.Textarea()
    tytle_en = forms.CharField()
    text_en = forms.Textarea()
    tytle_ky = forms.CharField()
    text_ky = forms.Textarea()

    class Meta:
        model = Post
        fields = '__all__'

