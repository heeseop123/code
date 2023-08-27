import cv2
import mediapipe as mp
import numpy as np
import pygame
from gtts import gTTS
import time
from PIL import ImageFont, ImageDraw, Image
import socket
playing = 0
mf = 1
music = 2
pygame.init()
pygame.mixer.init()

text3 = "조명등"

tts = gTTS(text3, lang='ko')
tts.save("output3.mp3")
text4 = "스피커"
tts = gTTS(text4, lang='ko')
tts.save("output4.mp3")


text1 = "실행"
tts = gTTS(text1, lang='ko')
tts.save("output1.mp3")
text0 = "정지"
tts = gTTS(text0, lang='ko')
tts.save("output0.mp3")


text1 = "켰습니다"
tts = gTTS(text1, lang='ko')
tts.save("output11.mp3")
text0 = "껐습니다"
tts = gTTS(text0, lang='ko')
tts.save("output00.mp3")


mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

# 카메라 열기
cap = cv2.VideoCapture(0)
sw = 0
ldata = [0,0,0]
##HOST = '192.168.0.16'
### Enter IP or Hostname of your server
##PORT = 5050
### Pick an open Port (1000+ recommended), must match the server port
##s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##s.connect((HOST,PORT))
## Mediapipe 모델 로드
yy = 0
kk = 0
with mp_pose.Pose(min_detection_confidence=0.5) as pose_model, \
        mp_hands.Hands(min_detection_confidence=0.5) as hands_model:

    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 전처리
        frame = cv2.flip(frame, 1)  # 프레임 좌우 반전
        cv2.imshow("Frame", frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) == ord('q'):
            break       
        # Pose detection
        if sw == 0:
            pose_results = pose_model.process(frame)
            if pose_results.pose_landmarks:
                # Pose 관련 작업 수행
                # 예: 각 관절 점 찾기, 자세 분석 등
    ##            right_index_finger_tip = pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX_FINGER_TIP]
                uii_x = []
                uii_y = []
                for i in pose_results.pose_landmarks.landmark: # 11: 왼쪽 어깨 /  12 : 오른쪽 어깨  / 13 : 왼쪽 팔꿈치  / 14 : 오른쪽 팔꿈치 / 15 : 왼쪽 손목 / 16 : 오른쪽 손목
                    uii_x.append(i.x)
                    uii_y.append(i.y)
                if uii_y[2] > uii_y[15]:
                    pygame.mixer.music.load("output3.mp3")
                    pygame.mixer.music.play()
                    time.sleep(1)
                    ldata[0] = 1
                    sw = 1
                if uii_y[16] < uii_y[5]:
                    pygame.mixer.music.load("output4.mp3")
                    pygame.mixer.music.play()
                    ldata[0] = 2
                    time.sleep(1)
                    sw = 1
                    print("스피커")
##                else:
                    pass

                    
        if sw == 1 or sw == 2:
            hands_results = hands_model.process(frame)
            if hands_results.multi_hand_landmarks:
                # Hands 관련 작업 수행
                # 예: 손가락 점 찾기, 손가락 제스처 분석 등
                frame.flags.writeable = True
                image_height, image_width, _ = frame.shape
                # 예시: 손가락 개수 출력
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    

                    # 손가락의 상태를 나타내는 플래그 변수 초기화
                    thumb_finger_state = 0
                    index_finger_state = 0
                    middle_finger_state = 0
                    ring_finger_state = 0
                    pinky_finger_state = 0

                    # 엄지 손가락 상태 확인
                    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height:
                                thumb_finger_state = 1

                    # 검지 손가락 상태 확인
                    if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height:
                                index_finger_state = 1

                    # 중지 손가락 상태 확인
                    if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height:
                                middle_finger_state = 1

                    # 약지 손가락 상태 확인
                    if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height:
                                ring_finger_state = 1
                    # 새끼 손가락 상태 확인
                    if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height:
                        if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height:
                            if hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y * image_height > hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height:
                                pinky_finger_state = 1
##                    print(thumb_finger_state, index_finger_state,middle_finger_state,ring_finger_state,pinky_finger_state )
                    
                    # 가위바위보 조건식
                    if sw== 1 and   ldata[0] ==2:
                        if thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                            ldata[1] = 1
                            pygame.mixer.music.load("output1.mp3")#보 = 실행
                            pygame.mixer.music.play()
                            time.sleep(1)
                            sw = 2
                        if thumb_finger_state == 1 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                            ldata[1] = 0
                            pygame.mixer.music.load("output0.mp3")#보 = 실행
                            pygame.mixer.music.play()
                            sw = 0
                    if sw== 1 and   ldata[0] ==1:
                        if thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                            ldata[1] = 1
                            sw = 3
                            pygame.mixer.music.load("output11.mp3")#보 = 실행
                            pygame.mixer.music.play()
                            time.sleep(1)
                        if thumb_finger_state == 1 and index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                            ldata[1] = 0
                            sw = 3
                            pygame.mixer.music.load("output00.mp3")#보 = 실행
                            pygame.mixer.music.play()
                            time.sleep(1)
                    if sw == 2:
                        #mp3 권한 sw == 2
##                        print(mf)
                        if mf == 1:
                            print("노래실행", music)
                            
                            sound = pygame.mixer.Sound(str(music) + ".mp3")
                            sound.play()
                            sound.set_volume(1 - yy)
                            mf = 2
    
##                            time.sleep(1)
                        if mf == 2:
                             if thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 0 and pinky_finger_state == 0:
                                    print("가위",kk)
                                    yy = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y #손가락의 높이
                                    sound.set_volume(1 - yy)
                                    kk = kk+1
                             if kk >= 100:
                                 if thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                                        xx = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x
                                        print("노래 넘기기", xx)
                                        
                                        if xx <= 0.2:
                                                print("넘겼다")
                                                sound.stop()
                                                music=music+1
                                                time.sleep(1)
                                                sound = pygame.mixer.Sound(str(music) + ".mp3")
                                                sound.play()
                                                sound.set_volume(1 - yy)
                                                mf = 3
                                        if music == 4:
                                            music = 1
                    if sw == 3:
                        redata = str(ldata[0]) + " " + str(ldata[1]) + " " +str(ldata[2])
                        s.send(str(redata).encode('utf-8'))
                        reply = s.recv(1024)
                        sw = int(reply.decode('utf-8'))
                        print("보낼 데이터 값", ldata)
          
                                            


# 종료
cap.release()
cv2.destroyAllWindows()
