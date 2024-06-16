import json

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.contrib.auth import get_user, get_user_model
from .models import *
import pandas as pd


class FetchHandler(View):
    def get(self, request):
        # print(request.GET.get('user_search'))
        all_users = get_user_model()
        all_users = list(all_users.objects.values())
        all_marks = list(Mark.objects.values())

        user_marks_count = {}
        for user in all_users:
            for mark in all_marks:
                if user['id'] == mark['user_id_id']:
                    if user['username'] not in user_marks_count.keys():
                        user_marks_count[user['username']] = 1
                    else:
                        user_marks_count[user['username']] += 1

        # user_marks_count_list = list(sorted(user_marks_count.items(), key=lambda x: x[1]))
        # user_marks_count_list.reverse()
        # user_marks_count = dict(user_marks_count_list)
        # print(user_marks_count)
        # print(f'{user_marks_count = }')
        user_marks_count = list(sorted(user_marks_count.items(), key=lambda x: x[1]))
        user_marks_count.reverse()
        user_marks_count = dict(user_marks_count)
        # print(f'{user_marks_count = }')

        user_context = request.user
        curr_user = request.user.id
        if request.GET.get('user_search') != "":
            user = get_user_model()
            user = list(user.objects.filter(username=request.GET.get('user_search')).values())
            if len(user) != 0:
                curr_user = user[0]['id']
                user_context = user[0]['username']

        content_list = list(Mark.objects.filter(user_id=curr_user).values('content_id'))
        content_indexes = [elem['content_id'] for elem in content_list]
        content = list(Content.objects.filter(id__in=content_indexes).values('id', 'title', 'description'))
        photos = list(Photo.objects.filter(content_id__in=content_indexes).values('id', 'photo', 'content_id'))
        marks = list(Mark.objects.filter(user_id=curr_user).values('latitude', 'longitude', 'content_id',
                                                                   'user_id'))
        content_likes = list(Like.objects.values('content_id').annotate(dcount=Count('content_id')))

        # if curr_user != get_user(request).id:
        #     marks = list(
        #         Mark.objects.filter(user_id=curr_user, is_approved=True).values('latitude', 'longitude',
        #                                                                         'content_id',
        #                                                                         'user_id'))
        user_likes = self.get_liked_users()

        context = {
            'marks': marks,
            'content': content,
            'photos': photos,
            'user_context': user_context,
            'users_list': user_marks_count.items(),
            'content_likes': content_likes,
            'user_likes': user_likes.items()
        }
        # print("content = ")
        # print(*context, sep='\n')
        # print(content[0]["id"])

        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     return JsonResponse({'Uknown': 1})
        # #print(request.user.id)
        return render(request, 'main/index.html', context)

    def post(self, request):
        # Получаем значения из ответа
        values = json.loads(request.body.decode('utf-8'))
        user = get_user(request)

        # Если POST-запрос для лайка, то ..., иначе POST-запрос для выставления метки
        if values['is_like']:
            cnt_id = values['content_id']
            print(cnt_id)
            content_obj_id = Content.objects.get(pk=cnt_id)  # айди должен принадлежать модели, а не быть int
            repeat_like = Like.objects.filter(content_id=content_obj_id, user_id=user).count()
            if repeat_like < 1:
                Like.objects.create(content_id=content_obj_id, user_id=user)
                print("Лайк поставлен")
            else:
                Like.objects.filter(content_id=content_obj_id, user_id=user).delete()
                print("Лайк отменён")
        else:
            content = Content.objects.create(title=values['title'], description=values['description'])
            for source in values['sources']:
                Photo.objects.create(photo=source, content_id=content)
            Mark.objects.create(latitude=values['lat'], longitude=values['lng'], user_id=user, content_id=content)

        self.points_adding(request)
        return JsonResponse({'val': 'data'}, status=200)
        # print(f)
        # return JsonResponse()

    def get_liked_users(self):

        # user_likes1 = list(
        #     Like.objects
        #     .values('user_id_id')
        #     .annotate(count=Count('user_id_id'))
        # )
        # user_likes2 = (
        #     Like.objects
        #     .select_related('content_id')
        #     .values('user_id_id', 'content_id_id')
        #     .order_by('user_id_id')
        # )
        # user_likes3 = (
        #     Like.objects
        #     .select_related('content_id')
        #     .values('user_id_id')
        #     .annotate(count=Count('user_id_id'))
        # )
        # user_likes4 = Like.objects.raw(
        #     'select 1 as id,'
        #     'mm.user_id_id, '
        #     'count(mm.user_id_id) '
        #     'from main_like ml left join '
        #     'main_mark mm on ml.content_id_id = mm.content_id_id '
        #     'group by mm.user_id_id')
        # user_likes6 = list(
        #     Like.objects
        #     .select_related('content_id')
        #     .values('user_id_id', 'content_id')
        #     # .annotate(dcount=Count('user_id_id'))
        #     .order_by('user_id_id')
        # )
        user_likes5 = list(Like.objects.raw('''
                select
                    1 as id,  
                    mm.user_id_id,
                    ml.content_id_id
                from main_like ml 
                    left join main_mark mm on ml.content_id_id = mm.content_id_id;
        '''))
        df = pd.DataFrame()
        i = 0
        for elem in user_likes5:
            df.loc[i, 'user_id'] = str(elem.user_id)
            df.loc[i, 'content_id'] = elem.content_id.id
            i += 1
        a = df.groupby("user_id").aggregate({'user_id': 'count'})
        a = a.rename(columns={'user_id': 'count'})
        b = {}
        for i in range(len(a)):
            b[a.iloc[i].name] = a.iloc[i][0]
        return b

    def points_adding(self, request):
        values = json.loads(request.body.decode('utf-8'))
        print(values)
        curr_user = get_user(request)
        if values['actionType'] == 'addingMark':
            marks_number = len(list(Mark.objects.filter(user_id=curr_user).values()))

            if marks_number >= 5:
                points = self._adding_achievement_for_user(request, 2)
                if points is not None:
                    self._raising_user_level(request, points)
        elif values['actionType'] == 'addingLike':
            all_likes_count = len(list(Like.objects.filter(user_id=curr_user)))
            if all_likes_count >= 5:
                points = self._adding_achievement_for_user(request, 1)
                if points is not None:
                    self._raising_user_level(request, points)
            user_content_id = Mark.objects.filter(user_id=curr_user).values('content_id_id')
            user_content = [elem['content_id_id'] for elem in user_content_id]
            other_likes = len(list(Like.objects.filter(content_id__in=user_content).values()))
            print(user_content_id)
            print(other_likes)
            if other_likes >= 5:
                points = self._adding_achievement_for_user(request, 3)
                if points is not None:
                    self._raising_user_level(request, points)

    def _check_achievement(self, request, achievement_id) -> bool:
        current_user = get_user(request)
        user_achievements = list(UsersAchievements.objects.filter(user_id=current_user).values('achievement_id_id'))
        user_ach_list = []
        for ach in user_achievements:
            user_ach_list.append(ach['achievement_id_id'])

        if achievement_id not in user_ach_list:
            return True
        return False

    def _raising_user_level(self, request, points):
        current_user = get_user(request)
        if len(list(UsersLevel.objects.filter(user_id=current_user).values())) == 0:
            UsersLevel.objects.create(user_id=current_user, total_points=0, level=0)
        # print(UsersLevel.objects.filter(user_id=current_user).values('total_points')[0]['total_points'])
        user_points = list(UsersLevel.objects.filter(user_id=current_user).values('total_points'))[0][
                          'total_points'] + points

        num = UsersLevel.objects.filter(user_id=current_user).update(total_points=user_points)

        new_level = list(Levels.objects.filter(points_for_level=points).values())[0]['id']
        user_level = UsersLevel.objects.filter(user_id=current_user).update(level=new_level)

    def _adding_achievement_for_user(self, request, achievement_id):
        achievement_check = self._check_achievement(request, achievement_id)
        if achievement_check:
            achievement = Achievements.objects.get(id=achievement_id)
            print(get_user(request))
            UsersAchievements.objects.create(user_id=get_user(request), achievement_id=achievement)
            points = Achievements.objects.filter(id=achievement_id).values('points')
            points = list(points)[0]['points']
            return points
        return None


class Search(ListView):
    template_name = 'templates/index.html'

    def get_queryset(self):
        print(self.request.GET.get('user_search'))
        # user = get_user()
        return Mark.objects.filter(user_id=self.request.GET.get('user_search'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_search'] = Mark.objects.filter(user_id=self.request.GET.get('user_search'))
        print(context)
        return context

# def index(request):
#     # №context = {'marks': list(Mark.objects.values('latitude', 'longitude', 'content_id', 'user_id'))}
#     # print(context)
#     return render(request, 'main/index.html')


# def about(request):
#     return render(request, 'main/add.html')
