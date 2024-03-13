"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index, name='home'),
    path('error/', views.error, name='error'),

    #authentikacija
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #administrator
    path('create_user/', views.create_user, name='create_user'),
    path('predmeti/', views.predmeti_list, name='predmeti'),
    path('predmeti/predmet-edit/<int:pk>/', views.predmet_edit, name='predmet-edit'),
    path('predmeti/predmet-detail/<int:pk>/', views.predmeti_detail, name='predmet-detail'),
    path('predmeti/create-predmet/', views.predmeti_create, name='predmet-create'),
    path('predmeti/<int:predmet_id>/studenti-popis/', views.studenti_popis, name='studenti-popis'),
    path('studenti/', views.student_list, name='studenti'),
    path('studenti/student-edit/<int:pk>/', views.student_edit, name='student-edit'),
    path('studenti/student-detail/<int:pk>/', views.student_detail, name='student-details'),
    path('studenti/create-student/', views.student_create, name='student-create'),
    path('profesori/', views.profesor_list, name='profesori'),
    path('profesori/profesor-edit/<int:pk>/', views.profesor_edit, name='profesor-edit'),
    path('profesori/profesor-detail/<int:pk>/', views.profesor_detail, name='profesor-details'),
    path('profesori/create-profesori/', views.profesor_create, name='profesor-create'),
    path('upisni/', views.upisni_listovi, name='upisni-listovi'),
    path('upisni/upisli-list-edit/<int:pk>/', views.upisni_list_edit, name='upisni-list-edit'),
    path('upisni/upisni-list-create/', views.upisni_list_create, name='upisni-list-create'),
    
    #profesor
    path('predmetProfesor/', views.predmeti_list_for_each_profesor, name='predmet-profesor'),
    path('predmetProfesor/<int:predmet_id>/students/', views.popis_studenata, name='popis-studenata'),
    path('predmetProfesor/<int:predmet_id>/student/<int:student_id>/edit-status/', views.status_edit, name='status-edit'),
    path('predmetProfesor/izgubio-potpis/<int:predmet_id>/', views.popis_studenata_izgubljen_potpis, name='izgubio-potpis'),
    path('predmetProfesor/upisan/<int:predmet_id>/', views.popis_studenata_upisan, name='upisan'),
    path('predmetProfesor/polozen/<int:predmet_id>/', views.popis_studenata_polozen, name='polozen'),

    #student
    path('predmeti-list/', views.upis_predmeta, name='predmeti-list'),
    path('predmeti/add/<int:predmet_id>/', views.add_predmet, name='add_predmet'),
    path('upisi_list/', views.upisni_list, name='upisi_list'),
    path('upisi/delete/<int:upis_id>/', views.upisi_delete, name='upisi_delete'),

    path('zad1/', views.zad, name='zad1'),
    path('vidi-detalje/<int:predmet_id>/', views.drugi, name='vidi-detalje'),
]
