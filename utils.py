import json
import numpy as np
import cv2

"""COCO_PERSON_SKELETON = [
        [16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13],
    [6, 7], [6, 8], [7, 9], [8, 10], [9, 11]]"""
COCO_HEAD = [[3,4]]
COCO_PERSON_SKELETON = [
        [16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13],
    [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3],
    [2, 4], [3, 5], [4, 6], [5, 7]]

keypoints_names = ['nose', 'left_eye','right_eye','left_ear','right_ear','left_shoulder',
'right_shoulder','left_elbow','right_elbow','left_wrist','right_wrist','left_hip','right_hip',
'left_knee','right_knee','left_ankle','right_ankle']

TEXT_FACE = cv2.FONT_HERSHEY_DUPLEX
TEXT_SCALE = 0.3
TEXT_THICKNESS = 1



def normalize(X, Y, divide=True):
    center_p = (int((X[11]+X[12])/2), int((Y[11]+Y[12])/2))
    #X_new = np.array(X)-center_p[0]
    X_new = np.array(X)
    Y_new = np.array(Y)-center_p[1]
    width = abs(np.max(X_new)-np.min(X_new))
    height = abs(np.max(Y_new)-np.min(Y_new))
    if divide:
        Y_new /= max(width, height)
        X_new /= max(width, height)
    return X_new, Y_new

def draw_kps(img, kps, type='fullbody'):
    blk = np.zeros(img.shape, np.uint8)
    X, Y, C = kps[:17], kps[17:34], kps[34:]
    keypoints_list = keypoints_names
    if type == 'head':
        X, Y, C = X[:5], Y[:5], C[:5]
        keypoints_list = keypoints_names[:5]
    elif type == 'body':
        X, Y, C = X[5:], Y[5:], C[5:]
        keypoints_list = keypoints_names[5:]

    for i in range(len(Y)):
        #if i not in COCO_HEAD[0]:
            #c = int(255*C[i])
            #blk =cv2.circle(blk, (int(X[i]), int(Y[i])), 1, (255, 255-c, 255-c), 2)
        if 'nose' in keypoints_list[i]:
            cv2.circle(img, (int(X[i]), int(Y[i])), 2, (0, 0, 0), 4)
        elif 'eye' in keypoints_list[i]:
            cv2.circle(img, (int(X[i]), int(Y[i])), 2, (0, 0, 255), 4)
        elif 'left' in keypoints_list[i]:
            cv2.circle(img, (int(X[i]), int(Y[i])), 2, (150, 0, 0), 4)
        elif 'right' in keypoints_list[i]:
            cv2.circle(img, (int(X[i]), int(Y[i])), 2, (0,200,0), 4)
        #cv2.circle(img, (int(X[i]), int(Y[i])), 1, (255, 0, 0), 3)
        #cv2.putText(img, keypoints_list[i], (int(X[i]), int(Y[i])), TEXT_FACE, TEXT_SCALE, (127,127,255), TEXT_THICKNESS, cv2.LINE_AA)
    #img = cv2.addWeighted(img, 1.0, blk, 1, 0)
    return img

def draw_skeleton(img, kps, color, type='fullbody'):
    blk = np.zeros(img.shape, np.uint8)
    X, Y, C = kps[:17], kps[17:34], kps[34:]
    # In coco, connection shifted by 1 (starts at 1)
    skeleton=np.array(COCO_PERSON_SKELETON) - 1
    if type == 'head':
        skeleton = [c for c in skeleton if c[0] < 5 and c[1] < 5]
    elif type == 'body':
        skeleton = [c for c in skeleton if c[0] > 4 and c[1] > 4]

    linewidth = 2
    height = abs(Y[0]-Y[-1])
    for _, connection in enumerate(skeleton):
        c1, c2 = connection
        img = cv2.line(img,(int(X[c2]),int(Y[c2])),(int(X[c1]),int(Y[c1])), color,linewidth)

    """head = COCO_HEAD[0]
    c1, c2 = head
    radius = int(0.09*height)
    center = int((X[c1]+X[c2])/2), int((Y[c1]+Y[c2])/2)
    img = cv2.circle(img, center, radius, color, -1)
    img = cv2.circle(img, center, radius, (255, 255, 255), 2)"""
    return img


def add_legend(img, kps_type='full'):
    alpha = 0.9
    values = ['nose', 'eyes', "person's right joint", "person's left joint"]
    colors = [(0, 0, 0), (0, 0, 255), (0,128,0), (128, 0, 0)]
    # initialize the legend visualization
    #legend = np.zeros(img.shape, dtype='uint8')
    # loop over the class names + colors
    for (i, (className, color)) in enumerate(zip(values, colors)):
    	# draw the class name + color on the legend
    	cv2.putText(img, className, (10, i * 5 + 10),
    		cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
    	cv2.circle(img, (10, i * 5 + 10), 5, color, 2)
    #image = cv2.addWeighted(img, alpha, legend, 1 - alpha, 0)
    return img


def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    #print(rect)
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False
