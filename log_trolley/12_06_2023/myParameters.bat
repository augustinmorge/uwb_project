@echo off
:menu
cls
echo ---- Rejeux pour DelphINS ----
echo.

rem Ajout des paramètres à ajouter à la fin du XML

set "xmlFile=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\12_06_2023\12_06_2023_PH-2248_A_POSTPROCESSING-parameters.xml"

findstr "<advancedOutputs" %xmlFile% > nul
if %errorlevel% equ 0 (
    echo La balise "<advancedOutputs>" existe deja dans le fichier XML. Les lignes ne seront pas ajoutees.
    echo Execution du programme...
    echo.
    "C:\Program Files (x86)\iXblue\Delph INS Research & Development\Postproins\PostproIns.exe" "C:\Users\augustin.morge\Documents\uwb_project\log_trolley\12_06_2023\12_06_2023_PH-2248_A_POSTPROCESSING-parameters.xml"
    goto end
)

set "tempFile=%temp%\temp.xml"

rem Supprimer la dernière ligne du fichier XML en la filtrant vers un fichier temporaire
type %xmlFile% | findstr /V "</postproInsParameters>" > %tempFile%

rem Ajouter les lignes spécifiées à la fin du fichier temporaire
echo ^<advancedOutputs enabled="true"^> >> %tempFile%
echo    ^<output name="RANGE_KAL_MEAS" enabled="true"/^> >> %tempFile%
echo    ^<output name="POS_KAL_MEAS" enabled="true"/^> >> %tempFile%
echo ^</advancedOutputs^> >> %tempFile%
echo ^</postproInsParameters^> >> %tempFile%

rem Remplacer le fichier XML d'origine par le fichier temporaire
move /Y %tempFile% %xmlFile%

echo.
echo Les lignes ont ete ajoutees avec succes au fichier XML.
echo Execution du programme...
echo.

rem Execution du fichier
"C:\Program Files (x86)\iXblue\Delph INS Research & Development\Postproins\PostproIns.exe" "C:\Users\augustin.morge\Documents\uwb_project\log_trolley\12_06_2023\12_06_2023_PH-2248_A_POSTPROCESSING-parameters.xml"
rem pause 

:end

rem Demander à l'utilisateur s'il souhaite rejouer le programme
set /p "retry=Voulez-vous rejouer le programme ? (O/Y/ENTER for yes): "
if /i "%retry%"=="O" goto menu
if /i "%retry%"=="Y" goto menu
if /i "%retry%"=="" goto menu

pause