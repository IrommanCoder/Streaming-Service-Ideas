import reflex as rx
import httpx
import logging
from app.states.state import Movie


class MovieDetailState(rx.State):
    movie: Movie | None = None
    suggestions: list[Movie] = []
    is_loading: bool = True

    @rx.var
    def movie_id(self) -> str:
        return self.router.page.params.get("id", "0")

    @rx.event(background=True)
    async def get_movie_details(self):
        async with self:
            self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "movie_id": self.movie_id,
                    "with_images": "true",
                    "with_cast": "true",
                }
                response = await client.get(
                    "https://yts.mx/api/v2/movie_details.json", params=params
                )
                response.raise_for_status()
                data = response.json()
                if data["status"] == "ok":
                    async with self:
                        self.movie = data.get("data", {}).get("movie")
                suggest_params = {"movie_id": self.movie_id}
                suggest_response = await client.get(
                    "https://yts.mx/api/v2/movie_suggestions.json",
                    params=suggest_params,
                )
                suggest_response.raise_for_status()
                suggest_data = suggest_response.json()
                if suggest_data["status"] == "ok":
                    async with self:
                        self.suggestions = suggest_data.get("data", {}).get(
                            "movies", []
                        )
        except httpx.HTTPStatusError as e:
            logging.exception(f"HTTP error occurred: {e}")
        except Exception as e:
            logging.exception(f"An error occurred: {e}")
        finally:
            async with self:
                self.is_loading = False