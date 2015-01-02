#!/bin/bash
rm ui_*.py
rm ui_*.pyc
pyside-uic weathertrek.ui > ui_weathertrek.py
pyside-uic locationFrame.ui > ui_locationFrame.py
