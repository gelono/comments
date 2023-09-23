from PIL import Image
from django.contrib.auth.models import User
from .models import Comment, CommentImage, UploadedFile
from io import BytesIO
from django.core.files.base import ContentFile


class Utils:
    def comment_process(self, form, request):
        user, created = User.objects.get_or_create(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email']
        )
        if created:
            user.set_unusable_password()
            user.save()

        parent_comment_id = request.POST.get('parent_comment')
        if parent_comment_id is not None:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
            comment = form.save(commit=False)
            comment.user = user
            comment.parent_comment = parent_comment
            comment.save()
        else:
            form.instance.user = user
            comment = form.save()

        attachment = request.FILES.get('attachment')
        if attachment:
            if attachment.content_type.startswith('image'):
                self.process_image(attachment, comment)
            elif attachment.content_type == 'text/plain':
                self.process_text_file(attachment, comment, form)

    @staticmethod
    def process_image(uploaded_image, comm):
        with Image.open(uploaded_image) as img:
            # Size change to 320x240
            img.thumbnail((320, 240))

            # Save image
            img_io = BytesIO()
            img.save(img_io, format='JPEG')

            # Create object CommentImage
            comment_image = CommentImage(
                comment=comm,
                image_path=ContentFile(img_io.getvalue(), name=uploaded_image.name),
                image_width=img.width,
                image_height=img.height
            )
            comment_image.save()

    @staticmethod
    def process_text_file(uploaded_file, comm, form):
        if uploaded_file.size > 100 * 1024:
            raise form.ValidationError('Файл слишком большой.')
        if not uploaded_file.name.endswith('.txt'):
            raise form.ValidationError('Недопустимый формат файла.')
        UploadedFile.objects.create(
            file_path=uploaded_file,
            file_type='text',
            comment=comm
        )
