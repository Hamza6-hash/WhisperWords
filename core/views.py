from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, BlogPosts
from django.contrib.auth import login, logout, authenticate
from itertools import chain


# Create your views here.
def register(req):
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']

        if len(email.lstrip()) == 0 or len(username.lstrip()) == 0 or len(password.lstrip()) == 0:
            messages.info(req, "No empty fields are allowed")
        elif User.objects.filter(username=username).exists():
            messages.info(req, "Username exists")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(req, 'Email Taken')
            return redirect('register')
        elif username == password:
            messages.info(req, "User name and password cannot be the same")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password)
            user.save()

            user_login = authenticate(username=username, password=password)
            login(req, user_login)

            user_model = User.objects.get(username=username)
            new_profile = UserProfile.objects.create(
                user=user_model, user_id=user_model.id)
            new_profile.save()

            return redirect('settings')
    return render(req, 'register.html')


def login_user(req):
    if not req.user.is_authenticated:
        if req.method == 'POST':
            username = req.POST['username']
            password = req.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('home')
            elif not User.objects.filter(username=username).first():
                messages.info(req, "User doesn't exist")
            else:
                messages.info(req, "Invalid credentials")
    else:
        return redirect('home')
    return render(req, 'login.html')


def logout_user(req):
    logout(req)
    return redirect('login')


def settings(req):
    if req.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=req.user)
        if req.method == 'POST':
            bio = req.POST['bio']
            about = req.POST['about']
            if len(bio.lstrip()) and len(about.lstrip()) > 0:
                user_profile.bio = bio
                user_profile.aboutAuthor = about
                user_profile.save()
                return redirect(f'profile/{req.user.id}')
            else:
                messages.info(req, "Update both fields please")
                return redirect('settings')
    else:
        messages.info(req, "Login required!!")
        return redirect('login')
    return render(req, 'settings.html', {'user_profile': user_profile})


def update_profile(req):
    user_profile = UserProfile.objects.get(user=req.user)
    if req.user.is_authenticated:
        if req.method == 'POST':
            if req.FILES.get('image') != None:
                image = req.FILES.get('image')
                user_profile.image = image
                user_profile.save()
                return HttpResponseRedirect(f'profile/{req.user.id}')

            if req.FILES.get('image') == None:
                messages.info(req, 'Add pic please')
                return redirect('settings')


def home(req):
    posts = BlogPosts.objects.all()
    new_posts = sorted(posts, key=lambda obj: obj.createdAt, reverse=True)
    return render(req, "home.html", {'posts': new_posts})


def post(req):
    len_desc = 4500
    user_profile = UserProfile.objects.get(user=req.user.id)
    if req.method == 'POST':
        title = req.POST['title']
        description = req.POST['description']
        category = req.POST['category']
        post_img = req.FILES.get('post_img')
        if len(description.lstrip()) == 0 or len(title.lstrip()) == 0:
            messages.info(req, 'Add title and description!!')
        if post_img == None:
            messages.info(req, "Attach a file")
        else:
            new_post = BlogPosts.objects.create(
                user_profile=user_profile, description=description, title=title, category=category, post_img=post_img)
            new_post.save()

        return redirect('write')
    return render(req, "write.html", {"len_desc": len_desc})


def delete_post(req, pk):
    if req.user.is_authenticated:
        delete_it = BlogPosts.objects.get(id=pk)
        delete_it.delete()
        messages.info(req, "Post deleted successfully")
        return redirect('home')
    else:
        messages.info(req, "You must be logged in to delete your post")


def profile(req, pk):
    user_profile = UserProfile.objects.get(id=pk)
    user_posts = BlogPosts.objects.filter(
        user_profile=user_profile)
    # print(user_posts.count())
    context = {
        'user_posts': user_posts,
        'user_profile': user_profile
    }
    return render(req, 'profile.html', context)


# Search functionality for the future
'''
def search(req):
    user_object = User.objects.get(username=req.user.username)
    user_profile = UserProfile.objects.get(user=user_object)

    if req.method == 'POST':
        username = req.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            user_profile.append(users.id)

        for ids in username_profile:
            profile_lists = UserProfile.objects.filter(user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(req, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
'''


def full_post(req, pk):
    user_post = BlogPosts.objects.get(id=pk)
    return render(req, "fullPost.html", {'user_post': user_post})


def edit_post(req, pk):
    user_post = BlogPosts.objects.get(id=pk)
    if req.method == 'POST':
        description = req.POST['description']
        user_post.description = description
        user_post.save()
        messages.info(req, "Post updated successfully")
        return redirect('home')
    return render(req, 'edit.html', {'user_post': user_post})


def tech_view(req):
    tech_posts = BlogPosts.objects.filter(category="technology")
    new_tech_posts = sorted(
        tech_posts, key=lambda obj: obj.createdAt, reverse=True)
    for post in new_tech_posts:
        print(post.description)
    return render(req, "tech.html", {"tech_posts": new_tech_posts})


def art_view(req):
    art_posts = BlogPosts.objects.filter(category="art")
    new_art_posts = sorted(
        art_posts, key=lambda obj: obj.createdAt, reverse=True)
    return render(req, "art.html", {"art_posts": new_art_posts})


def sci_view(req):
    sci_posts = BlogPosts.objects.filter(category="science")
    new_sci_posts = sorted(
        sci_posts, key=lambda obj: obj.createdAt, reverse=True)
    return render(req, "science.html", {"sci_posts": new_sci_posts})
