# How to Run the Application Step-by-Step

This guide provides instructions on how to set up and run the PlantDocBot application locally.

## Prerequisites
Before you start, make sure you have the following installed:
- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js (v18+) and npm](https://nodejs.org/)
- A Google Gemini API key ([Get one here](https://aistudio.google.com/apikey))

---

## Step 1: Set Up and Run the Backend (FastAPI)

1. Open your terminal and navigate to the `backend` directory:
   ```bash
   cd d:\Plnt_bot\backend
   ```

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```cmd
     .\venv\Scripts\activate.bat
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install the required backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment variables:
   - Create a file named `.env` in the `backend/` directory.
   - Add your Gemini API key:
     ```env
     GEMINI_API_KEY=your_actual_gemini_api_key_here
     ```

6. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   - The backend API will be running at **http://localhost:8000**
   - You can view the interactive API documentation (Swagger UI) at **http://localhost:8000/docs**

---

## Step 2: Set Up and Run the Frontend (React + Vite)

1. Open a new terminal window or tab and navigate to the `frontend` directory:
   ```bash
   cd d:\Plnt_bot\frontend
   ```

2. Install the frontend dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm run dev
   ```
   - The frontend will be running at **http://localhost:5173**

---

## Step 3: Run Both & Test the Application

1. Open **http://localhost:5173** in your web browser.
2. **Test Image Upload**: Drag & drop or browse a leaf image to diagnose.
3. **Test Symptom Chatbot**: Write descriptions of plant symptoms (e.g., "yellow leaves with spots") to receive diagnostic treatments.
