#from typing_extensions import Required
#try:
#      from typing_extensions import Required
#except ImportError:
#      from typing import Generic, TypeVar
#
#      T = TypeVar("T")
#
#      class Required(Generic[T]):
#           pass


from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
#from django.db.models.fields import
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum, Count
import random


from django.db.models.deletion import CASCADE

# Create your models here.

class QuestionManager(models.Manager):
        
    def top(self):
        return self.annotate(rating = Sum('votes__vote')).order_by('-rating')

    def new(self):
        return self.order_by('-pub_date')

    def tag(self, pk):
        #self.annotate(tag = ('tags'))
        t = Tag.objects.get(id = pk)
        return t.questions.annotate(rating = Sum('votes__vote')).order_by('-rating')


    #def make_many(self):
    #    str = "some description " * 20
    #    
    #    return [Question(head = f"Question number {i+1}", body = str, author = u, likes = f"{random.randint(1, 9)}" ) for i in range(100)]


class Question(models.Model):
    tags = models.ManyToManyField('Tag', related_name='questions')
    head = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey('Profile', models.CASCADE, related_name='questions')
    pub_date = models.DateTimeField(auto_now_add=True)
    #likes = models.IntegerField(default=0)
    votes = GenericRelation('Like', related_query_name='questions')
    #num_votes = models.IntegerField(default=0)
    


    objects = QuestionManager()

    def get_tags(self):
        return list(self.tags.all())


    def get_ans(self):
        return self.answers.all()

    def get_likes(self):
        return self.votes.sum_likes()

    def __str__(self):
        return self.head

    
class AnswerManager(models.Manager):

    def top(self, pk):
        return self.filter(question_id = pk).annotate(rating = Sum('votes__vote')).order_by('-correct').order_by('-rating')


class Answer(models.Model):
    question = models.ForeignKey(Question, models.CASCADE, related_name='answers')
    body = models.TextField()
    author = models.ForeignKey('Profile', models.CASCADE, related_name='answers')
    correct = models.BooleanField(default=False)
    #likes = models.IntegerField(default=0) #лайки вынести в отдельную модель!!
    pub_date = models.DateTimeField(auto_now_add=True)
    votes = GenericRelation('Like', related_name='answers')


    objects = AnswerManager()

    def get_likes(self):
        return self.votes.sum_likes()

    def __str__(self):
        return (self.body[:32] + '...')

class TagManager(models.Manager):
    def top_tags(self):
        return self.annotate(raiting = Count('questions')).order_by('-raiting')[:5]

class Tag(models.Model):
    name = models.CharField(max_length=20)

    objects = TagManager()

    def __str__(self):
        return self.name  

#class ProfileManager(models.Manager):
 #   def me(self):
  #      return self.filter(self.user.username() = "no_mercy")
class ProfileManager(models.Manager):
    def top(self):
        return self.annotate(raiting = Count('questions')).order_by('-raiting')[:5]


class Profile(models.Model):
    avatar = models.ImageField(blank = True, upload_to = "DBimages/")
    user = models.OneToOneField(User, models.CASCADE)

    objects = ProfileManager()
    
    def __str__(self):
        return self.user.username

class LikeManager(models.Manager):
    use_for_related_fields = True
    def sum_likes(self):
        res = self.filter(vote__gt = 0).aggregate(Sum('vote')).get('vote__sum')
        if not res:
            res = 0
        return res

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum')

class Like(models.Model):
    LIKE = 1
    NOTH = 0
    DISLIKE = -1
 
    VOTES = (
        (LIKE, 'Like'),
        (NOTH, 'Nothing'),
        (DISLIKE, 'Dislike')
    )
 
    vote = models.SmallIntegerField(choices=VOTES, default=NOTH)
    user = models.ForeignKey(Profile, models.CASCADE, related_name=('likes'))
 
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
 
    objects = LikeManager()