from django.urls import path
from .views import SubmitRecommendationView, ListRecommendationsView, ManageUserInteractionsView, BookSearchView

urlpatterns = [
    path('recommendations/', SubmitRecommendationView.as_view(), name='submit_recommendation'),
    path('recommendations/list/', ListRecommendationsView.as_view(), name='list_recommendations'),
    path('user-interactions/', ManageUserInteractionsView.as_view(), name='manage_user_interactions'),
    path('search/', BookSearchView.as_view(), name='book_search'),
]
