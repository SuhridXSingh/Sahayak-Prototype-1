# 🧪 Sahayak (Prototype Playground)

This is the UI/UX prototype for **Sahayak**. It demonstrates the "Electric Fence" document grounding logic, real-time animation integration, and the Gemini 3.0 Flash API backend.

---

## ⚡ Quick Start Guide

### 1. Download and Install
Open your terminal in the folder where you want to save the project.

```bash
# Clone the repository
git clone [https://github.com/YOUR-USERNAME/Sahayak-Prototype-Playground.git](https://github.com/YOUR-USERNAME/Sahayak-Prototype-Playground.git)
cd Sahayak-Prototype-Playground

# Install dependencies
pip install -r requirements.txt
2. Setup API Key
You need a Google Gemini API Key.

Get a free key from Google AI Studio.

Create a new file in this folder named .env

Paste your key inside it like this:

Ini, TOML

GOOGLE_API_KEY="AIzaSyDxxxxxxxxx..."
3. Run the App
Bash

streamlit run app.py
A browser window will open automatically at http://localhost:8501.

📂 Project Structure
app.py: Frontend UI (Streamlit)

backend.py: Logic & AI (Gemini 3.0 Flash)

requirements.txt: Dependencies

🛠️ Troubleshooting
Command not found: Try python -m streamlit run app.py

Model Error: If Gemini 3.0 fails, change backend.py line 20 to gemini-1.5-flash.
