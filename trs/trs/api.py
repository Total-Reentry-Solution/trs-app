from ninja import NinjaAPI
import asyncio

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return "Hello world"


@api.get("/say-after")
async def say_after(request, delay: int, word: str):
    await asyncio.sleep(delay)
    return {"saying": word}
