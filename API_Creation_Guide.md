# Quick Guide to Creating a REST API in Django (IF YOU WANT TO EXTEND API CREATION FOR BOOKS)

## 1. Setup

### Install Django and Django REST Framework:

```bash
pip install django djangorestframework
```


## Create a Django Project and App:

django-admin startproject myproject
cd myproject
python manage.py startapp myapp


Update settings.py:


INSTALLED_APPS = [
    ...
    'rest_framework',
    'myapp',
]



## 2. Define Models
```bash
myapp/models.py:

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```


## 3. Create Serializers
```bash
myapp/serializers.py:


from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

```


## 4. Create Views
```bash
myapp/views.py:


from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```


## 5. Define URLs
```bash
myapp/urls.py:

from django.urls import path
from .views import ItemListCreateView, ItemDetailView

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
]
```

myproject/urls.py:

```bash
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
]
```



## 6. Migrate Database and Run Server

```bash
Apply Migrations:

python manage.py makemigrations
python manage.py migrate
```


## 7. Run the Development Server:

```bash
python manage.py runserver
```