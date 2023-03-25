from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
	shared_body = models.TextField(blank=True, null=True)
	shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(default='Hola, estoy usando Infotec', max_length=100)
	image = models.ImageField(default='descarga.png')

	def __str__(self):
		return f'Perfil de {self.user.username}'

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user)\
									.values_list('to_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user)\
									.values_list('from_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

class Post(models.Model):
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

	
	def countLikes(self):
		return Like.objects.filter(user=self.user).count()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return self.content	


class Relationship(models.Model):
	from_user = models.ForeignKey(User, related_name='relationship', on_delete=models.CASCADE)
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)

def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		post_save.connect(create_profile, sender=User)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content}"