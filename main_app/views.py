from .models import *

# API

from .serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, authenticate, user_logged_out
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import status

class TestApiView(APIView):
    permission_classes = [IsAuthenticated]
    import requests
    from django.core.files.base import ContentFile
    def get(self, request):
        import requests
        response = requests.get('https://random.dog/woof.json')
        if response.status_code == 200:
            data = response.json()
            filename = data['url'].split("/")[-1]
            format = filename.split(".")[-1]
            processed_data = { 'count': len(data), 'results': data }
            image = requests.get(data['url'])
            image_content = image.content
            image_file = self.ContentFile(image_content, name=filename)
            return Response(image_file, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Ошибка при получении данных с внешнего API'}, status=response.status_code)

    def post(self, request):
        import requests
        from django.core.files.base import ContentFile
        response = requests.get('https://random.dog/woof.json')
        if response.status_code == 200:
            data = response.json()
            filename = data['url'].split("/")[-1]
            format = filename.split(".")[-1]
            if format == 'mp4':
                pass
            else:
                image_file = ContentFile((data['url']).content)
                post = Posts.objects.create(
                    author=CustomUser.objects.get(id=request.user.id),
                    title='Пост со сгенерированной картинкой',
                    text='Моё дополнение к увиденному:'
                )
                post.image.save(filename, image_file, save=True)
                return Response({'message': "Ваш пост сгенерирован!"}, status=status.HTTP_201_CREATED)\


class LikePostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        like_posts = []
        my_likes = Likes.objects.filter(author=request.user.id)
        for like in my_likes:
            post = like.post
            like_posts.append(post)
        data = PostSerializer(like_posts, many=True).data
        return Response(data)

    def post(self, request):
        post_id = request.data.get('post')
        from django.shortcuts import get_object_or_404
        post = get_object_or_404(Posts, id=post_id)
        author = request.user.id
        if len(Likes.objects.filter(author=author, post=post)):
            return Response({'message': 'Этот пост уже ранее был оценен вами!'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['author'] = author
        like = LikeDislikeSerializer(data=request.data)
        if like.is_valid():
            post.likes_count += 1
            post.save()
            like.save()
            return Response({'message': 'Вы оценили пост❤️'}, status=status.HTTP_201_CREATED)
        else:
            return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        post_id = request.data.get('post')
        from django.shortcuts import get_object_or_404
        post = get_object_or_404(Posts, id=post_id)
        author = request.user.id
        like = Likes.objects.filter(author=author, post=post)
        if not len(like):
            return Response({'message': 'Этот еще не был оценен вами!'}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()
        post.likes_count -= 1
        post.save()
        return Response({'message': 'Ваша оценка удалена!'}, status=status.HTTP_400_BAD_REQUEST)
class DislikePostApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dislike_posts = []
        my_likes = Dislikes.objects.filter(author=request.user.id)
        for dislike in my_dislikes:
            post = dislike.post
            dislike_posts.append(post)
        data = PostSerializer(dislike_posts, many=True).data
        return Response(data)
    def post(self, request):
        post_id = request.data.get('post')
        from django.shortcuts import get_object_or_404
        post = get_object_or_404(Posts, id=post_id)
        author = request.user.id
        if len(Disikes.objects.filter(author=author, post=post)):
            return Response({'message': 'Этот пост уже ранее был оценен вами!'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['author'] = author
        dislike = LikeDislikeSerializer(data=request.data)
        if dislike.is_valid():
            post.dislikes_count += 1
            post.save()
            like.save()
            return Response({'message': 'Вы оценили пост💩'}, status=status.HTTP_201_CREATED)
        else:
            return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        post_id = request.data.get('post')
        from django.shortcuts import get_object_or_404
        post = get_object_or_404(Posts, id=post_id)
        author = request.user.id
        dislike = Disikes.objects.filter(author=author, post=post)
        if not len(dislike):
            return Response({'message': 'Этот еще не был оценен вами!'}, status=status.HTTP_400_BAD_REQUEST)
        dislike.delete()
        post.dislikes_count -= 1
        post.save()
        return Response({'message': 'Ваша оценка удалена!'}, status=status.HTTP_400_BAD_REQUEST)
class FriendApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        for_user = Friends.objects.filter(to_user=user_id)
        from_user = Friends.objects.filter(from_user=user_id)
        invites_for_user = FriendSerializer(for_user, many=True).data
        invites_from_user = FriendSerializer(from_user, many=True).data
        return Response(data={'Запросы тебе': invites_for_user, 'Запросы от тебя': invites_from_user}, status=status.HTTP_200_OK)
    def patch(self, request):
        invite_id = request.data.get('id')
        status_invite = request.data.get('status')
        user_id = request.user.id
        if invite_id is None:
            return Response(data={'detail': 'Впишите id запроса в друзья!'}, status=status.HTTP_400_BAD_REQUEST)
        elif status_invite is None:
            return Response(data={'detail': 'Впишите status запроса в друзья!'}, status=status.HTTP_400_BAD_REQUEST)
        from django.shortcuts import get_object_or_404
        invite = get_object_or_404(Friends, id=invite_id, to_user=user_id)
        request.data['to_user'] = request.user.id
        invite_serializer = FriendSerializer(invite, data=request.data, partial=True) # partial=True позволяет обновлять только некоторые поля модели
        if invite_serializer.is_valid():
            invite_serializer.save()
            if status_invite == 'accepted':
                # set([]) - устанавливает, add() - добавляет, remove() - удаляет.
                request.user.friends.add(request.data['from_user'])
            else:
                request.user.friends.remove(request.data['from_user'])
                return Response(data={f"Статус изменен на {status_invite}"}, status=status.HTTP_200_OK)
        else:
            return Response(data=invite_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class FindpeopleApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        order = request.GET.get('order')
        search = request.GET.get('search')
        users_by_names = CustomUser.objects.filter(name__contains=search) ?
        users_by_surnames = CustomUser.objects.filter(surname__contains=search)
        # __search -> Ищет слово целиком
        # __contains -> Ищет символы без регистра
        # __icontains -> Ищет символы c регистра
        if order is not None:
            if order == 'desc':
                users_by_names = users_by_names.order_by('-name')
                users_by_surnames = users_by_surnames.order_by('-surname')
            elif order == 'asc':
                users_by_names = users_by_names.order_by('name')
                users_by_surnames = users_by_surnames.order_by('surname')
        data = FindUserSerializer(users_by_names, many=True).data
        data2 = FindUserSerializer(users_by_surnames, many=True).data
        return Response([data,data2], status=status.HTTP_200_OK)

    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        invite_friend = request.data.get('to_user')
        if invite_friend is None:
            return Response(data={'detail': 'Отсутсвует id получателя! (fild: to_user)'}, status=status.HTTP_400_BAD_REQUEST)
        invite_list = Friends.objects.filter(to_user=invite_friend, from_user=request.user.id)
        if len(invite_list) >= 1:
            return Response(data={'detail': f'У вас уже есть запрос для этого человека! Его id={invite_list[0].id}'},
                            status=status.HTTP_409_CONFLICT)
        request.data['from_user'] = request.user.id
        request.data['status'] = 'no_request'
        invite = FriendSerializer(data=request.data)
        if invite.is_valid():
            request.user.friends.add(invite_friend)
            invite.save()
            invite_list = Friends.objects.filter(to_user=invite_friend, from_user=request.user.id)
            set = []
            for invite in invite_list:
                set.append(invite.id)
            return Response({'message': f'Ваш запрос в друзья отправлен! Его id={set}'}, status=status.HTTP_201_CREATED)
        return Response(invite.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        invite_id = request.data.get('id')
        if invite_id is None:
            return Response(data={'detail': 'Отсутсвует id запроса в друзья!'},
                            status=status.HTTP_400_BAD_REQUEST)
        from django.shortcuts import get_object_or_404
        invite_delete = get_object_or_404(Friends, id=invite_id)
        request.user.friends.remove(invite_delete.id)
        invite_delete.delete()
        return Response(data={'message': 'Запрос на предложение дружбы удален!'}, status=status.HTTP_200_OK)
class CommentApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        comments = Comments.objects.filter(author=user_id)
        comments_user = CommentSerializer(comments, many=True).data
        return Response(comments_user, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['author'] = request.user.id
        comment = CommentSerializer(data=request.data)

        if comment.is_valid():
            comment.save()
            return Response({'message': "Ваш комментарий добавлен!"}, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request):
        comment_id = request.data.get('id')
        if comment_id is None:
            return Response(data={'detail': 'Отсутсвует id комментария!'}, status=status.HTTP_400_BAD_REQUEST)

        from django.shortcuts import get_object_or_404
        comment = get_object_or_404(Comments, id=comment_id)
        request.data['author'] = request.user.id
        comment_serializer = PostSerializer(comment, data=request.data, partial=True)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(data={"Коментарий Изменен"}, status=status.HTTP_200_OK)
        else:
            return Response(data=comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        comment_id = request.data.get('id')
        if comment_id is None:
            return Response(data={'detail': 'Отсутсвует id комментария!'}, status=status.HTTP_400_BAD_REQUEST)
        from django.shortcuts import get_object_or_404
        comment = get_object_or_404(Comments, id=comment_id)
        comment.delete()
        return Response(data={"Комментарий Удален!"}, status=status.HTTP_200_OK)
class PostUserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        list_user_posts = []
        user_id = request.user.id
        posts = Posts.objects.filter(author=user_id)
        posts_user = PostSerializer(posts, many=True).data
        for post in posts_user:
            id_post = post['id']
            comments = Comments.objects.filter(post=id_post)
            comments_for_post = CommentSerializer(comments, many=True).data
            list_user_posts.append([post, comments_for_post])
        return Response(list_user_posts, status=status.HTTP_200_OK)
    def post(self, request):
        request.data['author'] = request.user.id
        post = PostSerializer(data=request.data)
        if post.is_valid():
            post.save()
            return Response({'message': "Ваш пост создан!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(post.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        post_id = request.data.get('id')

        if post_id is None:
            return Response(data={'detail': 'Отсутсвует id поста'}, status=status.HTTP_400_BAD_REQUEST)

        from django.shortcuts import get_object_or_404
        post = get_object_or_404(Posts, id=post_id)

        request.data['author'] = request.user.id
        post_serializer = PostSerializer(post, data=request.data, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(data={"Пост Изменен"}, status=status.HTTP_200_OK)
        else:
            return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post_id = request.data.get('id')
        if post_id is None:
            return Response(data={'detail': 'Отсутсвует id поста'}, status=status.HTTP_400_BAD_REQUEST)
        from django.shortcuts import get_object_or_404
        post = get_object_or_404(Posts, id=post_id)
        post.delete()
        return Response(data={"Пост Удален"}, status=status.HTTP_200_OK)
class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth.models import AbstractBaseUser
        from django.db import IntegrityError
        username = request.data.get('phone_number')
        password = request.data.get('password')
        try:
            CustomUser.objects.create_user(phone_number=username, password=password)
            return Response(data={'message': 'Registration success'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response(data={'message': 'Username is already registered'}, status=status.HTTP_400_BAD_REQUEST)
class CabinetApiView(APIView):
     permission_classes = [IsAuthenticated]

     def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        list4 = UserSerializer(user, many=False).data
        return Response(list4, status=status.HTTP_200_OK)

     def patch(self, request):
         user_id = request.user.id
         from django.shortcuts import get_object_or_404
         user = get_object_or_404(CustomUser, id=user_id)
         user_serializer = UserSerializer(user, data=request.data, partial=True)
         if user_serializer.is_valid():
             user_serializer.save()
             return Response(data={}, status=status.HTTP_200_OK)
         else:
             return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def delete(self, request):
        request.user.delete()
        return Response(data={'message': 'OK!'}, status=status.HTTP_200_OK)
class AuthApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('phone_number')
        password = request.data.get('password')
        user = authenticate(phone_number=username, password=password)
        if user is None:
            return Response(data={'message': 'Invalid username/password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            login(request, user)
            return Response(data={'message': 'Auth success!'}, status=status.HTTP_200_OK)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(data={'message': 'You are nor logged in.'}, status=status.HTTP_401_UNAUTHORIZED)
        logout(request)
        return Response(data={'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)


 # экран для пользователя

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout

def main_view(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Posts.objects.all()
        print(user)
        context = {
            'user': user,
            'posts': posts
        }
        return render(request, 'main.html', context=context)
    else:
        return render(request, 'main.html')