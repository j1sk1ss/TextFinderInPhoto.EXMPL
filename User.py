import easyocr
import concurrent.futures


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.is_sending = False
        self.photos = []

        self.setting_language = False

        self.reader = None
        self.recognized_photos = {}

    def model_init(self, language='ru'):
        self.reader = easyocr.Reader([language])

    def recognize(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.recognize_photo, photo) for photo in self.photos]

            concurrent.futures.wait(futures)

            for i, future in enumerate(futures):
                photo = self.photos[i]
                text = future.result()
                self.recognized_photos[photo] = text

        return self.recognized_photos

    def recognize_photo(self, photo):
        text = []
        for part in self.reader.readtext(photo):
            text.append(part[1])
        return text

    def get_photos(self, text: str):
        end_photos = []
        for photo in list(self.recognized_photos.keys()):
            for line in self.recognized_photos[photo]:
                if text.lower() in line.lower():
                    end_photos.append(photo)

        return end_photos
