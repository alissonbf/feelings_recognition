import os
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud.storage import Blob
from google.cloud import vision
from google.cloud.vision import types

KEY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'feelings_recognition/keys/abftecnologia-56388dd8d1e6.json'
)

SCORE_NAME = {
    'UNKNOWN': 0,
    'VERY_UNLIKELY': 1,
    'UNLIKELY': 2,
    'POSSIBLE': 3,
    'LIKELY': 4,
    'VERY_LIKELY': 5,
}

FEELING_EMOTICON = {
    'joy': 'https://storage.cloud.google.com/abftecnologia.appspot.com/joy.png',
    'sorrow': 'https://storage.cloud.google.com/abftecnologia.appspot.com/sorrow.png',
    'anger': 'https://storage.cloud.google.com/abftecnologia.appspot.com/angry.png',
    'surprise': 'https://storage.cloud.google.com/abftecnologia.appspot.com/surprise.png',
}


class GCloudStorage(object):

    def __init__(self, bucket_name, project_name):
        self.client = None
        self.blob = None
        self.bucket = bucket_name
        self.__create_client(project_name=project_name)
        self.__create_bucket(bucket_name=bucket_name)

    def __create_client(self, project_name):
        credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
        self.client = storage.Client(project_name, credentials=credentials)

    def __create_bucket(self, bucket_name):
        self.bucket = self.client.get_bucket(bucket_name)

    def upload_file(self, file_name, file_stream):
        self.blob = Blob(file_name, self.bucket)
        self.blob.upload_from_file(file_stream)
        self.blob.make_public()


class Vision(object):

    def __init__(self, image_uri):
        self.client = None
        self.feeling = None
        self.feeling_emoticon = None
        self.__create_client()
        self.__detect_feeling(uri=image_uri)

    def __create_client(self):
        creds = service_account.Credentials.from_service_account_file(KEY_PATH)
        self.client = vision.ImageAnnotatorClient(credentials=creds)

    def __detect_feeling(self, uri):
        image = types.Image()
        image.source.image_uri = uri

        response = self.client.face_detection(image=image)
        faces = response.face_annotations
        for face in faces:
            print(face)
            likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')

            feelings = {
                'joy': SCORE_NAME[likelihood_name[face.joy_likelihood]],
                'sorrow': SCORE_NAME[likelihood_name[face.sorrow_likelihood]],
                'anger': SCORE_NAME[likelihood_name[face.anger_likelihood]],
                'surprise': SCORE_NAME[likelihood_name[face.surprise_likelihood]],
            }

            score = 0
            self.feeling = None
            for key, value in feelings.items():
                if value > score:
                    score = value
                    self.feeling = key
            if self.feeling:
                self.feeling_emoticon = FEELING_EMOTICON[self.feeling]
