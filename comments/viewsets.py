from django.views.generic import ListView
from .forms import CommentForm
from .models import Comment

from .utils import Utils


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

            return self.get(request, *args, **kwargs)

        else:
            return self.get(request, *args, **kwargs)
