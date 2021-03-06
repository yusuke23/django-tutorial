from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# オブジェクトのリストを表示する
class IndexView(generic.ListView):
    # 指定のテンプレート名
    template_name = 'polls/index.html'

    # デフォルトでは'question_list'を'latest_question_list'に変更
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # ビューが取得するオブジェクトを取得するために使われるクエリセットを返す
        # context_object_nameの値がこれで決められる
        return Question.objects.order_by('-pub_date')[:5]


# オブジェクトの詳細を表示する
class DetailView(generic.DetailView):
    model = Question
    # 指定のテンプレート名
    template_name = 'polls/detail.html'


# オブジェクトの詳細を表示する
class ResultsView(generic.DetailView):
    model = Question
    # 指定のテンプレート名
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # <input name="choice">からパラメータが取れる
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # POSTデータに'choice'がない場合KeyError
        # 例外が補足されると
        # もう一度投票ページに戻す
        context = {
            'question': question,
            'error_massage': "You didn't select a choice."
        }
        return render(request, 'polls/details.html', context)
    else:
        # tryで例外が発生しなかった場合の処理
        selected_choice.votes += 1
        selected_choice.save()
        # POSTデータが成功した場合は常にHttpResponseRedirectで返す必要がある
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # テンプレートのロード
#     # template = loader.get_template('polls/index.html')
#     # テンプレート内で使う変数
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # テンプレートにコンテキストを渡す
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     # try:
#         # 一個取ってくる
#         # question = Question.objects.get(pk=question_id)
#         # context = {'question': question}
#     # except Question.DoesNotExist:
#         # raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/details.html', context)

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         'question': question
#     }
#     return render(request, 'polls/results.html', context)
