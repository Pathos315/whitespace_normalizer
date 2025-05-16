@echo off
echo Building Whitespace Normalizer executable with direct command...

REM Ensure we're using Poetry environment
call poetry install

REM Create icon
call create_icon.bat

REM Build the executable directly with a single command
call poetry run pyinstaller ^
--name "Whitespace Normalizer" ^
--icon=app_icon.ico ^
--windowed ^
--add-data "LICENSE;." ^
--hidden-import=pyspellchecker ^
--version-file=file_version_info.txt ^
--clean ^
--noconfirm ^
main.py

echo Build complete!
echo The executable can be found in the dist folder.
pause
