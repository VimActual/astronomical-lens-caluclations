#!/usr/bin/env python
# units are assumed to be in mm and arcseconds
class CameraAndLensCalculator():
    def __init__(self, **data):
        self.arcseconds_per_radian = 206.265
        self.data = {}
        self.data["camera"] = {}
        self.data["lens"] = {}
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
            if 'pixel_size' in self.data["camera"] and 'focal_length' in self.data["lens"]:
                self.get_camera_arc_sec_per_pixel()
                done += 1
            if 'obj_angular_size' in self.data["object"] and 'arc_sec_per_pixel' in self.data["camera"]:
                self.get_obj_final_pixel_width()
                done += 1
            if 'obj_angular_size' in self.data["object"] and 'obj_au' in self.data["object"] and 'focal_length' in self.data["lens"]:
                self.get_image_scale()
                done += 1
            if 'image_scale' in self.data["image_qualities"] and 'focal_length' in self.data["lens"] and 'lp_mm' in self.data["lens"]:
                self.get_lens_arc_resolution()
                done += 1
            if 'focal_length' in self.data["lens"] and 'f_stop' in self.data["lens"]:
                self.get_lens_aperture_diameter()
                done += 1
            if 'lens_arc_resolution' in self.data["lens"] and 'image_scale' in self.data["image_qualities"]:
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
        self.data['camera']['arc_sec_per_pixel'] = (self.arcseconds_per_radian * self.data['camera']['pixel_size']) / self.data['lens']['focal_length']
        return self.data['camera']['arc_sec_per_pixel']
    
    def get_obj_final_pixel_width(self):
    # This formula calculates the number of pixels wide Jupiter is in the final image, based on the angular size of Jupiter and the arcseconds per pixel.
        self.data['image_qualities']['obj_final_pixel_width'] = self.data['object']['obj_angular_size'] / self.data['camera']['arc_sec_per_pixel']
        return self.data['image_qualities']['obj_final_pixel_width']
    
    def get_image_scale(self):
        # This formula calculates the image scale, which is the number of arcseconds per millimeter in the final image, based on the angular size of the object,
        # the distance to the object, and the focal length of the lens or telescope.
        self.data['image_qualities']['image_scale'] = (self.arcseconds_per_radian * self.data['object']['obj_angular_size']) / (self.data['object']['obj_au'] * self.data['lens']['focal_length'])
        return self.data['image_qualities']['image_scale']

    def get_lens_llmp(self):
        self.data['lens']['lp_mm'] = (self.data['image_qualities']['image_scale'] * self.data['lens']['lens_arc_resolution']) / self.arcseconds_per_radian
        return self.data['lens']['lp_mm']
    
    def get_lens_arc_resolution(self):
        # This formula calculates the arcsecond resolution of a lens, based on the image scale and the focal length of the lens, and the lp/mm (Line Pairs per millimeter)
        self.data['lens']['lens_arc_resolution'] = (self.arcseconds_per_radian * self.data['image_qualities']['image_scale']) / (self.data['lens']['focal_length'] * self.data['lens']['lp_mm'])
        return self.data['lens']['lens_arc_resolution']
    
    def get_lens_aperture_diameter(self):
    # Used for getting the brightness ratio of two lenses
        self.data['lens']['lens_aperture_diameter'] = (self.data['lens']['focal_length'] / self.data['lens']['f_stop'])
        return self.data['lens']['lens_aperture_diameter']
    
    def get_brightness_ratio_two_lenses(self, compareLens):
    # Brightness Ratio = (aperture Diameter of Lens^2) / (Aperture Diameter of Telescope^2)
        cLens = compareLens
        cLensAD = cLens.data['lens']['lens_aperture_diameter']
        cLensFS = cLens.data['lens']['f_stop']
        brightness_ratio = round((self.data['lens']['lens_aperture_diameter'] / cLensAD)**2 / (self.data['lens']['f_stop'] / cLensFS), 2)
        return brightness_ratio

    def get_brightness_factor(self, compareLens):
        cLens = compareLens
        cLensAD = cLens.data['lens']['lens_aperture_diameter']
        cLens_brightness_ratio = (1 / (self.data['lens']['lens_aperture_diameter']**2) / cLensAD)
        return cLens_brightness_ratio

if __name__ == '__main__':
    print("\nCanon 80D Paired with Canon 250mm")
    calc1 = CameraAndLensCalculator(camera={'Make_Model':'Canon 80D', 'pixel_size':3.7}, lens={'Make_Model':'Canon 250 f/5.6','focal_length':250, 'lp_mm':44.00, 'f_stop':5.6}, object={'obj_angular_size':50,'obj_au':3.95})
    calc1.get_data()
    print("\nCanon 80D Paired with Orion XT6")
    calc2 = CameraAndLensCalculator(camera={'Make_Model':'Canon 80D', 'pixel_size':3.7}, lens={'Make_Model':'Orion XT6', 'focal_length':1178, 'f_stop':7.8}, object={'obj_angular_size':50,'obj_au':3.95})
    #print(calc2.get_brightness_ratio_two_lenses(calc1))
    calc2.get_data()
    print("\nCanon 80D Paired with Orion XT8")
    calc3 = CameraAndLensCalculator(camera={'Make_Model':'Canon 80D', 'pixel_size':3.7}, lens={'Make_Model':'Orion XT8', 'focal_length':1219, 'f_stop':5.9}, object={'obj_angular_size':50,'obj_au':3.95})
    calc3.get_data()
    print("\nCanon 80D Paired with Orion AstroView")
    calc4 =  CameraAndLensCalculator(camera={'Make_Model':'Canon 80D', 'pixel_size':3.7}, lens={'Make_Model':'Orion AstroView', 'focal_length':910, 'f_stop':10.1}, object={'obj_angular_size':50,'obj_au':3.95})
    calc4.get_data()
    print(f"\nCanon 80D Paired with {calc4.data['lens']['Make_Model']}")
    calc5 = CameraAndLensCalculator(camera={'Make_Model':'Canon 80D', 'pixel_size':3.7}, lens={'Make_Model':'Sky-Watcher N 200/1000 Explorer 200P OTA', 'focal_length':1000, 'f_stop':5}, object={'obj_angular_size':50,'obj_au':3.95})
    calc5.get_data()
    print(f"Using the Canon 80D the {calc1.data['lens']['Make_Model']} is {calc1.get_brightness_ratio_two_lenses(calc2)} brighter than {calc2.data['lens']['Make_Model']}")
    print(f"Using the Canon 80D the {calc2.data['lens']['Make_Model']} is {calc2.get_brightness_ratio_two_lenses(calc1)} brighter than {calc1.data['lens']['Make_Model']}")
    print(f"Using the Canon 80D the {calc3.data['lens']['Make_Model']} is {calc3.get_brightness_ratio_two_lenses(calc1)} brighter than {calc1.data['lens']['Make_Model']}")
    print(f"Using the Canon 80D the {calc3.data['lens']['Make_Model']} is {calc3.get_brightness_ratio_two_lenses(calc2)} brighter than {calc2.data['lens']['Make_Model']}")
    print(f"Using the Canon 80D the {calc4.data['lens']['Make_Model']} is {calc4.get_brightness_ratio_two_lenses(calc1)} brighter than {calc1.data['lens']['Make_Model']}")
    print(f"Using the Canon 80D the {calc4.data['lens']['Make_Model']} is {calc4.get_brightness_ratio_two_lenses(calc3)} brighter than {calc3.data['lens']['Make_Model']}")
    print(f"Using the Canon 80D the {calc5.data['lens']['Make_Model']} is {calc5.get_brightness_ratio_two_lenses(calc3)} brighter than {calc1.data['lens']['Make_Model']}")
