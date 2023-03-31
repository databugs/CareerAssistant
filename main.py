from fastapi import FastAPI, Response
from http import HTTPStatus

app = FastAPI()

@app.post('/', status_code=HTTPStatus.ACCEPTED)
async def telegram_webhook(request: Response):
    payload = await request.json()
    print(payload)
    return payload