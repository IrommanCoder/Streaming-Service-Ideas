import reflex as rx
from app.states.state import AppState
from app.states.movie_detail import MovieDetailState
from app.components.movie import hero_section, category_row, movie_card
from app.components.navbar import navbar


def search_results_grid() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            f"Search results for: {AppState.query}",
            class_name="text-3xl font-bold text-white mb-6 px-4 md:px-12",
        ),
        rx.el.div(
            rx.foreach(AppState.search_results, movie_card),
            class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6 px-4 md:px-12",
        ),
        class_name="py-8",
    )


def index() -> rx.Component:
    """The main page of the app."""
    return rx.el.main(
        navbar(),
        hero_section(),
        rx.el.div(
            rx.cond(
                AppState.is_searching,
                search_results_grid(),
                rx.el.div(
                    category_row("Trending Now", AppState.trending_now),
                    category_row("New Releases", AppState.new_releases),
                    category_row("Action & Adventure", AppState.action_movies),
                    category_row("Comedies", AppState.comedies),
                ),
            ),
            class_name="bg-black text-white",
        ),
        class_name="font-['Inter'] bg-black",
    )


def movie_details() -> rx.Component:
    return rx.el.main(
        navbar(),
        rx.cond(
            MovieDetailState.is_loading,
            rx.el.div(
                rx.spinner(class_name="text-red-500 h-12 w-12"),
                class_name="w-full h-screen flex items-center justify-center bg-black",
            ),
            rx.cond(
                MovieDetailState.movie,
                rx.el.div(
                    rx.el.div(
                        rx.image(
                            src=MovieDetailState.movie["background_image_original"],
                            class_name="absolute top-0 left-0 w-full h-full object-cover z-0 opacity-20",
                        ),
                        rx.el.div(
                            class_name="absolute top-0 left-0 w-full h-full bg-gradient-to-t from-black via-black/80 to-transparent z-10"
                        ),
                        class_name="relative w-full h-[50vh] text-white overflow-hidden",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=MovieDetailState.movie["large_cover_image"],
                                class_name="w-64 rounded-lg shadow-lg -mt-32 z-20",
                            ),
                            rx.el.div(
                                rx.el.h1(
                                    MovieDetailState.movie["title"],
                                    class_name="text-5xl font-black text-white drop-shadow-lg",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        MovieDetailState.movie["year"],
                                        class_name="font-semibold",
                                    ),
                                    rx.el.span("•", class_name="mx-2"),
                                    rx.el.p(
                                        f"{MovieDetailState.movie['rating']}/10 ⭐"
                                    ),
                                    rx.el.span("•", class_name="mx-2"),
                                    rx.el.p(
                                        MovieDetailState.movie["genres"].join(", ")
                                    ),
                                    class_name="flex items-center text-gray-400 mt-2",
                                ),
                                rx.el.p(
                                    MovieDetailState.movie["description_full"],
                                    class_name="mt-4 max-w-3xl text-gray-400",
                                ),
                                class_name="ml-8 text-white",
                            ),
                            class_name="flex items-start z-20",
                        ),
                        rx.el.h3(
                            "Downloads",
                            class_name="text-2xl font-bold text-white mt-8 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                MovieDetailState.movie["torrents"],
                                lambda torrent: rx.el.a(
                                    rx.icon("download"),
                                    f"{torrent['quality']} ({torrent['type']}) - {torrent['size']}",
                                    href=torrent["url"],
                                    class_name="flex items-center space-x-2 bg-gray-800 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors",
                                    target="_blank",
                                ),
                            ),
                            class_name="flex flex-wrap gap-4",
                        ),
                        rx.cond(
                            MovieDetailState.suggestions.length() > 0,
                            rx.el.div(
                                rx.el.h3(
                                    "More Like This",
                                    class_name="text-2xl font-bold text-white mt-12 mb-4",
                                ),
                                rx.el.div(
                                    rx.foreach(
                                        MovieDetailState.suggestions, movie_card
                                    ),
                                    class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6",
                                ),
                            ),
                        ),
                        class_name="relative container mx-auto px-4 md:px-12 py-8",
                    ),
                    class_name="bg-black",
                ),
                rx.el.div(
                    "Movie not found.", class_name="text-white text-center py-20"
                ),
            ),
        ),
        class_name="font-['Inter'] bg-black min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/style.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    title="Notflix - Watch TV Shows Online, Watch Movies Online",
    on_load=AppState.on_app_load,
)
app.add_page(
    movie_details,
    route="/movie/[id]",
    title="Movie Details",
    on_load=MovieDetailState.get_movie_details,
)