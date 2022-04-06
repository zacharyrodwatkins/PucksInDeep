#include <tracker.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 


void tracker::get_offsets(float position[], float offsets[]){
    float x = position[0];
    float y = position[1];
    offsets[0] = A*(x-TABLE_X_DIMS/2)*(y)*(y-TABLE_Y_DIMS);
    offsets[1] = B*(y-TABLE_Y_DIMS/2)*x*(x-TABLE_X_DIMS);
}

int tracker::process_frame(void){
    cap.read(raw);
    if (raw.empty()) {
        cerr << "Blank frame grabbed\n";
        return -1;
    }


    cvtColor(raw, hsv, COLOR_BGR2HSV);
    inRange(hsv,lowerb, upperb,bin);
    inRange(hsv,lowerb1,upperb1,bin1);

    bin = bin | bin1;



    // cut to table here

    moms = moments(bin);

    if (moms.m00>M00_cut){
        if (lost_frames>0)
            lost_frames = 0;
        float x_img = 1.0*moms.m10/moms.m00;
        float y_img = 1.0*moms.m01/moms.m00; 
        // cout << x_img << " " << y_img << " " <<"\n";
        float scale_fac = transform_matrix.at<double>(2,0)*x_img + transform_matrix.at<double>(2,1)*y_img + transform_matrix.at<double>(2,2);
        float xt = (transform_matrix.at<double>(0,0)*x_img + transform_matrix.at<double>(0,1)*y_img + transform_matrix.at<double>(0,2))/scale_fac;  
        float yt = (transform_matrix.at<double>(1,0)*x_img + transform_matrix.at<double>(1,1)*y_img + transform_matrix.at<double>(1,2))/scale_fac;  
        this->x = xt*this->IMG_X_TO_CM;
        this->y = yt*this->IMG_Y_TO_CM;
        float offsets[2]; 
        float xy[] = {x,y};
        get_offsets(xy,offsets);
        this->x += offsets[0];
        this->y += offsets[1];
        xy[0] = x;
        xy[1] = y; 
        savgol.update_velocity(xy);
        vx = savgol.vel[0];
        vy = savgol.vel[1];
        }

    else {
        if (lost_frames>lost_thresh){
            this->x = -69;
            this->y = -69;
            this->vx = 0;
            this->vy = 0;
        }
        else
            lost_frames++;
    }

    return 0;
}

void tracker::show(void){
    imshow("Live", bin);
    imshow("raw",raw);

    cvtColor(bin, bin_send, COLOR_GRAY2BGR);

    if (raw.empty())
        exit(-1);
    // video.write(bin_send);
    if (waitKey(1) >= 0)
        exit(0);
}

void tracker::writeVideo(void){
    cap >> raw;
    // If the frame is empty, break immediately
    if (raw.empty())
        exit(-1);
    //   break;
    // Write the frame into the file 'outcpp.avi'
    video.write(raw);
}

void tracker::tracker_write(void){
    char buffer[256];
    bzero(buffer,256);
    sprintf(buffer, "%.4f %.4f %.4f %.4f", x, y,vx,vy);
    n = write(sockfd,buffer,strlen(buffer));
    if (n<= 0){
        cerr << "Server down... Exiting.\n";
        exit(-1);
    }
}

void tracker::setup_socket(void){

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        cerr << "ERROR opening socket";
        exit(-1);
    }
    server = gethostbyname(IP);
    if (server == NULL) {
        fprintf(stderr,"ERROR, no such host\n");
        exit(-1);
    }
    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    serv_addr.sin_port = htons(PORT);
    if (connect(sockfd,(struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0){
        cerr << "ERROR connecting\nIs the server running?\n";
        exit(-1);
    }
        

}