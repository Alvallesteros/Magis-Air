from django.contrib import admin
from .models import CrewMember

@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ('crew_member_id', 'last_name', 'first_name', 'middle_initial')
    search_fields = ('last_name', 'first_name')
