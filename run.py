from flask import Flask, render_template, Response
import cv2

app = Flask(__name__, template_folder="html")

camera = cv2.VideoCapture(1)
print(camera)

def getFrames():
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            print("cannot get camera frame")
            continue
        
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        
        # concat frame one by one and show result
        yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video_feed")
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(getFrames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
