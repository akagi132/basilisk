import cv2

cap = cv2.VideoCapture(1)

ret, frame = cap.read()

img = cv2.resize(frame, (int(frame.shape[1]), int(frame.shape[0])))
cv2.imwrite('usb.png', img)

cap.release()
cv2.destroyAllWindows()
