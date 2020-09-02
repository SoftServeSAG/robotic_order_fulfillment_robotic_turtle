//
// Created by root on 8/11/20.
//

#ifndef ROBOTIC_ORDER_FULFILLMENT_ROBOTIC_TURTLE_BARCODE_READ_H
#define ROBOTIC_ORDER_FULFILLMENT_ROBOTIC_TURTLE_BARCODE_READ_H

#include <memory>
#include <string>
#include <chrono>
#include "barcode_detect.h"
#include <rclcpp/clock.hpp>
#include <image_transport/image_transport.hpp>
#include <cv_bridge/cv_bridge.h>
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "sensor_msgs/image_encodings.hpp"
#include <opencv2/photo.hpp>
#include "xv2_msgs/srv/barcode_detect.hpp"
//#include "std_srvs/srv/trigger.hpp"
#include <thread>

rclcpp::Service<xv2_msgs::srv::BarcodeDetect>::SharedPtr is_detected_srv_;
rclcpp::Node::SharedPtr node = nullptr;

bool is_barcode_detected = false;
bool detect_barcode = false;
std::string detected_barcode = "";

std::chrono::duration<double> max_detect_time = static_cast<std::chrono::duration<double>>(30); //seconds


//void do_detect(const std::shared_ptr<rmw_request_id_t>/*request_header*/,
//               const std::shared_ptr<std_srvs::srv::Trigger::Request>/*request*/,
//               std::shared_ptr<std_srvs::srv::Trigger::Response> response);

void handle_service(
        const std::shared_ptr<rmw_request_id_t> request_header,
        const std::shared_ptr<xv2_msgs::srv::BarcodeDetect::Request> request,
        const std::shared_ptr<xv2_msgs::srv::BarcodeDetect::Response> response);

#endif //ROBOTIC_ORDER_FULFILLMENT_ROBOTIC_TURTLE_BARCODE_READ_H
