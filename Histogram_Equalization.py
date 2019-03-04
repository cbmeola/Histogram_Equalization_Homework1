# Charlotte Meola
# ECE 5470, Digital Image Processing
# Homework 1: Histogram Equalization Assignment

# "Histogram_Equalization" generates a histogram of original pixel intensity and performs histogram
# equalization for (1) a black and white image and (2) a color image.  Returns images of the
# original histogram, equalized histogram, original image, and equalized image to project folder.
#-----------------------------------------------------------------------------------------


import cv2, imageio
from matplotlib import pyplot as plt
import numpy as np


# Function "makeHistogram" first returns the size of the inputted image for the user.
# Then, it maps an image and returns a histogram for the inputted image.
# Image histogram plot is saved as a .jpg in the project folder.
def makeHistogram(imgFileName):

    # Open the image to get name, then finds dimensions and # of channels:
    print("\nApplying histogram equalization to '" + imgFileName + "'.")
    height, width, channels = imageio.imread(imgFileName).shape
    print("Width of '" + imgFileName + "' = %d" % (width))
    print("Height of '" + imgFileName + "' = %d" % (height))

    # Create a (flattened) histogram for the image and save histogram as image:
    image = cv2.imread(imgFileName)
    channels = cv2.split(image)
    # If image is in color, histogram will display three channels in histogram plot.
    colors = ("b", "g", "r")
    plt.title("Histogram for '" + imgFileName[:-4] + "' Pixel Intensity")
    plt.xlabel("Intensity")
    plt.ylabel("Number of Pixels")

    # Finds and plots the image histogram.
    for (chan, color) in zip(channels, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        plt.plot(hist, color = color)
        # Limits pixel values from 0 - 256:
        plt.xlim([0, 256])
        # Plot is saved in project folder for viewing:
        plt.savefig("" + imgFileName[:-4] + "_histogram.jpg")

    # Clear the plot data, so that new histogram may be plotted for next image:
    plt.cla()


# Function "equalizeImage" open an image, copies it, gets the cumulative sum of
# the histogram data, and uses this value to calculate the CDF of image pixel data.
# Outputs an equalized image to the project folder, then calls the makeHistogram
# function to create a histogram of the new, equalized image.
def equalizeImage(imgFileName):

    # Opens image and copies all pixel data:
    image = cv2.imread(imgFileName)
    data = image.copy()
    hist, bins = np.histogram(data, 256, density = True)
    # Using sum to calculate CDF of image data:
    cdf = hist.cumsum()
    cdf = 255 * cdf / cdf[-1]
    img_eq = np.interp(data, bins[:-1], cdf)
    re = img_eq.reshape(image.shape)
    # Defines new image name:
    newImgFileName = imgFileName[:-4] + "_equalized.jpg"
    # Saves new, equalized image to project folder:
    cv2.imwrite(newImgFileName, re)

    # Calls the previous function to make one more histogram for
    # the equalized image:
    makeHistogram(newImgFileName)


# MAIN CODE & FUNCTION CALLS:----------------------------------------

# Calling the functions to be used on a black and white image:
makeHistogram('astronaut.jpg')
equalizeImage('astronaut.jpg')

# Calling the functions to be used on a color image:
makeHistogram('aurora.jpg')
equalizeImage('aurora.jpg')


