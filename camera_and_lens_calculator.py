class CameraAndLensCalculator():
  def __init__(self):
    self.arcseconds_per_radian = 206.265
    self.pixel_size = self.focal_length = self.angular_obj_size = self.lp_mm = self.focal_length = None
  def get_arc_sec_per_pixel(self):
    # This formula calculates the number of arcseconds per pixel in an image, based on the size of the camera's pixels and the focal length of the lens.
    self.arc_sec_per_pixel = (self.arcseconds_per_radian * self.pixel_size) / self.focal_length
    return self.ar_sec_per_pixel
  def get_obj_final_pixel_width(self):
    # This formula calculates the number of pixels wide Jupiter is in the final image, based on the angular size of Jupiter and the arcseconds per pixel.
    self.obj_final_pixel_width = self.angular_obj_size / self.ar_sec_per_pixel
    return self.obj_final_pixel_width
  def get_image_scale(self):
    # This formula calculates the image scale, which is the number of arcseconds per millimeter in the final image, based on the angular size of the object,
    # the distance to the object, and the focal length of the lens or telescope.
    self.image_scale = (self.arcseconds_per_radian * self.angular_obj_size) / (self.obj_au * self.focal_length)
    return self.image_scale
  def get_lens_arc_resolution(self):
    # This formula calculates the arcsecond resolution of a lens, based on the image scale and the focal length of the lens, and the lp/mm (Line Pairs per millimeter)
    #Arcsecond Resolution = (206.265 * Image Scale) / (Focal Length * lp/mm)
    lens_arc_resolution = (self.arcseconds_per_radian * self.image_scale) / (self.focal_length * self.lp_mm)
    return self.lens_arc_resolution
  if __name__ == '__main__':
    return 0
