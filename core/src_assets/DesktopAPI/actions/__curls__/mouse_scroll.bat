REM Scroll Mouse
curl -X POST -H "Content-Type: application/json" ^
-d "{\"action\": \"mouse\", \"api_key\": \"666\", \"args\": {\"function\": \"scroll\", \"amount\": 10}}" ^
https://amused-molly-unified.ngrok-free.app/actions

pause