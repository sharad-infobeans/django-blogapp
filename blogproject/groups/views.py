from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.urls import reverse,reverse_lazy
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views import generic
from . import models
from django.utils import timezone
# Create your views here.

class ListGroups(generic.ListView):
   model = models.Group
   template_name = 'group_list.html'

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    model = models.Group
    fields = ("name", "description","group_image")
    template_name = 'groups_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['name'].widget.attrs['class'] = 'form-control'
        form.fields['name'].label = 'Group Title'
        form.fields['name'].widget.attrs['placeholder'] = 'Enter the Group title'

        form.fields['description'].widget.attrs['class'] = 'form-control'
        form.fields['description'].label = 'Group Description'
        form.fields['description'].widget.attrs['placeholder'] = 'Enter the Group intro'

        form.fields['group_image'].widget.attrs['class'] = 'form-control'
        form.fields['group_image'].label = 'Group Image'
        form.fields['group_image'].widget.attrs['placeholder'] = 'Choose a Group image'

        return form

    def form_valid(self, form):
        form.instance.group_created_date = timezone.now()  # Set publish date as current date
        return super().form_valid(form)
    
class SingleGroup(generic.DetailView):
    context_object_name = 'group_details'
    model = models.Group
    template_name = 'group_detail.html'



class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not logged in, redirect to login page
            return redirect('blog_app:login')  # Replace 'account:login' with your actual login URL

        group = get_object_or_404(models.Group, slug=self.kwargs.get("slug"))

        try:
            models.GroupMember.objects.create(user=self.request.user, group=group)

        except IntegrityError:
            messages.warning(self.request, "Warning, already a member of {}".format(group.name))

        else:
            messages.success(self.request, "You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)