from django import forms
from .models import Image
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        try:
            extension = url.rsplit('.', 1)[1].lower()
            # Remove any query parameters from extension
            extension = extension.split('?')[0]
        except IndexError:
            raise forms.ValidationError(
                'The given URL does not have a valid image extension.'
            )
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not match valid image extension.'
            )
        return url
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        try:
            extension = image_url.rsplit('.', 1)[1].lower()
            extension = extension.split('?')[0]
        except IndexError:
            extension = 'jpg'
        image_name = f'{name}.{extension}'
        # download image from the given URL
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image.image.save(
                image_name,
                ContentFile(response.content),
                save=False
            )
        except requests.RequestException as e:
            raise forms.ValidationError(
                f'Could not download image from URL: {str(e)}'
            )
        if commit:
            image.save()
        return image