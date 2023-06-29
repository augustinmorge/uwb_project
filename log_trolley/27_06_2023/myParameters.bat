@echo off

echo Creation de la copie du fichier xpfFile...
copy "%xpfFileAll%" "%~dp0\27_06_2023_PH-2248_A_POSTPROCESSING-ins_copy.xpf"

:menu

set "template.popudt=C:\Program Files (x86)\iXblue\Delph INS Research & Development\Templates\LBL.popudt"
set "template.gtd=C:\Program Files (x86)\iXblue\Delph INS Research & Development\Templates\LBL.gtd"

set "xmlFile=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\27_06_2023\27_06_2023_PH-2248_A_POSTPROCESSING-parameters.xml"

set "txtFileAll=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\27_06_2023\27_06_2023_PH-2248_A_POSTPROCESSING-ins.xpf.txt"
set "txtFileAnchor=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\27_06_2023\anchor_27_06_2023_PH-2248_A_POSTPROCESSING-ins.xpf.txt"
set "txtFileDbm=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\27_06_2023\dbm_27_06_2023_PH-2248_A_POSTPROCESSING-ins.xpf.txt"

set "xpfFileAll=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\27_06_2023\27_06_2023_PH-2248_A_POSTPROCESSING-ins.xpf"
set "xpfFileAnchor=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\27_06_2023\anchor_27_06_2023_PH-2248_A_POSTPROCESSING-ins.xpf.xpf"
set "xpfFileDbm=C:\Users\augustin.morge\Documents\uwb_project\log_trolley\27_06_2023\dbm_27_06_2023_PH-2248_A_POSTPROCESSING-ins.xpf.xpf"


cls
echo ---- Rejeux pour DelphINS ----
echo.

rem Ajout des parametres à ajouter à la fin du XML

findstr "<advancedOutputs" "%xmlFile%" > nul
if %errorlevel% equ 0 (
    echo La balise "<advancedOutputs>" existe deja dans le fichier XML. Les lignes ne seront pas ajoutees.
    echo Execution du programme...
    echo.
    goto run_program
)

set "tempFile=%temp%\temp.xml"

rem Supprimer la derniere ligne du fichier XML en la filtrant vers un fichier temporaire
type "%xmlFile%" | findstr /V "</postproInsParameters>" > "%tempFile%"

rem Ajouter les lignes specifiees à la fin du fichier temporaire
echo ^<advancedOutputs enabled="true"^> >> "%tempFile%"
echo    ^<output name="RANGE_KAL_MEAS" enabled="true"/^> >> "%tempFile%"
echo    ^<output name="POS_KAL_MEAS" enabled="true"/^> >> "%tempFile%"
echo ^</advancedOutputs^> >> "%tempFile%"
echo ^</postproInsParameters^> >> "%tempFile%"

rem Remplacer le fichier XML d'origine par le fichier temporaire
move /Y "%tempFile%" "%xmlFile%"

echo.
echo Les lignes ont ete ajoutees avec succes au fichier XML.

:run_program



@REM echo.
@REM echo Execution de UdtExporter.exe...
@REM cd /d "C:\Program Files (x86)\iXblue\Delph INS Research & Development"
@REM UdtExporter.exe /t "%template.popudt%" "%xpfFileAll%" "%txtFileAll%"
@REM echo.
@REM echo Exportation terminee.



@REM echo.
@REM echo Execution du programme Python...
@REM cd /d "C:\Users\augustin.morge\Documents\uwb_project\log_trolley"
@REM python separate_data.py
@REM echo.
@REM echo Programme Python termine.



@REM echo.
@REM echo Execution de GenericText2Xpf.exe...
@REM cd /d "C:\Program Files (x86)\iXblue\Delph INS Research & Development"
@REM GenericText2Xpf.exe /def "%template.gtd%" "%txtFileAnchor%" "%xpfFileAnchor%"
@REM @REM GenericText2Xpf.exe /def "%template.gtd%" "%txtFileDbm%" "%xpfFileDbm%"
@REM echo.
echo Importation terminee.



echo.
echo Execution de PostproIns.exe...
cd /d "C:\Program Files (x86)\iXblue\Delph INS Research & Development\Postproins"
PostproIns.exe "%xmlFile%"
echo.
echo Execution du programme terminee.



rem Demander à l'utilisateur s'il souhaite rejouer le programme
set /p "retry=Voulez-vous rejouer le programme ? (O/Y/ENTER for yes): "
if /i "%retry%"=="O" goto menu
if /i "%retry%"=="Y" goto menu
if /i "%retry%"=="" goto menu

pause
