import socket
import time
import pygame
import pyttsx3

# TTS 엔진 초기화
engine = pyttsx3.init()


HOST = '192.168.0.12'
sw=0
x = 1
y = 0
z = 0
PORT = 5050
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

try:
	s.bind((HOST, PORT))
except socket.error:
	print ('Bind failed ')

s.listen(5)
(conn, addr) = s.accept()
print ('Connected')

c=0
bosw = 0
while True:
    pygame.mixer.init()
    data = conn.recv(1024)
    data = data.decode('utf-8')
    if sw==0:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(str(x) + ".mp3")
        sound.set_volume(0.5)
        sound.play()

        sw=1
   
    data = data.split(" ")
    print( data)
    if x >= 8:
        x = 1
    if data[0] == "보":
        sound.set_volume(1 - float(data[1]))
        if bosw == 0:
                print("Ddd")
                text1 = '노래 실행'
                engine.setProperty('rate', 175)
                engine.setProperty('volume', 1 - float(data[1]))
                engine.say(text1)
                engine.runAndWait()
                time.sleep(1)
                bosw = 1
       
        pygame.mixer.music.unpause()
        y = 0
    if data[0] == "주먹":
        pygame.mixer.music.pause()
        text2 = '정지'
        bosw = 0
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 1)
        engine.say(text2)
        engine.runAndWait()
        time.sleep(1)
        y = 0
       
    a = 1
    reply =str(a)
    text_byte = reply.encode('utf-8')
    conn.send((text_byte))
conn.close()
