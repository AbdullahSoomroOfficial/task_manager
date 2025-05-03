from django.contrib import admin
from .models import Task, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'due_date', 'completed')
    list_filter = ('completed', 'priority', 'category', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
