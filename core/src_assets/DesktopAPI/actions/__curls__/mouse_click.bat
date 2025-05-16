REM Click Mouse
curl -X POST -H "Content-Type: application/json" ^
-d "{\"action\": \"mouse\", \"api_key\": \"666\", \"args\": {\"function\": \"click\", \"x\": 500, \"y\": 300, \"button\": \"left\"}}" ^
https://amused-molly-unified.ngrok-free.app/actions

pause