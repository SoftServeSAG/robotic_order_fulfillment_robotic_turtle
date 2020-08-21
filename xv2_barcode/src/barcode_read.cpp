//
// Created by root on 8/10/20.
//

#include "../include/xv2_barcode/barcode_read.h"
using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
public:
    MinimalSubscriber()
            : Node("minimal_subscriber")
    {
//        subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
//                "turtle_0/image", 10, std::bind(&MinimalSubscriber::topic_callback, this, std::placeholders::_1));
        subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
                "image_raw", 10, std::bind(&MinimalSubscriber::topic_callback, this, std::placeholders::_1));
//        sub_= n_->create_subscription<sensor_msgs::msg::Image>("depth", std::bind(&TurtlebotFollower::imagecb, this, std::placeholders::_1), rmw_qos_profile_sensor_data);
    }

private:

    void topic_callback(sensor_msgs::msg::Image::SharedPtr msg) const
//    void topic_callback(const sensor_msgs::ImageConstPtr& msg) const


    {
//        std::vector<std::string> encodings = getEncodings();
//        std::string dst_encoding = encodings[0];

        cv_bridge::CvImageConstPtr cv_ptr;
        try
        {
//            cv_ptr = cv_bridge::toCvShare(msg, sensor_msgs::image_encodings::BGR8);
//            cv_ptr = cv_bridge::toCvShare(msg, /*sensor_msgs::image_encodings::BGR8*/ dst_encoding);
            cv_ptr = cv_bridge::toCvShare(msg, static_cast<std::string>(sensor_msgs::image_encodings::BGR8));
        }
        catch (cv_bridge::Exception& e)
        {
            RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
            return;
        }
//
        // Draw an example circle on the video stream
//        if (cv_ptr->image.rows > 60 && cv_ptr->image.cols > 60)
//            cv::circle(cv_ptr->image, cv::Point(50, 50), 10, CV_RGB(255,0,0));
//
//        // Update GUI Window
//        cv::imshow("circle window", cv_ptr->image);
//        cv::waitKey(3);

//        RCLCPP_INFO(this->get_logger(), "I heard: '%s'", /*msg->data.c_str()*/"Image");
        // Variable for decoded objects
        vector<decodedObject> decodedObjects;

        cv::Mat gray;
//        cv::detailEnhance 	(cv_ptr->image, cv_ptr->image, /*sigma_s = */200.0f, /*sigma_r = */0.05f);
        cv::cvtColor(cv_ptr->image, gray, CV_BGR2GRAY);

//        cv::edgePreservingFilter(gray, gray, 1);

//        cv::detailEnhance 	(gray, gray, /*sigma_s = */200.0f, /*sigma_r = */0.05f);

//        Mat sharp;
//        Mat sharpening_kernel = (Mat_<double>(3, 3) << -1, -1, -1,
//                -1, 9, -1,
//                -1, -1, -1);
//        filter2D(gray, gray, -1, sharpening_kernel);

//        cv::threshold( gray, gray, 150, 255, THRESH_BINARY);

//        cv::Mat dst, cdst, cdstP;
//
//        // Edge detection
//        Canny(cv_ptr->image, dst, 50, 200, 3);
//        // Copy edges to the images that will display the results in BGR
//        cvtColor(dst, cdst, COLOR_GRAY2BGR);
//        cdstP = cdst.clone();
//        // Standard Hough Line Transform
//        vector<Vec2f> lines; // will hold the results of the detection
//        HoughLines(dst, lines, 1, CV_PI/180, 150, 0, 0 ); // runs the actual detection
//        // Draw the lines
//        for( size_t i = 0; i < lines.size(); i++ )
//        {
//            float rho = lines[i][0], theta = lines[i][1];
//            Point pt1, pt2;
//            double a = cos(theta), b = sin(theta);
//            double x0 = a*rho, y0 = b*rho;
//            pt1.x = cvRound(x0 + 1000*(-b));
//            pt1.y = cvRound(y0 + 1000*(a));
//            pt2.x = cvRound(x0 - 1000*(-b));
//            pt2.y = cvRound(y0 - 1000*(a));
//            line( cdst, pt1, pt2, Scalar(0,0,255), 3, LINE_AA);
//        }
//        // Probabilistic Line Transform
//        vector<Vec4i> linesP; // will hold the results of the detection
//        HoughLinesP(dst, linesP, 1, CV_PI/180, 50, 50, 10 ); // runs the actual detection
//        // Draw the lines
//        for( size_t i = 0; i < linesP.size(); i++ )
//        {
//            Vec4i l = linesP[i];
//            line( cdstP, Point(l[0], l[1]), Point(l[2], l[3]), Scalar(0,0,255), 3, LINE_AA);
//        }
//
//        cv::imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst);
//        cv::imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP);
//        cv::waitKey(1);
//
//        cv::threshold(gray, gray, 0, 255, /*cv::THRESH_BINARY |*/ cv::THRESH_OTSU);
        cv::imshow("WebSource", gray);
        cv::waitKey(1);

        // Find and decode barcodes and QR codes
        decode(cv_ptr->image, decodedObjects);

        // Display location
//        display(cv_ptr->image, decodedObjects);
    }
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr subscription_;

};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MinimalSubscriber>());
    rclcpp::shutdown();
    return 0;
}