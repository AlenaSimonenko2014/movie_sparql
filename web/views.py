from django.http import HttpResponseRedirect

from django.urls import reverse
from django.views.generic import FormView, TemplateView

from movie_sparql.query import get_movie
from web.forms import SearchForm
from web.models import Movie, Contributor, Genre


class SearchView(FormView):
    template_name = 'web/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        """
        If the form is valid, query db and persist data
        """
        movie_obj = get_movie("Asturias")  # form.data['movie_name'])

        # TODO get_or_create contibutors, genres

        movie, created = Movie.objects.get_or_create(name=movie_obj["name"])
        return HttpResponseRedirect(reverse('movie-detail', kwargs={'name': movie.name}))


class MovieView(TemplateView):
    template_name = 'web/movie.html'

    def get_context_data(self, **kwargs):
        kwargs.update({'object': Movie.objects.get(name=kwargs["name"])})
        return super().get_context_data(**kwargs)


class ContributorView(TemplateView):
    template_name = 'web/contributor.html'

    def get_context_data(self, **kwargs):
        kwargs.update({'object': Contributor.objects.get(name=kwargs["name"])})
        return super().get_context_data(**kwargs)


class GenreView(TemplateView):
    template_name = 'web/genre.html'

    def get_context_data(self, **kwargs):
        kwargs.update({'object': Genre.objects.get(name=kwargs["name"])})
        return super().get_context_data(**kwargs)
