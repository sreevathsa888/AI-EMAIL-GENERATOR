import os
import base64
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()  # 👈 Loads environment variables from .env

import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json
from io import StringIO


# ── 1. Configuration ────────────────────────────────────────────────────────────
GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY")          # <-- export this!
SENDER_EMAIL     = os.getenv("SENDER_EMAIL")            # <-- export this!
RECIPIENT_EMAIL  = os.getenv("RECIPIENT_EMAIL")         # <-- export this!
SCOPES           = ["https://www.googleapis.com/auth/gmail.send"]

if not all([GEMINI_API_KEY, SENDER_EMAIL, RECIPIENT_EMAIL]):
    raise RuntimeError("❌ Set GEMINI_API_KEY, SENDER_EMAIL, and RECIPIENT_EMAIL env vars.")

# Gemini client
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("models/gemini-1.5-flash")

# Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ai-email-generator-1-dcno.onrender.com"}})

# ── 2. Gmail OAuth helper ───────────────────────────────────────────────────────
def get_gmail_service():
    creds = None
    creds_data = os.getenv("GOOGLE_TOKEN_JSON")
    creds_dict = json.loads(creds_data) if creds_data else None

    if creds_dict:
        creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            if not creds_json:
                raise RuntimeError("❌ GOOGLE_CREDENTIALS_JSON not set in .env")
            flow = InstalledAppFlow.from_client_config(json.loads(creds_json), SCOPES)
            creds = flow.run_local_server(port=8080, access_type="offline", prompt="consent")

            # Optionally: log token to console to update .env manually
            print("🔐 NEW GOOGLE_TOKEN_JSON:\n", creds.to_json())

    return build("gmail", "v1", credentials=creds)
# ── 3. Email-generation helpers ────────────────────────────────────────────────
def generate_email(summary: str) -> tuple[str, str]:
    """Return (subject, body) from Gemini."""
    prompt = f"""
You are an expert email copy-writer.
Write a professional email using these main points (bullet list may appear):

{summary}

Respond in exactly this format:
Subject: <subject text>
Body: <body text>
"""
    res = gemini_model.generate_content(prompt)
    output = (res.text or "").strip()
    print("🔍 Gemini raw output:\n", output)

    if "Subject:" not in output or "Body:" not in output:
        # Fallback if Gemini deviates
        return "AI-Generated Email", output

    try:
        subject_part, body_part = output.split("Body:", 1)
        subject = subject_part.replace("Subject:", "").strip()
        body    = body_part.strip()
        return subject, body
    except ValueError:
        return "AI-Generated Email", output

def build_gmail_message(sender: str, to: str, subject: str, body: str) -> dict:
    msg = MIMEText(body)
    msg["to"]      = to
    msg["from"]    = sender
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {"raw": raw}

def send_email_via_gmail(subject: str, body: str, to_email: str) -> str:
    service = get_gmail_service()
    message = build_gmail_message(SENDER_EMAIL, to_email, subject, body)
    sent_msg = service.users().messages().send(userId="me", body=message).execute()
    return sent_msg["id"]


# ── 4. Routes ──────────────────────────────────────────────────────────────────
@app.route("/", methods=["GET"])
def to_react():
    """Redirect root GET to React app."""
    return redirect("https://ai-email-generator-1-dcno.onrender.com/email")

@app.route("/", methods=["POST"])
def handle_generate_and_send():
    data = request.get_json(silent=True) or {}
    summary = data.get("summary", "").strip()
    recipient_email = data.get("email", "").strip()

    if not summary or not recipient_email:
        return jsonify({"success": False, "error": "Summary and recipient email are required"}), 400

    try:
        subject, body = generate_email(summary)
        gmail_id = send_email_via_gmail(subject, body, recipient_email)

        return jsonify({
            "success": True,
            "email_id": gmail_id,
            "subject": subject,
            "body": body
        })
    except Exception as err:
        print("❌ Backend error:", err)
        return jsonify({"success": False, "error": str(err)}), 500


# ── 5. Entrypoint ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)  # 👈 ADD `host="0.0.0.0"`

