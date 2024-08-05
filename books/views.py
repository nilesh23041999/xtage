from rest_framework import generics
from .third_party_calls import search_books, trim_book_data
from .serializers import *
from .response_handler import *
from .request_handler import request_handler
from .models import Book, UserInteraction
from django.shortcuts import render



def index(request):
    return render(request, 'index.html')


class BookSearchView(generics.GenericAPIView):
    """
    Search for books using keywords, authors, or categories.
    """
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        compulsory_query_parameters = []
        optional_query_parameters = ['q', 'authors', 'category']
        optional_body_args = []

        result = request_handler(request, compulsory_query_parameters, optional_query_parameters, optional_body_args)
        
        if isinstance(result, ErrorResponse):
            return result

        query = result['query_params'].get('q', None)
        authors = result['query_params'].get('authors', None)
        category = result['query_params'].get('category', None)
        
        if not query and not authors and not category:
            return ErrorResponse(error_code=400, error_message="At least one search parameter ('q', 'author', 'category') is required.")
        
        search_terms = []
        if query:
            search_terms.append(query)
        if authors:
            search_terms.append(f"inauthor:{authors}")
        if category:
            search_terms.append(f"subject:{category}")

        params = {'q': ' '.join(search_terms)}

        try:
            data = search_books(params)
            fields = ['id', 'title', 'authors', 'description', 'cover_image', 'averageRating', 'ratingsCount', 'categories']
            trimmed_data = trim_book_data(data.get('items', []), fields)
        

            return OkResponse(data=trimmed_data)
        except Exception as e:
            return ErrorResponse(error_code=500, error_message=str(e))
        
        
        
        
        

class SubmitRecommendationView(generics.GenericAPIView):
    """
    Endpoint to submit a new book recommendation.
    """
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        compulsory_query_parameters = []
        optional_query_parameters = []
        optional_body_args = ['title', 'authors', 'categories', 'rating', 'publication_date']

        result = request_handler(request, compulsory_query_parameters, optional_query_parameters, optional_body_args)

        if isinstance(result, SubmitRecommendationErrorResponse):
            return result
        
        data = request.data.copy()
        data['source'] = 'user'
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return OkResponse(data=serializer.data)
        print(serializer.errors)
        return SubmitRecommendationErrorResponse(error_code=400, error_message=serializer.errors)





class ListRecommendationsView(generics.GenericAPIView):
    """
    Endpoint to list book recommendations with filtering options.
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        compulsory_query_parameters = []
        optional_query_parameters = ['title', 'authors', 'categories', 'min_rating', 'max_rating', 'start_date', 'end_date']
        optional_body_args = []

        result = request_handler(self.request, compulsory_query_parameters, optional_query_parameters, optional_body_args)

        if isinstance(result, ListRecommendationsErrorResponse):
            return result

        queryset = Book.objects.filter(source='user')
        title = result['query_params'].get('title')
        authors = result['query_params'].get('authors')
        categories = result['query_params'].get('categories')
        min_rating = result['query_params'].get('min_rating')
        max_rating = result['query_params'].get('max_rating')
        start_date = result['query_params'].get('start_date')
        end_date = result['query_params'].get('end_date')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if authors:
            queryset = queryset.filter(authors__contains=[authors])
        if categories:
            queryset = queryset.filter(categories__contains=[categories])
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        if max_rating:
            queryset = queryset.filter(rating__lte=max_rating)
        if start_date:
            queryset = queryset.filter(publication_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(publication_date__lte=end_date)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if isinstance(queryset, ListRecommendationsErrorResponse):
            return queryset

        serializer = self.get_serializer(queryset, many=True)
        return OkResponse(data=serializer.data)




class ManageUserInteractionsView(generics.GenericAPIView):
    """
    Endpoint to create or update user interactions with book recommendations.
    """
    serializer_class = UserInteractionSerializer

    def post(self, request, *args, **kwargs):
        compulsory_query_parameters = []
        optional_query_parameters = []
        optional_body_args = ['book', 'liked', 'comment']

        result = request_handler(request, compulsory_query_parameters, optional_query_parameters, optional_body_args)

        if isinstance(result, ErrorResponse):
            return result

        book_id = result['body_params'].get('book')
        liked = result['body_params'].get('liked', False)
        comment = result['body_params'].get('comment', '')


        if not book_id:
            return ErrorResponse(error_code=400, error_message="Book ID is required.")

        # Ensure the book exists
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return ErrorResponse(error_code=404, error_message="Book not found.")



        interaction_type = 'like' if liked else 'comment'
        if interaction_type == 'comment' and not comment:
            return ErrorResponse(error_code=400, error_message="Comment text is required for comments.")

        interaction = UserInteraction.objects.create(
            book=book,
            interaction_type=interaction_type,
            comment=comment
        )

        if interaction_type == 'like':
            book.like_count = (book.like_count or 0) + 1
        elif interaction_type == 'comment':
            book.comment_count = (book.comment_count or 0) + 1
        book.save()

        return OkResponse(data={"message": "Interaction recorded successfully."})