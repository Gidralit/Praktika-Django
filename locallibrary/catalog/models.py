from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.utils.html import format_html

class Genre(models.Model): #Модель жанра
    name = models.CharField(max_length=255, help_text='Введите категорию книги(Художественная, документальная или роман)')

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text='Введите язык на котором написана книга(Английский, Французкий, Русский)')

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author', help_text='Выберите авторов книги') #Foreign key используем потому что автор у книги может быть только один, но авторы могут написать много книг
    summary = models.TextField(max_length=1000, help_text="Напишите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13, help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN номера</a>')
    genre = models.ManyToManyField(Genre, help_text='Выберите жанр книги')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    user_who_read = models.ManyToManyField(User, related_name='read_books', null=True)

    def display_authors(self):

        authors_links = []
        for author in self.authors.all():
            url = reverse('author-detail', args=[author.id])
            authors_links.append(f'<a href="{url}">{author.first_name} {author.last_name}</a>')
        return format_html(', '.join(authors_links))
        # return ', '.join([Author.first_name for Author in self.authors.all()])


    def clean_author(self):
        if self.author.count() > 4:
            raise ValueError('У книги не может быть более 4 авторов')

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Уникальный идентификатор этой книги во всей библиотеки')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Статус книги')

    class Meta:
        ordering = ['due_back']
        permissions = [
            ('can_mark_returned', 'can mark book as returned'),
        ]

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return '{0} ({1})'.format(self.book.title, self.id)

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)

# Create your models here.
