from django.contrib import admin

from tracker.models import Way


@admin.register(Way)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'spot', 'data_time', 'action', 'is_nice_way', 'periodicity', 'reward', 'associated_way', 'time_execution',
        'is_public', 'owner')
