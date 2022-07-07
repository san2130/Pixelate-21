import gym
import pixelate_arena
import time
import pybullet as p
import pybullet_data
import cv2
import numpy as np
from cv2 import aruco

ARUCO_PARAMETERS = aruco.DetectorParameters_create()
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
size = 12
gr = np.zeros((12, 12), int)
env = gym.make("pixelate_arena-v0")
time.sleep(12)
hcov, hncov, onx, ony, ond, patx, paty = ([] for i in range(7))
patstat = [0, 0]
orient = 2
start = 35
dict = {0: -size, 1: size, 2: -1, 3: 1}
dict2 = {0: 1, 1: 0, 2: 3, 3: 2}
c = np.zeros((size * size, 4), int)
t = q = 0
current = 0


def camera3():
    global orient
    img = env.camera_feed()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(imggray, ARUCO_DICT, parameters=ARUCO_PARAMETERS)
    pos = [(corners[0][0][0][0] + corners[0][0][2][0]) / 2, (corners[0][0][0][1] + corners[0][0][2][1]) / 2]
    a = complex(corners[0][0][0][0] - corners[0][0][3][0], corners[0][0][0][1] - corners[0][0][3][1])
    if a.imag == 0:
        if a.real > 0:
            orient = 3
        else:
            orient = 2
    elif a.real == 0:
        if a.imag > 0:
            orient = 1
        else:
            orient = 0
    return pos, a


def initorient():
    global orient, start
    pos, a = camera3()
    x = 65.5
    posy = round((pos[0] - x) / 53.5)
    posx = round((pos[1] - x) / 53.5)
    start = posx * size + posy
    print("Orientation=", orient, " Start=", start)


def orientx():
    _, a = camera3()
    if a.real > 0 and a.real <= 4 and orient == 0:
        for i in range(round(140 * a.real)):
            env.move_husky(-1, 1, -1, 1)
            p.stepSimulation()
    elif a.real <= -1 and a.real >= -4 and orient == 0:
        for i in range(round(140 * a.real * -1)):
            env.move_husky(1, -1, 1, -1)
            p.stepSimulation()
    elif a.imag > 0 and a.imag <= 4 and orient == 3:
        for i in range(round(140 * a.imag)):
            env.move_husky(-1, 1, -1, 1)
            p.stepSimulation()
        env.move_husky(0, 0, 0, 0)
        p.stepSimulation()
    elif a.imag <= -1 and a.imag >= -4 and orient == 3:
        for i in range(round(140 * a.imag * -1)):
            env.move_husky(1, -1, 1, -1)
            p.stepSimulation()
    elif a.imag > 0 and a.imag <= 4 and orient == 2:
        for i in range(round(140 * a.imag)):
            env.move_husky(1, -1, 1, -1)
            p.stepSimulation()
        env.move_husky(0, 0, 0, 0)
        p.stepSimulation()
    elif a.imag <= -1 and a.imag >= -4 and orient == 2:
        for i in range(round(140 * a.imag * -1)):
            env.move_husky(-1, 1, -1, 1)
            p.stepSimulation()
    elif a.real > 0 and a.real <= 4 and orient == 1:
        for i in range(round(140 * a.real)):
            env.move_husky(1, -1, 1, -1)
            p.stepSimulation()
    elif a.real <= -1 and a.real >= -4 and orient == 1:
        for i in range(round(140 * a.real * -1)):
            env.move_husky(-1, 1, -1, 1)
            p.stepSimulation()
    env.move_husky(0, 0, 0, 0)
    p.stepSimulation()


def forward(s):
    orientx()
    nodey = s // size * 53.5 + 65.5
    nodex = s % size * 53.5 + 65.5
    pos, slope = camera2()
    d = max(abs(pos[0] - nodex), abs(pos[1] - nodey))
    # print("forward")
    for i in range(0, round(620 / 54 * d)):
        env.move_husky(2, 2, 2, 2)
        p.stepSimulation()
    env.move_husky(0, 0, 0, 0)
    p.stepSimulation()


def right(dir1, x):
    # print("right")
    if x == 1:
        for i in range(365):
            env.move_husky(1, 1, 1, 1)
            p.stepSimulation()
    pos, slope = camera2()
    z = np.angle(dir1) - np.angle(slope)
    for i in range(0, round(829 - round(z, 4) * 6.4)):
        env.move_husky(3, -3, 3, -3)
        p.stepSimulation()
    env.move_husky(0, 0, 0, 0)
    p.stepSimulation()


def left(dir1, x):
    # print("left")
    if x == 1:
        for i in range(365):
            env.move_husky(1, 1, 1, 1)
            p.stepSimulation()
    pos, slope = camera2()
    z = np.angle(dir1) - np.angle(slope)
    for i in range(0, round(829 - round(z, 4) * 6.4)):
        env.move_husky(-3, 3, -3, 3)
        p.stepSimulation()
    env.move_husky(0, 0, 0, 0)
    p.stepSimulation()


def turn180(dir1, x):
    _, slope = camera3()
    if orient == 0 and x % 12 == 11:
        left(slope * complex(0, -1), 0)
        left(dir1, 0)
    elif orient == 3 and x >= 132:
        left(slope * complex(0, -1), 0)
        left(dir1, 0)
    else:
        right(slope * complex(0, 1), 0)
        right(dir1, 0)


def camera2():
    global orient, current
    img = env.camera_feed()
    img3 = img.copy()
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(imggray, ARUCO_DICT, parameters=ARUCO_PARAMETERS)
    pos = [(corners[0][0][0][0] + corners[0][0][2][0]) / 2, (corners[0][0][0][1] + corners[0][0][2][1]) / 2]
    if orient == 2 and current % 12 >= 6:
        pos[0] -= 6
        pos[1] -= 2
    elif orient == 2 and current % 12 < 6 and current > 59:
        pos[0] += 7
    elif orient == 2 and current % 12 >= 6 and current > 59:
        pos[0] += 6
    elif orient == 2:
        pos[0] += 6
    elif orient == 0 and current % 12 >= 6 and current > 59:
        pos[1] -= 5
    elif orient == 0 and current % 12 < 6 and current > 59:
        pos[1] += 2
    elif orient == 0 and current % 12 > 6 and current < 59:
        pos[1] += 8
    elif orient == 0:
        pos[1] += 2
    elif orient == 3 and current < 59 and current % 12 < 6:
        pos[0] += 8
        pos[1] -= 2
    elif orient == 3 and current > 59 and current % 12 > 6:
        pos[0] -= 14
    elif orient == 3 and current > 59 and current % 12 < 6:
        pos[0] += 8
    elif orient == 3:
        pos[0] -= 2
        pos[1] -= 2
    elif orient == 1 and current % 12 < 6 and current < 59:
        pos[1] += 8
    elif orient == 1 and current % 12 < 6:
        pos[1] -= 8
    elif orient == 1 and current % 12 >= 6 and current >72:
        pos[1] -= 8
    elif orient == 1:
        pos[1] += 8
    if (corners[0][0][0][0] - corners[0][0][3][0]) != 0:
        slope = complex(abs((corners[0][0][0][0] - corners[0][0][3][0])),
                        abs((corners[0][0][0][1] - corners[0][0][3][1])))
    else:
        slope = 0
    cv2.circle(img3, (round(pos[0]), round(pos[1])), 2, (0, 0, 255), 3)
    cv2.imshow("Check", img3)
    cv2.waitKey(30)
    return pos, slope


def exist(i, j):
    if i < 0 or j < 0 or i > size - 1 or j > size - 1:
        return False
    else:
        return True


def updatec(gr):
    x = 0
    global c
    for i in range(0, size):
        for j in range(0, size):
            if gr[i][j] == 0:
                c[x][:] = 0
            else:
                if exist(i - 1, j):
                    c[x][0] = gr[i - 1][j]
                if exist(i + 1, j):
                    c[x][1] = gr[i + 1][j]
                if exist(i, j - 1):
                    c[x][2] = gr[i][j - 1]
                if exist(i, j + 1):
                    c[x][3] = gr[i][j + 1]
            x += 1
    for i in range(len(onx)):
        f = True
        node = onx[i] * size + ony[i]
        for j in range(0, 4):
            if j != ond[i]:
                c[node][j] = 0
        if ony[i] == 11 and ond[i] == 3:
            f = False
        elif onx[i] == 11 and ond[i] == 1:
            f = False
        elif onx[i] == 0 and ond[i] == 0:
            f = False
        elif ony[i] == 0 and ond[i] == 2:
            f = False
        if f == True:
            node = node + dict.get(ond[i])
            c[node][dict2.get(ond[i])] = 0


def getContours(img, imgblur):
    x = y = w = h = 0
    centerx, centery, onex, oney, nc = ([] for i in range(5))
    global ond, t, q
    cont, a = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for con in cont:
        area = cv2.contourArea(con)
        ep = 0.048 * cv2.arcLength(con, True) - 0.7
        app = cv2.approxPolyDP(con, ep, True)
        x, y, w, h = cv2.boundingRect(app)
        if len(app) == 4 and area < 4000:
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            centerx.append(x + w / 2)
            centery.append(y + h / 2)
        elif len(app) == 3 and q == 0:
            k = -1
            onex.append(x + w / 2)
            oney.append(y + h / 2)
            for i in range(0, 3):
                for j in range(i + 1, 3):
                    if abs(app[i][0][1] - app[j][0][1]) < 4:
                        k = app[i][0][1]
                        break
            if k != -1:
                if k > oney[-1]:
                    ond.append(0)
                else:
                    ond.append(1)
            k = -1
            for i in range(0, 3):
                for j in range(i + 1, 3):
                    if abs(app[i][0][0] - app[j][0][0]) < 4:
                        k = app[i][0][0]
                        break
            if k != -1:
                if k > onex[-1]:
                    ond.append(2)
                else:
                    ond.append(3)
        elif len(app) > 4:
            nc.append(x + w / 2)
            nc.append(y + h / 2)
    return centerx, centery, onex, oney, nc


def color(lower, upper, lower2, upper2, img, x, t):
    y = []
    z = []
    ax = []
    ay = []
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(imghsv, lower, upper)
    mask2 = cv2.inRange(imghsv, lower2, upper2)
    mask = mask1 + mask2
    kern1 = np.ones((5, 5), np.uint8)
    kern2 = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kern2)
    mask = cv2.dilate(mask, kern1)
    imggreen = cv2.bitwise_and(img, img, mask)
    imggreen[mask == 0] = (255, 255, 255)
    imgblur = cv2.GaussianBlur(imggreen, (3, 3), 0)
    centx, centy, onex, oney, nc = getContours(mask, imgblur)

    if x != 5 and x != 6 and t == 0:
        for i in range(len(centx)):
            y.append(round((centx[i] - 65.5) / 53.5))
            z.append(round((centy[i] - 65.5) / 53.5))
        for i in range(len(y)):
            gr[z[i]][y[i]] = x
    elif x == 5 and t == 0:
        hcov.append(round((centy[0] - 65.5) / 53.5))
        hcov.append(round((centx[0] - 65.5) / 53.5))
        hncov.append(round((nc[1] - 65.5) / 53.5))
        hncov.append(round((nc[0] - 65.5) / 53.5))
        for i in range(len(onex)):
            onx.append(round((oney[i] - 65.5) / 53.5))
            ony.append(round((onex[i] - 65.5) / 53.5))
        gr[hcov[0]][hcov[1]] = 0
        gr[hncov[0]][hncov[1]] = 0
    elif x == 5 and t == 1:
        for i in range(len(centx)):
            ax.append(round((centy[i] - 65.5) / 53.5))
            ay.append(round((centx[i] - 65.5) / 53.5))
        for i in range(len(patx)):
            for j in range(len(ax)):
                if patx[i] == ax[j] and paty[i] == ay[j]:
                    patstat[i] = 1
    elif t == 0:
        for i in range(len(centx)):
            patx.append(round((centy[i] - 65.5) / 53.5))
            paty.append(round((centx[i] - 65.5) / 53.5))
        for i in range(len(patx)):
            gr[patx[i]][paty[i]] = 1


def camera(z):
    img = env.camera_feed()
    global img2
    img2 = img.copy()
    color(np.array([48, 166, 0]), np.array([65, 255, 255]), np.array([1, 0, 0]), np.array([0, 0, 0]), img, 2, z)
    color(np.array([28, 132, 0]), np.array([58, 255, 255]), np.array([1, 0, 0]), np.array([0, 0, 0]), img, 3, z)
    color(np.array([0, 0, 168]), np.array([0, 0, 255]), np.array([1, 0, 0]), np.array([0, 0, 0]), img, 1, z)
    color(np.array([133, 61, 8]), np.array([168, 255, 255]), np.array([1, 0, 0]), np.array([0, 0, 0]), img, 6, z)
    color(np.array([69, 130, 28]), np.array([116, 255, 255]), np.array([1, 0, 0]), np.array([0, 0, 0]), img, 1, z)
    color(np.array([0, 6, 135]), np.array([6, 255, 255]), np.array([169, 74, 0]), np.array([180, 255, 255]), img, 4, z)
    color(np.array([94, 130, 28]), np.array([124, 255, 255]), np.array([1, 0, 0]), np.array([0, 0, 0]), img, 5, z)


env.remove_car()
camera(0)
env.respawn_car()
initorient()
q = 1
ver = []
updatec(gr)


def unvisit(x):
    flag = True
    for i in range(len(ver)):
        if x == ver[i]:
            flag = False
            break
    return flag


def dikstra(g, side, start, end):
    min = 99999
    global ver
    l = time.time()
    z = time.time()
    dist = np.zeros(size * size, int)
    parent = np.zeros(size * size, int)
    path = []
    for i in range(0, len(dist)):
        if i != start:
            dist[i] = 99999
    current = start
    ver.append(start)
    while unvisit(end) and z - l < 3:
        z = time.time()
        for i in range(0, side[1]):
            if g[current][i] != 0:
                x = g[current][i] + dist[current]
                y = dict.get(i)
                if x < dist[current + y]:
                    dist[current + y] = x
                    parent[current + y] = current
        for i in range(0, len(dist)):
            if dist[i] < min and dist[i] != 0 and unvisit(i):
                min = dist[i]
                current = i

        ver.append(current)
        min = 99999
    x = end
    while x != start and z - l < 3:
        x = parent[x]
        path.append(x)
    path.reverse()
    path.append(end)
    ver = []
    return path, dist[end]


def exist2(i):
    if i >= 0 and i < 144:
        return True
    else:
        return False


def minnode(c, patx, paty, start, z):
    pat = patx * size + paty
    min = 9999
    path = []
    if z == 0:
        if c[pat][0] > 0 or (exist2(pat + dict.get(0)) and c[pat + dict.get(0)][1] > 0):
            end1 = pat + dict.get(0)
            if c[end1][1] > 0:
                pa, cost = dikstra(c, [size * size, 4], start, end1)
                if cost < min:
                    min = cost
                    path = pa
        if c[pat][1] > 0 or (exist2(pat + dict.get(1)) and c[pat + dict.get(1)][0] > 0):
            end2 = pat + dict.get(1)
            if c[end2][0] > 0:
                pa, cost = dikstra(c, [size * size, 4], start, end2)
                if cost < min:
                    min = cost
                    path = pa
        if c[pat][2] > 0 or (exist2(pat + dict.get(2)) and c[pat + dict.get(2)][3]) > 0:
            end3 = pat + dict.get(2)
            if c[end3][3] > 0:
                pa, cost = dikstra(c, [size * size, 4], start, end3)
                if cost < min:
                    min = cost
                    path = pa
        if c[pat][3] > 0 or (exist2(pat + dict.get(3)) and c[pat + dict.get(3)][2]) > 0:
            end4 = pat + dict.get(3)
            if c[end4][2] > 0:
                pa, cost = dikstra(c, [size * size, 4], start, end4)
                if cost < min:
                    min = cost
                    path = pa
    else:
        path, min = dikstra(c, [size * size, 4], start, pat)
    return path, min


def move(path):
    x = 0
    global orient, current
    while True:
        if x < len(path) - 1:
            z = path[x + 1]
            current = path[x]
            # print("Next node",z)
            if path[x] - path[x + 1] == 1:
                if orient == 3:
                    turn180(complex(-1, 0), path[x])
                    orient = 2
                elif orient == 0:
                    left(complex(-1, 0), 1)
                    orient = 2
                elif orient == 1:
                    right(complex(-1, 0), 1)
                    orient = 2
                forward(z)
            elif path[x] - path[x + 1] == size:
                if orient == 1:
                    turn180(complex(0, -1), path[x])
                    orient = 0
                elif orient == 2:
                    right(complex(0, -1), 1)
                    orient = 0
                elif orient == 3:
                    left(complex(0, -1), 1)
                    orient = 0
                forward(z)
            elif path[x] - path[x + 1] == -size:
                if orient == 0:
                    turn180(complex(0, 1), path[x])
                    orient = 1
                elif orient == 3:
                    right(complex(0, 1), 1)
                    orient = 1
                elif orient == 2:
                    left(complex(0, 1), 1)
                    orient = 1
                forward(z)
            elif path[x] - path[x + 1] == -1:
                if orient == 2:
                    turn180(complex(1, 0), path[x])
                    orient = 3
                elif orient == 0:
                    right(complex(1, 0), 1)
                    orient = 3
                elif orient == 1:
                    left(complex(1, 0), 1)
                    orient = 3
                forward(z)
        else:
            break
        x += 1


path = []
pat = 0
minimum = 9999
for i in range(2):
    gr[patx[1 - i]][paty[1 - i]] = 0
    updatec(gr)
    path1, min = minnode(c, patx[i], paty[i], start, 0)
    if min < minimum:
        minimum = min
        path = path1
        pat = i
    gr[patx[1 - i]][paty[1 - i]] = 1
    updatec(gr)
if pat == 0:
    gr[patx[1]][paty[1]] = 0
    updatec(gr)
else:
    gr[patx[0]][paty[0]] = 0
    updatec(gr)
print(path, min)
move(path)
env.remove_cover_plate(patx[pat], paty[pat])
camera(1)
move([path[len(path) - 1], patx[pat] * size + paty[pat]])
gr[start // size][start % size] = 0
if patstat[pat] == 0:
    gr[hncov[0]][hncov[1]] = 1
    updatec(gr)
    path, min = minnode(c, hncov[0], hncov[1], patx[pat] * size + paty[pat], 1)
    print(path, min)
    move(path)
    gr[patx[pat]][paty[pat]] = 0
    if pat == 0:
        pat = 1
    else:
        pat = 0
    gr[patx[pat]][paty[pat]] = 1
    updatec(gr)
    path, min = minnode(c, patx[pat], paty[pat], hncov[0] * size + hncov[1], 0)
    print(path, min)
    move(path)
    env.remove_cover_plate(patx[pat], paty[pat])
    move([path[len(path) - 1], patx[pat] * size + paty[pat]])
    gr[hncov[0]][hncov[1]] = 0
    gr[hcov[0]][hcov[1]] = 1
    updatec(gr)
    path, min = minnode(c, hcov[0], hcov[1], patx[pat] * size + paty[pat], 1)
    print(path, min)
    move(path)
else:
    gr[hcov[0]][hcov[1]] = 1
    updatec(gr)
    path, min = minnode(c, hcov[0], hcov[1], patx[pat] * size + paty[pat], 1)
    print(path, min)
    move(path)
    gr[patx[pat]][paty[pat]] = 0
    if pat == 0:
        pat = 1
    else:
        pat = 0
    gr[patx[pat]][paty[pat]] = 1
    updatec(gr)
    path, min = minnode(c, patx[pat], paty[pat], hcov[0] * size + hcov[1], 0)
    print(path, min)
    move(path)
    env.remove_cover_plate(patx[pat], paty[pat])
    move([path[len(path) - 1], patx[pat] * size + paty[pat]])
    gr[hcov[0]][hcov[1]] = 0
    gr[hncov[0]][hncov[1]] = 1
    updatec(gr)
    path, min = minnode(c, hncov[0], hncov[1], patx[pat] * size + paty[pat], 1)
    print(path, min)
    move(path)
cv2.waitKey(0)