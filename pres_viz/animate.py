import numpy as np 
import cv2
import math
import imageio
import matplotlib.pyplot as plt
# from skimage import color
# from skimage import io



class large_pulley:

    def __init__ (self, position, radius, motor = True, image_dims=None):

        self.position=np.array(position)
        self.radius = radius
        self.image_dims = image_dims
        if motor == True:
            self.colour = (150,78,0)
        else:
            self.colour = ((94,81,239))
        

    def draw(self, img):

        cv2.circle(img, self.cvt_to_image_coords(self.image_dims, self.position), self.radius, self.colour, thickness=-1)
    
    @staticmethod
    def cvt_to_image_coords (image_dims, pos): 
        return ( int(image_dims[0]/2 + pos[0]), int(image_dims[1]/2 - pos[1]))

class fb_carriages:

    def __init__ (self, small_pulley_radius=12, length=40, width=20, sp_dist=10, x_offset=25, lp_xloc= 25, lp_r = 25,rail_width=5, rail_length=450,height = None, image_dims = None):
        self.spr=int( small_pulley_radius)
        self.image_dims = image_dims
        if height != None:
            self.height = height
        else:
            self.height = self.image_dims[0]/2
        self.x_offset = x_offset
        self.sp_dist = sp_dist
        self.length = length
        self.width = width
        self.lp_xloc = lp_xloc
        self.lp_r = lp_r
        self.rail_length = rail_length
        self.rail_width = rail_width
        self.sp_locs = [(lp_xloc+lp_r+self.spr, self.height+small_pulley_radius+int(sp_dist/2)),(lp_xloc+lp_r+self.spr, self.height-small_pulley_radius-int(sp_dist/2))]
        self.sp_mirror = [(self.image_dims[0]-self.sp_locs[0][0], self.sp_locs[0][1]), (self.image_dims[0]-self.sp_locs[0][0], self.sp_locs[1][1])]

    def update_h(self, h):
        oldh = self.height
        self.height = h
        self.sp_locs[0] = (self.sp_locs[0][0], self.sp_locs[0][1]+h-oldh)
        self.sp_locs[1] = (self.sp_locs[1][0], self.sp_locs[1][1]+h-oldh)
        self.sp_mirror[0] = (self.sp_mirror[0][0], self.sp_locs[0][1])
        self.sp_mirror[1] = (self.sp_mirror[1][0], self.sp_locs[1][1])



    
    def draw(self, img):
        belt_colour = (70,70,75)
        belt_thick = 2
         #rail
        cv2.rectangle(img, (int((self.image_dims[1]-self.rail_length)/2), self.height+int(self.rail_width/2)), (int(self.image_dims[1]/2+self.rail_length/2), int(self.height-self.rail_width/2)), color = (150,150,150), thickness=-1)

         
        cv2.rectangle(img, (int(self.x_offset-self.width/2), int(self.height-self.sp_dist/2)-self.spr),(self.x_offset+int(self.width/2)+2*self.spr, self.height+int(self.sp_dist/2)+self.spr),color = (100,100,100), thickness=-1)
        cv2.rectangle(img, (self.x_offset-int(self.width/2), self.height-int(self.length/2)), (self.x_offset+int(self.width/2), self.height+int(self.length/2)), color = (100,100,100), thickness=-1)
        for sp in self.sp_locs:
            cv2.circle(img, (int(sp[0]), int(sp[1])), self.spr, color = (255,0,0), thickness=-1)

        linex = self.sp_locs[0][0] - self.spr-1
        line_stop_bottom = int(self.sp_locs[0][1])
        line_start_bottom = int(self.image_dims[1]-self.lp_r)
        line_start_top = int(self.lp_r)
        line_stop_top = int(self.sp_locs[1][1])
        side_sidep1 = (int(self.sp_locs[0][0]), int(self.sp_locs[0][1]-self.spr))
        side_sidep2 = (int(self.image_dims[1]) - int(self.sp_locs[0][0]), int(self.sp_locs[0][1]-self.spr))
        cv2.line(img, side_sidep1, side_sidep2, color = belt_colour, thickness=belt_thick)
        
        side_sidep1 = (int(self.sp_locs[1][0]), int(self.sp_locs[1][1]+self.spr))
        side_sidep2 = (int(self.image_dims[1] - self.sp_locs[1][0]), int(self.sp_locs[1][1]+self.spr))
        cv2.line(img, side_sidep1, side_sidep2, color = belt_colour, thickness=belt_thick)

        cv2.line(img, (linex, line_start_top), (linex, line_stop_top), color = belt_colour, thickness=belt_thick)
        cv2.line(img, (linex, line_stop_bottom), (linex, line_start_bottom), color = belt_colour, thickness=belt_thick)
        

        linex = int(self.image_dims[1]-linex)
        cv2.line(img, (linex, line_start_top), (linex, line_stop_top), color = belt_colour, thickness=belt_thick)
        cv2.line(img, (linex, line_stop_bottom), (linex, line_start_bottom), color = belt_colour, thickness=belt_thick)

        cv2.line(img, (1, self.lp_r), (1, self.image_dims[1]-self.lp_r), color=belt_colour, thickness=belt_thick)
        cv2.line(img, (self.image_dims[0]-2, self.lp_r), (self.image_dims[0]-2, self.image_dims[1]-self.lp_r), color=belt_colour, thickness=belt_thick)

    


        cv2.rectangle(img, (self.image_dims[0]-int(self.x_offset-self.width/2), int(self.height-self.sp_dist/2-self.spr)),(self.image_dims[0]-int(self.x_offset+self.width/2+2*self.spr), self.height+int(self.sp_dist/2+self.spr)),color = (100,100,100), thickness=-1)
        cv2.rectangle(img, (self.image_dims[0]-int(self.x_offset-self.width/2), int(self.height-self.length/2)), (self.image_dims[0]-int(self.x_offset+self.width/2), self.height+int(self.length/2)), color = (100,100,100), thickness=-1)
        
        for sp in self.sp_locs:
            cv2.circle(img, (int(sp[0]), int(sp[1])), self.spr, color = (94,81,239), thickness=-1)
        for spm in self.sp_mirror:
            cv2.circle(img, (int(spm[0]), int(spm[1])), self.spr, color = (94,81,239), thickness=-1)


class Rails:

    def __init__(self, width = 10, pulley_locs = None):
        self.pulley_locs = pulley_locs if pulley_locs is not None else [ (25,25), (25,475), (475,25), (475,475) ] 
        self.width = width
        self.points = [np.array(self.pulley_locs[i])+(-1)**(i % 2 +1)*np.array((int(self.width/2), 0)) for i in range(4)]

    def draw(self, img):
        for i in range(2):
            cv2.rectangle(img, tuple(self.points[2*i]), tuple(self.points[2*i+1]), color = (150,150,150), thickness=-1)

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
        cv2.circle(img, large_pulley.cvt_to_image_coords(self.image_dims, self.position), int(self.size), (29,118,56), thickness=-1)
        cv2.circle(img, large_pulley.cvt_to_image_coords(self.image_dims, self.position), int(self.handle_size),(125,196,147), thickness=-1)


class mallet_mount():
    def __init__(self, position, l=20, w=10, fo = 2):
        self.position = position
        self.l = l
        self.w = w
        self.forward_offset = fo


    def draw(self, img):
        p1 = tuple(np.array(self.position)-np.array((self.l/2,self.w/2+self.forward_offset)).astype(int))
        p2 = tuple(np.array(self.position)+np.array((self.l/2,self.w/2-self.forward_offset)).astype(int))
        cv2.rectangle(img, p1, p2, color = (100,100,100), thickness=-1)


class controller:

    def __init__(self, large_pulleys, sp, banger, rails_, mmount, image_dims = None):
        self.large_pulleys = large_pulleys
        self.sp = sp
        self.banger = banger
        self.radius_vectors = None
        self.line_lengths = None
        self.clicked = False
        self.image_dims = image_dims        
        self.rails = rails_
        self.mmount = mmount
        self.motor_1angle = -np.pi/2
        self.motor_2angle = -np.pi/2
        self.delta = 0
        self.update()


    @staticmethod
    def cvt_to_local_coords(image_dims, image_position):
        return np.array( [int(image_position[0] - image_dims[0]/2 ), int(image_dims[1]/2 - image_position[1])])

    def update(self):
        #self.radius_vectors = [self.radial_vector_for_large_pulley(s) for s in self.large_pulleys]
        for small_p in self.sp:
            small_p.update_h(large_pulley.cvt_to_image_coords( self.image_dims, self.banger.position)[1])

        self.mmount.position = large_pulley.cvt_to_image_coords( self.image_dims, self.banger.position)
        
            

    def radial_vector_for_large_pulley(self, spl):
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


    def update_banger_pos(self,inc):
        self.motor_1angle += (inc[0] + inc[1])/self.large_pulleys[0].radius
        self.motor_2angle += (inc[0] - inc[1])/self.large_pulleys[0].radius
        self.banger.position = np.array(self.banger.position) + inc
        self.update()

    def draw(self, img):
        self.rails.draw(img)
        self.banger.draw(img)

        for sp in self.sp:
            sp.draw(img)

        self.mmount.draw(img)

        i = 0
        for s in self.large_pulleys:
            s.draw(img)

            if i>1:
                if i == 3:
                    angle = self.motor_1angle

                else:
                    angle = self.motor_2angle
                
                outerPoint = (large_pulley.cvt_to_image_coords((500,500), s.position) + s.radius*np.array((math.cos(angle), math.sin(angle)))).astype(int)
                cv2.line(img, large_pulley.cvt_to_image_coords((500,500), s.position), tuple(outerPoint), (20,20,20), thickness=4)

            i += 1
            
        


            # #draw lines
            # cv2.line(img, large_pulley.cvt_to_image_coords( img.shape, self.banger.position), \
            #     large_pulley.cvt_to_image_coords(img.shape, s.position + radius_vector), (0,0,0), thickness=1)

            # cv2.line(img, large_pulley.cvt_to_image_coords(img.shape, s.position), \
            #     large_pulley.cvt_to_image_coords(img.shape, s.position + radius_vector), (0,0,0), thickness=2)


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


def combine_img(img, table_segment):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not (img[i,j,:] == [255,255,255]).all():
                table_segment[i,j,:] = img[i,j,:] 
    return table_segment

if __name__ == "__main__":
    table = cv2.imread("air-hockey-table-isolated-white-background-d-render-95664131.jpg")
    table = cv2.rotate(table, cv2.ROTATE_90_CLOCKWISE) 
    table = cv2.resize(table, ( 600, int(800*600/480)))
    table = table[50:-50,:]
    table_og = table
    std_radius = 25
    sp_radius = 12
    s1 = large_pulley((250-std_radius, 250-std_radius), std_radius, motor = False,image_dims= (500,500))
    s2 = large_pulley((-250+std_radius, 250-std_radius), std_radius, motor=False, image_dims=(500,500))
    s4 = large_pulley((250-std_radius, -250+std_radius), std_radius, motor=True, image_dims=(500,500))
    s3 = large_pulley((-250+std_radius, -250+std_radius), std_radius, motor=True, image_dims= (500,500))
    large_pulleys = [s1,s2,s3,s4]
    sp1 = fb_carriages(image_dims = (500,500))
    r = Rails()
    sps = [sp1]


        

    img = np.ones((500,500,3))*255
    

    b = banger((0,-50), 20, image_dims=(500,500))
    mmount = mallet_mount(large_pulley.cvt_to_image_coords((500,500), b.position))

    c = controller(large_pulleys, sps, b, r, mmount, image_dims=(500,500))
    c.update_banger_pos((0,-75))
    c.draw(img)
    
    windowName = "Stringulator"
    cv2.namedWindow(windowName)
    cv2.setMouseCallback(windowName, c.move_banger)
    with imageio.get_writer('Parabola.gif', mode='I') as writer:
        v = 0
        x = np.array(range(50)).astype(float)/10

        '''X(t) = 493.82716049383083*t^5 + -370.3703703703728*t^4 + 74.0740740740745*t^3 + 0.5            
        Y(t) = -370.3703703703714*t^5 + 185.18518518518584*t^4 + -1.0279842820603364e-13*t^3 + 0.2'''

        Frames = 100
        Ttotal = 0.3
        Xend = 0.7
        Y = 0.8

        
        T = np.linspace(0,0.3, 30)
        print (T)

        fx = lambda t : (493.82716049383083*t**5 + -370.3703703703728*t**4 + 74.0740740740745*t**3 )*(350) 
        fy = lambda t : (-370.3703703703714*t**5 + 185.18518518518584*t**4 + -1.0279842820603364e-13*t**3)*350-125
        y = [fy(t) for t in T]
        x = [fx(t) for t in T]
        ptsimg = np.array([large_pulley.cvt_to_image_coords((500,500),(x[i],y[i])) for  i in range(len(T))])

        # pts = np.zeros((len(x),2),np.int32)
        # pts[:,0]=x
        # pts[:,1]=y

        pts = ptsimg.reshape((-1, 1,2)) 
        # print(pts)
        for dx,dy in zip(np.diff(x), np.diff(y)):

            v =  np.array([dx,dy])
            img = np.ones(img.shape)*255
            
            c.draw(img)
            cv2.polylines(img, [pts], False, color=(10,10,10), thickness=3, lineType=cv2.LINE_AA)
            imgthresh = cv2.inRange(img, (254,254,254), (256,256,256),cv2.THRESH_BINARY).reshape(500,500,1)/255
            
            c.update_banger_pos(v)
            c.update()
            table = np.copy(table_og)
            table[400:,50:-50] = table[400:,50:-50]*imgthresh + img#combine_img(img, table[400:,50:-50])
            tablergb = cv2.cvtColor(table, cv2.COLOR_BGR2RGB)
            cv2.imshow(windowName, tablergb)
            if cv2.waitKey(20) == ord('q'):
                break
            writer.append_data(tablergb)

    cv2.destroyAllWindows()