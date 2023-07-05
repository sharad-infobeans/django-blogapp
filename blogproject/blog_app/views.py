from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from blog_app.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponseRedirect,HttpResponse
from ckeditor.fields import RichTextField
from django.urls import reverse,reverse_lazy
from . import models
from .models import UserProfileInfo,BlogPosts
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse



# Create your views here.

class indexView(TemplateView):
    template_name = 'index.html'


class BlogListView(ListView):
    context_object_name = 'BlogPosts'
    model=models.BlogPosts    
    queryset = BlogPosts.objects.order_by('-blog_published_date')
    template_name = 'blog_app/blog_grid.html'
    #ordering = ['blog_published_date']
    paginate_by = 3

class BlogDetailView(DetailView):
    context_object_name = 'blog_details'
    model=models.BlogPosts
    template_name = 'blog_app/blog_detail.html'

    def get_queryset(self):
        return super().get_queryset().order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        # Find the current blog index in the queryset
        current_index = list(queryset).index(context["object"])

        # Get the previous and next blogs based on the current index
        previous_blog = queryset[current_index - 1] if current_index > 0 else None
        next_blog = queryset[current_index + 1] if current_index < len(queryset) - 1 else None

        context["previous_blog"] = previous_blog
        context["next_blog"] = next_blog
        author_profile = self.object.blog_author.userprofileinfo  # Access UserProfileInfo model through userprofileinfo
        context['author_image'] = author_profile.profile_pic.url
        context['author_bio'] = author_profile.profile_bio
        context['author_profession'] = author_profile.profession

        current_author = self.object.blog_author

        # Retrieve related posts by the current author
        related_posts = models.BlogPosts.objects.filter(blog_author=current_author).exclude(id=self.object.id)

        context['related_posts'] = related_posts
        return context

class BlogCreateView(CreateView):
    fields = ('blog_title','blog_content','blog_image',)
    model = models.BlogPosts

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['blog_title'].widget.attrs['class'] = 'form-control'
        form.fields['blog_title'].label = 'Blog Title'
        form.fields['blog_title'].widget.attrs['placeholder'] = 'Enter the blog title'

        form.fields['blog_content'].widget.attrs['class'] = 'form-control'
        form.fields['blog_content'].label = 'Blog Content'
        form.fields['blog_content'].widget.attrs['placeholder'] = 'Enter the blog content'

        form.fields['blog_image'].widget.attrs['class'] = 'form-control'
        form.fields['blog_image'].label = 'Blog Image'
        form.fields['blog_image'].widget.attrs['placeholder'] = 'Choose a blog image'

        return form

    def form_valid(self, form):
        form.instance.blog_published_date = timezone.now()  # Set publish date as current date
        form.instance.blog_author = self.request.user  # Set the current user as the blog author
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    fields = ('blog_title','blog_content','blog_image',)
    model = models.BlogPosts

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['blog_title'].widget.attrs['class'] = 'form-control'
        form.fields['blog_title'].label = 'Blog Title'
        form.fields['blog_title'].widget.attrs['placeholder'] = 'Enter the blog title'

        form.fields['blog_content'].widget.attrs['class'] = 'form-control'
        form.fields['blog_content'].label = 'Blog Content'
        form.fields['blog_content'].widget.attrs['placeholder'] = 'Enter the blog content'

        form.fields['blog_image'].widget.attrs['class'] = 'form-control'
        form.fields['blog_image'].label = 'Blog Image'
        form.fields['blog_image'].widget.attrs['placeholder'] = 'Choose a blog image'

        return form

    def form_valid(self, form):
        form.instance.blog_published_date = timezone.now()  # Set publish date as current date
        form.instance.blog_author = self.request.user  # Set the current user as the blog author
        return super().form_valid(form)

class BlogDeleteView(View):
    model = models.BlogPosts
    def post(self, request, *args, **kwargs):
        blog_id = kwargs['pk']
        try:
            blog_post = self.model.objects.get(id=blog_id)
            blog_post.delete()
            return JsonResponse({'success': True})
        except self.model.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog post does not exist.'})


class UserProfileView(TemplateView):
    template_name = 'userprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfileInfo.objects.get(user=self.request.user)
        context['user_profile'] = user_profile
        return context

@login_required
def special(request):
    return HttpResponse("You are logged in ")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog_app:blogs'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True
            #return redirect("blog_app:login")
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('blog_app:blogs'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('Someone tried to login')
            print(f'login username: {username} and password: {password}')
            messages.error(request, 'Invalid login credentials. Please try again.')
            return redirect('blog_app:login')
    else:
        return render(request,'login.html',{})
