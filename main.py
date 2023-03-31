import logging
import json

from fastapi import FastAPI, Request, Response, HTTPException, status

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.post('/', status_code=status.HTTP_202_ACCEPTED)
async def telegram_webhook(request: Request):
    payload = await request.body()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty payload")
    json_payload = payload.decode('utf-8')
    json_payload = json.loads(json_payload)
    logging.info(f"Received JSON payload: {json_payload}")
    logging.info(f"Type of JSON payload: {type(json_payload)}")
    return Response(status_code=status.HTTP_202_ACCEPTED)
