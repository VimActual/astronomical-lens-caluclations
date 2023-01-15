class CameraAndLensCalculator():
    def __init__(self, **kwargs):
        self.arcseconds_per_radian = 206.265
        self.kwargs = kwargs
        
    def get_arc_sec_per_pixel(self):
    # This formula calculates the number of arcseconds per pixel in an image, based on the size of the camera's pixels and the focal length of the lens.
    # Verified
        self.arc_sec_per_pixel = (self.arcseconds_per_radian * self.kwargs['pixel_size']) / self.kwargs['focal_length']
        return self.arc_sec_per_pixel
    
    def get_obj_final_pixel_width(self):
    # This formula calculates the number of pixels wide Jupiter is in the final image, based on the angular size of Jupiter and the arcseconds per pixel.
    # Verified
        self.obj_final_pixel_width = self.kwargs['angular_obj_size'] / self.kwargs['arc_sec_per_pixel']
        return self.obj_final_pixel_width
    
    def get_image_scale(self):
    # This formula calculates the image scale, which is the number of arcseconds per millimeter in the final image, based on the angular size of the object,
    # the distance to the object, and the focal length of the lens or telescope.
    # 
        self.image_scale = (self.arcseconds_per_radian * self.kwargs['angular_obj_size']) / (self.kwargs['obj_au'] * self.kwargs['focal_length'])
        return self.image_scale
    
    def get_lens_arc_resolution(self):
    # This formula calculates the arcsecond resolution of a lens, based on the image scale and the focal length of the lens, and the lp/mm (Line Pairs per millimeter)
    # Verified
        self.lens_arc_resolution = (self.arcseconds_per_radian * self.kwargs['image_scale']) / (self.kwargs['focal_length'] * self.kwargs['lp_mm'])
        return self.lens_arc_resolution
    
    def get_lens_aperture_diameter(self):
    # Used for getting the brightness ratio of two lenses
    # Verified
        self.lens_aperture_diameter = (self.kwargs['focal_length'] / self.kwargs['f_stop'])
        return self.lens_aperture_diameter
    
    def get_brightness_ratio_two_lenses(self):
    # Brightness Ratio = (aperture Diameter of Lens^2) / (Aperture Diameter of Telescope^2)

        self.lens1_aperture_diameter = (self.kwargs['focal_length'] / self.kwargs['f_stop'])
        self.lens2_aperture_diameter = (self.kwargs['focal_length_2'] / self.kwargs['f_stop_2'])
        self.brightness_ratio = (self.lens1_aperture_diameter**2) / (self.lens2_aperture_diameter**2)
