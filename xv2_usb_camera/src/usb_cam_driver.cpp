//
// Created by ldemk on 7/27/20.
//

#include "../include/xv2_usb_camera/usb_cam_driver.h"

/// Convert an OpenCV matrix encoding type to a string format recognized by sensor_msgs::Image.
/**
 * \param[in] mat_type The OpenCV encoding type.
 * \return A string representing the encoding type.
 */
std::string
mat_type2encoding(int mat_type)
{
    switch (mat_type) {
        case CV_8UC1:
            return "mono8";
        case CV_8UC3:
            return "bgr8";
        case CV_16SC1:
            return "mono16";
        case CV_8UC4:
            return "rgba8";
        default:
            throw std::runtime_error("Unsupported encoding type");
    }
}


/// Convert an OpenCV matrix (cv::Mat) to a ROS Image message.
/**
 * \param[in] frame The OpenCV matrix/image to convert.
 * \param[in] frame_id ID for the ROS message.
 * \param[out] Allocated shared pointer for the ROS Image message.
 */
void convert_frame_to_message(
        const cv::Mat & frame, size_t frame_id, sensor_msgs::msg::Image::SharedPtr msg)
{
    // copy cv information into ros message
    msg->height = frame.rows;
    msg->width = frame.cols;
    msg->encoding = mat_type2encoding(frame.type());
    msg->step = static_cast<sensor_msgs::msg::Image::_step_type>(frame.step);
    size_t size = frame.step * frame.rows;
    msg->data.resize(size);
    memcpy(&msg->data[0], frame.data, size);
    msg->header.frame_id = std::to_string(frame_id);
}

int main(int argc, char * argv[])
{
    // Pass command line arguments to rclcpp.
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("usb_cam_driver");
    rclcpp::Logger node_logger = node->get_logger();

    int width = 1080;
    int height = 720;

    double freq = 30.0;
    // Set a loop rate for our main event loop.
    rclcpp::WallRate loop_rate(freq);

    bool show_camera = true;
    std::string topic("image");

    rmw_qos_profile_t custom_camera_qos_profile = rmw_qos_profile_default;

    RCLCPP_INFO(node_logger, "Publishing data on topic '%s'", topic.c_str());

    auto pub = node->create_publisher<sensor_msgs::msg::Image>(topic, 10);

    cv::VideoCapture cap;

    cap.open(2);
//    RCLCPP_WARN(node_logger, "CamInfo: %s", cap.getBackendName());



    // Set the width and height based on command line arguments.
    cap.set(cv::CAP_PROP_FRAME_WIDTH, static_cast<double>(width));
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, static_cast<double>(height));
    cap.set(cv::CAP_PROP_MODE, 9);
    cap.set(cv::CAP_PROP_BRIGHTNESS, 0.55);
    cap.set(cv::CAP_PROP_CONTRAST, 0.1);
    cap.set(cv::CAP_PROP_SATURATION, 0.2);
    cap.set(cv::CAP_PROP_HUE, 1.0);
    cap.set(cv::CAP_PROP_GAIN, 0.1);
    cap.set(cv::CAP_PROP_EXPOSURE, -10000.0);



    if (!cap.isOpened()) {
        RCLCPP_ERROR(node_logger, "Could not open video stream");
        return 1;
    }


    // Initialize OpenCV image matrices.
    cv::Mat frame;
    cv::Mat flipped_frame;

    // Initialize a shared pointer to an Image message.
    auto msg = std::make_shared<sensor_msgs::msg::Image>();
    msg->is_bigendian = false;

    size_t i = 1;
    while (rclcpp::ok()) {

        cap >> frame;

        convert_frame_to_message(frame, i, msg);

    if (show_camera) {
        // NOTE(esteve): Use C version of cvShowImage to avoid this on Windows:
        // http://stackoverflow.com/questions/20854682/opencv-multiple-unwanted-window-with-garbage-name
//        cv::Mat cvframe = frame;
        // Show the image in a window called "cam2image".
//        cv::imshow("cam2image", frame);
        // Draw the image to the screen and wait 1 millisecond.
//        cv::waitKey(1);
    }

        // Publish the image message and increment the frame_id.
        RCLCPP_INFO(node_logger, "Publishing image #%zd", i);
        pub->publish(*msg);
        ++i;

// Do some work in rclcpp and wait for more to come in.
        rclcpp::spin_some(node);
        loop_rate.sleep();

    }
rclcpp::shutdown();

return 0;
}