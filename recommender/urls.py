from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.moviePage, name ="moviePage"),
    path('signin/', views.signIn, name='signIn'),
    path('signup/', views.signUp, name='signUp'),
    path('logout/', views.logOut, name='logOut'),
    path('login/', views.logIn, name='logIn'),
    path('test/', views.testingExperiment, name='testingExperiment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)