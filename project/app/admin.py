from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Prompt

# Register your models here.


# Unregister Groups
admin.site.unregister(Group)

# Put profile info into user info
class ProfileInline(admin.StackedInline):
	model = Profile

# Extend User Model
class UserAdmin(admin.ModelAdmin):
	model = User

	# Just display username fields on admin page
	fields = ["username"]
	inlines = [ProfileInline]

# unregister initial user
admin.site.unregister(User)
# reregister user and profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

admin.site.register(Prompt)

# admin.site.register(OutputImage)







