from datetime import datetime

import cv2
from cvzone.HandTrackingModule import HandDetector
import Clicks

cap = cv2.VideoCapture(0)

detector = HandDetector(detectionCon=0.5, maxHands=2)
waitingSeconds = 1
distance = 100
waitingFrames = 20

waitingSeconds = waitingSeconds * 1000

handTypes = {}  # This dict stores hands via type ("Right": rightHand)

lastAction = datetime.now()  # To prevent to sequence access
checkRightCounter = 0  # Counter to count frames that achieve the condition (Right hand)
checkLeftCounter = 0  # Counter to count frames that achieve the condition (Left hand)

while True:
    _, img = cap.read()
    _img = img
    hands, img = detector.findHands(img)

    if len(hands) == 2:
        hand1 = hands[0]
        hand2 = hands[1]

        handType1 = hand1["type"]
        handType2 = hand2["type"]

        # cv2.circle(img, index_finger1, 10, color, cv2.FILLED)
        handTypes[handType1] = hand1
        handTypes[handType2] = hand2

        rightHand = handTypes.get("Right", 0)
        leftHand = handTypes.get("Left", 0)

        if not rightHand or not leftHand:
            continue

        index_finger1 = rightHand["lmList"][8]
        index_finger2 = leftHand["lmList"][8]

        rightUpFingers = detector.fingersUp(rightHand)
        leftUpFingers = detector.fingersUp(leftHand)
        now = datetime.now()
        diffSeconds = (now - lastAction).seconds * 1000

        if leftUpFingers[0] and leftUpFingers[1] and leftUpFingers[2] and not leftUpFingers[3] and not \
                leftUpFingers[4] and rightUpFingers[0] and rightUpFingers[1] and rightUpFingers[2] and rightUpFingers[3] \
                and rightUpFingers[4]:
            length, info, img = detector.findDistance(index_finger1, index_finger2, img)
            if length > distance:

                checkRightCounter += 1
                if diffSeconds > waitingSeconds and checkRightCounter > waitingFrames:
                    lastAction = now
                    checkRightCounter = 0
                    print("Right")
                    Clicks.swipe_right()
            else:
                checkRightCounter = 0

        if rightUpFingers[0] and rightUpFingers[1] and rightUpFingers[2] and not rightUpFingers[3] and not \
                rightUpFingers[4] and leftUpFingers[0] and leftUpFingers[1] and leftUpFingers[2] and leftUpFingers[3] \
                and leftUpFingers[4]:
            length, info, img = detector.findDistance(index_finger1, index_finger2, img)
            if length > distance:
                checkLeftCounter += 1
                if diffSeconds > waitingSeconds and checkLeftCounter > waitingFrames:
                    lastAction = now
                    print("Left")
                    print(1)
                    Clicks.swipe_left()
                    print(2)
                    checkLeftCounter = 0
            else:
                checkLeftCounter = 0

    img = cv2.flip(img, 1)
    cv2.imshow("Image", _img)
    cv2.waitKey(1)
    print(13)
