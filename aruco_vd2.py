from __future__ import print_function
from inspect import ArgSpec
import sys # Python 2/3 compatibility
import cv2 # Import the OpenCV library
import numpy as np # Import Numpy library
import imutils
import matplotlib.pyplot as plt # Libreria per mostrare immagini
import time
 
desired_aruco_dictionary = "DICT_ARUCO_ORIGINAL"
 
# Librerie ARUCO
ARUCO_DICT = {
  "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
  "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
  "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
  "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
  "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
  "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
  "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
  "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
  "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
  "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
  "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
  "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
  "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
  "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
  "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
  "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
  "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

def main():
  """
  Main method of the program.
  """
  # Costante di ingrandimento dell'immagine
  ingrandimento = int(1200)
  args = {
    "scoiattolo": "squirrel.jpg",
    "canyon": "canyon.jpg",
    "luna": "luna.jpg"
    }
  scoiattolo = cv2.imread(args["scoiattolo"])
  luna = cv2.imread(args["luna"])
  canyon = cv2.imread(args["canyon"])
  color = ()

  # Controlla se l'aurco marker è corretto
  if ARUCO_DICT.get(desired_aruco_dictionary, None) is None:
    print("[INFO] ArUCo tag of '{}' is not supported".format(
      ArgSpec["type"]))
    sys.exit(0)
     
  # Carica il dizionario Aruco
  print("[INFO] detecting '{}' markers...".format(
    desired_aruco_dictionary))
  this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
  this_aruco_parameters = cv2.aruco.DetectorParameters_create()
   
  # Inizia lo stream video [VideoCapture(0)=Webcam incorporata, da fare droidcam]
  cap = cv2.VideoCapture(0)

  # Cache strana
  cache = []
  cachi = []

  count = int(0)
  skip = False
  tempo_frame_nuovo=0
  tempo_frame_old=0
  font = cv2.FONT_HERSHEY_SIMPLEX

  fpsm=0
  fpsmi=100

  while(True):
  
    #cattura video webcam
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    (imgH, imgW) = frame.shape[:2]  

    # Detect ArUco markers in the video frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(
      frame, this_aruco_dictionary, parameters=this_aruco_parameters)
    
    if len(corners)==0:
      corners = cache
      ids = cachi
      count=count+1
    else:
      cache = corners
      cachi = ids
      count=0   

    # Controllo cache migliorata e se vengono trovati dei corners
    if count<15 and len(corners)!=0:
      # Flatten the ArUco IDs list
      ids = ids.flatten()
      
      if ids[0] == 1007:
        source_image = scoiattolo
      elif ids[0] == 150:
        source_image = canyon
      elif ids[0] == 1001:
        source_image  = luna
      else: 
        print("ERRORE")
        print(ids[0])
        skip=True
        # Da discutere se fare break oppure se mostrare foto Pesce Luna

      # Loop dei corners
      for (marker_corner, marker_id) in zip(corners, ids):
        
        # Skip per controllo coincidenza (se non corrisponde al posto di mostrare "Luna", break)
        if skip==True:
          skip=False
          break

        # Extract the marker corners
        corners = marker_corner.reshape((4, 2))
        (top_left, top_right, bottom_right, bottom_left) = corners

        # Convert the (x,y) coordinate pairs to integers
        # diff = (int(top_right[0])-int(top_left[0]))

        diff = np.sqrt(((top_right[0] - top_left[0])**2) + ((top_right[1] - top_left[1])**2))
        if top_right[1]>bottom_right[1]:
          diff = diff*-1
        if not diff==0:
          diff = ingrandimento // diff

        top_right = (int(top_right[0]+diff), int(top_right[1]-diff))
        bottom_right = (int(bottom_right[0]+diff), int(bottom_right[1]+diff))
        bottom_left = (int(bottom_left[0]-diff), int(bottom_left[1]+diff))
        top_left = (int(top_left[0]-diff), int(top_left[1]-diff))

        dstMat = [top_left, top_right, bottom_right, bottom_left]
        dstMat = np.array(dstMat)

        (srcH, srcW) = source_image.shape[:2]
        srcMat = np.array([[0, 0], [srcW, 0], [srcW, srcH], [0, srcH]])

        (H, _) = cv2.findHomography(srcMat, dstMat)
        warped = cv2.warpPerspective(source_image, H, (imgW, imgH))

        mask = np.zeros((imgH, imgW), dtype="uint8")
        cv2.fillConvexPoly(mask, dstMat.astype("int32"), (255, 255, 255),
	      cv2.LINE_AA)

        maskScaled = mask.copy() / 255.0
        maskScaled = np.dstack([maskScaled] * 3)

        warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
        #plt_imshow("warpedMultiplied", warpedMultiplied.astype("uint8"))

        marker_imageMultiplied = cv2.multiply(frame.astype(float), 1.0 - maskScaled)
        #plt_imshow("marker_imageMultiplied", marker_imageMultiplied.astype("uint8"))

        output = cv2.add(warpedMultiplied, marker_imageMultiplied)
        output = output.astype("uint8")
        frame=output
    
    tempo_frame_nuovo = time.time()
    fps = 1/(tempo_frame_nuovo-tempo_frame_old)
    tempo_frame_old=tempo_frame_nuovo

    if fps > fpsm:
      fpsm = fps
    
    if fps<fpsmi:
      fpsmi = fps

    if fps >= 60:
      color = (0, 255, 100)
    elif fps < 60 and fps > 30:
      color = (0, 255,  255)
    elif fps <= 30:
      color = (0, 0,  255)

    fps = str(int(fps))

    cv2.putText(frame, fps, (7, 30), font, 0.5, color, 1, cv2.LINE_AA)

    cv2.imshow("OpenCV AR Output", frame)      

    # If "q" is pressed on the keyboard, 
    # exit this loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  # Close down the video stream
  cap.release()
  cv2.destroyAllWindows()
  print("fps massimi: "+fpsm)
  print("fps minimi: "+fpsmi)
   
if __name__ == '__main__':
  print(__doc__)
  main()