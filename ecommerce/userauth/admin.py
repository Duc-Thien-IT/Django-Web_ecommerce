from django.contrib import admin
from userauth.models import User

class UserAdmin(admin.ModelAdmin):
    #model = User
    list_display = ('email', 'username', 'bio')
    #search_fields = ('email', 'username')
    #ordering = ('email',)

admin.site.register(User, UserAdmin)
