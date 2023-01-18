from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
import random
from haskyApp.models import Question, Answer, Tag, Profile, Like

random.seed()

class Command(BaseCommand):
    help = 'Initialize database by random values'

    def create_profiles(self):
        users = [User(username=f"User {i}", password=random.randint(1000, 10000), email=f"email{i}@vk.ru") for i in range(3, 20)]
        User.objects.bulk_create(users)
        users1 = User.objects.all()
        profiles = [Profile(user = users1[i]) for i in range(20)]
        Profile.objects.bulk_create(profiles)

    def create_tags(self):
        tags = [Tag(name = f"Tag{i}") for i in range(4, 10)]
        Tag.objects.bulk_create(tags)
    
    def create_questions(self):
        profiles = Profile.objects.all()
        qbody = "some description " * 30
        questions = [Question(head=f"Question number {i}", body = qbody, author = random.choice(profiles)) for i in range(3, 20)]
        Question.objects.bulk_create(questions)

    def create_tags_to_questions(self):
        tags_ids = list(Tag.objects.values_list('id', flat=True))
        questions_ids = Question.objects.values_list('id', flat=True)
        tags_questions_rels = []
        for question_id in questions_ids:
            tag_1_id = random.choice(tags_ids)
            tag_2_id = random.choice(tags_ids)
            while tag_2_id == tag_1_id:
                tag_2_id = random.choice(tags_ids)
            tags_questions_rels.append(Question.tags.through(tag_id=tag_1_id, question_id=question_id))
            tags_questions_rels.append(Question.tags.through(tag_id=tag_2_id, question_id=question_id))
        Question.tags.through.objects.bulk_create(tags_questions_rels)

    def create_answers(self):
        profiles = Profile.objects.all()
        questions = Question.objects.all()
        abody = "a witty answer " * 30
        answers = [Answer(question = random.choice(questions), body = f"Answer {i} " + abody, author = random.choice(profiles)) for i in range(2, 120)]
        Answer.objects.bulk_create(answers)

    def create_qlikes(self):
        profiles = Profile.objects.all()
        questions_ids = Question.objects.values_list('id', flat=True)
        qtype = ContentType.objects.get_for_model(Question)
        qlikes = [Like(content_type = qtype, vote = 1, user = random.choice(profiles), object_id = random.choice(questions_ids)) for i in range(50)]
        Like.objects.bulk_create(qlikes)

    def create_alikes(self):
        profiles = Profile.objects.all()
        answers_ids = Answer.objects.values_list('id', flat=True)
        atype = ContentType.objects.get_for_model(Answer)
        alikes = [Like(content_type = atype, vote = 1, user = random.choice(profiles), object_id = random.choice(answers_ids)) for i in range(300)]
        Like.objects.bulk_create(alikes)

    def handle(self, *args, **options): 
        self.create_profiles()
        #self.create_tags()
        #self.create_questions()
        #self.create_tags_to_questions()
        #self.create_answers()
        #elf.create_qlikes()
        #self.create_alikes()
        