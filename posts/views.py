from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from .forms import PostForm, PictureForm
from django.urls import reverse_lazy, reverse
from cloudinary.forms import cl_init_js_callbacks
from .models import Post
from .forms import PostForm


def index(request):
    # If the method is POST
   
    if request.method == 'POST':
         form = PostForm(request.POST, request.FILES )
        # If the form is valid
         if form.is_valid():
            form.save() 

            #Yes, Save

            #Redirect to Home
            return HttpResponseRedirect('/')

         else:
            #No, Show Error
            return HttpResponseRedirect(form.errors.as_json())


    #Get all posts, limit = 20 
    posts = Post.objects.all().order_by('-created_at')[:20]

    #Show 
    return render(request, 'posts.html', 
                    {'posts': posts,})


def delete(request, post_id):
    #Find post 
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')

def edit(request, post_id):
    posts = Post.objects.get(id = post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=posts)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            return HttpResponse(form.errors.as_json())    

    form = PostForm

    return render (request, 'edit.html', {'post': posts, 'form': form})
    
def like(request, post_id):
    likedtweet = Post.objects.get(id = post_id)
    new_value=likedtweet.like_count +1
    likedtweet.like_count=new_value
    likedtweet.save()
    return HttpResponseRedirect('/')