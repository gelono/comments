from django.contrib.auth.models import User
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField(blank=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class UploadedFile(models.Model):
    file_path = models.FileField(storage=S3Boto3Storage(), upload_to='uploaded_files/')
    file_type = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class CommentImage(models.Model):
    image_path = models.ImageField(storage=S3Boto3Storage(), upload_to='comment_images/')
    image_width = models.PositiveIntegerField()
    image_height = models.PositiveIntegerField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class HTMLTag(models.Model):
    tag_name = models.CharField(max_length=20)
