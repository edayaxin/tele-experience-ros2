import cv2
from serpapi import GoogleSearch


def search_image():
    params = {
    "engine": "google_reverse_image",
    "image_url": './tmp.jpg',
    "api_key": "f7b6b7636e1c103bcae3421bb217c5064e44325ff0c710344d3871f7676d72ac"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # inline_images = results["inline_images"]

    print(results)


def live_stream():
    capture = cv2.VideoCapture("http://192.168.0.102:8080/video")

    idx = 0
    while(True):
        ret, frame = capture.read()

        #transformations
        #    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        #    mirror = cv2.flip(gray, 1)
        cv2.imshow('livestream', frame)


        if (idx % 20 == 0):
            cv2.imwrite('tmp.jpg', frame)
            search_image()

        if cv2.waitKey(1) == ord('q'):
            break

        idx += 1

    capture.release()
    cv2.destroyAllWindows()



# search_image()
live_stream()