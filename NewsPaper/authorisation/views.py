from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class IndexView(LoginRequiredMixin, TemplateView):                  # authorisation main view class
    template_name = 'authorisation/default.html'

    def get_context_data(self, **kwargs):                           # modify context to know if in authors group
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):                                            # resposible for adding people to authors group
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():     # if not in authors then add otherwise skip
        author_group.user_set.add(user)
    return redirect('/')
