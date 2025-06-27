from django.contrib import admin

from .models import Choice, Question

class ChoiceInLine(admin.StackedInLine):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # fields = ["pub_date", "question_text"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInLine]

admin.site.register(Question, QuestionAdmin)

# admin.site.register(Question, QuestionAdmin)