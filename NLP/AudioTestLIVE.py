import speech_recognition as sr
import datetime

r = sr.Recognizer()
m = sr.Microphone()

now = datetime.datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
print("date and time =", dt_string)

f = open("ClosedCaptions" + dt_string + ".txt", "x")

try:
    print("A moment of silence, please...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
                f.write(format(value).encode("utf-8") + '\n')

            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))
                f.write(format(value) + '\n')
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
