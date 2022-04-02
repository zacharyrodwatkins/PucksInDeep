#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <stdio.h>
#include <ctime>
#include <chrono>
#include <fstream>

using namespace cv;
using namespace std;

#define CORNERS_FILE "calibration/calibrate.txt"
#define HSV_FILE "calibration/HSV.txt"


class tracker {


    private:

        // Dimesion constants
        const float TABLE_Y_DIMS = 200; // cm
        const float TABLE_X_DIMS = 100; // cm
        const float PUCK_RADIUS = 3; //cm
        const int FRAME_WIDTH = 640;
        const int FRAME_HEIGHT = 480;
        const int M00_cut = 0.5 *3.1415*(3*3*TABLE_Y_DIMS*TABLE_X_DIMS/FRAME_WIDTH*FRAME_HEIGHT); 
        

        // CV2 transform constants
        Point2f inQuad[4];
        Point2f outQuad[4];
        Scalar shift;
        bool shift_flag;
        Size transformSize = Size(FRAME_WIDTH,FRAME_HEIGHT);
        Mat transform_matrix;
       
        // HSV bounds
        Scalar lowerb;// = Scalar(45,45,155);
        Scalar upperb;// = Scalar(65+shift_int,65,175);


        // Frames 
        Mat transformed;
        Mat hsv;
        Mat bin;
        Mat raw;

        Moments moms;

        VideoCapture cap;
        // VideoWriter writer;

        float x;
        float y;
        float vx;
        float vy;
        

    public:
        tracker(void){
            
            outQuad[0] = Point2f(0,FRAME_WIDTH);
            outQuad[1] = Point2f(0,0);
            outQuad[2] = Point2f(FRAME_HEIGHT,0);
            outQuad[3] = Point2f(FRAME_HEIGHT,FRAME_WIDTH);


            // READ FILES 
            fstream cornerfile(CORNERS_FILE, ios_base::in);
            for (int i = 0; i<4; i++){
                int x=-1;
                int y=-1;
                if ((!(cornerfile >> x)) ||  (!(cornerfile >> y))){
                    cerr << "Error reading " << CORNERS_FILE << '\n';
                    exit(1);
                }
                inQuad[i] = Point2f(x,y);
            }

            transform_matrix = getPerspectiveTransform(inQuad, outQuad);


            // lower first then upper
            fstream hsvfile(HSV_FILE, ios_base::in);
            int bounds[2][3];
            for (int i = 0; i<2; i++){
                int val=0;
                for (int j= 0 ; j < 3; j ++){
                    if (!(hsvfile >> val)){
                        cerr << "Error reading " << HSV_FILE << '\n';
                        exit(1);
                    }
                    printf("%d\n",val);
                    bounds[i][j] = val;
                }
            }



            if (bounds[0][0]>bounds[1][1]){
                int h_shift = 180 - bounds[0][0];
                bounds[1][0] += h_shift;
                bounds[0][0] = 0;
                shift = Scalar(h_shift);
                shift_flag = true;
            }
            else{
                shift  = Scalar(0);
                shift_flag = false;
            }

            //Does this block idk?
            cap = VideoCapture("udp://10.42.0.124:5000?overrun_nonfatal=1&fifo_size=50000000");
            if (!cap.isOpened()) {
                cerr << "Unable to open camera\n";
                exit(-1);
            }

            // writer = VideoWrite("udp://10.42.0.124:5001?overrun_nonfatal=1")
        }

        int process_frame(void);
        void show(void);

        enum PUCK_STATUS {PUCK_FOUND = 0, PUCK_LOST = 1};

};