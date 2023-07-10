from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import forms
from . import models
from groups.models import GroupMember
from django.http import JsonResponse


from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allgroups = models.Group.objects.all()
        context["allgroups"] = allgroups
        return context

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['message'].widget.attrs['class'] = 'form-control'
        form.fields['message'].label = 'Post Message'
        form.fields['message'].widget.attrs['placeholder'] = 'Enter Your Message'

        form.fields['group'].widget.attrs['class'] = 'form-control'
        form.fields['group'].label = 'Select A Group'
        form.fields['group'].widget.attrs['placeholder'] = 'Choose a Group'
        form.fields['group'].empty_label = 'Choose a Group'

        return form

    def form_valid(self, form):
        group = form.cleaned_data['group']
        if not group.members.filter(id=self.request.user.id).exists():
            messages.error(self.request, "Sorry,You need to Join this group first")
            return self.form_invalid(form)

        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )



class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        joined_groups = GroupMember.objects.filter(user=self.post_user).select_related("group")
        context["joined_groups"] = joined_groups
        return context



class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.View):
    model = models.Post
    select_related = ("user", "group")
    def post(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        try:
            grp_post = self.model.objects.get(id=post_id)
            grp_post.delete()
            return JsonResponse({'success': True})
        except self.model.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog post does not exist.'})