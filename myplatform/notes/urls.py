from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllNotesList.as_view(), name="notes"),
    path('note/', views.createNote, name="create"),
    path('note/<int:pk>', views.NoteDetail.as_view(), name="get_note"),


    path('categories', views.AllCategoriesList.as_view(), name="categories"),
    path('category', views.createCategory, name="create-category"),

]