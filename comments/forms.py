from html.parser import HTMLParser

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import bleach
from django import forms
from .models import Comment, HTMLTag
from django.core.validators import RegexValidator
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()
    attachment = forms.FileField(required=False)

    # username field validation
    username = forms.CharField(validators=[
        RegexValidator(r'^[a-zA-Z0-9]*$', message='Поле должно содержать только цифры и латинские буквы')])

    def validate_xhtml(self, text):
        class MyHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.open_tags = []

            def handle_starttag(self, tag, attrs):
                self.open_tags.append(tag)

            def handle_endtag(self, tag):
                if self.open_tags:
                    self.open_tags.pop()

        parser = MyHTMLParser()
        parser.feed(text)

        if parser.open_tags:
            raise ValidationError('Неверное закрытие тегов.')

        return text

    def clean_text(self):
        text = self.cleaned_data.get('text')
        allowed_tags = HTMLTag.objects.values_list('tag_name', flat=True)
        cleaned_text = bleach.clean(text, tags=allowed_tags, strip=True)

        if text != cleaned_text:
            raise forms.ValidationError('Использованы недопустимые теги.')

        self.validate_xhtml(cleaned_text)

        return cleaned_text

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')

        return username

    class Meta:
        model = Comment
        fields = ['username', 'email', 'home_page', 'text', 'attachment', 'captcha', ]
