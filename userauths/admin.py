from django.contrib import admin

# Register your models here.
from userauths.models import User, Profile # mandatory to register models(db) in admin; tabhi admin vale url te show hoyega eh model

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio'] # write name of cols u want to display in admin page

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'bio', 'phone']

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)

