#!/usr/bin/env python
# units are assumed to be in mm and arcseconds

class CameraCalc():
    def __init__(self):
        return 0

    def get_camera_arc_sec_per_pixel(self):
    # This formula calculates the number of arcseconds per pixel in an image, based on the size of the camera's pixels and the focal length of the lens.
        self.data['camera']['arc_sec_per_pixel'] = (self.arcseconds_per_radian * self.data['camera']['pixel_size']) / self.data['lens']['focal_length']
        return self.data['camera']['arc_sec_per_pixel']

class SimulatedObjImage():
    def __init__():
        return 0

    def get_image_scale(self):
        # This formula calculates the image scale, which is the objects number of arcseconds per millimeter in the final image, based on the angular size of the object,
        # the distance to the object, and the focal length of the lens or telescope.
        # image scale tells you how large the object is in terms of angle per a specific physical distance (millimeters) in the final image.
        self.data['image_qualities']['image_scale'] = (self.arcseconds_per_radian * self.data['object']['obj_angular_size']) / (self.data['object']['obj_au'] * self.data['lens']['focal_length'])
        return self.data['image_qualities']['image_scale']

    def get_obj_final_pixel_width(self):
    # This formula calculates the number of pixels wide Jupiter is in the final image, based on the angular size of Jupiter and the arcseconds per pixel.
        self.data['image_qualities']['obj_final_pixel_width'] = self.data['object']['obj_angular_size'] / self.data['camera']['arc_sec_per_pixel']
        return self.data['image_qualities']['obj_final_pixel_width']

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
            #print(f'previ: {previous_done}\tdone" {done}')
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
            if 'price' in self.data['lens'] and 'obj_final_pixel_width' in self.data['image_qualities']:
                self.get_price_per_pixel()
                done +=1

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
        #self.data['lens']['lp_mm'] = (self.data['image_qualities']['image_scale'] * self.data['lens']['lens_arc_resolution']) / self.arcseconds_per_radian
        #self.data['lens']['MTF'] = self.data['lens']['lens_aperture_diameter'] / 550 # 550 is whitelight in mm
        self.data['lens']['MTF'] = 1 # Assuming a perfect quality lens
        #self.data['lens']['lp_mm'] = (2 * self.data['lens']['MTF']) / (self.data['lens']['focal_length'] * (self.data['lens']['lens_aperture_diameter']/ 1000)) #self.data[
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

    def get_price_per_pixel(self):
        self.data['image_qualities']['price_per_pixel'] = round(self.data['lens']['price'] / self.data['image_qualities']['obj_final_pixel_width'], 2)

if __name__ == '__main__':
    perf = SimulatedObjImage
    celestial_object = {'obj_angular_size':50,'obj_au':3.95}
    canon80D = {'Make_Model':'Canon 80D', 'pixel_size':3.7}
    # Lenses
    lenses = {}
    lenses['Canon 250mm f/5.6'] = {'Brand':'Canon', 'Model': 'EFS 55-250', 'type': 'lens', 'focal_length':250, 'lp_mm':44.00, 'f_stop':5.6, 'price': 300}
    lenses['Tokina 11 f/2.8'] = {'Brand': 'Tokina', 'Model': '11-16', 'type': 'lens', 'focal_length':11, 'f_stop':2.8, 'price': 274}
    lenses['Celestron 70'] = {'Brand':'Celestron', 'Model': '70mm f/5.7', 'type': 'refractor', 'focal_length':400, 'f_stop':5.7, 'price' : 120}
    lenses['Celestron 130'] = {'Brand':'Celestron', 'Model': '130mm f/5.0', 'type': 'refractor', 'focal_length':650, 'f_stop':5.0, 'price' : 480}
    lenses['Redcat_flouostar'] = {'Brand':'Fluorostar', 'Model': '156', 'type': 'refractor', 'focal_length':1217, 'f_stop':7.8, 'price': 7200}
    lenses['Redcat 71'] = {'Brand':'RedCat', 'Model': '71 APO', 'focal_length':350, 'f_stop':4.9, 'price': 1700}
    lenses['Skywatcher 200/1000'] = {'Brand':'Sky-Watcher', 'Model': 'N 200/1000 Explorer 200P OTA', 'focal_length':1000, 'f_stop':5, 'price': 500}
    lenses['Orion Astroview 6'] = {'Brand':'Orion', 'Model': 'AstroView 6" EQ Equatorial Reflector', 'focal_length':750, 'f_stop':5.0, 'price' : 600}
    lenses['Orion XT6'] = {'Brand':'Orion', 'Model': 'XT6', 'focal_length':1178, 'f_stop':7.8, 'price' : 600}
    lenses['Orion XT8'] = {'Brand':'Orion', 'Model': ' XT8', 'focal_length':1219, 'f_stop':5.9, 'price' : 700}
    lenses['Orion Newtonian 8'] = {'Brand':'Orion', 'Model': '8" f/4 Newtonian Reflector Astrograph', 'focal_length':800, 'f_stop':4.0, 'price': 700}
    lenses['Orion Newtonian 10'] = {'Brand':'Orion', 'Model': '10" f/4 Newtonian Reflector Astrograph', 'focal_length':1000, 'f_stop':4.0, 'price': 900}
    lenses['Orion BL135'] = {'Brand':'Orion', 'Model': 'BL135mm', 'focal_length':1100, 'f_stop':8.1, 'price' : 330}
    canon80D_combos = [CameraAndLensCalculator(camera=canon80D, lens=lens, object=celestial_object) for lens in lenses.values()]
    ppp = {}
    for combo in canon80D_combos:
        ppp[combo.data['lens']['Brand'] + combo.data['lens']['Model']] = combo.data['image_qualities']['price_per_pixel']
    ppp = dict(sorted(ppp.items(), key=lambda item: item[1]))
    for lens in ppp:
        print(f'lens: {lens:<45}\tprice ratio: {ppp[lens]}')
    #print(f"Using the Canon 80D the {calc1.data['lens']['Make_Model']} is {calc1.get_brightness_ratio_two_lenses(calc2)} brighter than {calc2.data['lens']['Make_Model']}")
    #print(canon80D_combos[0])
    '''
    print(f"Using the Canon 80D the {calc13.data['lens']['Make_Model']} is {calc13.get_brightness_ratio_two_lenses(calc3)} brighter than {calc3.data['lens']['Make_Model']}")
    #print(f"Using the Canon 80D the {calc11.data['lens']['Make_Model']} is {calc11.get_brightness_ratio_two_lenses(calc3)} brighter than {calc3.data['lens']['Make_Model']}")
    '''
