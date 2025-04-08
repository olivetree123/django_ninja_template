from ninja import Redoc, NinjaAPI

from main.handlers.user import user_router

main_api = NinjaAPI(title="API Doc", docs=Redoc(), version="0.1.0")

main_api.add_router("user", user_router)
