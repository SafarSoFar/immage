# Immage

Immage - an image analysis tool (steganography) and hidden data extractor. The tool applies different steganography algorithms (pixel color manipulations and bit manipulations) on the imported image in order to find hidden artifacts.

Written in Python. 
GUI - Tkinter.
GUI Design - Figma, Tkdesigner.


Linux v0.1 build : Python 3.9.19, 
pyinstaller execution config: pyinstaller --onefile --name immage --hidden-import='PIL._tkinter_finder' --add-data "assets/*.png:assets/" immage_app.py

