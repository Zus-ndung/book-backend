# book_app_backend

## Requirement
1. Python
2. ngrok
3. sqlite browser

## Summary technical idea
1. Database hosting locally with sqlite
2. API with Fastapi
3. Authentication with jwt
4. Publishing host port with ngrok

server host
```bash
pip install -r requirements.txt
uvicorn main:app
```

tunnel forward
```bash
ngrok http 8000
```