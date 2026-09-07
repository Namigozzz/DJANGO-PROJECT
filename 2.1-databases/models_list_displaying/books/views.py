from django.shortcuts import render
from datetime import datetime

from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books,
    }

    return render(request, template, context=context)

def books_paginated_view(request, pub_date):
    template = 'books/books_list.html'
    parsed_date = datetime.strptime(pub_date, '%Y-%m-%d').date()
    books = Book.objects.filter(pub_date=parsed_date).order_by('pub_date')
    prev_date = Book.objects.filter(pub_date__lt=parsed_date).order_by('-pub_date').first()
    next_date = Book.objects.filter(pub_date__gt=parsed_date).order_by('pub_date').first()
    context = {
        'books': books,
        'current_date': parsed_date,
        'next_date': next_date.pub_date if next_date else None,
        'prev_date': prev_date.pub_date if prev_date else None,
    }

    return render(request, template, context=context)
