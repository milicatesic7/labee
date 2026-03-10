# Welcome to Labee 🐝

### Your Intelligent Lab Report Assistant

Labee is a smart web application designed to help students verify their laboratory exercises with ease.
Simply upload a photo of your report, select one of the three available report types, and let Labee **buzz through the data** to generate your results in a structured table.

---

# Features

### Smart Image Upload

Quickly select images by clicking **"Select image"** or using the **"+ Drop your lab photo"** zone.

### Multiple Report Types

Support for **three specific laboratory report categories**.

### AI Data Extraction

Powered by **Gemini 2.5 Flash** to recognize handwriting and digits from your physical reports.

### Interactive Results

Results are automatically generated and displayed in **dynamic, easy-to-read tables**.

### Gracious Animations

Enjoy a calming animation of **bees flying across the screen** while the AI processes your data.

---

# Tech Stack

## Frontend

- **Vite + React.js**
- Standard **HTML, CSS, JavaScript**

Runs on:

```
http://localhost:5000/
```

---

## Backend

- **Python**
- **FastAPI** – web framework
- **Uvicorn** – ASGI server
- **CORS Middleware** – secure frontend communication

Runs on:

```
http://localhost:8000/
```

---

#  AI Feature: Gemini Integration

Labee integrates **Google Gemini 2.5 Flash** for precise analysis of laboratory data.

Note: You will need your own **Gemini API key** (available via Google AI Studio).

### Required Python Packages

```
google-genai
fastapi
uvicorn
python-multipart
```

---

# Setup Guide

## Getting Started

Follow these steps to run **Labee locally**.

---

# 1. Clone the Repository

```bash
git clone https://github.com/milicatesic7/labee.git
cd labee
```

---

# 2. Setup the Backend (Python + FastAPI)

### Prerequisites

- Python **3.10+**
- **pip** (Python package manager)

Navigate to the backend folder:

```bash
cd labee-backend
```

Install required libraries:

```bash
pip install fastapi uvicorn google-genai python-multipart
```

Create a **.env file** inside the backend folder and add your API key:

```
GEMINI_API_KEY=your_api_key_here
```

Start the backend server:

```bash
uvicorn frontend:app --reload
```

The API will run on:

```
http://localhost:8000/
```

---

# 3. Setup the Frontend (Vite + React)

### Prerequisites

- **Node.js (v18+ recommended)**
- **npm**

Navigate to the frontend folder:

```bash
cd labee-frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Open in your browser:

```
http://localhost:5000/
```

