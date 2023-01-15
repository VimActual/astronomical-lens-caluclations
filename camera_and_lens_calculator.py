class CameraAndLensCalculator():
    def __init__(self, **data):
        self.arcseconds_per_radian = 206.265
        self.data = data
        self.calculate_all()

    def calculate_all(self):
        if 'pixel_size' in self.data and 'focal_length' in self.data:
            self.get_camera_arc_sec_per_pixel()
        if 'angular_obj_size' in self.data and 'arc_sec_per_pixel' in self.data:
            self.get_obj_final_pixel_width()
        if 'angular_obj_size' in self.data and 'obj_au' in self.data and 'focal_length' in self.data:
            self.get_image_scale()
        if 'image_scale' in self.data and 'focal_length' in self.data and 'lp_mm' in self.data:
            self.get_lens_arc_resolution()
        if 'focal_length' in self.data and 'f_stop' in self.data:
            self.get_lens_aperture_diameter()
        if 'focal_length' in self.data and 'f_stop' in self.data and 'focal_length_2' in self.data and 'f_stop_2' in self.data:
            self.get_brightness_ratio_two_lenses()

    def get_data(self):
        for data in self.data:
            print(f'{data:<25}: {round(self.data[data], 2)}')

    def get_camera_arc_sec_per_pixel(self):
    # This formula calculates the number of arcseconds per pixel in an image, based on the size of the camera's pixels and the focal length of the lens.
        self.data['arc_sec_per_pixel'] = (self.arcseconds_per_radian * self.data['pixel_size']) / self.data['focal_length']
        return self.data['arc_sec_per_pixel']
    
    def get_obj_final_pixel_width(self):
    # This formula calculates the number of pixels wide Jupiter is in the final image, based on the angular size of Jupiter and the arcseconds per pixel.
        self.data['obj_final_pixel_width'] = self.data['angular_obj_size'] / self.data['arc_sec_per_pixel']
        return self.data['obj_final_pixel_width']
    
    def get_image_scale(self):
    # This formula calculates the image scale, which is the number of arcseconds per millimeter in the final image, based on the angular size of the object,
    # the distance to the object, and the focal length of the lens or telescope.
        self.data['image_scale'] = (self.arcseconds_per_radian * self.data['angular_obj_size']) / (self.data['obj_au'] * self.data['focal_length'])
        return self.data['image_scale']
    
    def get_lens_arc_resolution(self):
    # This formula calculates the arcsecond resolution of a lens, based on the image scale and the focal length of the lens, and the lp/mm (Line Pairs per millimeter)
        self.data['lens_arc_resolution'] = (self.arcseconds_per_radian * self.data['image_scale']) / (self.data['focal_length'] * self.data['lp_mm'])
        return self.data['lens_arc_resolution']
    
    def get_lens_aperture_diameter(self):
    # Used for getting the brightness ratio of two lenses
        self.data['lens_aperture_diameter'] = (self.data['focal_length'] / self.data['f_stop'])
        return self.data['lens_aperture_diameter']
    
    def get_brightness_ratio_two_lenses(self):
    # Brightness Ratio = (aperture Diameter of Lens^2) / (Aperture Diameter of Telescope^2)
        self.lens1_aperture_diameter = (self.data['focal_length'] / self.data['f_stop'])
        self.lens2_aperture_diameter = (self.data['focal_length_2'] / self.data['f_stop_2'])
        self.data['brightness_ratio'] = (self.lens1_aperture_diameter**2) / (self.lens2_aperture_diameter**2)
        return self.data['brightness_ratio']

if __name__ == '__main__':
    calc = CameraAndLensCalculator()
    calc2 = CameraAndLensCalculator(pixel_size=3.7, focal_length=250, angular_obj_size=50, obj_au=3.95, lp_mm=44, f_stop=5.6, focal_length_2=1219, f_stop_2=5.9)
    calc2.get_data()
