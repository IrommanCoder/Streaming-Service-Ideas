import reflex as rx
from app.states.state import Movie, AppState


def movie_card(movie: Movie) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=movie["medium_cover_image"],
            alt=movie["title"],
            class_name="w-full h-full object-cover group-hover:opacity-80 transition-opacity",
        ),
        rx.el.div(
            rx.el.div(
                class_name="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"
            ),
            rx.el.div(
                rx.el.h3(movie["title"], class_name="font-bold text-white"),
                rx.el.p(
                    f"{movie['year']} • {movie['rating']}/10 ⭐",
                    class_name="text-sm text-gray-300",
                ),
                class_name="absolute bottom-0 left-0 p-4",
            ),
            class_name="absolute inset-0",
        ),
        on_click=lambda: AppState.go_to_movie(movie["id"]),
        class_name="group relative aspect-[2/3] w-full h-auto rounded-lg overflow-hidden shadow-lg transform transition-transform duration-300 ease-in-out hover:scale-105 hover:shadow-white/20 cursor-pointer bg-gray-800",
    )


def category_row(category_name: str, movies: list[Movie]) -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            category_name, class_name="text-3xl font-bold text-white mb-6 px-4 md:px-12"
        ),
        rx.el.div(
            rx.foreach(movies, movie_card),
            class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6 px-4 md:px-12",
        ),
        class_name="py-8 bg-black",
    )


def hero_section() -> rx.Component:
    from app.states.state import AppState

    return rx.cond(
        AppState.featured_movie,
        rx.el.div(
            rx.image(
                src=AppState.featured_movie["background_image_original"],
                class_name="absolute top-0 left-0 w-full h-full object-cover z-0 opacity-30",
            ),
            rx.el.div(
                class_name="absolute top-0 left-0 w-full h-full bg-gradient-to-t from-black to-transparent z-10"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        AppState.featured_movie["title"],
                        class_name="text-5xl md:text-7xl font-black text-white drop-shadow-lg",
                    ),
                    rx.el.div(
                        rx.el.p(
                            AppState.featured_movie["year"], class_name="font-semibold"
                        ),
                        rx.el.span("•", class_name="mx-2"),
                        rx.el.p(
                            AppState.featured_movie["genres"].join(", "),
                            class_name="font-semibold",
                        ),
                        class_name="flex items-center text-gray-300 mt-4",
                    ),
                    rx.el.p(
                        AppState.featured_movie["summary"],
                        class_name="mt-4 max-w-2xl text-lg text-gray-200 drop-shadow-md",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("play", class_name="mr-2"),
                            "Play",
                            class_name="flex items-center bg-white text-black font-bold px-8 py-3 rounded-md hover:bg-gray-200 transition-colors",
                        ),
                        rx.el.button(
                            rx.icon("info", class_name="mr-2"),
                            "More Info",
                            class_name="flex items-center bg-gray-700/60 text-white font-bold px-8 py-3 rounded-md hover:bg-gray-600/80 transition-colors",
                            on_click=lambda: AppState.go_to_movie(
                                AppState.featured_movie["id"]
                            ),
                        ),
                        class_name="mt-8 flex space-x-4",
                    ),
                    class_name="animate-fade-in-up",
                ),
                class_name="relative z-20 container mx-auto px-4 md:px-12 flex items-center h-full",
            ),
            class_name="relative w-full h-[70vh] flex items-center pb-12 pt-24 text-white overflow-hidden bg-black",
        ),
        rx.el.div(
            rx.el.div(class_name="animate-pulse bg-gray-800 w-full h-full"),
            class_name="relative w-full h-[70vh] flex items-center pb-12 pt-24 text-white overflow-hidden bg-black",
        ),
    )