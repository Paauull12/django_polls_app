from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('add_comment/<int:question_id>/', views.add_comment, name='add_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('add_question/', views.add_question, name="add_question"),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete_comment/<int:comment_id>/', views.delete_commment, name='delete_comment'),
]
