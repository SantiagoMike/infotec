from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Post, Relationship, Like, Comment
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm, UserUpdateForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
#from django.contrib.comments.models import Comment



@login_required
def home(request): 
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {'posts':[], 'form' : form }
    return render(request, 'twitter/newsfeed.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            u = form.save()
            profile = Profile.objects.create(user=u)
            profile.save()
            u.save()
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {'form' : form}
    return render(request, 'twitter/register.html', context)

    context = {'form' : form}
    return render(request, 'twitter/register.html', context)

def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('home')

def profile(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all()
    context = {'user':user, 'posts':posts}
    return render(request, 'twitter/profile.html', context)

def editar(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('home')
    else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm()

    context = {'u_form' : u_form, 'p_form' : p_form}
    return render(request, 'twitter/editar.html', context)

def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    return redirect ('home')

def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id)
    rel.delete()
    return redirect ('home')

def posts(request):
    posts = Post.objects.all()
    _posts = []
    for p in posts:
        _posts.append({ 
            "id":         p.id,
            "img":        p.user.profile.image.url, 
            "userid":     p.user.id,
            "firstname":  p.user.first_name,
            "username":   p.user.username,
            "fecha":      p.timestamp,
            "contenido":  p.content,
            "esAutor":    (request.user == p.user),
            "like":       Like.objects.filter(user=request.user, post=p).count(),
            "likes":      Like.objects.filter(post=p).count(),
        })
    data = {"state": True, "posts": _posts}
    return JsonResponse(data)

def like(request, id):
    post = Post.objects.get(pk=id)
    n = Like.objects.filter(user=request.user, post=post).count()
    bl = True
    noLikes = 0
    if n==1 :
        Like.objects.filter(user=request.user, post=post).delete()
        bl = False
    else:
        Like.objects.create(user=request.user, post=post, timestamp=datetime.now()).save()
        bl = True
    noLikes = Like.objects.filter(post=post).count(),
    return JsonResponse({"state": True, "like": bl, "noLikes":noLikes})

def vista5(request):
    diccionario = {}
    return render(request, "twitter/imagen.html", context=diccionario)

def politicas(request):
    diccionario = {}
    return render(request, "twitter/politicas.html", context=diccionario)

def ayuda(request):
    diccionario = {}
    return render(request, "twitter/ayuda.html", context=diccionario)

def titulacion(request):
    return render(request, "administrativas/titulacion.html", {})

def residencias(request):
    return render(request, "administrativas/residencias.html", {})

def actcomplementarias(request):
    return render(request, "administrativas/actcomplementarias.html", {})

def servicios(request):
    return render(request, "administrativas/servicios.html", {})

def creditos(request):
    return render(request, "administrativas/creditos.html", {})

def diasfestivos(request):
    return render(request, "eventos/diasfestivos.html", {})

def aniversario(request):
    return render(request, "eventos/aniversario.html", {})

def conferencias(request):
    return render(request, "eventos/conferencias.html", {})

def eventosdep(request):
    return render(request, "eventos/eventosdep.html", {})

def convocatorias(request):
    return render(request, "noticias/convocatorias.html", {})

def comunicados(request):
    return render(request, "noticias/comunicados.html", {})

def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment = comment
            comment.user = request.user
            comment.save()
            return redirect('comment')
    else:
        form = CommentForm()

    context = {
        'form': form
    }
    return render(request, 'twitter/comment.html', context)

def ver_comentarios(request):
    comment = Comment.objects.all()
    comment = []
    for p in comment:
        _comment.append ({
            "username":   p.user.username,
            "contenido":  p.content,
            "fecha":      p.timestamp,
        })

    data = {"state": True, "comment": comment}
            
    return render(request, 'twitter/ver_comentarios.html', {'comment': comment})
