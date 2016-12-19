# CropSquare
Crops images of a culture plate into a tight square at the edges of the plate. Used for further analyses (such as R scripts for MICs, FoGs, etc.).

# Requirements
- Python 2.7 or above
- install Pillow library ("pip install Pillow")

# Description:
Script to crop pictures of plates into nice little squares for further R script analyses.
Cropped files will be saved in a folder named "cropped" within your current pictures' folder.

# Instructions for Mac:
	1. Go to folder directly containing the pictures
	2. Right click on folder, hold alt/option and select 'Copy ___ as pathname'
	3. Paste the pathname into the single quotations below, SAVE THIS FILE
	5. Go to Cropper.py in Finder, right click on Cropper.py and copy its pathname (see step 2)
	6. Open terminal
	7. If you haven't done so already, run this line without quotations: "pip install Pillow"
	8. Type "python " without quotations and paste Cropper.py's pathname
		e.g. python /Users/your_username/Documents/Cropper.py
		** Python 2.7 needs to be installed to work
