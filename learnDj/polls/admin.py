from django.contrib import admin

from .models import Question, Choice, Comment


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text", "user"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
        (None, {"fields": ["is_for_adults"]}),
        (None, {"fields": ["is_allowed"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "was_published_recently", "is_for_adults", "is_allowed"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'text', 'created_at')
    list_filter = ('created_at', 'question', 'user')
    search_fields = ('text',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fields = ('user', 'question', 'text', 'created_at')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment, CommentAdmin)
# Register your models here.
