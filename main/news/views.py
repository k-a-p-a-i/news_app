from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from .models import Book, Author, BookInstance, Genre
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genres = Genre.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,

    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'news/index.html', context=context)

def about(request):
    return render(request, 'news/about.html' )


def error_404(request, exception):
    "функция вызова ошибки 404"
    context = {}
    return render(request, 'news/404.html', context)


def new_req(request):
    return render(request, 'news/news.html' )

def user_account(request):
    return render(request, 'news/user_account.html' )


