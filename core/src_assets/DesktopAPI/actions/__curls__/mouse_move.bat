REM Move Mouse
curl -X POST -H "Content-Type: application/json" ^
-d "{\"action\": \"mouse\", \"api_key\": \"666\", \"args\": {\"function\": \"move\", \"x\": 500, \"y\": 300}}" ^
https://amused-molly-unified.ngrok-free.app/actions
pause