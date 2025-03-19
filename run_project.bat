@echo off
echo 🚀 Starting Project...

:: Step 1: Start MySQL Server (If Not Running)
echo 🔄 Checking MySQL...
net start MySQL80 2>nul
if %ERRORLEVEL% == 2 (
    echo ✅ MySQL is already running.
) else (
    echo ✅ MySQL started successfully.
)

:: Step 2: Compile Java (Password Encryptor)
echo 🔄 Compiling Java...
javac -cp . PasswordEncryptor.java
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Java compilation failed!
    exit /b
)
echo ✅ Java compiled successfully.

:: Step 3: Run Flask App
echo 🔥 Running Flask App...
start cmd /k "python app.py"

echo ✅ Project Running! Open in Browser: http://127.0.0.1:5000
pause
