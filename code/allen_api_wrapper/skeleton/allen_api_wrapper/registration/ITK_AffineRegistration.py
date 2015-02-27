#!/usr/bin/env python
'''
ITK_AffineRegistration.py
Written by: Kristi Potter
Date: 2/19/15
Purpose: Registers a volume of images using itk. Based on the c++ examples, translated to python.
         http://itk.org/Wiki/ITK/Examples/Included/Registration
Input:   imageVolume (skimage.io.ImageCollection) : the volume of images to align.
Output:

'''
import sys, os
import warnings
warnings.filterwarnings("ignore")
import itk
import numpy as np


class Registrator():
    
    # -- init --
    def __init__(self, parent = None):
        print "Initialize"
        #super(AffineRegistration, self).__init__(parent)
        self.newVolume = []
        self.outputImages = []
        self.count = 1

        pixelType = itk.UC
        Dimension = 2

        # This line is what takes so long
        self.ImageType = itk.Image[pixelType, Dimension]
        self.ReaderType = itk.ImageFileReader[self.ImageType]
        
        # The transform that will map the fixed image into the moving image.
        TransformType = itk.AffineTransform[itk.D, 2]
        OptimizerType = itk.RegularStepGradientDescentOptimizer
        MetricType = itk.MeanSquaresImageToImageMetric[self.ImageType, self.ImageType]
        InterpolatorType = itk.LinearInterpolateImageFunction[self.ImageType, itk.D]
        RegistrationType = itk.ImageRegistrationMethod[self.ImageType, self.ImageType]
        
        # Create the components
        metric = MetricType.New()
        transform = TransformType.New()
        optimizer = OptimizerType.New()
        interpolator = InterpolatorType.New()
        self.registration = RegistrationType.New()

        self.registration.SetMetric( metric )
        self.registration.SetTransform( transform )
        self.registration.SetInterpolator( interpolator )
        
        # Configure the optimizer
        optimizer.SetMaximumStepLength( .1 )
        optimizer.SetMinimumStepLength( 0.01 )
        optimizer.SetNumberOfIterations( 200 )
        self.registration.SetOptimizer( optimizer )

        # Configure the transform
        initialParameters = transform.GetParameters()
        self.registration.SetInitialTransformParameters( initialParameters )

        ResampleFilterType = itk.ResampleImageFilter[self.ImageType,self.ImageType]
        self.resampler = ResampleFilterType.New()
        
        self.CastFilterType = itk.CastImageFilter[self.ImageType,self.ImageType]

        self.fixedImageReader = self.ReaderType.New()
        self.fixedImage = self.ImageType.New()

        self.movingImageReader = self.ReaderType.New()
        self.movingImage = self.ImageType.New()
        
        
    def setFixedImage(self, fileName):
        print "Set Fixed Image"
        self.fixedImageReader.SetFileName(fileName)
        self.fixedImageReader.Update()
        self.fixedImage = self.fixedImageReader.GetOutput()
        self.registration.SetFixedImage( self.fixedImage )
        self.registration.SetFixedImageRegion( self.fixedImage.GetLargestPossibleRegion() )
        self.resampler.SetSize( self.fixedImage.GetLargestPossibleRegion().GetSize() )
        self.resampler.SetOutputOrigin ( self.fixedImage.GetOrigin() )
        self.resampler.SetOutputSpacing( self.fixedImage.GetSpacing() )
        self.resampler.SetOutputDirection( self.fixedImage.GetDirection())
        self.resampler.SetDefaultPixelValue( 100 )
        
    def register(self, movingFileName):

        print "Register ", movingFileName

        self.movingImageReader.SetFileName(movingFileName)
        self.movingImageReader.Update()
        self.movingImage = self.movingImageReader.GetOutput()
        
        self.registration.SetMovingImage( self.movingImage )
        self.registration.Update()

        self.resampler.SetInput( self.movingImage )
        self.resampler.SetTransform( self.registration.GetOutput().Get() )
     
        caster = self.CastFilterType.New()
        caster.SetInput( self.resampler.GetOutput() )
        self.outputImages.append(caster.GetOutput())

        WriterType = itk.ImageFileWriter[self.ImageType]
        writer = WriterType.New()

        # name the output image same as moving image + "aligned" 
        writer.SetFileName( "alignedImage%d.jpg" % self.count) 
        alignedImage = "alignedImage%d.jpg" % self.count
        self.count += 1
        writer.SetInput( caster.GetOutput() )
        writer.Update()
        
        
# - - module template function - - #
def ITK_AffineRegistration(imageFiles):
    '''
    This registration module takes in a list of filename files,
    and return a list of output images. Registers all images to
    the first one.
    '''
    
    # Print the parameters
    print "ITK Affine Registration Module."
    print "First parameter: ", type(imageFiles)

    # Set up the registrator class and call registration
    r = Registrator()
    align = imageFiles[0]
    r.setFixedImage(align)
    for i in range(1, len(imageFiles)):
        r.register(imageFiles[i])

    return r.outputImages
    

## -- Wrap main so we can call this via command line OR from another file -- ##
if __name__ == '__main__':

    p1 = None
    p2 = None
    
    if len(sys.argv) > 1: 
        p1 = sys.argv[0]
    #if len(sys.argv) > 2:
    #    p2 = sys.argv[1]
        
    # for ease, we are assuming parameters from the command line are in the
    # same order as the function
    ITK_AffineRegistration(p1, p2)


    
