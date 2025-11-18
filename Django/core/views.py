from django.shortcuts import render, get_object_or_404

from .models import Category, Item

def index(request):
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)[0:6]
    return render(request, 'core/index.html', {
        'categories': categories, 
        'items': items
    })

def contact(request):
    return render(request, 'core/contact.html')