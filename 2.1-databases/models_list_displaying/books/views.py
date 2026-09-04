from django.shortcuts import render
from datetime import datetime, timedelta

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
    books = Book.objects.filter(pub_date=parsed_date)
    context = {
        'books': books,
        # 'current_date': parsed_date,
        'next_date': parsed_date + timedelta(days=1),
        'prev_date': parsed_date - timedelta(days=1),
    }

    return render(request, template, context=context)
