@ECHO OFF
chcp 65001 > NUL
rem Utilisation de UTF-8

SET INSTALLDIR=%APPDATA%\SAE\
SET CURDIR=%cd%
SET RESDIREXTRACT=%INSTALLDIR%\RES\

rem extraction des composants dnas un dossier temporaire
IF NOT EXIST %RESDIREXTRACT% mkdir %RESDIREXTRACT%
tar -xf %CURDIR%\res.zip -C %INSTALLDIR%\RES\

IF NOT EXIST %INSTALLDIR%\Python\ goto installPython
echo Python is already installed, skipping. . .
:afterPython

echo.

IF NOT EXIST %INSTALLDIR%\Server\ goto installServer
echo The recruiter app is already installed, skipping. . .
:afterServer

goto end


:installPython
echo Python is not installed, installing. . .
mkdir %INSTALLDIR%\Python\
tar -xf %RESDIREXTRACT%\python-3108.zip -C %INSTALLDIR%\Python\
goto afterPython

:installServer
echo Installing recruiter app. . .
rem Extraction du programme dans le dossier
mkdir %INSTALLDIR%\Server\
tar -xf %RESDIREXTRACT%\server.zip -C %INSTALLDIR%\Server\

echo.

rem creation du bat de lancement du serveur
echo Creating the recruiter launcher
IF NOT EXIST %CURDIR%\Launcher\ mkdir %CURDIR%\Launcher\

echo cd %INSTALLDIR%\Server\ > %CURDIR%\Launcher\LaunchRecruiter.bat
echo %INSTALLDIR%\Python\python.exe %INSTALLDIR%\Server\server.py >> %CURDIR%\Launcher\LaunchRecruiter.bat

echo Location of the launcher : %CURDIR%\Launcher\LaunchRecruiter.bat

IF NOT EXIST %CURDIR%\Uninstaller\ mkdir %CURDIR%\Uninstaller\

rem ------------- Création du desinstalleur ----------------
echo @ECHO OFF > %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo chcp 65001 ^> NUL >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo rem Supression du serveur >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo rmdir /S /Q %INSTALLDIR%\Server >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo del /Q %CURDIR%\Launcher\LaunchRecruiter.bat >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo echo The recruiter app has been uninstalled ! >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo. >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat

echo rem Check si le CLIENT est installé ou non pour faire une supression totale ^(python et dossiers des scripts de lancement/desinstall^) >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo IF EXIST %INSTALLDIR%\Client\ goto simpleDesinstall >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo echo Uninstalling python. . . >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo rmdir /S /Q %INSTALLDIR%\Python >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo rmdir /S /Q %CURDIR%\Launcher >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo rem On crée un nouveau cmd pour libérer ce fichier et éviter un crash du cmd car le fichier n'existe plus >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo rem On change de dossier pour éviter un crash du cmd >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo cd .. >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo start cmd /k "@ECHO OFF && chcp 65001 > NUL && rmdir /S /Q %CURDIR%\Uninstaller && exit" >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo goto end >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo. >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat

echo :simpleDesinstall >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo rem On crée un nouveau cmd pour libérer ce fichier et éviter un crash du cmd car le fichier n'existe plus >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo start cmd /k "@ECHO OFF && chcp 65001 > NUL && del /Q %CURDIR%\Uninstaller\UninstallerRecruier.bat && exit" >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo. >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat

echo :end >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
echo pause >> %CURDIR%\Uninstaller\UninstallerRecruiter.bat
rem ------------- Création du desinstalleur ----------------

echo Loccation of the uninstaller : %CURDIR%\Uninstaller\UninstallerRecruiter.bat
goto afterServer

:end
rem Supression du dossier temporaire contanant les composants
rmdir /S /Q %RESDIREXTRACT%
echo.
echo Press any key to exit . . . 
pause > NUL
