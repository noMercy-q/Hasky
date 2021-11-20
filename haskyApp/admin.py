from django.contrib import admin
from haskyApp.models import Question, Answer, Tag, Profile, Like

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Like)
