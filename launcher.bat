@echo off

:top

cls
title Tetris Launcher
echo #### #### #### #### Tetris Launcher #### #### #### ####

py %~dp0Tetris.py

echo #### #### #### #### Run ended #### #### #### ####

echo Restarting...
pause
goto top