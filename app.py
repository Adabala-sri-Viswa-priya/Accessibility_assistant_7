from flask import Flask, render_template, request, jsonify
import subprocess
import webbrowser
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import time
from openpyxl import load_workbook
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "FAQ_Data.xlsx"

# --------------------------------------------------
# OPEN APPLICATION (EXE + MICROSOFT STORE APPS)
# --------------------------------------------------
def open_application(app_name):
    try:
        subprocess.run(f'start "" "{app_name}"', shell=True)
        return True
    except:
        return False


# --------------------------------------------------
# PROCESS VOICE COMMAND
# --------------------------------------------------
def process_command(command):
    command = command.lower().strip()

    # ---------------- WEBSITES ----------------
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "chatgpt": "https://chat.openai.com"
    }

    for name, url in websites.items():
        if f"open {name}" in command:
            webbrowser.open(url)
            return f"{name} opened successfully."

    # ---------------- MICROSOFT STORE APPS ----------------
    store_apps = {
        "whatsapp": "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
        "spotify": "shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify",
        "telegram": "shell:AppsFolder\\TelegramMessengerLLP.TelegramDesktop_t4vj0pshhgkwm!App",
        "zoom": "shell:AppsFolder\\ZoomVideoCommunications.Zoom_f4y2bhs0kz7ap!Zoom"
    }

    for app, shell_cmd in store_apps.items():
        if f"open {app}" in command:
            subprocess.run(f'start "" {shell_cmd}', shell=True)
            return f"{app} opened successfully."

    # ---------------- NORMAL EXE APPS ----------------
    exe_apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
        "command prompt": "cmd",
        "vs code": "code"
    }

    for app, exe in exe_apps.items():
        if f"open {app}" in command:
            open_application(exe)
            return f"{app} opened successfully."

    # ---------------- OPEN ANY WEBSITE ----------------
    if command.startswith("open"):
        target = command.replace("open", "").strip()
        if "." in target:
            if not target.startswith("http"):
                target = "https://" + target
            webbrowser.open(target)
            return "Website opened successfully."

    return "Sorry, I did not understand. Try saying open google or open whatsapp."


# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/accessibility_tools')
def accessibility_tools():
    return render_template('accessibility_tools.html')

@app.route('/text_to_speech')
def text_to_speech():
    return render_template('text_to_speech.html')

@app.route('/speech_to_text')
def speech_to_text():
    return render_template('speech_to_text.html')

@app.route('/navigation_help')
def navigation_help():
    return render_template('navigation_help.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


# ---------------- CHAT API ----------------
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    command = data.get("message", "")

    response_text = process_command(command)

    tts = gTTS(text=response_text, lang="en")
    audio_file = f"static/response_{int(time.time()*1000)}.mp3"
    tts.save(audio_file)

    return jsonify({
        "reply": response_text,
        "audio": f"/{audio_file}"
    })


# ---------------- TRANSLATION ----------------
@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text")
    target = data.get("target")

    translated = GoogleTranslator(source="auto", target=target).translate(text)
    return jsonify({"translatedText": translated})


# ---------------- TTS ----------------
@app.route("/tts", methods=["POST"])
def tts_api():
    data = request.get_json()
    text = data.get("text", "")
    lang = data.get("lang", "en")

    tts = gTTS(text=text, lang=lang)
    filename = f"static/output_{int(time.time() * 1000)}.mp3"
    tts.save(filename)

    return jsonify({"audio": f"/{filename}"})


# ---------------- FAQ FEEDBACK ----------------
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()

    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.append([
        data.get("name"),
        data.get("email"),
        data.get("message"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ])
    wb.save(EXCEL_FILE)

    return jsonify({"status": "success"})


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
