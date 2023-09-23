from django.views.generic import ListView
from .forms import CommentForm
from .models import Comment

from .utils import Utils


# class MainPageView(FormView, ListView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'comments/main_page.html'
#     success_url = reverse_lazy('home')
#     context_object_name = 'comments'
#     ordering = ['-created_at']
#     paginate_by = 25
#
#     def form_valid(self, form):
#         # Was a POST request sent?
#         if self.request.method == 'POST':
#             if not form.is_valid():
#                 return self.form_invalid(form)
#
#         # Get or create user
#         user, created = User.objects.get_or_create(
#             username=form.cleaned_data['username'],
#             email=form.cleaned_data['email']
#         )
#         if created:
#             user.set_unusable_password()
#             user.save()
#
#         # Creating of the comment with the related user
#         parent_comment_id = self.request.POST.get('parent_comment')
#         if parent_comment_id is not None:
#             parent_comment = Comment.objects.get(pk=parent_comment_id)
#
#             # Creating of the comment with the related user and parent comment
#             comment = form.save(commit=False)
#             comment.user = user
#             comment.parent_comment = parent_comment
#         else:
#             comment = form.save(commit=False)
#             comment.user = user
#
#         comment.save()
#
#         return super().form_valid(form)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Комментарии'
#         # print(self.request.POST)
#         if self.request.POST:
#             context['form'] = self.form_class(self.request.POST)
#         else:
#             context['form'] = self.form_class()
#
#         context['comments'] = Comment.objects.filter(parent_comment=None).order_by('-created_at')
#
#         return context

class MainPageView(ListView):
    model = Comment
    template_name = 'comments/main_page_copy.html'
    context_object_name = 'comments'
    ordering = ['-created_at']
    paginate_by = 25

    def get_queryset(self):
        return Comment.objects.filter(parent_comment=None).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Комментарии'
        context['form'] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            utils = Utils()
            utils.comment_process(form, request)
            # user, created = User.objects.get_or_create(
            #     username=form.cleaned_data['username'],
            #     email=form.cleaned_data['email']
            # )
            # if created:
            #     user.set_unusable_password()
            #     user.save()
            #
            # parent_comment_id = request.POST.get('parent_comment')
            # if parent_comment_id is not None:
            #     parent_comment = Comment.objects.get(pk=parent_comment_id)
            #     comment = form.save(commit=False)
            #     comment.user = user
            #     comment.parent_comment = parent_comment
            #     comment.save()
            # else:
            #     form.instance.user = user
            #     comment = form.save()
            #
            # attachment = request.FILES.get('attachment')
            # if attachment:
            #     if attachment.content_type.startswith('image'):
            #         self.process_image(attachment, comment)
            #     elif attachment.content_type == 'text/plain':
            #         self.process_text_file(attachment, comment, form)

            return self.get(request, *args, **kwargs)

        else:
            return self.get(request, *args, **kwargs)

    # def process_image(self, uploaded_image, comm):
    #     with Image.open(uploaded_image) as img:
    #         # Size change to 320x240
    #         img.thumbnail((320, 240))
    #
    #         # Save image
    #         img_io = BytesIO()
    #         img.save(img_io, format='JPEG')
    #
    #         # Create object CommentImage
    #         comment_image = CommentImage(
    #             comment=comm,
    #             image_path=ContentFile(img_io.getvalue(), name=uploaded_image.name),
    #             image_width=img.width,
    #             image_height=img.height
    #         )
    #         comment_image.save()
    #
    # def process_text_file(self, uploaded_file, comm, form):
    #     if uploaded_file.size > 100 * 1024:
    #         raise form.ValidationError('Файл слишком большой.')
    #     if not uploaded_file.name.endswith('.txt'):
    #         raise form.ValidationError('Недопустимый формат файла.')
    #     uploaded_file = UploadedFile.objects.create(
    #         file_path=uploaded_file,
    #         file_type='text',
    #         comment=comm
    #     )
