@echo off
git add .
git commit -m "Deployment ready, Kaggle dataset integration, and UI update"
git branch -M main
git remote | findstr origin >nul
if %errorlevel% equ 0 (
    git remote set-url origin https://github.com/Sandhyasakthi/customer_satisfaction
) else (
    git remote add origin https://github.com/Sandhyasakthi/customer_satisfaction
)
echo Pushing to GitHub...
git push -u origin main
