# ✉️ AI-Powered Email Generator

An intelligent web app that takes summary points from a user, uses **Google's Gemini Pro** API to generate a professional email, and sends it via **Gmail API** — all from a clean and modern React UI with a Python Flask backend.

---

## 🚀 Features

- 🔥 Generate polished email copy using AI (Gemini Pro)
- 📧 Send emails automatically with Gmail API (OAuth2)
- 🌐 Sleek React frontend with responsive design
- 🔒 Secure token-based Google authentication
- 🌙 Dark mode UI with animated background visuals

---

---

## 🛠 Tech Stack

| Layer       | Tech                           |
|-------------|--------------------------------|
| Frontend    | React + Vite + Tailwind CSS    |
| Backend     | Flask                          |
| AI Email    | Google Generative AI (Gemini)  |
| Mail Sender | Gmail API (OAuth2)             |

---

## 📦 Folder Structure
email-generator/
│
├── frontend/ # React app (Vite + JSX)
│ └── src/
│ ├── App.jsx
│ ├── EmailApp.jsx
│ ├── Landing.jsx
│ └── index.css
│
├── backend/ # Flask backend
│ ├── app.py
│ ├── credentials.json # Gmail OAuth creds
│ └── token.json # Gmail token (auto-generated)
│
├── assets/
│ └── email123.webp # Background image
│
├── screenshots/ # For README screenshots
│
└── README.md

✅SCREENSHOTS:

![Screenshot 2025-07-02 123046](https://github.com/user-attachments/assets/e9f5779e-6f87-44f1-b31e-f6a77f0d27c0)

![Screenshot 2025-07-02 123054](https://github.com/user-attachments/assets/863b2537-e93b-4ca0-8e8f-e405c05da1cd)

![Screenshot 2025-07-02 124142](https://github.com/user-attachments/assets/5b5bedbd-b82a-48b5-9538-72ed592fabf3)





✅ 2. Setup Python Flask Backend
cd backend
pip install -r requirements.txt
python app.py

Required Files:

credentials.json → from Google Cloud Console

token.json → will be generated on first Gmail OAuth login

✅ 3. Setup React Frontend
cd frontend
npm install
npm run dev

🔑 Environment Variables 
# .env (backend)
GEMINI_API_KEY=your_gemini_key_here

import os
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

🔄 API Integration
➤ POST / (from React)

{
  "success": true,
  "email_id": "17d8f654c4b7f5f6",
  "subject": "Introducing Our New AI Tool!",
  "body": "We're excited to announce..."
}

✅ Powered By:

Gemini Pro (Google Generative AI)

Gmail API (OAuth2)

Flask

React + Vite

✅ To-Do Enhancements:
 
 Add login with Google (OAuth)

 Email preview in UI before sending

 Export email as PDF

 Add email templates/themes

 📝 License
MIT © 2025 — oleti sree vathsa

