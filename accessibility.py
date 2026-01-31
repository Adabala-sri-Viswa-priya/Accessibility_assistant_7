import webbrowser
import subprocess
import os
import shutil

def open_application(app_name):
    # Try to open directly using shell
    try:
        subprocess.Popen(app_name, shell=True)
        return True
    except:
        pass

    # Search in Program Files
    program_paths = [
        os.getenv("PROGRAMFILES"),
        os.getenv("PROGRAMFILES(X86)"),
        os.getenv("LOCALAPPDATA"),
        os.getenv("APPDATA")
    ]

    exe_name = app_name.replace(" ", "").lower() + ".exe"

    for root in program_paths:
        if root:
            for folder, subfolders, files in os.walk(root):
                for file in files:
                    if file.lower() == exe_name:
                        full_path = os.path.join(folder, file)
                        subprocess.Popen(full_path)
                        return True

    return False


def process_command(command):
    command = command.lower().strip()

    # ---------- Open ANY WEBSITE ----------
    if "open" in command:
        content = command.replace("open", "").strip()

        # If includes .com / .in / .org / .net / .edu
        if "." in content:
            url = content
            if not url.startswith("http"):
                url = "https://" + url
            webbrowser.open(url)
            return f"Opening {content}..."

    # ---------- Known Websites ----------
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "amazon": "https://www.amazon.in",
        "flipkart": "https://www.flipkart.com",
        "chatgpt": "https://chat.openai.com",
    }

    for name, link in websites.items():
        if f"open {name}" in command:
            webbrowser.open(link)
            return f"Opening {name}..."

    # ---------- Open Apps ----------
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "whatsapp": "whatsapp.exe",
        "spotify": "spotify.exe",
        "telegram": "telegram.exe",
        "zoom": "zoom.exe",
        "obs": "obs64.exe",
        "vs code": r"code.exe",
    }

    for app, path in apps.items():
        if f"open {app}" in command:
            if open_application(path):
                return f"Opening {app}..."
            return f"{app} not found on system."

    # ---------- Try opening unknown app names ----------
    if "open" in command:
        app_name = command.replace("open", "").strip()
        if open_application(app_name):
            return f"Opening {app_name}..."
        else:
            return f"Could not find {app_name} installed."

    return "I didn’t understand that. Try: open spotify OR open flipkart.com"
