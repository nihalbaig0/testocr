from paddleocr import PaddleOCR,draw_ocr
import cv2
import paddle
import time
import serial

#Checking paddleocr requirements
paddle.utils.run_check()
ocr = PaddleOCR(use_angle_cls=True)

#Select Arduino PORT
ARDUINO_PORT = "COM8"
while True:
    # Trying to connect arduino
    try:
        ser = serial.Serial(ARDUINO_PORT, 115200, timeout=1.0)
        print("Successfully connected to arduino")
        break
    except serial.SerialException:
        print("Coudn't connect to arduino. Try again")
        time.sleep(1)

time.sleep(3)
ser.reset_input_buffer()
print("Serial ok")

def ocr_arduino():
    #Getting stream from video file
    #cap = cv2.VideoCapture('video.mp4')

    #Getting stream from webcam
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = ocr.ocr(rgb)
        txts = [line[1][0] for line in result]
        #print(txts)

        #Getting data from Arduino
        if ser.in_waiting > 0:
            send_sig = ser.readline().decode('utf-8').rstrip()
            print("received")
            print(send_sig)

        #Sending ocr data to Arduino
        if (len(txts) > 0):
            text = txts[0]+'\n'
            print("sent")
            print(text)
            ser.write(text.encode('utf-8'))
        cv2.imshow('frame', rgb)
        if cv2.waitKey(1) == ord('q'):
            break
        time.sleep(0.1)
    cap.release()
    cv2.destroyAllWindows()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ocr_arduino()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
