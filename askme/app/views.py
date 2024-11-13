from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

import random # !

CNT_ON_PAGE = 4

arr_questions = []
CNT_Q = 80

for i in range(CNT_Q):
	arr_questions.append({
		'id': i,
		'likes': 5,
		'title': 'How to build a moon park ? ' + str(i + 1),
		'description': 'Guys, i have trouble with a moon park. Cant find the black-jack...',
		'cnt_comments': 3,
		'comments': [
			{
				'likes': 7,
				'answer': 'First of all I would like to thank you for the invitation to participate in such a ... Russia is the huge territory which in many respects needs to be render habitable.' + str(i + 1),
				'isCorrect': True,
			},
			{
				'likes': 7,
				'answer': 'First of all I would like to thank you for the invitation to participate in such a ... Russia is the huge territory which in many respects needs to be render habitable.' + str(i + 1),
				'isCorrect': True,
			},
			{
				'likes': 7,
				'answer': 'First of all I would like to thank you for the invitation to participate in such a ... Russia is the huge territory which in many respects needs to be render habitable.' + str(i + 1),
				'isCorrect': True,
			},
		],
		'tags': ['black-jack', 'bender']
	})

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
	# Получаю данные arr_questions

	paginated_questions, cur_page = paginate(arr_questions, request, CNT_ON_PAGE)

	if not paginated_questions:
		return render(request, 'app/error.html')

	data = {
	'questions': paginated_questions,
	'cnt_pages': range(1, (CNT_Q + CNT_ON_PAGE - 1) // CNT_ON_PAGE + 1),
	'cur_page': cur_page
	}

	return render(request, 'app/index.html', data)

def ask(request):
    return render(request, 'app/ask.html')

def login(request):
    return render(request, 'app/login.html')

def signup(request):
    return render(request, 'app/signup.html')

def answer(request):
	def find_question_by_id(arr_questions, question_id):
		for question in arr_questions:
			if question['id'] == question_id:
				return question
		return None

	# Получаю данные arr_questions

	question_id = int(request.GET.get('id'))
	found_question = find_question_by_id(arr_questions, question_id)
    
	if not found_question:
		return render(request, 'app/error.html')
      
	return render(request, 'app/answer.html', {'question': found_question})


def hot(request):
	# Получаю данные arr_questions
	shuffled_questions = random.sample(arr_questions, len(arr_questions)) # !

	paginated_questions, cur_page = paginate(shuffled_questions, request, CNT_ON_PAGE)
	
	if not paginated_questions:
		return render(request, 'app/error.html')

	data = {
		'questions': paginated_questions,
		'cnt_pages': range(1, (CNT_Q + CNT_ON_PAGE - 1) // CNT_ON_PAGE + 1),
		'cur_page': cur_page
	}

	return render(request, 'app/hot.html', data)

def error(request):
    return render(request, 'app/error.html')