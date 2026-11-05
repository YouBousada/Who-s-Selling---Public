from django import forms
from login.models import Profile
from .models import Post, Category



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "location", "asking_price", "image", "category"]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Title of your item…",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 7,
                    "placeholder": "Describe the item, condition, and any pickup details…",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "e.g. Balz-Dobie, Alderman Library lobby",
                }
            ),
            "asking_price": forms.NumberInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "e.g. 20.00 (use 0 for FREE)",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-file",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

        labels = {
            "asking_price": "Price",
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image','nickname', 'phone_number', 'bio', 'sustainability_interests')
        widgets = {
            
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-file",
                }
            ),

            "nickname": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter nickname e.g. ILoveTrees03, leave blank to use your google username",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter phone number e.g. +1 555-123-4567",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 5,
                    "placeholder": "Write a short bio about yourself…",
                }
            ),
            "sustainability_interests": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "rows": 5,
                    "placeholder": "Optional: Share your sustainability interests…",
                }
            ),
        }
