from easypy.collections import ListCollection

from deletarr.api import TautulliAPI
from deletarr.components.library import Library


class Tautulli:
    def __init__(self, *, base_url, apikey) -> None:
        self.api = TautulliAPI(base_url, apikey)
        self.refresh_libraries()

    def refresh_libraries(self):
        self.libraries = ListCollection(
            Library.from_data(tautulli=self, data=data) for data in self.api.get_libraries())

    @property
    def movies_lib(self) -> 'Library':
        return self.libraries.get(section_type="movie", agent="tv.plex.agents.movie")

    @property
    def series_lib(self) -> 'Library':
        return self.libraries.get(section_type="show", agent="tv.plex.agents.series")
