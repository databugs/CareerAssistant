from fastapi import FastAPI, Response
from http import HTTPStatus

app = FastAPI()

@app.post('/', status_code=HTTPStatus.ACCEPTED)
async def telegram_webhook(request):
    payload = await request
    print(payload)
    print(type(payload))
    return payload