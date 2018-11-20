import cv2

# Permette di avere informazioni sulla camera in uso
# Il set può essere effettuato solamente per alcune impostazioni

cap = cv2.VideoCapture(1)

print("GAIN:"+str(cap.get(cv2.CAP_PROP_GAIN)))
print("Frame_width:"+str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("Frame_height:"+str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print("FPS:"+str(cap.get(cv2.CAP_PROP_FPS)))
print("Brightness:"+str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
print("Contrast:"+str(cap.get(cv2.CAP_PROP_CONTRAST)))
print("Saturation:"+str(cap.get(cv2.CAP_PROP_SATURATION)))
print("Exposure:"+str(cap.get(cv2.CAP_PROP_EXPOSURE)))
print("White Balance U:"+str(cap.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U)))
print("White Balance V:"+str(cap.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V)))








