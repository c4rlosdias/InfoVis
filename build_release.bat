@echo off

set "ZIP=%1"

mkdir ".\releases\InfoVis"

copy ".\__init__.py" ".\releases\InfoVis"
copy ".\auth.py" ".\releases\InfoVis"

xcopy ".\modules" ".\releases\InfoVis\modules" /E /I /Y
xcopy ".\data" ".\releases\InfoVis\data" /E /I /Y
xcopy ".\libs311" ".\releases\InfoVis\libs311" /E /I /Y
xcopy ".\libs313" ".\releases\InfoVis\libs313" /E /I /Y
xcopy ".\resources" ".\releases\InfoVis\resources" /E /I /Y

powershell -command "Compress-Archive -Path '.\releases\InfoVis' -DestinationPath '.\releases\%ZIP%.zip' -Force"

echo ZIP criado com sucesso!
pause
