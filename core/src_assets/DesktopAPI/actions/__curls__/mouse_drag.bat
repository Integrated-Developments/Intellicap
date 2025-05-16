REM Drag Mouse
curl -X POST -H "Content-Type: application/json" ^
-d "{\"action\": \"mouse\", \"api_key\": \"666\", \"args\": {\"function\": \"drag\", \"x\": 800, \"y\": 600, \"duration\": 1}}" ^
https://amused-molly-unified.ngrok-free.app/actions

pause