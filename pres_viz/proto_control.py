import numpy as np 
import cv2
import math



class spool:

    def __init__ (self, position, radius, image_dims=None):

        self.position=np.array(position)
        self.radius = radius
        self.image_dims = image_dims

    def draw(self, img):

        cv2.circle(img, self.cvt_to_image_coords(self.image_dims, self.position), self.radius, (255, 0, 4), thickness=-1)
    
    @staticmethod
    def cvt_to_image_coords (image_dims, pos):
        return ( int(image_dims[0]/2 + pos[0]), int(image_dims[1]/2 - pos[1]))

class banger():

    def __init__(self, position, size, handle_size=None, image_dims=None):
        self.position = np.array(position)
        self.size = size
        if handle_size is None:
            self.handle_size = size/2
        
        else:
            self.handle_size = handle_size

        self.image_dims = image_dims

    
    def draw(self, img):
        cv2.circle(img, spool.cvt_to_image_coords(self.image_dims, self.position), self.size, (10, 127, 0), thickness=-1)
        cv2.circle(img, spool.cvt_to_image_coords(self.image_dims, self.position), self.handle_size, (20, 255, 0), thickness=-1)

class controller:

    def __init__(self, spools, banger, image_dims = None):
        self.spools = spools
        self.banger = banger
        self.radius_vectors = None
        self.line_lengths = None
        self.clicked = False
        self.image_dims = image_dims
        self.update()

    @staticmethod
    def cvt_to_local_coords(image_dims, image_position):
        return np.array( [int(image_position[0] - image_dims[0]/2 ), int(image_dims[1]/2 - image_position[1])])

    def update(self):
        self.radius_vectors = [self.radial_vector_for_spool(s) for s in self.spools]
        old_lines = self.line_lengths
        self.line_lengths = [np.linalg.norm(spl.position + r-self.banger.position) for spl,r in zip(self.spools, self.radius_vectors)]
        if old_lines is not None:
            deltas = np.array(self.line_lengths)-np.array(old_lines)
            rots = 180.0/(np.pi*self.spools[0].radius)*deltas
            print(rots)

    def radial_vector_for_spool(self, spl):
        d = spl.position - self.banger.position
        l_abs = math.sqrt(np.linalg.norm(d)**2 - spl.radius**2)
        dangle = math.atan(1.0*d[0]/d[1]) 
        langle = math.asin(l_abs/np.linalg.norm(d))
        if (spl.position[0] > 0):
            if spl.position[1]<0:
                wrap_angle = np.pi/2-dangle-langle
            else:
                wrap_angle = 3*np.pi/2 -dangle + langle
        else:
            if spl.position[1]<0:
                wrap_angle = np.pi/2-dangle + langle
                
            else:
                wrap_angle = 3*np.pi/2 - dangle - langle

        return spl.radius * np.array([math.cos(wrap_angle), math.sin(wrap_angle)])



    def draw(self, img):
        self.banger.draw(img)

        for s, radius_vector in zip(self.spools, self.radius_vectors):
            s.draw(img)
  
            #draw lines
            cv2.line(img, spool.cvt_to_image_coords( img.shape, self.banger.position), \
                spool.cvt_to_image_coords(img.shape, s.position + radius_vector), (0,0,0), thickness=1)

            cv2.line(img, spool.cvt_to_image_coords(img.shape, s.position), \
                spool.cvt_to_image_coords(img.shape, s.position + radius_vector), (0,0,0), thickness=2)


    def move_banger(self,event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            if np.linalg.norm(controller.cvt_to_local_coords(self.image_dims, np.array([x,y]))-\
            self.banger.position) < self.banger.size:
                self.clicked = True

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.clicked==True:
                self.banger.position = controller.cvt_to_local_coords(self.image_dims,  np.array ([x,y]))
                self.update()

        elif event == cv2.EVENT_LBUTTONUP:
            self.clicked = False





if __name__ == "__main__":
    std_radius = 25
    s1 = spool((250-std_radius, 250-std_radius), std_radius, (500,500))
    s2 = spool((-250+std_radius, 250-std_radius), std_radius, (500,500))
    s4 = spool((250-std_radius, -250+std_radius), std_radius, (500,500))
    s3 = spool((-250+std_radius, -250+std_radius), std_radius, (500,500))
    spools = [s1,s2,s3,s4]
    
    img = np.ones((500,500,3))*255

    b = banger((0,0), 15, image_dims=(500,500))
  

    c = controller(spools, b, image_dims=(500,500))
    c.draw(img)
    
    windowName = "Stringulator"
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, c.move_banger)
    while (True):
        img = np.ones(img.shape)*255
        c.draw(img)
        cv2.imshow(windowName, img)
        if cv2.waitKey(20) == 27:
            break

    cv2.destroyAllWindows()