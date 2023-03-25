from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='twitter/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('editar/', views.editar, name='editar'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),

    path('posts.json',       views.posts, name='posts'),
    path('like/<int:id>',    views.like, name='like'),
    path('ruta5', views.vista5, name='vista5'),
    path('politicas', views.politicas, name='politicas'),
    path('ayuda', views.ayuda, name='ayuda'),
    path('administrativas/titulacion', views.titulacion, name='titulacion'),
    path('administrativas/residencias', views.residencias, name='residencias'),
    path('administrativas/actcomplementarias', views.actcomplementarias, name='actcomplementarias'),
    path('administrativas/servicios', views.servicios, name='servicios'),
    path('administrativas/creditos', views.creditos, name='creditos'),
    path('eventos/diasfestivos', views.diasfestivos, name='diasfestivos'),
    path('eventos/aniversario', views.aniversario, name='aniversario'),
    path('eventos/conferencias', views.conferencias, name='conferencias'),
    path('eventos/eventosdep', views.eventosdep, name='eventosdep'),
    path('noticias/convocatorias', views.convocatorias, name='convocatorias'),
    path('noticias/comunicados', views.comunicados, name='comunicados'),
    path('comment', views.comment, name='comment'),
    path('comentarios/', views.ver_comentarios, name='ver_comentarios'),
  #  path('<slug:slug>/', views.comment, name='comment')
  






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)