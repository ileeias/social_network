"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cabinet', CabinetApiView.as_view()),
    path('', main_view, name='main_url'),
    path('auth', AuthApiView.as_view()),
    path('reg', RegistrationApiView.as_view()),
    path('my_posts', PostUserApiView.as_view()),
    path('my_comment', CommentApiView.as_view()),
    path('my_friend', FriendApiView.as_view()),
    path('ppl_search', FindpeopleApiView.as_view()),
    path('fast', FastPostApiView.as_view()),
    path('like', LikePostApiView.as_view()),
    path('dislike', DislikePostApiView.as_view()),
    path('all_posts', AllPostsApiView.as_view()),
]


from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)