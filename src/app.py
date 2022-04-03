import cv2
import eel
import pandas as pd
from deepface import DeepFace
from time import sleep, perf_counter


def checkCam():
    '''Verifica conexão com webcam'''
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        raise IOError('Não foi possível acessar webcam')
    return capture


def faceDetector(capture):
    '''Detecta faces nas imagens'''
    # Função de busca por objetos sendo definida para buscar faces
    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Captura frame do streaming da webcam
    success, frame = capture.read()
    # Analisa a imagem em busca de faces
    faces = faceCascade.detectMultiScale(frame, 1.1, 4)
    # Identifica as expressões nas faces encontradas
    predictions = DeepFace.analyze(frame, actions=['emotion'])
    reaction = predictions["dominant_emotion"]
    frame = outlineFaces(faces, frame, predictions)
    cv2.imshow('Original', frame)
    return reaction


def checkReaction(new_reaction, reaction, reactions, start):
    if new_reaction != reaction:
        running_time = perf_counter() - start
        reactions.append((new_reaction, running_time))
    return reactions


def outlineFaces(faces, frame, predictions):
    '''Adiciona retângulos com expressão contornando as faces identificadas'''
    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, predictions["dominant_emotion"], (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4)
    return frame


def noFaceDetected():
    '''Informa rosto não detectado'''
    print("Tentando novamente...")


def stopRunning(capture, reactions):
    capture.release()
    cv2.destroyAllWindows()
    print(reactions)
    results = pd.DataFrame(reactions)
    writer = pd.ExcelWriter('Results.xlsx', engine='xlsxwriter')
    results.to_excel(writer, sheet_name='welcome', index=False)
    writer.save()


# Início da aplicação
exit_character = 'q'
capture = checkCam()
start = perf_counter()
reaction = 'neutral'
reactions = [(reaction, start)]

while True:
    # Try apenas para continuar tentando caso ocorra um erro de identificação de face
    try:
        new_reaction = faceDetector(capture)
        reactions = checkReaction(new_reaction, reaction, reactions, start)
    except ValueError:
        noFaceDetected()
    exitApp = cv2.waitKey(1) & 0xFF == ord(exit_character)
    if exitApp:
        stopRunning(capture, reactions)
        break
    sleep(1)
