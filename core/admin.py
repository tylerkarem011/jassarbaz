# core/admin.py
from django.contrib import admin
from .models import (
    ClubMember, Skill, Achievement, 
    Event, GalleryImage, Video, Certificate, Training, News
)
from django.utils.html import format_html


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_id', 'group', 'join_date', 'is_active', 'get_photo', 'score')
    list_filter = ('group', 'is_active', 'join_date')
    search_fields = ('full_name', 'student_id')
    readonly_fields = ('get_photo_preview',)
    list_editable = ['score']

    def get_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;"/>', obj.photo.url)
        return "Нет фото"
    get_photo.short_description = "Фото"

    def get_photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="200"/>', obj.photo.url)
        return "Нет фото"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('member', 'skill_type', 'name', 'level', 'last_updated')
    list_filter = ('skill_type',)
    search_fields = ('member__full_name', 'name')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'member', 'date']
    list_filter = ['date']
    search_fields = ['title', 'member__full_name']
    autocomplete_fields = ['member']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'status']   # теперь всё есть
    list_filter = ['status', 'date']
    search_fields = ['title', 'location']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return format_html('<img src="{}" width="150"/>', obj.image.url)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('member', 'title', 'issue_date')
    list_filter = ('issue_date',)


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'status', 'instructor', 'location']
    list_filter = ['status', 'date']
    search_fields = ['title', 'instructor']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'date', 'is_published']
    list_filter = ['category', 'is_published', 'date']
    search_fields = ['title', 'content']
    list_editable = ['is_published']    