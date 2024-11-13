from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
import random
from django.db import transaction

fake = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения данных')

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        self.stdout.write(self.style.SUCCESS(f'Начало заполнения базы с коэффициентом: {ratio}'))
        self.create_users(ratio)
        tags = self.create_tags(ratio)
        questions = self.create_questions(ratio, tags)
        self.create_answers(ratio, questions)
        self.create_likes(ratio, questions)
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))

    def create_users(self, ratio):
        users = []
        profiles = []
        fake.unique.clear()

        for _ in range(ratio):
            username = fake.unique.user_name()
            email = fake.unique.email()
            user = User(username=username, email=email)
            users.append(user)

        User.objects.bulk_create(users)

        new_users = User.objects.order_by('-id')[:ratio]
        for user in new_users:
            if not Profile.objects.filter(user=user).exists():
                profile = Profile(user=user, avatar=None)
                profiles.append(profile)

        Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS(f'Создано пользователей: {len(profiles)}'))

    def create_tags(self, ratio):
        tags = set()

        while len(tags) < ratio:
            name = f"{fake.word()}_{len(tags)}"
            tags.add(name)

        tag_objects = [Tag(name=name) for name in tags]
        Tag.objects.bulk_create(tag_objects)
        self.stdout.write(self.style.SUCCESS(f'Создано тегов: {len(tag_objects)}'))
        return list(Tag.objects.all())

    def create_questions(self, ratio, tags):
        profiles = list(Profile.objects.all())
        questions = []
        for _ in range(ratio * 10):
            profile = random.choice(profiles)
            question = Question(
                user=profile,
                title=fake.sentence(),
                text=fake.paragraph(),
                image=None
            )
            questions.append(question)

        Question.objects.bulk_create(questions)
        questions = list(Question.objects.all())

        for question in questions:
            question.tags.add(*random.sample(tags, min(5, len(tags))))

        self.stdout.write(self.style.SUCCESS(f'Создано вопросов: {ratio * 10}'))
        return questions

    def create_answers(self, ratio, questions):
        profiles = list(Profile.objects.all())
        answers = []

        for question in questions:
            has_correct_answer = False

            for _ in range(ratio):
                profile = random.choice(profiles)

                if not has_correct_answer and random.random() < 0.7:
                    correct = True
                    has_correct_answer = True
                else:
                    correct = False

                answer = Answer(
                    question=question,
                    user=profile,
                    text=fake.paragraph(),
                    correct=correct
                )
                answers.append(answer)

        Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS(f'Создано ответов: {len(answers)}'))

    def create_likes(self, ratio, questions):
        profiles = list(Profile.objects.all())
        question_likes = []
        answer_likes = []

        for _ in range(ratio * 200):
            profile = random.choice(profiles)
            question = random.choice(questions)
            question_like = QuestionLike(
                user=profile,
                question=question
            )
            question_likes.append(question_like)

        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)

        answers = list(Answer.objects.all())
        for _ in range(ratio * 200):
            profile = random.choice(profiles)
            answer = random.choice(answers)
            answer_like = AnswerLike(
                user=profile,
                answer=answer
            )
            answer_likes.append(answer_like)

        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Создано лайков: {ratio * 200}'))