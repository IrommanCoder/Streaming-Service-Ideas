import reflex as rx
from typing import TypedDict, Optional
import httpx
import logging


class Torrent(TypedDict):
    url: str
    hash: str
    quality: str
    type: str
    size: str


class Movie(TypedDict):
    id: int
    title: str
    year: int
    rating: float
    summary: str
    description_full: str
    genres: list[str]
    medium_cover_image: str
    large_cover_image: str
    background_image_original: str
    torrents: list[Torrent]
    cast: Optional[list[dict]]


class AppState(rx.State):
    """The state for the Netflix-like app."""

    featured_movie: Movie | None = None
    trending_now: list[Movie] = []
    new_releases: list[Movie] = []
    action_movies: list[Movie] = []
    comedies: list[Movie] = []
    search_results: list[Movie] = []
    query: str = ""
    is_searching: bool = False
    API_URL = "https://yts.mx/api/v2/list_movies.json"

    async def _fetch_movies(
        self,
        sort_by: str = "date_added",
        genre: str = "all",
        limit: int = 20,
        query_term: str = "",
    ):
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "sort_by": sort_by,
                    "genre": genre,
                    "limit": limit,
                    "minimum_rating": 5,
                }
                if query_term:
                    params["query_term"] = query_term
                response = await client.get(self.API_URL, params=params)
                response.raise_for_status()
                data = response.json()
                if data["status"] == "ok":
                    return data.get("data", {}).get("movies", [])
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error occurred: {e}")
        except Exception as e:
            logging.exception(f"An error occurred: {e}")
        return []

    @rx.event(background=True)
    async def on_app_load(self):
        """Fetch all movie categories on app load."""
        async with self:
            self.is_searching = False
            trending = await self._fetch_movies(sort_by="like_count")
            if trending:
                self.trending_now = trending
                self.featured_movie = trending[0]
        async with self:
            self.new_releases = await self._fetch_movies(sort_by="date_added")
        async with self:
            self.action_movies = await self._fetch_movies(genre="action")
        async with self:
            self.comedies = await self._fetch_movies(genre="comedy")

    @rx.event
    async def search_movies(self, query: str):
        self.query = query
        if not query.strip():
            self.is_searching = False
            self.search_results = []
            return
        self.is_searching = True
        self.search_results = await self._fetch_movies(query_term=query, limit=50)

    @rx.event
    def go_to_movie(self, movie_id: int):
        return rx.redirect(f"/movie/{movie_id}")