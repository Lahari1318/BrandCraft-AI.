# BrandCraft AI 
### AI-Powered Branding and Content Generation Platform

BrandCraft AI is a web-based application that helps businesses, entrepreneurs, content creators, and small shop owners generate creative branding and marketing content using artificial intelligence.

The platform simplifies branding by providing AI-assisted ideas, marketing content, and customizable YouTube thumbnail designs.

## Features

- **Brand Name Generator:** Creates creative brand names based on industry, target audience, and brand personality.
- **Tagline Generator:** Generates catchy slogans based on brand identity.
- **YouTube Thumbnail Generator:** Creates customizable 1280 × 720 SVG thumbnails with colorful backgrounds, bold text, and multiple layouts.
- **Social Media Caption Generator:** Generates promotional captions, calls to action, and hashtags.
- **Content Writing:** Assists with blogs, advertisements, product descriptions, and other marketing content.
- **Full Brand Strategy:** Suggests brand positioning, color palettes, target audiences, and marketing strategies.
- **AI Chat Assistant:** Supports branding questions and follow-up conversations.

## Technologies Used

**Frontend**
- HTML
- CSS
- JavaScript

**Backend**
- Python
- FastAPI
- Uvicorn

**AI Integration**
- Groq API
- GPT-OSS-20B

## Project Structure

```text
BrandCraft-AI/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Lahari1318/BrandCraft-AI.git
cd BrandCraft-AI
```

Alternatively, download the repository as a ZIP and extract it.

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `backend` folder.

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never upload real API keys to GitHub.

### 4. Start the backend

```bash
python -m uvicorn main:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

### 5. Start the frontend

Open another terminal:

```bash
cd frontend
python -m http.server 5500
```

If you're currently inside the `backend` folder, use `cd ../frontend` instead.

Open `http://127.0.0.1:5500/index.html` in your browser.

## Example Use Cases

**Kirana Shop:** Generate shop names and promotional taglines.

**Bakery:** Create social media captions for cakes and pastries.

**Clothing Brand:** Generate brand names and marketing strategies.

**YouTube Creator:** Design colorful, text-based thumbnails for videos.

**Small Business:** Create advertisements, descriptions, and branding ideas.

## Future Enhancements

- AI-generated thumbnail images
- PNG and JPG thumbnail export
- User authentication
- Saved branding projects and chat history
- Cloud deployment

## Project Status

Functional local development prototype.

## Note

The YouTube thumbnail generator currently uses SVG-based designs rather than AI-generated photographs. The Groq API is used for text generation.
