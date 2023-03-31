from fastapi import FastAPI, Request, Response, HTTPException, status

app = FastAPI()

@app.post('/', status_code=status.HTTP_202_ACCEPTED)
async def telegram_webhook(request: Request):
    payload = await request.body()
    if not payload:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty payload")
    json_payload = payload.decode('utf-8')
    print(json_payload)
    print(type(json_payload))
    return Response(status_code=status.HTTP_202_ACCEPTED)
