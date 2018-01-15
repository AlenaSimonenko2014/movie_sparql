from django.http import HttpResponseRedirect

from django.urls import reverse
from django.views.generic import FormView, TemplateView

from movie_sparql.query import get_contributors_for_movie
from web.forms import SearchForm
from web.models import Movie, Contributor, Genre


class SearchView(FormView):
    template_name = 'web/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        """
        If the form is valid, query db and persist data
        """
        movie, created = Movie.objects.get_or_create(name=form.data['movie_name'])

        new_genre_count = new_contributor_count = 0

        for obj in get_contributors_for_movie(movie.name):
            genre, created = Genre.objects.get_or_create(name=obj["genre"])
            if created:
                new_genre_count += 1

            contributor, created = Contributor.objects.get_or_create(
                name=obj["name"], genre=genre)
            if created:
                new_contributor_count += 1
            if contributor not in movie.contributors.all():
                movie.contributors.add(contributor)

            same_genre_contributor, created = Contributor.objects.get_or_create(
                name=obj["same_genre_contributor"], genre=genre)
            if created:
                new_contributor_count += 1

        print("Added %d new genres" % new_genre_count)
        print("Added %d new contributors" % new_contributor_count)

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
