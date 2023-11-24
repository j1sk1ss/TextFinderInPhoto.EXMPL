from Objects.Model import Model


class User:
    # Initialize user
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.photos = []

        self.is_sending = False
        self.setting_language = False

        self.model = None
        self.recognized_photos = {}

    # Initialize model
    def model_init(self, language='ru'):
        self.model = Model(language)

    # Recognize provided photos
    def recognize(self):
        self.recognized_photos = self.model.recognize(self.photos)

    # Find photo by text
    def get_photos(self, text: str):
        end_photos = []
        for photo in list(self.recognized_photos.keys()):
            for line in self.recognized_photos[photo]:
                if text.lower() in line.lower():
                    end_photos.append(photo)

        return end_photos
