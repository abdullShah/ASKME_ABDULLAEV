from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from app.models import Question, Answer, Tag, Profile
from django.db.models import Count
# from django.http import Http404

CNT_QUESTS_ON_PAGE = 4
CNT_ANSWERS_ON_PAGE = 2

def paginate(obj_list, req, per_page=4):
	paginator = Paginator(obj_list, per_page)
	page_number = req.GET.get('page', 1)

	try:
		page_number = int(page_number)
	except ValueError:
		return None, None

	try:
		page = paginator.page(page_number)
		return page, page_number
	except (EmptyPage, PageNotAnInteger):
		return None, None


def index(request):
	questions = Question.objects.new()
	if questions.count() == 0:
		return render(request, 'app/empty.html', {'popular_tags': Tag.objects.popular().values_list('name', flat=True)})

	paginated_questions, cur_page = paginate(questions, request, CNT_QUESTS_ON_PAGE)
	if not paginated_questions:
		return render(request, 'app/site_404.html')
		#return render(request, 'app/error.html')
		#raise Http404("Страница не найдена")

	data = {
		'questions': paginated_questions,
		'cnt_pages': range(1, (questions.count() + CNT_QUESTS_ON_PAGE - 1) // CNT_QUESTS_ON_PAGE + 1),
		'cur_page': cur_page,
		'popular_tags': Tag.objects.popular().values_list('name', flat=True)
	}

	return render(request, 'app/index.html', data)

def ask(request):
	return render(request, 'app/ask.html')

def login(request):
	return render(request, 'app/login.html')

def signup(request):
	return render(request, 'app/signup.html')

def answer(request, question_id):
	try:
		question_id = int(question_id)
	except ValueError:
		return render(request, 'app/site_404.html')

	question = Question.objects.new().filter(id=question_id).first()
	if question is None:
		return render(request, 'app/empty.html', {'popular_tags': Tag.objects.popular().values_list('name', flat=True)})

	answers = Answer.objects.answers(question=question)

	paginated_answers, cur_page = paginate(answers, request, CNT_ANSWERS_ON_PAGE)
	if not paginated_answers:
		return render(request, 'app/site_404.html')

	return render(request, 'app/answer.html', {
		'question': question,
		'answers': paginated_answers,
		'cnt_pages': range(1, (answers.count() + CNT_ANSWERS_ON_PAGE - 1) // CNT_ANSWERS_ON_PAGE + 1),
		'cur_page': cur_page,
		'popular_tags': Tag.objects.popular().values_list('name', flat=True)
	})


def hot(request):
	popular_questions = Question.objects.popular()
	popular_questions_count = popular_questions.count()

	if popular_questions_count == 0:
		return render(request, 'app/empty.html', {'popular_tags': Tag.objects.popular().values_list('name', flat=True)})

	paginated_questions, cur_page = paginate(popular_questions, request, CNT_QUESTS_ON_PAGE)

	if not paginated_questions:
		return render(request, 'app/site_404.html')

	data = {
		'questions': paginated_questions,
		'cnt_pages': range(1, (popular_questions_count + CNT_QUESTS_ON_PAGE - 1) // CNT_QUESTS_ON_PAGE + 1),
		'cur_page': cur_page,
		'popular_tags': Tag.objects.popular().values_list('name', flat=True)
	}

	return render(request, 'app/hot.html', data)

def tag(request, tag_name):
	tag = Tag.objects.filter(name=tag_name).first()
	if tag is None:
		return render(request, 'app/empty.html', {'popular_tags': Tag.objects.popular().values_list('name', flat=True)})

	questions_by_tag = Question.objects.filter(tags=tag).order_by('-created_at')

	paginated_questions, cur_page = paginate(questions_by_tag, request, per_page=CNT_QUESTS_ON_PAGE)
	if not paginated_questions:
		return render(request, 'app/site_404.html')

	data = {
		'tag': tag,
		'questions': paginated_questions,
		'cnt_pages': range(1, (questions_by_tag.count() + CNT_QUESTS_ON_PAGE - 1) // CNT_QUESTS_ON_PAGE + 1),
		'cur_page': cur_page,
		'popular_tags': Tag.objects.popular().values_list('name', flat=True)
	}

	return render(request, 'app/tag.html', data)

def error(request):
	return render(request, 'app/error.html')

def site_404(request):
	return render(request, 'app/site_404.html')