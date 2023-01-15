#!/usr/bin/env python
# units are assumed to be in mm and arcseconds
class CameraAndLensCalculator():
    def __init__(self, **data):
        self.arcseconds_per_radian = 206.265
        self.data = {}
        self.data["camera"] = {}
        self.data["lens_1"] = {}
        self.data["lens_2"] = {}
        self.data["image_qualities"] = {}
        self.data["object"] = {}
        self.data.update(data)
        if 'obj_au' not in self.data["object"]:
            self.data["object"]['obj_au'] = 3.95
            self.data["object"]['obj_angular_size'] = 50
        self.calculate_all()

    def calculate_all(self):
        previous_done = 0
        done = 0
        while done <= previous_done:
            previous_done = done
            if 'pixel_size' in self.data["camera"] and 'focal_length' in self.data["lens_1"]:
                self.get_camera_arc_sec_per_pixel()
                done += 1
            if 'obj_angular_size' in self.data["object"] and 'arc_sec_per_pixel' in self.data["camera"]:
                self.get_obj_final_pixel_width()
                done += 1
            if 'obj_angular_size' in self.data["object"] and 'obj_au' in self.data["object"] and 'focal_length' in self.data["lens_1"]:
                self.get_image_scale()
                done += 1
            if 'image_scale' in self.data["image_qualities"] and 'focal_length' in self.data["lens_1"] and 'lp_mm' in self.data["lens_1"]:
                self.get_lens_arc_resolution()
                done += 1
            if 'focal_length' in self.data["lens_1"] and 'f_stop' in self.data["lens_1"]:
                self.get_lens_aperture_diameter()
                done += 1
            if 'focal_length' in self.data["lens_1"] and 'f_stop' in self.data["lens_1"] and 'focal_length_2' in self.data["lens_2"] and 'f_stop_2' in self.data["lens_2"]:
                self.get_brightness_ratio_two_lenses()
                done += 1
            if 'brightness_ratio' in self.data["lens_1"]:
                self.get_brightness_factor()
                done += 1
            if 'lens_arc_resolution' in self.data["lens_1"] and 'image_scale' in self.data["image_qualities"]:
                self.get_lens_llmp()
                done += 1

    def get_data(self):
        for equipment in self.data:
            for details in self.data[equipment]:
                if isinstance(self.data[equipment][details], float):
                    print(f'{details:<25}: {round(self.data[equipment][details], 2)}')
                else:
                    print(f'{details:<25}: {self.data[equipment][details]}')

    def get_camera_arc_sec_per_pixel(self):
    # This formula calculates the number of arcseconds per pixel in an image, based on the size of the camera's pixels and the focal length of the lens.
        self.data['camera']['arc_sec_per_pixel'] = (self.arcseconds_per_radian * self.data['camera']['pixel_size']) / self.data['lens_1']['focal_length']
        return self.data['camera']['arc_sec_per_pixel']
    
    def get_obj_final_pixel_width(self):
    # This formula calculates the number of pixels wide Jupiter is in the final image, based on the angular size of Jupiter and the arcseconds per pixel.
        self.data['image_qualities']['obj_final_pixel_width'] = self.data['object']['obj_angular_size'] / self.data['camera']['arc_sec_per_pixel']
        return self.data['image_qualities']['obj_final_pixel_width']
    
    def get_image_scale(self):
        # This formula calculates the image scale, which is the number of arcseconds per millimeter in the final image, based on the angular size of the object,
        # the distance to the object, and the focal length of the lens or telescope.
        self.data['image_qualities']['image_scale'] = (self.arcseconds_per_radian * self.data['object']['obj_angular_size']) / (self.data['object']['obj_au'] * self.data['lens_1']['focal_length'])
        return self.data['image_qualities']['image_scale']

    def get_lens_llmp(self):
        self.data['lens_1']['lp_mm'] = (self.data['image_qualities']['image_scale'] * self.data['lens_1']['lens_arc_resolution']) / self.arcseconds_per_radian
        return self.data['lens_1']['lp_mm']
    
    def get_lens_arc_resolution(self):
        # This formula calculates the arcsecond resolution of a lens, based on the image scale and the focal length of the lens, and the lp/mm (Line Pairs per millimeter)
        self.data['lens_1']['lens_arc_resolution'] = (self.arcseconds_per_radian * self.data['image_qualities']['image_scale']) / (self.data['lens_1']['focal_length'] * self.data['lens_1']['lp_mm'])
        return self.data['lens_1']['lens_arc_resolution']
    
    def get_lens_aperture_diameter(self):
    # Used for getting the brightness ratio of two lenses
        self.data['lens_1']['lens_aperture_diameter'] = (self.data['lens_1']['focal_length'] / self.data['lens_1']['f_stop'])
        return self.data['lens_1']['lens_aperture_diameter']
    
    def get_brightness_ratio_two_lenses(self):
    # Brightness Ratio = (aperture Diameter of Lens^2) / (Aperture Diameter of Telescope^2)
        self.lens1_aperture_diameter = (self.data['lens_1']['focal_length'] / self.data['lens_1']['f_stop'])
        self.lens2_aperture_diameter = (self.data['lens_2']['focal_length_2'] / self.data['lens_2']['f_stop_2'])
        self.data['lens_1']['brightness_ratio'] = (self.lens1_aperture_diameter**2) / (self.lens2_aperture_diameter**2)
        return self.data['lens_1']['brightness_ratio']

    def get_brightness_factor(self):
        self.data['lens_2']['brightness_factor_lens2'] = 1 / self.data['lens_1']['brightness_ratio']
        return self.data['lens_2']['brightness_factor_lens2']

if __name__ == '__main__':
    print("\nCanon 80D: Canon 250mm vs Orion 6xt as brightness_factor_lens2, focal_lenght2, f_stop_2")
    calc1 = CameraAndLensCalculator(camera={'pixel_size':3.7}, lens_1={'focal_length':250, 'lp_mm':44.00, 'f_stop':5.6}, object={'obj_angular_size':50,'obj_au':3.95}, lens_2={'focal_length_2':1178, 'f_stop_2':7.8})
    calc1.get_data()
    print("\nCanon 80D: Canon 250mm vs Orion 8xt as brightness_factor_lens2, focal_lenght2, f_stop_2")
    calc2 = CameraAndLensCalculator(camera={'pixel_size':3.7}, lens_1={'focal_length':250, 'lp_mm':44.00, 'f_stop':5.6}, object={'obj_angular_size':50,'obj_au':3.95}, lens_2={'focal_length_2':1219, 'f_stop_2':5.9})
    calc2.get_data()
    print("\nCanon 80D: Orion xt6\" vs Orion 8xt brightness_factor_lens2, focal_lenght2, f_stop_2")
    calc3 = CameraAndLensCalculator(camera={'pixel_size':3.7}, lens_1={'focal_length':1178, 'f_stop':7.8}, object={'obj_angular_size':50,'obj_au':3.95}, lens_2={'focal_length_2':1219, 'f_stop_2':5.9})
    calc3.get_data()
    print("\nCanon 80D: Orion xt8\" vs Canon 250mm")
    calc4 = CameraAndLensCalculator(camera={'pixel_size':3.7}, lens_1={'focal_length':1219, 'f_stop':5.9}, object={'obj_angular_size':50,'obj_au':3.95}, lens_2={'focal_length_2':250, 'f_stop_2':5.6})
    calc4.get_data()
