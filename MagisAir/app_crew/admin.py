from django.contrib import admin
from .models import CrewMember, CrewAssignment

@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ('crew_member_id', 'last_name', 'first_name', 'middle_initial')
    search_fields = ('last_name', 'first_name')

@admin.register(CrewAssignment)
class CrewAssignmentAdmin(admin.ModelAdmin):
    list_display = ('crew_id', 'scheduled_flight_id', 'crew_member_id', 'role')
    search_fields = ('crew_id', 'scheduled_flight_id__flight_id', 'crew_member_id__crew_member_id', 'role')

