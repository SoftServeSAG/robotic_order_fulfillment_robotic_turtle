//
// Created by root on 8/10/20.
//

#ifndef ROBOTIC_ORDER_FULFILLMENT_ROBOTIC_TURTLE_BARCODE_H
#define ROBOTIC_ORDER_FULFILLMENT_ROBOTIC_TURTLE_BARCODE_H

#include <opencv2/opencv.hpp>
#include <zbar.h>

using namespace cv;
using namespace std;
using namespace zbar;

typedef struct
{
    string type;
    string data;
    vector <Point> location;
} decodedObject;



void decode(Mat im, vector<decodedObject>&decodedObjects);
void display(Mat im, vector<decodedObject>&decodedObjects);

#endif //ROBOTIC_ORDER_FULFILLMENT_ROBOTIC_TURTLE_BARCODE_H
