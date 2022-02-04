import torch
import numpy as np 
import cv2
import math
import scipy.spatial as spatial
import scipy.cluster as cluster
from collections import defaultdict
from . import checkersAIWrapper as ai
from .PythonCheckersAI.minimax.algorithm import minimaxForWhite,minimaxForRed
from .PythonCheckersAI.checkers.constants import RED, WHITE

class CheckersDetector():
    
    def __init__(self, pathToModel,pathToYolo, debug=False,debugOutputPath = ''):
        self.model = torch.hub.load(pathToYolo, "custom",path = pathToModel, device="cpu",source='local') # local
        self.debug = debug
        self.debugOutputPath = debugOutputPath
        self.counter = 0

    def _placeCheckers(self, points, checkers):
        field = np.zeros(shape = (8,8))
        for ch in checkers:
            xmin,ymin,xmax,ymax,cl = ch
            mindist1 = mindist2 = 100000
            minI = minJ = 0 
            for i in range(len(points)-1):
                line1 = points[i]
                line2 = points[i+1]
                for j in range(min(len(line1),len(line2))-1):
                    dist1 = math.sqrt((xmin - line1[j][0] )**2 +(ymin -line1[j][1])**2)
                    dist2 = math.sqrt((xmax -line2[j+1][0] )**2+(ymax -line2[j+1][1])**2 )
                    if dist1 < mindist1 and dist2 < mindist2:
                        mindist1 = dist1
                        mindist2 = dist2
                        minI = i 
                        minJ = j  
            field[minI,minJ] = cl + 1
        return field

    def _getIntersections(self, hLines,vLines):
        points = []
        for vline in vLines:
            vline = vline[0]
            for hline in hLines:
                hline = hline[0]
                s = np.vstack([[vline[0],vline[1]],[vline[2],vline[3]],[hline[0],hline[1]],[hline[2],hline[3]]])        # s for stacked
                h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
                l1 = np.cross(h[0], h[1])           # get first line
                l2 = np.cross(h[2], h[3])           # get second line
                x, y, z = np.cross(l1, l2)          # point of intersection
                if z != 0:
                    points.append([np.int32(x/z),np.int32(y/z)])
        return np.array(points)                  

    def _hvSplit(self, lines):
        hLines= []
        vLines= []
        const = 70
        for line in lines:
            if abs(line[0][0]-line[0][2])< const:
                hLines.append(line)
            elif abs(line[0][1]-line[0][3]) < const:
                vLines.append(line)
        return np.array(hLines),np.array(vLines)

    def _maskImage(self, img):
        grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grayed, (5,5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        c = 0
        for i in contours:
                area = cv2.contourArea(i)
                if area > 1000:
                        if area > max_area:
                            max_area = area
                            best_cnt = i
                            #cv2.drawContours(img, contours, c, (0, 255, 0), 3)
                c+=1
        mask = np.zeros((grayed.shape),np.uint8)
        cv2.drawContours(mask,[best_cnt],0,255,-1)
        cv2.drawContours(mask,[best_cnt],0,0,2)
        out = np.zeros_like(img)
        out[mask == 255] = img[mask == 255]
        return out

    def _findPointsPerline(self, points):
        res = []
        # TODO figure out smarter way to determine the epsilon
        epsilon = 10 
        lineStart = 0
        a , _ = points.shape 
        index = 0 
        while index < a - 1:
            j = index
            lineStart = points[j]
            tmp = []
            while j < a - 1 and abs(lineStart[1]-points[j][1]) < epsilon :
                tmp.append(list(points[j]))
                j += 1
            res.append(sorted(tmp))
            index = j 
        return np.array(res) 

    def _distance(self, point1, point2):
        return math.sqrt((point1[0]-point2[0])**2+ (point1[1]-point2[1])**2)

    #как же мне стыдно за это 
    def _correctPoints(self, points):
        points = points.tolist()
        epsilon = 10
        # correct xs
        for i in range(len(points)-1):
            if len(points[i]) < 1:
                points.pop(i)
        for i in range(len(points)):
            line = points[i]
            diffs = []
            for j in range(len(line)-1):
                diffs.append(self._distance(line[j],line[j+1]))
            diffs = np.array(diffs)
            mean = np.mean(diffs)
            newLine = []
            for j in range(len(line)):
                if j == len(line)-1 :
                    if self._distance(line[j],line[j-1])  >= mean - epsilon:
                        newLine.append(line[j])
                    continue
                if j == 0 :
                    if self._distance(line[j],line[j+1])  >= mean - epsilon:
                        newLine.append(line[j])
                    continue
                if self._distance(line[j],line[j+1])  >= mean - epsilon or self._distance(line[j],line[j-1])  >= mean - epsilon:
                    newLine.append(line[j])
            
            points[i] = newLine
        
        # we dont need lines with 1 or 2 points
        tmp=[]
        for point in points:
            if len(point) >= 7:
                tmp.append(point)
        points = tmp
        
        #correct ys
        diffs = []
        for i in range(len(points)-2):
            if len(points[i]) <= 1 or len(points[i+1]) <= 1: 
                continue
            diffs.append(self._distance(points[i][0],points[i+1][0]))
        mean = np.mean(np.array(diffs))
        res = []
        
        res = []
        eps = 20
        for i in range(len(points) - 2):
            if self._distance(points[i][0],points[i+1][0]) >= self._distance(points[i+1][0],points[i+2][0]) - eps:
                res.append(points[i])
        ln = len(points)
        if self._distance(points[ln-3][0],points[ln-2][0]) >= self._distance(points[ln-3][0],points[ln-2][0]) - eps:
                res.append(points[ln-2])
        if self._distance(points[ln-2][0],points[ln-1][0]) >= self._distance(points[ln-4][0],points[ln-5][0]) - eps:
                res.append(points[ln-1])  
        return res

    def _clusterPoints(self, points):
        dists = spatial.distance.pdist(points)
        single_linkage = cluster.hierarchy.single(dists)
        flat_clusters = cluster.hierarchy.fcluster(single_linkage, 10,'distance')
        cluster_dict = defaultdict(list)
        for i in range(len(flat_clusters)):
            cluster_dict[flat_clusters[i]].append(points[i])
        cluster_values = cluster_dict.values()
        clusters = map(lambda arr: (np.mean(np.array(arr)[:, 0]), np.mean(np.array(arr)[:, 1])), cluster_values)
        return np.array(sorted(list(clusters), key=lambda k: [k[1], k[0]]))

    def _visualize(self, img, grid,field):

        centerx = (np.int32(grid[1][0][0]) + np.int32(grid[0][1][0]))/2
        centery = (np.int32(grid[1][0][1]) + np.int32(grid[0][0][1]))/2
        color = img[np.int32(centery),np.int32(centerx)]
        colors = [(0,0,0),(255,255,255)] # 0 - black  1 - white 
        
        if color[0] > 100 or color[1] > 100 or color[2] > 100:
            switch = 1 
        else:
            switch = 0 
        res = np.zeros((640,640,3), np.uint8)
        
        for y in range(8):
            for x in range(8):
                cv2.rectangle(res,(x*80,y*80),((x+1)*80,(y+1)*80), colors[switch],-1 )
                switch = (switch + 1) %2
            switch = (switch + 1) %2
        
        for y in range(8):
            for x in range(8):
                if field[y][x] == 1:
                    cv2.circle(res,(80*x+40,80*y+40),35,(105,105,105),-1)
                elif field[y][x] == 2:
                    cv2.circle(res,(80*x+40,80*y+40),35,(255,255,255),-1)
                    
        return res 

    def _visualizeSuggestions():
        pass

    def _getSuggestions(self,field, grid, img,roll):
        game = ai.CustomGame(None, field,roll)
        
        _, newBoardForBlack = minimaxForRed(game.get_board(), 4, RED, game)
        _, newBoardForWhite = minimaxForWhite(game.get_board(), 4, WHITE, game)
        newBoardForBlack = newBoardForBlack.convertBoard()
        newBoardForWhite = newBoardForWhite.convertBoard()

        centerx = (np.int32(grid[1][0][0]) + np.int32(grid[0][1][0]))/2
        centery = (np.int32(grid[1][0][1]) + np.int32(grid[0][0][1]))/2
        color = img[np.int32(centery),np.int32(centerx)]
        colors = [(0,0,0),(255,255,255)] # 0 - black  1 - white 
        
        if color[0] > 100 or color[1] > 100 or color[2] > 100:
            switch = 1 
        else:
            switch = 0 
        resWhite = np.zeros((640,640,3), np.uint8)
        resBlack = np.zeros((640,640,3), np.uint8)
        
        for y in range(8):
            for x in range(8):
                
                if field[y][x] != newBoardForWhite[y][x]: 
                    cv2.rectangle(resWhite,(x*80,y*80),((x+1)*80,(y+1)*80), (0,255,0), -1 )
                else:
                    cv2.rectangle(resWhite,(x*80,y*80),((x+1)*80,(y+1)*80), colors[switch],-1 )
                
                if field[y][x] != newBoardForBlack[y][x]:
                    cv2.rectangle(resBlack,(x*80,y*80),((x+1)*80,(y+1)*80), (0,255,0), -1 )
                else:
                    cv2.rectangle(resBlack,(x*80,y*80),((x+1)*80,(y+1)*80), colors[switch],-1 )
                
                switch = (switch + 1) %2
            switch = (switch + 1) %2
        
        for y in range(8):
            for x in range(8):
                if newBoardForWhite[y][x] == 1:
                    cv2.circle(resWhite,(80*x+40,80*y+40),35,(105,105,105),-1)
                elif newBoardForWhite[y][x] == 2:
                    cv2.circle(resWhite,(80*x+40,80*y+40),35,(255,255,255),-1)
                
                if newBoardForBlack[y][x] == 1:
                    cv2.circle(resBlack,(80*x+40,80*y+40),35,(105,105,105),-1)
                elif newBoardForBlack[y][x] == 2:
                    cv2.circle(resBlack,(80*x+40,80*y+40),35,(255,255,255),-1)
                
        return (resWhite,resBlack) 

    def getGameField(self, img, visualize = False, roll = False):
        img = cv2.resize(img, (640,640))
        gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        edges = cv2.Canny(blur,50,150,apertureSize = 3)
        minLineLength=100
        lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=90,lines=np.array([]), minLineLength=minLineLength,maxLineGap=90)

        #detecting grid
        hLines, vLines = self._hvSplit(lines)
        points = self._getIntersections(hLines, vLines)
        points = self._clusterPoints(points)
        grid = self._findPointsPerline(points)
        grid = self._correctPoints(grid)

        #detecting checkers
        res = self.model(img)
        df = res.pandas().xyxy[0] 
        df = df[df.confidence>0.5] 
        df = df.drop(columns =["confidence","name"])
        checkers = df.to_numpy()
        field = self._placeCheckers(grid,checkers)

        if visualize:
            fl = self._visualize(img,grid,field)
        else:
            fl = field

        resWhite, resBlack = self._getSuggestions(field,grid,img,roll)

        if self.debug:
            a,_, = checkers.shape
            for i in range(a):
                if checkers[i][4] == 1 :
                    color = (255,0,0)
                else:
                    color = (0,0,255)
                cv2.rectangle(img, (np.int32(checkers[i][0]),np.int32(checkers[i][1])),(np.int32(checkers[i][2]),np.int32(checkers[i][3])), color = color)
            for j in range(len(grid)):
                color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
                for i in range(len(grid[j])):
                    cv2.circle(img, (np.int32(grid[j][i][0]),np.int32(grid[j][i][1])), radius=4, color=color, thickness=-1)   
                
            cv2.imwrite(self.debugOutputPath + "\\"+str(self.counter) + ".jpg",img)
            self.counter += 1
        
        return (fl, img, resWhite, resBlack)
