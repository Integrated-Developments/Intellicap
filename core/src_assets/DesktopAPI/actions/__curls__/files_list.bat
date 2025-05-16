REM List Files
curl -X POST -H "Content-Type: application/json" ^
-d "{\"action\": \"files\", \"api_key\": \"666\", \"args\": {\"function\": \"list\", \"arg\": \"C:\\\\Users\\\\angry\\\\My Drive\\\\Shared GDrive\\\\1.] Dev Coding\"}}" ^
https://amused-molly-unified.ngrok-free.app/actions

pause
