from flask import Flask
from flask import request
from flask import jsonify
from flask import json

app = Flask(__name__)


@app.route("/keyboard")
def keyboard():
    response = {
        "type" : "buttons",
        "buttons" : ["처음으로", "챗봇등록", "취소하기"]
    }
    response = json.dumps(response, ensure_ascii=False)
    return response


@app.route("/message", methods=["POST"])
def message():
    data = json.loads(request.data)
    content = data["content"]
    if content == "처음으로":
        text = "처음으로 돌아왔습니다."
        url = "http://cfile237.uf.daum.net/image/2265F24B5603A3D704F183"
    elif content == "챗봇등록":
        text = "챗봇만들기에 성공하셨습니다!"
        url = "http://ppss.kr/wp-content/uploads/2017/05/3-51-540x303.jpg"
    else:
        text = "취소되었습니다."
        url = "http://thumbs.dreamstime.com/x/cancel-sign-button-3053748.jpg"

    response = {
      "message": {
        "text": text,
        "photo": {
          "url": url,
          "width": 640,
          "height": 480
        },
        "message_button": {
          "label": "네이버 홈으로",
          "url": "https://naver.com"
        }
      },
      "keyboard": {
        "type": "buttons",
        "buttons": [
          "처음으로",
          "챗봇등록",
          "취소하기"
        ]
      }
    }

    response = json.dumps(response, ensure_ascii=False)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
