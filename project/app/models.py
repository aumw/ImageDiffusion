from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.



# Create diffusion model
class Prompt(models.Model):
	user = models.ForeignKey(User, related_name="prompts", on_delete=models.DO_NOTHING)
	prompt = models.CharField(max_length=50)
	original_image = models.ImageField(null=True, blank=True, upload_to="images/")
	created_at = models.DateTimeField(auto_now_add=True)
	diffused_image = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return(f"{self.user} " 
			   f"({self.created_at:%Y-%m-%d-%H-%M}): " 
			   f"{self.prompt}...")


# class OutputImage(models.Model):
# 	prompt = models.OneToOneField(Prompt, on_delete=models.CASCADE)
# 	output_image = models.CharField(max_length=200)




class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	follows = models.ManyToManyField("self", 
		related_name="followed_by",
		symmetrical= False,
		blank=True)
	date_modified = models.DateTimeField(User, auto_now=True)

	def __str__(self):
		return self.user.username

def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()
		# have user follow themself
		user_profile.follows.set([instance.profile.id])
		user_profile.save()

post_save.connect(create_profile, sender=User)

