import argparse
import cv2
import time
import face_recognition 
from face_recognition import face_locations, face_encodings, load_image_file, compare_faces
import os
from intake_stream import get_input_stream
from typing import Dict, List, Tuple

class Doorman():
    def __init__(self) -> None:
        known_face_image_paths = [(face_file.split('.')[0], "./known_faces/"+face_file) for face_file in os.listdir("./known_faces")]
        self.known_face_encodings = dict([(name ,face_encodings(load_image_file(image_path))[0]) for name, image_path in known_face_image_paths])
    
    def detect_people(self,frame) -> Tuple(bool, int):
        return (True, 1)

    #shouldn't have to run two different models
    def recognize(self, frame):
        input_faces_encodings = face_recognition.face_encodings(frame)
        for input_face_encoding in input_faces_encodings:
            results = face_recognition.compare_faces(self.known_face_encodings.values, input_face_encoding)
            if any(results):
                return True
        return False

    def run(cap):
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--door_stream", action='store_true')
    parser.add_argument("--video", type=str, help="video path")
    args = parser.parse_args()

    if args.door_stream:
        cap = get_input_stream()
    elif args.video:
        cap = cv2.VideoCapture(args.video)
    else:
        cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    doorman = Doorman()
    
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Camera", frame)
            if Doorman.detect_people(frame)[0]:
                person_recognized = Doorman.recognize(frame)
                if person_recognized:
                    print("person_recognized! Unlock the door")
            time.sleep(0.5)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            raise ResourceWarning(f"Could not read from cap")
        
    # Release the camera
    cap.release()
    # Close all the windows
    cv2.destroyAllWindows()

    

