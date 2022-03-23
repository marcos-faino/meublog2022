from django.urls import path
from . import views

app_name = 'meublog'

urlpatterns = [
    path('', views.listar_posts, name='listar_posts'),
    path('<int:ano>/<int:mes>/<int:dia>/<slug:slug>/',
         views.detalhar_post, name='detalhe'),
]