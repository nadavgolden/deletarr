from easypy.collections import ListCollection

from deletarr.api import TautulliAPI
from deletarr.components.library import Library, ShowsLibrary, MoviesLibrary


class Tautulli:
    def __init__(self, *, base_url, apikey, ignore_list: list=None) -> None:
        self.api = TautulliAPI(base_url, apikey)
        self.ignore_list = ignore_list

    @property
    def libraries(self) -> ListCollection:
        libraries = ListCollection(
            Library(tautulli=self, data=data) for data in self.api.get_libraries())

        if self.ignore_list:
            libraries = ListCollection(libraries.filtered(lambda l: l.section_name not in self.ignore_list))

        return libraries

    @property
    def movie_libraries(self):
        return self.libraries.filtered(section_type="movie")

    @property
    def show_libraries(self):
        return self.libraries.filtered(section_type="show")

    @property
    def all_movies(self) -> ListCollection:
        return ListCollection(
            movie for library in self.movie_libraries for movie in library.media
        )

    @property
    def all_shows(self) -> ListCollection:
        return ListCollection(
            show for library in self.show_libraries for show in library.media
        )

    @property
    def all_episodes(self):
        return ListCollection(
            episode for show in self.all_shows for season in show.seasons for episode in season.episodes
        )
