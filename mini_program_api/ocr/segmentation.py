import cv2
import numpy as np
import os

def segment(pic,
            MIN_COUNT=100,RHO_THRES=50,THETA_THRES=30/52,THETA_OFFSET=10/52,DEBUG=0):

    """
    这个函数用于将书籍照片分割为单个的书籍，返回一个储存单本书的bytes数组
    :param imgpath:     图片的路径
    :param MIN_COUNT:   200 霍夫变换中计数器的最小阈值，用于筛选不合格的直线。这个值越大，越不明显的直线就会被消除
    :param RHO_THRES:   rho的收敛半径，在这一范围内的直线都会被视作一条直线。这个值越大，越大范围内的直线就会被视作一条直线
    :param THETA_THRES: theta的收敛角度，在这一角度内的直线会被视作一条直线。这个值越大，越大倾斜角度内的直线就会被视作一个直线
    :param THETA_OFFSET:theta的过滤角度，在这一个角度之外的直线不会被视作书籍的分割线。这个值越大，倾斜的越厉害的直线就会被视作分割线
    :param DEBUG:       如果使用DEBUG模式的话，会生成一些中间结果以及展示效果。比如边缘、分割线、cut输出
    :return:            返回一个cuts数组，每个元素表示切出来的图片数组
    """
    # ================= 霍夫变换 ==================
    imgpath ="./test"
    img = cv2.imdecode(np.fromstring(pic, dtype=np.uint8), -1)
    IMG_HEIGHT = img.shape[0]
    IMG_WIDTH = img.shape[1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # 灰度处理
    edges = cv2.Canny(gray, 50, 150)                # 提取边缘
    lines = cv2.HoughLines(edges, 0.8, np.pi / 180, MIN_COUNT)  # 霍夫变换
    print("Hough change succeed...")
    # 输出文件
    dir_name = "./{0}_output".format(imgpath.split('.')[0])
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    if DEBUG:
        cv2.imwrite(dir_name + "/edges.png", edges)

    # ================= 过滤及聚簇 ====================

    results = []    # results 保存直线的tho和theta信息

    for line in lines:
        rho, theta = line[0]
        if abs(theta) < THETA_OFFSET or abs(np.pi-theta) < THETA_OFFSET:    # 保证正斜率与负斜率都被考虑到
            found = 0
            if len(results) == 0:
                results.append(line[0])
            else:
                for result in results:
                    rho_diff = abs(abs(result[0])-abs(rho))
                    if theta > np.pi/2:
                        theta = np.pi-theta
                    theta_diff = abs(theta - result[1])
                    # theta_diff_pi = abs(theta-np.pi)
                    # if theta < theta_diff_pi: theta_diff = theta
                    # else : theta_diff = theta_diff_pi
                    if rho_diff < RHO_THRES and theta_diff < THETA_THRES:
                        found = 1
                        break
                if not found: results.append(line[0])

    results.sort(key=(lambda x:x[0]))   # 按照rho的大小排序

    print("Collection succeed...")
    
    # ================= 矩形裁剪 ==================
    # 极坐标转换为直角坐标系
    linesEndpoints = []  # linesEndpoints 保存矩形的两个端点的信息
    for result in results:
        rho, theta = result
        x1, y1, x2, y2 = changeToPolar(rho, theta, IMG_HEIGHT)
        linesEndpoints.append((x1, y1, x2, y2))

    # 防止线相交
    linesEndpoints.sort(key=lambda point: point[0])
    for index, endPoints in enumerate(linesEndpoints):
        if index < len(linesEndpoints) - 1:
            if endPoints[2] > linesEndpoints[index + 1][2]:
                linesEndpoints.pop(index)
                print("remove!!!")

    cuts = []
    for index,endpoints in enumerate(linesEndpoints):
        if index < len(linesEndpoints) - 1:
            x1, y1, x2, y2 = endpoints
            x1_n, y1_n, x2_n, y2_n = linesEndpoints[index+1]
            # 左边界
            left = np.min([x1,x2,x1_n,x2_n])
            if left < 0: left = 0 # 防止越界
            # 右边界
            right = np.max([x1,x2,x1_n,x2_n])
            if right > IMG_WIDTH: right = IMG_WIDTH
            # 切割
            cut = img[:,left:right]
            cuts.append(cut)
            if DEBUG:
                cv2.imwrite(dir_name+"/cut_{0}.png".format(index), cut)

    print("Cut change succeed...")
    # ================= 绘图及保存 ==================

    if DEBUG:
        for index,endPoints in enumerate(linesEndpoints):
            x1, y1, x2, y2 = endPoints
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 10*index), 3)
        cv2.imwrite(dir_name + "/lines.png", img)
    string_cuts = []
    for cut in cuts:
        string_cuts.append(cv2.imencode(".jpg",cut)[1].tostring())
    return string_cuts


def changeToPolar(rho, theta,img_height):
    x1 = int(rho/np.cos(theta))
    y1 = 0
    x2 = int(x1 - img_height*np.tan(theta))
    y2 = img_height

    return x1,y1,x2,y2


if __name__ == "__main__":
    segment("test.png",DEBUG=1)
