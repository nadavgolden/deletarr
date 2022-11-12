from easypy.bunch import Bunch
from easypy.collections import ListCollection
from datetime import datetime
from typing import Optional, TYPE_CHECKING, Self

if TYPE_CHECKING:
    from deletarr.tautulli import Tautulli


class Title:
    _MEDIA_TYPE_REG = {}

    def __init_subclass__(cls) -> None:
        cls._MEDIA_TYPE_REG[cls.MEDIA_TYPE] = cls

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        media_type = kwargs.get("data").media_type
        type_cls = cls._MEDIA_TYPE_REG[media_type]
        instance = super().__new__(type_cls)
        instance.__init__(*args, **kwargs)
        return instance

    def __init__(self, tautulli: 'Tautulli', data: Bunch) -> None:
        self.data = data
        self.tautulli = tautulli

    @property
    def added_at(self) -> datetime:
        return datetime.fromtimestamp(int(self.data.added_at))

    @property
    def last_played(self) -> Optional[datetime]:
        if last_played := self.data.last_played:
            return datetime.fromtimestamp(int(last_played))

    @property
    def children(self):
        return ListCollection(
            Title(tautulli=self.tautulli, data=title) for title in
            self.tautulli.api.get_library_media_info(section_id=self.section_id, rating_key=self.rating_key).data
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:'{self.data.title}'>"

    def __getattr__(self, attr):
        try:
            return getattr(self.data, attr)
        except AttributeError:
            raise AttributeError(f"{self} has not attribute '{attr}'") from None


class Movie(Title):
    MEDIA_TYPE="movie"


class Series(Title):
    MEDIA_TYPE="show"

    @property
    def seasons(self):
        return self.children


class Season(Title):
    MEDIA_TYPE="season"

    @property
    def episodes(self):
        return self.children


class Episode(Title):
    MEDIA_TYPE="episode"

