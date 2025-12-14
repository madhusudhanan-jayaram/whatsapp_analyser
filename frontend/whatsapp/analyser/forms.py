from django import forms

class ChatUploadForm(forms.Form):
    chat_file = forms.FileField(label="Upload WhatsApp Chat (.txt)")