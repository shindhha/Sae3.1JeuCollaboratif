@ECHO OFF
chcp 65001 > NUL
rem Utilisation de UTF-8

SET INSTALLDIR=%APPDATA%\SAE\
SET CURDIR=%cd%
SET RESDIREXTRACT=%INSTALLDIR%\RES\

rem On teste pour voir si le chemin d'installation est sur un disque réseau
rem On teste pour voir si le chemin d'installation est sur un disque réseau
SET TESTUNC=%INSTALLDIR:~0,2%
IF %TESTUNC%==\\ (
	echo WARN : Installation directory is located with UNC path. Moving to %CURDIR%\softwareSource.
	SET INSTALLDIR=%CURDIR%\softwareSource
	SET RESDIREXTRACT=%CURDIR%\softwareSource\RES\
)
 
SET TESTUNC=%INSTALLDIR:~0,2%
IF %TESTUNC%==\\ (
	echo FATAL : Alternative installation directory is located with UNC path. Aborting . . .
	pause
	exit
)

rem extraction des composants dnas un dossier temporaire
IF NOT EXIST %RESDIREXTRACT% mkdir %RESDIREXTRACT%
tar -xf %CURDIR%\res.zip -C %INSTALLDIR%\RES\

IF NOT EXIST %INSTALLDIR%\Python\ goto installPython
echo Python is already installed, skipping. . .
:afterPython

echo.

IF NOT EXIST %INSTALLDIR%\Client\ goto installClient
echo The applicant app is already installed, skipping. . .
:afterClient

goto end



:installPython
echo Python is not installed, installing. . .
mkdir %INSTALLDIR%\Python\
tar -xf %RESDIREXTRACT%\python-3108.zip -C %INSTALLDIR%\Python\
goto afterPython

:installClient
echo Installing applicant app. . .
rem Extraction du programme dans le dossier
mkdir %INSTALLDIR%\Client\
tar -xf %RESDIREXTRACT%\client.zip -C %INSTALLDIR%\Client\

echo.

rem creation du bat de lancement du client
echo Creating the applicant launcher. . .
IF NOT EXIST %CURDIR%\Launcher\ mkdir %CURDIR%\Launcher\

echo cd %INSTALLDIR%\Client\ > %CURDIR%\Launcher\LaunchApplicant.bat 
echo %INSTALLDIR%\Python\python.exe %INSTALLDIR%\Client\client.py >> %CURDIR%\Launcher\LaunchApplicant.bat

echo Location of the launcher : %CURDIR%\Launcher\LaunchApplicant.bat

IF NOT EXIST %CURDIR%\Uninstaller\ mkdir %CURDIR%\Uninstaller\

rem ------------- Création du desinstalleur ----------------
echo @ECHO OFF > %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo chcp 65001 ^> NUL >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo rem Supression du client >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo rmdir /S /Q %INSTALLDIR%\Client >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo del /Q %CURDIR%\Launcher\LaunchApplicant.bat >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo echo The applicant app has been uninstalled ! >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo. >> %CURDIR%\Uninstaller\UninstallerApplicant.bat

echo rem Check si le SERVEUR est installé ou non pour faire une supression totale ^(python et dossiers des scripts de lancement/desinstall^) >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo IF EXIST %INSTALLDIR%\Server\ goto simpleDesinstall >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo echo Uninstalling python. . . >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo rmdir /S /Q %INSTALLDIR%\Python >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo rmdir /S /Q %CURDIR%\Launcher >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo rem On crée un nouveau cmd pour libérer ce fichier et éviter un crash du cmd car le fichier n'existe plus >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo rem On change de dossier pour éviter un crash du cmd >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo cd .. >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo start cmd /k "@ECHO OFF && chcp 65001 > NUL && rmdir /S /Q %CURDIR%\Uninstaller && exit" >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo goto end >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo. >> %CURDIR%\Uninstaller\UninstallerApplicant.bat

echo :simpleDesinstall >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo rem On crée un nouveau cmd pour libérer ce fichier et éviter un crash du cmd car le fichier n'existe plus >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo start cmd /k "@ECHO OFF && chcp 65001 > NUL && del /Q %CURDIR%\Uninstaller\UninstallerApplicant.bat && exit" >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo. >> %CURDIR%\Uninstaller\UninstallerApplicant.bat

echo :end >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
echo pause >> %CURDIR%\Uninstaller\UninstallerApplicant.bat
rem ------------- Création du desinstalleur ----------------

echo Location of the applicant uninstaller : %CURDIR%\Uninstaller\UninstallerApplicant.bat

goto afterClient

:end
rem Supression du dossier temporaire contanant les composants
rmdir /S /Q %RESDIREXTRACT%
echo.
echo Press any key to exit . . . 
pause > NUL

