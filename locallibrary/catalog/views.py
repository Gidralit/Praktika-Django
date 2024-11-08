from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime
from django.contrib import messages

from .forms import RenewBookForm

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()
    num_books_word = Book.objects.filter(title__icontains='Книга').count()

    return render(request, 'index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_books_word': num_books_word,
        'num_visits': num_visits,
    },)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # ваше собственное имя переменной контекста в шаблоне
    queryset = Book.objects.all() # Получение 5 книг, содержащих слово 'war' в заголовке
    template_name = 'books/book_list.html'  # Определение имени вашего шаблона и его расположения
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    queryset = Author.objects.all()
    template_name = 'authors/author_list.html'
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@method_decorator(permission_required('can_mark_returned'), name='dispatch')
class BookBorrowerListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.all()

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death':'12/10/2016'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

@login_required
def my_read_books(request):
    read_books = request.user.read_books.all()
    return render(request, 'catalog/books_reads.html', {'read_books': read_books})

@login_required
def mark_as_read(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user in book.user_who_read.all():
        messages.warning(request, "Вы уже прочитали эту книгу")
    else:
        book.user_who_read.add(request.user)
        messages.success(request, 'Книга успешно отмечена как прочитанная')
    return redirect('book-detail', pk=book.id)

# Create your views here.


