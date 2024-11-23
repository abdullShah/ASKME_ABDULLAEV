from django.core.management.base import BaseCommand
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike

class Command(BaseCommand):
    help = "Удалить все записи из таблиц Profile, Question, Answer, Tag, QuestionLike, и AnswerLike"

    def handle(self, *args, **options):
        Profile.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Tag.objects.all().delete()
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Все записи успешно удалены из таблиц Profile, Question, Answer, Tag, QuestionLike, и AnswerLike"))
