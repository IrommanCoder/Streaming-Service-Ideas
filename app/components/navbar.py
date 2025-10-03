import reflex as rx
from app.states.state import AppState


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("apple", class_name="h-8 w-8 text-white"),
                    href="/",
                    class_name="flex items-center space-x-2",
                ),
                rx.el.div(
                    rx.el.a(
                        "Home",
                        href="/",
                        class_name="text-gray-300 font-semibold hover:text-white transition-colors",
                    ),
                    class_name="hidden md:flex items-center space-x-6 ml-10",
                ),
                class_name="flex items-center space-x-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500",
                    ),
                    rx.el.input(
                        placeholder="Search titles...",
                        on_change=AppState.search_movies.debounce(300),
                        default_value=AppState.query,
                        class_name="bg-gray-900/80 text-white pl-10 pr-4 py-2 rounded-md w-64 focus:outline-none focus:ring-2 focus:ring-gray-600 transition-all",
                    ),
                    class_name="relative",
                ),
                rx.icon(
                    "bell",
                    class_name="text-gray-300 h-6 w-6 cursor-pointer hover:text-white transition-colors",
                ),
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=John",
                    class_name="h-8 w-8 rounded-md cursor-pointer",
                ),
                class_name="flex items-center space-x-6",
            ),
            class_name="container mx-auto px-4 md:px-12 flex justify-between items-center",
        ),
        class_name="fixed top-0 left-0 w-full p-4 bg-black/50 backdrop-blur-md z-50 transition-all duration-300",
    )