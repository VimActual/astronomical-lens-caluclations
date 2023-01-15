#!/usr/bin/env python
# units are assumed to be in mm and arcseconds
class CameraAndLensCalculator():
    def __init__(self, **data):
        self.arcseconds_per_radian = 206.265
        self.data = data
        if 'obj_au' not in self.data:
            self.data['obj_au'] = 3.95
            self.data['obj_angular_size'] = 50
        self.calculate_all()

    def calculate_all(self):
        previous_done = 0
        done = 0
        while done <= previous_done:
            previous_done = done
            if 'pixel_size' in self.data and 'focal_length' in self.data:
                self.get_camera_arc_sec_per_pixel()
                done += 1
            if 'obj_angular_size' in self.data and 'arc_sec_per_pixel' in self.data:
                self.get_obj_final_pixel_width()
                done += 1
            if 'obj_angular_size' in self.data and 'obj_au' in self.data and 'focal_length' in self.data:
                self.get_image_scale()
                done += 1
            if 'image_scale' in self.data and 'focal_length' in self.data and 'lp_mm' in self.data:
                self.get_lens_arc_resolution()
                done += 1
            if 'focal_length' in self.data and 'f_stop' in self.data:
                self.get_lens_aperture_diameter()
                done += 1
            if 'focal_length' in self.data and 'f_stop' in self.data and 'focal_length_2' in self.data and 'f_stop_2' in self.data:
                self.get_brightness_ratio_two_lenses()
                done += 1
            if 'brightness_ratio' in self.data:
                self.get_brightness_factor()
                done += 1
            if 'lens_arc_resolution' in self.data and 'image_scale' in self.data:
                self.get_lens_llmp()
                done += 1

    def get_data(self):
        for data in self.data:
            if isinstance(self.data[data], float):
                print(f'{data:<25}: {round(self.data[data], 2)}')
            else:
                print(f'{data:<25}: {self.data[data]}')

    def get_camera_arc_sec_per_pixel(self):
    # This formula calculates the number of arcseconds per pixel in an image, based on the size of the camera's pixels and the focal length of the lens.
        self.data['arc_sec_per_pixel'] = (self.arcseconds_per_radian * self.data['pixel_size']) / self.data['focal_length']
        return self.data['arc_sec_per_pixel']
    
    def get_obj_final_pixel_width(self):
    # This formula calculates the number of pixels wide Jupiter is in the final image, based on the angular size of Jupiter and the arcseconds per pixel.
        self.data['obj_final_pixel_width'] = self.data['obj_angular_size'] / self.data['arc_sec_per_pixel']
        return self.data['obj_final_pixel_width']
    
    def get_image_scale(self):
        # This formula calculates the image scale, which is the number of arcseconds per millimeter in the final image, based on the angular size of the object,
        # the distance to the object, and the focal length of the lens or telescope.
        self.data['image_scale'] = (self.arcseconds_per_radian * self.data['obj_angular_size']) / (self.data['obj_au'] * self.data['focal_length'])
        return self.data['image_scale']

    def get_lens_llmp(self):
        self.data['lp_mm'] = (self.data['image_scale'] * self.data['lens_arc_resolution']) / self.arcseconds_per_radian
        return self.data['lp_mm']
    
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

    def get_brightness_factor(self):
        self.data['brightness_factor_lens2'] = 1 / self.data['brightness_ratio']
        return self.data['brightness_factor_lens2']

if __name__ == '__main__':
    #calc = CameraAndLensCalculator()
    print("\nCanon 80D: Canon 250mm vs Orion 6xt as brightness_factor_lens2, focal_lenght2, f_stop_2")
    calc2 = CameraAndLensCalculator(pixel_size=3.7, focal_length=250, obj_angular_size=50, obj_au=3.95, lp_mm=44, f_stop=5.6, focal_length_2=1178, f_stop_2=7.8)
    calc2.get_data()
    print("\nCanon 80D: Canon 250mm vs Orion 8xt as brightness_factor_lens2, focal_lenght2, f_stop_2")
    calc3 = CameraAndLensCalculator(pixel_size=3.7, focal_length=250, obj_angular_size=50, obj_au=3.95, lp_mm=44, f_stop=5.6, focal_length_2=1219, f_stop_2=5.9)
    calc3.get_data()
    print("\nCanon 80D: Orion xt6\" vs Orion 8xt brightness_factor_lens2, focal_lenght2, f_stop_2")
    calc4 = CameraAndLensCalculator(pixel_size=3.7, focal_length=1178, obj_angular_size=50, obj_au=3.95, f_stop=7.8, focal_length_2=1219, f_stop_2=5.9)
    calc4.get_data()
    print("\nCanon 80D: Orion xt8\" compaired with 8xt")
    calc4 = CameraAndLensCalculator(pixel_size=3.7, focal_length=1219, obj_angular_size=50, obj_au=3.95, f_stop=5.9, focal_length_2=1219, f_stop_2=5.9)
    calc4.get_data()
