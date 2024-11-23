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
        self.stdout.write(self.style.SUCCESS(f'Создание пользователей'))
        profiles = self.create_users(ratio)
        self.stdout.write(self.style.SUCCESS(f'Создание тегов'))
        tags = self.create_tags(ratio)
        self.stdout.write(self.style.SUCCESS(f'Создание вопросов'))
        questions = self.create_questions(ratio, tags, profiles)
        self.stdout.write(self.style.SUCCESS(f'Создание ответов'))
        self.create_answers(ratio, questions, profiles)
        self.stdout.write(self.style.SUCCESS(f'Создание лайков'))
        self.create_likes(ratio, questions, profiles)
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))


    def create_users(self, ratio):
        users = []
        profiles = []
        fake.unique.clear()

        for i in range(ratio):
            username = fake.unique.user_name()
            email = fake.unique.email()
	
            if User.objects.filter(username=username).exists():
                continue

            user = User(username=username, email=email)
            users.append(user)

        User.objects.bulk_create(users)

        new_users = User.objects.order_by('-id')
        for user in new_users:
            # self.stdout.write(self.style.SUCCESS(f'\rНомер пользователя: {len(profiles)}'))
            if not Profile.objects.filter(user=user).exists():
                profile = Profile(user=user, avatar=None)
                profiles.append(profile)

        Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS(f'Создано пользователей: {len(profiles)}'))
        return profiles

    def create_tags(self, ratio):
        tags = set()

        while len(tags) < (ratio + 1):
            # self.stdout.write(self.style.SUCCESS(f'\rНомер тега: {len(tags)}'))
            name = f"{fake.word()}_{random.randint(0, 100)}"
            tags.add(name)

        tag_objects = [Tag(name=name) for name in tags]
        Tag.objects.bulk_create(tag_objects)
        self.stdout.write(self.style.SUCCESS(f'Создано тегов: {len(tag_objects)}'))
        return list(Tag.objects.all())

    def create_questions(self, ratio, tags, users):
        profiles = users
        questions = []
        title_pool = [fake.sentence() for i in range(1000)]
        text_pool = [fake.text() for i in range(1000)]
        for profile in profiles:
            for i in range(10):
                # self.stdout.write(self.style.SUCCESS(f'\rНомер вопроса: {len(questions)}'))
                question = Question(
                    user=profile,
                    title=random.choice(title_pool),
                    text=random.choice(text_pool),
                )
                questions.append(question)

        Question.objects.bulk_create(questions)
        questions = list(Question.objects.all())

        count = 1
        num_tags = len(tags)
        for question in questions:
            # self.stdout.write(self.style.SUCCESS(f'\rНомер тега вопроса: {count}'))
            question.tags.add(*random.sample(tags, min(num_tags, random.randint(5, 10))))
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Создано вопросов: {ratio * 10}'))
        return questions

    def create_answers(self, ratio, questions, users):
        profiles = users
        answers = []
        text_pool = [fake.text() for i in range(1000)]
        count = 0

        for question in questions:
            has_correct_answer = False
            for i in range(10):
                # self.stdout.write(self.style.SUCCESS(f'\rНомер ответа: {count}'))
                profile = random.choice(profiles)
                correct = random.random() < 0.1 and not has_correct_answer
                has_correct_answer = has_correct_answer or correct
                question.answers_count += 1
                question.save(update_fields=['answers_count'])
                answer = Answer(
                    question=question,
                    user=profile,
                    text=random.choice(text_pool),
                    correct=correct
                )
                answers.append(answer)
                count += 1

            if len(answers) >= 10000:
                Answer.objects.bulk_create(answers)
                answers.clear()

        if answers:
            Answer.objects.bulk_create(answers)

        self.stdout.write(self.style.SUCCESS(f'Создано ответов: {count}'))

    def create_likes(self, ratio, questions, users):
        profiles = users
        question_likes = []
        answer_likes = []

        for i in range(ratio * 200):
            # self.stdout.write(self.style.SUCCESS(f'\rНомер лайка вопроса: {i}'))
            profile = random.choice(profiles)
            question = random.choice(questions)
            question.likes_count += 1
            question.save(update_fields=['likes_count'])
            question_like =QuestionLike(
                user=profile,
                question=question
            )
            question_likes.append(question_like)

        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)

        answers = list(Answer.objects.all())
        for i in range(ratio * 200):
            # self.stdout.write(self.style.SUCCESS(f'\rНомер лайка ответа: {i}'))
            profile = random.choice(profiles)
            answer = random.choice(answers)
            answer.likes_count += 1
            answer.save(update_fields=['likes_count'])
            answer_like = AnswerLike(
                user=profile,
                answer=answer
            )
            answer_likes.append(answer_like)

        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Создано лайков: {ratio * 200}'))
