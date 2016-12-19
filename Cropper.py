#! /usr/bin/python

__author__ = "Ellen Fu"
__date__ = "Dec 19, 2016"

"""
Description:
Script to crop pictures of plates into nice little squares for further R script analyses.
Cropped files will be saved in a folder named "cropped" within your current pictures' folder.

Instructions for Mac:
	1. Go to folder directly containing the pictures
	2. Right click on folder, hold alt/option and select 'Copy ___ as pathname'
	3. Paste the pathname into the single quotations below, SAVE THIS FILE
	5. Go to Cropper.py in Finder, right click on Cropper.py and copy its pathname (see step 2)
	6. Open terminal
	7. If you haven't done so before, run this line without quotations: "pip install Pillow"
	8. Type "cd " without quotations and paste Cropper.py's pathname
		e.g. python /Users/your_username/Documents/Cropper.py
		** Python 2.7 needs to be installed to work
"""

file_directory = ''


import os
from PIL import Image

# The Cropper class contains the cropping methods and uses the files given to it by the
# FileManager
class Cropper:
	def __init__(self, dir):
		"""
		Initializes the Cropper and instantiates all instance variables, then calls
		all the cropping methods
		"""
		self.manager = FileManager(dir)
		self.images = self.manager.getImages()
		self.boundary_value = 200
		self.crop()

	def crop(self):
		"""
		Crops the images in the list gotten from the FileManager to squares
		"""
		for i in range(len(self.images)):
			self.images[i].rgbValues = self.get_rgb(self.images[i])
			self.crop_helper(self.images[i])

	def get_rgb(self, img):
		"""
		Returns the sum of RGB values at each pixel (shows brightness)
		"""
		rgb = []
		curr = img.load()
		for row in range(img.height):
			rgb.append([])
		rgb[0].append(curr[0,0])
		for row in range(img.height):
			for col in range(img.width):
				if (not (row==0 and col==0)):
					rgb[row].append(curr[col,row])

		for row in range(img.height):
			rgb[row] = [sum(tup) for tup in rgb[row]]

		return rgb

	def crop_helper(self, img):
		"""
		Contains the algorithm for cropping the image into a square
		"""
		midX = int(img.width/2)
		midY = int(img.height/2)

		maxXDia = 0
		maxYDia = 0
		maxindX = 0
		maxindY = 0

		radiiX = []
		radiiY = []



		for i in range(img.height):
			radiiX.append(self.find_x_boundary(img, midX, i))
			currDia = radiiX[-1][1] - radiiX[-1][0]
			if (currDia > maxXDia):
				maxXDia = currDia
				maxindX = len(radiiX)-1

		currDia = 0
		for i in range(img.width):
			radiiY.append(self.find_y_boundary(img, i, midY))
			currDia = radiiY[-1][1] - radiiY[-1][0]
			if (currDia > maxYDia):
				maxYDia = currDia
				maxindY = len(radiiY)-1

		left = radiiX[maxindX][0]
		right = radiiX[maxindX][1]
		top = radiiY[maxindY][0]
		bottom = radiiY[maxindY][1]

		img2 = img.crop((left, top, right, bottom))
		print (str(img.name) + " will be cropped at: left = " + str(left) + ", top = " + str(top) + ", right = " + str(right) + ", bottom = " + str(bottom))
		img2.save(self.manager.dir + "/" + img.name, "jpeg")

	def find_x_boundary(self, img, x, y):
		"""
		Finds the left and right boundaries of the plate
		"""
		initX = x
		counter = 0
		while x < img.size[0] and counter < 9:
			if (img.rgbValues[y][x] < self.boundary_value):
				counter += 1
			else:
				counter = 0
				x += 1
		right = x

		x = initX
		counter = 0
		while x >= 0 and counter < 9:
			if (img.rgbValues[y][x] < self.boundary_value):
				counter += 1
			else:
				counter = 0
				x -= 1
		left = x

		return [left, right]

	def find_y_boundary(self, img, x, y):
		"""
		Finds the top and bottom boundaries of the plate
		"""
		initY = y
		counter = 0
		while y < img.size[1] and counter < 9:
			if (img.rgbValues[y][x] < self.boundary_value):
				counter += 1
			else:
				counter = 0
				y += 1
		if (y != 1200):
			bottom = y
		else:
			bottom = initY

		y = initY
		counter = 0
		while y >= 0 and counter < 9:
			if (img.rgbValues[y][x] < self.boundary_value):
				counter += 1
			else:
				counter = 0
				y -= 1

		if (y != -1):
			top = y
		else:
			top = initY

		return [top, bottom]

			



class FileManager:
	def __init__(self, dir):
		"""
		Initializes the array of files (images) in the given directory
		"""
		self.files = []
		self.images = []
		print("Files: " + str(os.listdir(dir)))
		for file in os.listdir(dir):
			if file.endswith("jpg") or file.endswith("JPG") or file.endswith("jpeg") or file.endswith("JPEG"):
				self.files.append(file)
				img = Image.open(os.path.join(dir, file))
				img.name = file
				self.images.append(img)
				print file + ' is added to the queue...'
			else:
				raise UnexpectedFileException('There''s a non-JPG file in this directory, or there is an invisible .DS_Store file. If the latter case, please create a new folder and move all images to that folder and retry with the new path.')

		os.makedirs(dir + "/cropped")
		self.dir = dir + "/cropped"

	def getImages(self):
		"""
		Returns the array of files in the given directory
		"""
		return self.images



class UnexpectedFileException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


if __name__ == '__main__':
	print 'Cropping images...'
	cropper = Cropper(file_directory)
	print 'All images cropped!'