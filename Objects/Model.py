import easyocr
import concurrent.futures


class Model:
    # Initialize model
    def __init__(self, language="ru"):
        self.reader = easyocr.Reader([language])

    # Recognize photos in parallel
    def recognize(self, photos):
        recognized_photos = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.recognize_photo, photo) for photo in photos]

            concurrent.futures.wait(futures)

            for i, future in enumerate(futures):
                photo = photos[i]
                text = future.result()
                recognized_photos[photo] = text

        return recognized_photos

    # Recognizer
    def recognize_photo(self, photo):
        text = []
        for part in self.reader.readtext(photo):
            text.append(part)

        return text
