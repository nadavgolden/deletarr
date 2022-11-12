from typing import TYPE_CHECKING, Self

from easypy.bunch import Bunch
from easypy.collections import ListCollection

from deletarr.components.title import Title

if TYPE_CHECKING:
    from deletarr.tautulli import Tautulli


class Library:
    _SECTIONS_TYPE_REG = {}

    def __init_subclass__(cls) -> None:
        cls._SECTIONS_TYPE_REG[cls.SECTION_TYPE] = cls

    def __init__(self, tautulli: 'Tautulli', data: Bunch) -> None:
        self.tautulli = tautulli
        self.data = data

    @property
    def media(self) -> ListCollection:
        return ListCollection(
            Title.from_data(tautulli=self.tautulli, data=title)
            for title in self.tautulli.api.get_library_media_info(section_id=self.section_id).data
        )

    @classmethod
    def from_data(cls, *args, **kwargs) -> type[Self]:
        section_type = kwargs.get('data').section_type
        return cls._SECTIONS_TYPE_REG[section_type](*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.data, attr)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:'{self.section_name}'>"


class MoviesLibrary(Library):
    SECTION_TYPE = "movie"


class ShowsLibrary(Library):
    SECTION_TYPE = "show"


class MusicLibrary(Library):
    SECTION_TYPE="artist"


class PhotoLibrary(Library):
    SECTION_TYPE="photo"