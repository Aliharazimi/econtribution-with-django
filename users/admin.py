from django.contrib import admin
from .models import Contribution, Contributor, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user')

admin.site.register(Profile)

class ContAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)} 


admin.site.register(Contributor)
admin.site.register(Contribution, ContAdmin)