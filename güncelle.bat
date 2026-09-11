@echo off
chcp 65001 > nul
echo Git Otomatik Push Islemi Baslatiliyor...
echo.

:: Proje dizinine gecis yap
cd /d "C:\Claude\sseyyidmuhammedmaliki"

:: Tum degisiklikleri sahneye ekle
git add .

:: Commit mesajini al (bos birakilirsa varsayilan mesaj kullanilir)
set /p commit_msg="Commit mesajini girin (Varsayilan: Otomatik guncelleme): "
if "%commit_msg%"=="" set commit_msg=Otomatik guncelleme

:: Commit olustur
git commit -m "%commit_msg%"

:: Remote adresini kontrol et ve yoksa ekle
git remote remove origin 2>nul
git remote add origin https://github.com/tatesci/seyyidmuhammedmaliki.git

:: Ana dala push et (main/master kontrolu)
git branch -M main
git push -u origin main

echo.
echo ========================================
echo Degisiklikler GitHub'a basariyla gonderildi!
echo ========================================
pause