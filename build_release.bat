@echo off

set "ZIP=%1"

mkdir ".\releases\OG_Tools"

copy ".\__init__.py" ".\releases\OG_Tools"
copy ".\panels.py" ".\releases\OG_Tools"
copy ".\operators.py" ".\releases\OG_Tools"
copy ".\properties.py" ".\releases\OG_Tools"
copy ".\data.py" ".\releases\OG_Tools"


xcopy ".\libs" ".\releases\OG_Tools\libs" /E /I /Y
xcopy ".\resources" ".\releases\OG_Tools\resources" /E /I /Y

powershell -command "Compress-Archive -Path '.\releases\OG_Tools' -DestinationPath '.\releases\%ZIP%.zip' -Force"


echo ZIP criado com sucesso!
pause
