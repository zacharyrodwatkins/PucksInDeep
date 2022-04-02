#include <tracker.hpp>

int tracker::process_frame(void){
    cap.read(raw);
    if (raw.empty()) {
        cerr << "Blank frame grabbed\n";
        exit(-1);
    }

    cvtColor(raw, hsv, COLOR_BGR2HSV);
    hsv += shift;
    inRange(hsv,lowerb, upperb,bin);
    moms = moments(bin);

    if (moms.m00>M00_cut){
        float x = 1.0*moms.m01/moms.m00;
        float y = 1.0*moms.m10/moms.m00; 
        float scale_fac = transform_matrix.at<uint8_t>(2,0)*x + transform_matrix.at<uint8_t>(2,1)*y + 1;
        float xt = (transform_matrix.at<uint8_t>(0,0)*x + transform_matrix.at<uint8_t>(0,1)*y + transform_matrix.at<uint8_t>(0,2))/scale_fac;  
        float yt = (transform_matrix.at<uint8_t>(1,0)*x + transform_matrix.at<uint8_t>(1,1)*y + transform_matrix.at<uint8_t>(1,2))/scale_fac;  
        cout << "x: " << x << "\n";
        cout << "y: " << y << "\n";
        cout << "xt: " << xt << "\n";
        cout << "yt: " << yt << "\n";
        }
    return 0;
}

void tracker::show(void){
    imshow("Live", raw);
    if (waitKey(1) >= 0)
        exit(0);
}