import re
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                 DetailView,
                                 CreateView,
                                 UpdateView,
                                 DeleteView)
                                
# Create your views here.

def Home(request):

    context = {
        
        'posts': Post.objects.all()
        
            }

    return render(request,'blog/home.html',context)

class PostListView(ListView):

    model = Post 
    template_name = 'blog/home.html'  #app/model_viewtype.html  -- normal convention
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3
    
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

        ##get_object_or_404 is used if in case user does not exist it will return 404

class PostDetailView(DetailView):

    model = Post 
    #app/model_viewtype.html  -- normal convention

class PostCreateView(LoginRequiredMixin,CreateView):

    model = Post 
    fields = ['title','content'] 
  
    ''' This is created because if someobody 
        directly create post without logging 
        then it will be an issue as it cannot be without author.'''

    def form_valid(self, form) :

        form.instance.author = self.request.user 
        
        ''' the form you try to submit, before doing that, take that
        instance and set the author to current logged in user'''
        
        return super().form_valid(form)

    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    model = Post 
    fields = ['title','content'] 

    def form_valid(self, form) :

        form.instance.author = self.request.user 
        
        return super().form_valid(form)

    ## User should pass some certain test conditions
    def test_func(self) :
        
        post = self.get_object() ## Current Post 

        if self.request.user == post.author :

            return True
        
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):

    model = Post 
    success_url =  '/'

    ## User should pass some certain test conditions
    def test_func(self) :
        
        post = self.get_object() ## Current Post 

        if self.request.user == post.author :

            return True
        
        return False
    

def About(request):

    return render(request,'blog/about.html',{'title':'Django-About'})