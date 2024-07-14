import cv2 as cv
import mediapipe as mp
import math
class PoseDetector():

    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()


    def findPose(self, frame, draw=True):
        frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.fColor = self.pose.process(frameRGB)
        if self.fColor.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame, self.fColor.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return frame

    def findPosition(self, frame, draw=True):
        self.lmList = []
        if self.fColor.pose_landmarks:
            for id, lm in enumerate(self.fColor.pose_landmarks.landmark):
                h, w, c = frame.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if(draw):
                    cv.circle(frame, (cx, cy), 10, (255, 0, 0), cv.FILLED)
        return self.lmList

    def findAngle(self, frame, p1, p2, p3, draw = True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(math.atan2(y3-y2, x3-x2)-math.atan2(y1-y2, x1-x2))
        print(angle)

        if(draw):
            cv.line(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)
            cv.line(frame, (x2, y2), (x3, y3), (0, 0, 0), 3)
            cv.circle(frame, (x1, y1), 10, (0, 255, 0), cv.FILLED)
            cv.circle(frame, (x2, y2), 10, (0, 255, 0), cv.FILLED)
            cv.circle(frame, (x3, y3), 10, (0, 255, 0), cv.FILLED)
        return angle
