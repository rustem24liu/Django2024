from django.urls import path

from .views import *

urlpatterns = [
    path('list/', GradeListView.as_view(), name='grade-list'),
    path('create/', GradeCreateView.as_view(), name='grade-create'),
    path('detail/', GradeDetailView.as_view, name='grade-detail'),
    path('update/', GradeUpdateView.as_view(), name='grade-edit'),
    path('delete/', GradeDeleteView.as_view(), name='grade-delete'),
]