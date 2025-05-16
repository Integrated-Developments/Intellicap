## ----- Local Flask ----- ##

curl -X POST http://127.0.0.1:5000/screenshot -H "Content-Type: application/json" -d '{"key": "unique_request_id", "args": {}}' --output retrieved_screenshot.png

## ----- Ngrok ----- ##

curl -X POST https://your-ngrok-id.ngrok.io/screenshot -H "Content-Type: application/json" -d '{"key": "unique_request_id", "args": {}}' --output retrieved_screenshot.png