# -*- coding: utf-8 -*-
import numpy as np

from skimage import io
from skimage.color import rgb2gray
from skimage.transform import pyramid_gaussian
from skimage.filters import threshold_otsu, threshold_adaptive
from skimage import measure
from skimage import img_as_float
from scipy.ndimage import gaussian_filter
from skimage.morphology import reconstruction
from skimage.feature import daisy
from skimage import transform as tf
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)

from matplotlib import pyplot as plt

############# Input layer ##########################
def read_file(src_file ,dst_file):
    """ Read files and convert to grey"""
    src = io.imread(src_file ,as_grey=True) # query image
    dst = io.imread(dst_file ,as_grey=True) #training image
    print("this works") 
    return(src, dst)


############# Image pre-processing layer ##########################
def create_image_pyramid(img, downscale_dim=2, pyramid_layer=3):
    # I put in some automatic values for the definition call. I need to check that they actually work.
    """ Create image pyramid"""


    pyramid = tuple(pyramid_gaussian(pyramid_in, downscale=downscale_dim))

    """ Check pyramid results """
    #Also need to put some test cases that check that downscale_dim and pyramid_layer are correct values.

    return(pyramid)

def subtract_background(img):
    """ Subtract background"""

    # Convert to float: Important for subtraction later which won't work with uint8
    """ image 1 """
    image = gaussian_filter(image, 1)

    seed = np.copy(image)
    seed[1:-1, 1:-1] = image.min()
    mask = image

    dilated = reconstruction(seed, mask, method='dilation')

    img_background_subtracted = image - dilated

    return(img_background_subtracted)



def create_binary(img):
    """ Create global binary """

    global_thresh = threshold_otsu(img)
    binary_global = img > global_thresh
    
    return(binary_global)

def measure_contours(img):
    # Find contours at a constant value of 0.8
    contours = measure.find_contours(contour_in, 0.8, fully_connected='high')
    
    return(contours)

def show_contours(img, contours):
    # Display the image and plot all contours found
    fig, ax = plt.subplots()
    ax.imshow(contour_in, interpolation='nearest', cmap=plt.cm.gray)

    ax.imshow(contour_in2, interpolation='nearest', cmap=plt.cm.gray)

    for n, contour in enumerate(contours):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

    for n, contour in enumerate(contours2):
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
                
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(8, 2.5))

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.show()

################ Feature extraction layer ##############################

def daisy_extractor(img):
    """ Use daisy binary descriptor to extract features"""
    descs, descs_img = daisy(img, step=180, radius=58, rings=2, histograms=6,
                             orientations=8, visualize=True)
    return(descs,descs_img)

def orb_extractor(img, n_keypoints=100):
    """Try orb binary descriptor using binaries created by Otsu's method."""

    descriptor_extractor = ORB(n_keypoints)

    """ Extract descriptors for the original images """
    
    descriptor_extractor.detect_and_extract(img)
    keypoints = descriptor_extractor.keypoints
    descriptors = descriptor_extractor.descriptors

    return(keypoints, descriptors)

def match_descriptors(descriptor1, descriptor2):

    matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)
    
    return(matches12)

def plot_matches(src, dst, src_keypoints, dst_keypoints, matches_src_dst):

    fig, ax = plt.subplots(nrows=3, ncols=1)

    plt.gray()

    plot_matches(ax[0], src, dst, src_keypoints, dst_keypoints, matches_src_dst)

    ax[0].axis('off')

    plt.show()


################### Estimate Transform #######################

def estimate_transform(src, dst):
    """ Create source and destination feature match coordinates"""

    src = np.array([keypoints1[elem] for elem in matches12[:,0]])
    dst = np.array([keypoints2[elem] for elem in matches12[:,1]])

    """ Estimate transform
    Available transformations:
    (‘similarity’, ‘affine’, ‘piecewise-affine’, ‘projective’, ‘polynomial’)
    """

    tform = tf.estimate_transform('similarity', src, dst)

    """ Error check transform (should return True)"""
    assert  np.allclose(tform.inverse(tform(src)), src) == False

    return(tform)

################### Apply Transform ########################

def apply_transform(src, tform):
    """ Warp image """

    warped = tf.warp(src, inverse_map=tform.inverse) ### Since I'm using the inverse transform, should I apply this to dst?
    
    return(warped)
