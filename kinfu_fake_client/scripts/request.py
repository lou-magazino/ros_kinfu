#! /usr/bin/env python2

import rospy
import roslib; roslib.load_manifest('kinfu_msgs')
from kinfu_msgs.msg import KinfuTsdfRequest, KinfuRequestHeader

if __name__ == '__main__':
    rospy.init_node('kinfu_request')

    pub = rospy.Publisher("/kinfu_request_topic", KinfuTsdfRequest, queue_size = 3, latch = True)
    rate = rospy.Rate(1)
    msg = KinfuTsdfRequest()
    # headers
    msg.tsdf_header.request_type = KinfuRequestHeader.REQUEST_TYPE_GET_MESH
#    msg.tsdf_header.request_type = KinfuRequestHeader.REQUEST_TYPE_GET_TSDF
#    msg.tsdf_header.request_type = KinfuRequestHeader.REQUEST_TYPE_GET_CLOUD
#    msg.tsdf_header.request_type = KinfuRequestHeader.REQUEST_TYPE_GET_VIEW_CLOUD
    msg.tsdf_header.request_id = 0
    msg.tsdf_header.request_source_name = "test_scene"

    # request reset
    msg.request_reset = False
#    msg.request_reset = True

    # transform
    msg.request_transformation = False

    # bbox
    msg.request_bounding_box = False

    # sphere? another bounding maybe
    msg.request_sphere = False

    # subsample
    msg.request_subsample = False

    # bounding box view
    msg.request_bounding_box_view = False

    # send
    pub.publish(msg)
    rate.sleep()
