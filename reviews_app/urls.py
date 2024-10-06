from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.GameReviewHome.as_view(), name='home'),  # http://127.0.0.1:8000
    path('about/', views.about, name='about'),
    path('addreview/', views.AddPage.as_view(), name='add_review'),
    path('review/<slug:review_slug>/', views.ShowReview.as_view(), name='review'),
    path('category/<slug:cat_slug>/', views.GameReviewCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.GameReviewTags.as_view(), name='tag'),
    path('edit/<int:pk>', views.UpdatePage.as_view(), name='edit_page'),
]