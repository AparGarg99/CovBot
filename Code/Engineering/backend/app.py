from email import message
from flask import Flask, render_template, request, jsonify
from .api.FakeNewsEngine import fake_detector
from .api.CoughCovidTest import covid_test
from .api.QAEngine import qa_engine
from .api.option import Option
import wave
import six
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

# Static_folder: static resource, like css
# template_folder: template resource, like index.html
# static_url_path: Other resource
app = Flask(
    __name__,
    static_folder="./static",
    static_url_path="/",
    template_folder="./static")

@app.route('/')
def index():
    '''
        When browser visit the page, render index.html files in the dist folder.
    '''
    return render_template("index.html")

# Get message from user and return 
@app.route('/api/send_msg', methods=['POST'])
def send_msg():

    data = request.json
    content = data.get('content')
    option = data.get('option')
    # option_state = data.get('option_state')

    print('content = ', content)
    print('option = ', option)

    if option == None or content == None:
        return_data = {
            "message": f"Error option",
            "code": 1
        }
    elif option == Option.QA.value:
        # Do QA inference
        answer = qa_engine.predict(content)
        return_data = { # data return to FE
            "message": answer,
            "code": 0
        }
    elif option == Option.Fake.value:
        # Do fake detctor
        is_real, html = fake_detector.predict(content)

        real_text = 'real' if is_real else 'fake'
        if is_real:
            message = "This is a {} news.".format(real_text)
        else:
            message = "This is a {} news. The contributions of the components in the sentence to the results are shown below.".format(real_text)
            
        
        return_data = { # data return to FE
            "message": message,
            "html": html,
            "code": 0
        }
    else:
        return_data = { # data return to FE
            "message": f"Error option",
            "code": 1
        }
    return jsonify(return_data)



# Get cough audio from user and return covid test result
@app.route('/api/upload_audio', methods=['POST'])
def upload_audio():
    
    blob = request.files['file'].read() # bytes
    
    # # Test case to save the wav and manually check data
    # # reference: https://python.tutorialink.com/create-a-wav-file-from-blob-audio-django/
    # audio = wave.open('./testwav2.wav', 'wb')
    # audio.setnchannels(1)
    # audio.setsampwidth(2) # value by test
    # audio.setframerate(16000)
    # audio.writeframes(blob)
    # audio.close()

    # Test case to load test wav file
    # with open("testwav.wav", "rb") as wavfile:
    #     input_wav = wavfile.read()

    # print('blob', type(blob), type(input_wav))
    # print('check if blob === input_wav', blob == input_wav)
    # print('len()', len(blob), len(input_wav))
    
    #result=get_audio_prediction(blob)
    try:
        is_positive = covid_test.predict(raw_data = blob) # path='./testwav.wav'
        message = "Your Covid Test: {}.".format('Positive' if is_positive else 'Negative')
    except Exception as e:
        print('Exception', e)
        message = "Sorry. You may try later".format(e)

    return_data = {
            "message": message,
            "code": 0
    }
    return jsonify(return_data)


# translate function
@app.route('/api/translate', methods=['POST'])
def translation():
    data = request.json
    text = data.get('content')
    lang = data.get('lang') or 'zh'

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=lang)

    print('before translation===>', result["input"])
    print('after translation===>', result["translatedText"])
        
    return_data = {
            "message": result["translatedText"],
            "code": 0
    }
    return jsonify(return_data)
 

if __name__ == '__main__':
    app.run()