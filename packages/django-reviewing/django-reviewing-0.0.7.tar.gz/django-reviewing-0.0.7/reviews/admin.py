from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'score', )
    list_filter = ('score', )


class ReviewTabularInlineAdmin(GenericTabularInline):
    model = Review
    extra = 1


class ReviewStackedInlineAdmin(GenericStackedInline):
    model = Review
    extra = 1
