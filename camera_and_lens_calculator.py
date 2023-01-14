class CameraAndLensCalculator():
  def __init__(self):
    self.arcseconds_per_radian = 206.265
    self.pixel_size = self.focal_length = self.angular_obj_size = self.focal_length = None
  def get_arc_sec_per_pixel(self):
    self.arc_sec_per_pixel = (self.arcseconds_per_radian * self.pixel_size) / self.focal_length
    return self.ar_sec_per_pixel
  def get_image_scale(self):
    self.image_scale = (self.arcseconds_per_radian * self.angular_obj_size) / (self.obj_au * self.focal_length)
    return self.image_scale
  
  if __name__ == '__main__':
    return 0
