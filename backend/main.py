from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from resources import auth, restaurant, meal, order

app = FastAPI()
app.include_router(auth.router)
app.include_router(restaurant.router)
app.include_router(meal.router)
app.include_router(order.router)


origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
