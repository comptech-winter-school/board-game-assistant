import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt

from scipy.spatial import distance as dist

class Gameboard(object):
    boardtype = "3x3"

    def __init__(self, img_source, img_binary, intersection_width, intersection_points, gameboard=None, debug=False):
        self.source = img_source
        self.binary = img_binary
        self.intersection_width = intersection_width
        self.intersection_points = intersection_points
        self.intersection_mask = None
        self.debug = debug

        self.positions = []
        self._calculate_positions()
        # self.intersection_mask = gameboard.intersection_mask
        # self.intersection_points = gameboard.intersection_points

        self._draw_positions()
        self._detect_symbols()
        # if debug > 0:
        #     cv2.waitKey(0)

    def __repr__(self):
        jeje = str(self.status())
        return jeje

    def draw_symbol_on_slot(self, symbol, slot):
        pass

    def status(self):
        return [pos.symbol for pos in self.positions]

    def _detect_symbols(self):
        for position in self.positions:
            position.detect_symbol()

    def _draw_positions(self):
        for position in self.positions:
            position.draw_rectangle_on_image(self.source)
        if self.debug > 0:
            plt.imshow(self.source)
            plt.show()
            # cv2.imshow("Game positions", self.source)
        if self.debug > 1:
            cv2.waitKey(0)

    def _order_points(self, unordered_points):
        """ Orders given points from top left, top right, bottom left, bottom right """
        pts = np.array(unordered_points, dtype=int)
        # Sort by X coordinates
        xSorted = pts[np.argsort(pts[:, 0]), :]
        # Grab left-most and right-most points from the sorted x-coordinates
        leftMost = xSorted[:2, :]
        rightMost = xSorted[2:, :]
        # Sort left-most according to Y-coordinates to find top left and bottom left
        leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
        (tl, bl) = leftMost

        # Calculate Euclidian distance from top left anchor to bottom right anchor
        # using the Pythagorean theorem. The point with the largest distance
        # is the bottom right
        D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
        (br, tr) = rightMost[np.argsort(D)[::-1], :]
        return np.array([tl, tr, bl, br], dtype=int)

    def _slope(self, a, b):
        return float((b[1] - a[1]) / (b[0] - a[0]))

    def _create_line(self, p1, p2, vertical=True):
        p = [0, 0]
        q = list(self.source.shape[0:2])
        if not vertical:
            tmp = q[0]
            q[0] = q[1]
            q[1] = tmp

        if (p1[0] != p2[0]):
            m = self._slope(p1, p2)
            # y = m * x + b
            # b = y - (m*x)
            b = p1[1] - m * p1[0]
            p[1] = int(m * p[0] + b)
            q[1] = int(m * q[0] + b)
        else:
            p[0] = p2[0]
            q[0] = p2[0]
        p = tuple(p)
        q = tuple(q)
        return (p, q)

    def _create_mask(self, ordered_intersection_points):
        pts = ordered_intersection_points
        l1 = self._create_line(list(pts[0]), list(pts[2]))
        l2 = self._create_line(list(pts[1]), list(pts[3]))
        l3 = self._create_line(list(pts[0]), list(pts[1]), vertical=False)
        l4 = self._create_line(list(pts[2]), list(pts[3]), vertical=False)

        mask = np.zeros(self.source.shape, self.source.dtype)

        white = (255, 255, 255)
        black = (0, 0, 0)
        cv2.line(mask, l1[0], l1[1], white, int(self.intersection_width * 1.1))
        cv2.line(mask, l2[0], l2[1], white, int(self.intersection_width * 1.1))
        cv2.line(mask, l3[0], l3[1], white, int(self.intersection_width * 1.1))
        cv2.line(mask, l4[0], l4[1], white, int(self.intersection_width * 1.1))
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        # invert mask
        mask = cv2.bitwise_not(mask)

        if self.debug > 2:
            # cv2.imshow("mask", mask)
            # cv2.waitKey(0)

            plt.imshow(mask)
            plt.show()
        self.binary = cv2.bitwise_and(self.binary, mask)

    def _calculate_positions(self):
        middle = self._order_points(self.intersection_points)
        mask = self._create_mask(middle)

        dx = abs(int(round(dist.euclidean(middle[0], middle[1]), 0)))
        dy = abs(int(round(dist.euclidean(middle[0], middle[2]), 0)))
        w = 0  # int(self.intersection_width/2)

        offset_x_y = np.array([dx + w, dy + w])
        offset_nx_y = np.array([-dx - w, dy + w])
        offset_x_ny = np.array([dx + w, -dy - w])
        offset_x = np.array([dx + w, 0])
        offset_y = np.array([0, dy + w])

        topleft = np.subtract(middle, offset_x_y)
        topright = np.add(middle, offset_x_ny)
        topmid = np.subtract(middle, offset_y)
        bottommid = np.add(middle, offset_y)
        bottomright = np.add(middle, offset_x_y)
        bottomleft = np.subtract(middle, offset_x_ny)
        leftmost = np.subtract(middle, offset_x)
        rightmost = np.add(middle, offset_x)

        self.positions = [
            Gameposition(self.source, self.binary, "tl", topleft, self.debug),
            Gameposition(self.source, self.binary, "tm", topmid, self.debug),
            Gameposition(self.source, self.binary, "tr", topright, self.debug),
            Gameposition(self.source, self.binary, "ll", leftmost, self.debug),
            Gameposition(self.source, self.binary, "mm", middle, self.debug),
            Gameposition(self.source, self.binary, "rr", rightmost, self.debug),
            Gameposition(self.source, self.binary, "bl", bottomleft, self.debug),
            Gameposition(self.source, self.binary, "bm", bottommid, self.debug),
            Gameposition(self.source, self.binary, "br", bottomright, self.debug),
        ]

    @staticmethod
    def _get_center_position_of_rectangle(x1, x2, y1, y2):
        return (x1 + int((x2 - x1) / 2), int(y1 + (y2 - y1) / 2))

    @staticmethod
    def _preprocess_image_to_binary(image, debug=False):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thres, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        kernel = np.array((
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]), dtype="int")
        binary = cv2.erode(binary, kernel)
        # Invert the image
        binary = 255 - binary
        if debug > 2:
            # cv2.imshow("binary", binary)
            # cv2.waitKey(0)

            plt.imshow(binary)
            plt.show()
        return binary

    @staticmethod
    def update_gameboard(gameboard):
        source = gameboard.source
        binary = gameboard.binary
        w = gameboard.intersection_width
        positions = gameboard.positions
        return Gameboard(source, binary, w, positions, gameboard=gameboard)

    @staticmethod
    def detect_game_board(source, debug=False):
        image = Gameboard._preprocess_image_to_binary(source, debug)
        # Defining a kernel length
        kernel_length = np.array(image).shape[1] // 8
        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
        # A kernel of (3 X 3) ones
        kernel = np.array((
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]), dtype="int")
        # Morphological operation to detect vertical lines from an image
        img_temp1 = cv2.erode(image, verticle_kernel, iterations=1)
        verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=1)
        if debug > 3:
            # cv2.imshow("vlines", verticle_lines_img)
            # cv2.waitKey(0)

            plt.imshow(verticle_lines_img)
            plt.show()
        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(image, hori_kernel, iterations=1)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=1)
        if debug > 3:
            # cv2.imshow("hlines", horizontal_lines_img)
            # cv2.waitKey(0)

            plt.imshow(horizontal_lines_img)
            plt.show()
        intersections = cv2.bitwise_and(verticle_lines_img, horizontal_lines_img)
        if debug > 2:
            # cv2.imshow("intersections", intersections)
            # cv2.waitKey(0)
            plt.imshow(intersections)
            plt.show()
        # Create a mask, combine verticle and horizontal lines
        mask = verticle_lines_img + horizontal_lines_img
        # Find contours
        contours, hierarchy = cv2.findContours(intersections, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Find center positions, order = bottom left, bottom right, upper left, upper right
        positions = []
        red = (0, 0, 255)
        blue = (255, 0, 0)

        for i, cnt in enumerate(contours):
            boardweight = 0.1  # decrease this for finer detection
            approx = cv2.approxPolyDP(cnt, boardweight * cv2.arcLength(cnt, True), True)
            cv2.drawContours(source, [cnt], 0, red, -1)
            if debug > 3:
                # cv2.imshow("Showing game board intersection {0}".format(i + 1), source)
                # cv2.waitKey(0)

                plt.imshow(source)
                plt.show()
            if len(approx) == 4:
                # get the bounding rect
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(source, (x, y), (x + w, y + h), (255, 0, 0), 1)
                if debug > 1:
                    # cv2.imshow("rectangle", source)
                    # cv2.waitKey(0)
                    plt.imshow(source)
                    plt.show()
                center = Gameboard._get_center_position_of_rectangle(x, x + w, y, y + h)
                positions.append(center)
            else:
                raise Exception("Unable to detect game board intersections. Try to adjust the weight.")
        if (len(positions) != 4):
            raise Exception("Unable to detect 3x3 game board")
        return Gameboard(source, image, w, positions, debug=debug)


class Gameposition(object):
    def __init__(self, src_image, bin_image, title, positions, debug=False):
        self.source = src_image
        self.image = bin_image
        self.id = str(id(self))
        self.title = title
        self.symbol = "?"
        self.area = None
        self.positions = positions
        self.solidity = None
        self.debug = debug
        self._process_subimage(positions)

    def _process_subimage(self, positions):
        (tl, tr, bl, br) = tuple(positions)
        self.startpos = list(tl)
        self.endpos = list(br)
        dx = int(round(dist.euclidean(tl, tr), 0))
        dy = int(round(dist.euclidean(tl, bl), 0))

        # NOTE: self.image.shape returns [y,x] and not [x,y]
        if (self.endpos[0] > self.image.shape[1]):
            self.endpos[0] = list(self.image.shape)[1]
        if (self.endpos[1] > self.image.shape[0]):
            self.endpos[1] = list(self.image.shape)[0]
        self.startpos = tuple(self.startpos)
        self.endpos = tuple(self.endpos)
        self.roi = self.image[self.startpos[1]:self.endpos[1], self.startpos[0]:self.endpos[0]]

        self.roi_in_source = self.source[self.startpos[1]:self.endpos[1], self.startpos[0]:self.endpos[0]]
        self.area = dx * dy

    def draw_rectangle_on_image(self, image=None):
        if (type(image) != np.ndarray):
            image = self.image
        cv2.rectangle(image, self.startpos, self.endpos, (255, 0, 0), 1)
        coordinate = (int((self.endpos[0] + self.startpos[0]) / 2), int((self.endpos[1] + self.startpos[1]) / 2))
        font = cv2.FONT_HERSHEY_SIMPLEX
        black = (0, 0, 0)
        cv2.putText(self.source, self.title, coordinate, font, 2, black, 2, cv2.LINE_AA)

    def draw_symbol_on_position(self, symbol, position):
        coordinate = tuple(self.positions[0])
        font = cv2.FONT_HERSHEY_SIMPLEX
        black = (0, 0, 0)
        cv2.putText(self.source, symbol, coordinate, font, 4, black, 2, cv2.LINE_AA)

    def is_checked(self):
        return False

    def detect_symbol(self, avg_area=None):
        """ Attempts to detect a symbol in self.roi
        based on:
        * https://gurus.pyimagesearch.com/lesson-sample-advanced-contour-properties/
        * http://qtandopencv.blogspot.com/2015/11/analyze-tic-tac-toe-by-computer-vision.html
        """
        imgcopy = self.roi.copy()
        cnts = cv2.findContours(imgcopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        lSolidity = []
        for (i, c) in enumerate(cnts):
            # compute the area of the contour along with the bounding box
            # to compute the aspect ratio
            area = cv2.contourArea(c)
            # if there are multiple contours detected, check if the detected contour is at
            # least 6% of total area
            # also ignore the contour if it is larger than 70% of total area or less than 6% of total area
            ratio = area / self.area
            if ((len(cnts) > 1 and i >= 0 and (area < self.area * 0.01)) or ratio > 0.70 or ratio < 0.06):
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            # compute the convex hull of the contour, then use the area of the
            # original contour and the area of the convex hull to compute the
            # solidity
            hull = cv2.convexHull(c)
            hullArea = cv2.contourArea(hull)
            if (hullArea == 0):
                hullArea = 0.01
            solidity = area / float(hullArea)
            self.solidity = solidity
            lSolidity.append(solidity)
            found = False
            if (self._detect_if_o(solidity)):
                self.symbol = "O"
                found = True
            elif (self._detect_if_x(solidity)):
                found = True
                self.symbol = "X"

            if found:
                if self.debug > 0:
                    print("{0}: Contours: {1}, Solidity: {2}, Ratio: {3}, Detected: {4}".format(self.title, len(cnts),
                                                                                                solidity, ratio,
                                                                                                self.symbol))
                    img = self.roi_in_source.copy()

                    plt.imshow(img)
                    plt.show()
                break
        if (self.symbol in ("O", "X")):
            cv2.putText(self.roi_in_source, self.symbol, (int(x + (w / 2)), int(y + (h / 2))), cv2.FONT_HERSHEY_SIMPLEX,
                        1.25, (0, 0, 255), 4)
            return True
        return False

    def _detect_if_x(self, solidity):
        if (solidity > 0.30 and solidity < 0.9):
            return True
        return False

    def _detect_if_o(self, solidity):
        if (solidity > 0.9):
            return True
        return False