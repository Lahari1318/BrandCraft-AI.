
import os
import re
import uuid
import base64
import textwrap
from html import escape
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

load_dotenv()

app = FastAPI(title="BrandCraft AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-20b"

client = Groq(api_key=API_KEY) if API_KEY else None

sessions = {}


class ChatMessage(BaseModel):
    text: str
    feature: Optional[str] = None
    answers: Optional[dict] = None
    session_id: Optional[str] = None


# ------------------------------------
# AI TEXT GENERATION
# ------------------------------------

def ask_ai(prompt, history=None):
    if not client:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is missing in .env"
        )

    messages = [{
        "role": "system",
        "content": (
            "You are BrandCraft AI, a creative branding "
            "and digital marketing assistant. "
            "Generate original, useful, specific results. "
            "Use clear formatting. Avoid generic answers. "
            "Never invent facts about a real business."
        )
    }]

    messages.extend((history or [])[-12:])

    messages.append({
        "role": "user",
        "content": prompt
    })

    result = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.75,
        max_tokens=1800
    )

    return result.choices[0].message.content or ""


# ------------------------------------
# SVG UTILITIES
# ------------------------------------

def safe(value):
    return escape(str(value), quote=True)


def svg_url(svg):
    data = base64.b64encode(
        svg.encode("utf-8")
    ).decode("ascii")

    return "data:image/svg+xml;base64," + data


COLORS = {
    "red": "#E63946",
    "blue": "#2563EB",
    "green": "#15966B",
    "purple": "#7C3AED",
    "pink": "#E84D9A",
    "orange": "#F97316",
    "yellow": "#F5B700",
    "gold": "#D4A017",
    "black": "#151515",
    "white": "#FFFFFF",
    "brown": "#80502F",
    "teal": "#0891B2",
    "cyan": "#06B6D4",
    "navy": "#172554"
}


def pick_color(text, default="#7C3AED"):
    text = str(text).lower()

    for word, value in COLORS.items():
        if re.search(r"\b" + word + r"\b", text):
            return value

    return default


def thumbnail_palette(answers):
    preference = str(answers.get("q4", "")).lower()
    style = str(answers.get("q5", "")).lower()

    primary = pick_color(preference)

    if "dark" in preference or "cinematic" in style:
        return "#0B1020", primary, "#FFFFFF"

    if "pastel" in preference:
        return "#F5E9FF", "#8B5CF6", "#21153B"

    if "neon" in preference:
        return "#0A1020", "#22D3EE", "#FFFFFF"

    if "bright" in preference:
        return "#3B0764", "#FDE047", "#FFFFFF"

    if "light" in preference:
        return "#F8FAFC", primary, "#172033"

    if primary == "#FFFFFF":
        return "#172554", "#FDE047", "#FFFFFF"

    return primary, "#FDE047", "#FFFFFF"


# ------------------------------------
# THUMBNAIL DESIGN
# ------------------------------------

def thumbnail_svg(answers, variation=0):
    topic = str(
        answers.get("q1", "Amazing Video")
    ).strip()

    emotion = str(
        answers.get("q2", "Exciting")
    ).strip()

    title = str(
        answers.get("q3", topic)
    ).strip() or topic

    style = str(
        answers.get("q5", "Bold")
    ).lower()

    background, accent, foreground = thumbnail_palette(
        answers
    )

    variation = variation % 4

    # Keep text readable on the thumbnail
    title = title[:100]

    lines = textwrap.wrap(
        title.upper(),
        width=17,
        break_long_words=True
    )[:4]

    if not lines:
        lines = ["YOUR VIDEO"]

    font_size = 86 if len(lines) <= 2 else 70

    # Alternate the position of the headline
    if variation == 0:
        x = 110
        anchor = "start"
    elif variation == 1:
        x = 640
        anchor = "middle"
    elif variation == 2:
        x = 110
        anchor = "start"
    else:
        x = 640
        anchor = "middle"

    title_svg = ""

    start_y = 280 - (len(lines) - 2) * 30

    for index, line in enumerate(lines):
        y = start_y + index * 100

        title_svg += f"""
        <text
            x="{x}"
            y="{y}"
            text-anchor="{anchor}"
            font-family="Arial, sans-serif"
            font-size="{font_size}"
            font-weight="900"
            fill="{foreground}"
            stroke="#000000"
            stroke-opacity="0.12"
            stroke-width="2"
            paint-order="stroke"
        >{safe(line)}</text>
        """

    # Four different decorative layouts
    if variation == 0:
        decoration = f"""
        <circle cx="1110" cy="350" r="250"
                fill="{accent}" opacity="0.85"/>
        <circle cx="1110" cy="350" r="185"
                fill="none" stroke="white"
                stroke-width="13" opacity="0.75"/>
        <path d="M1050 245 L1050 455 L1210 350 Z"
              fill="white"/>
        """

    elif variation == 1:
        decoration = f"""
        <circle cx="110" cy="110" r="170"
                fill="{accent}" opacity="0.5"/>
        <circle cx="1170" cy="620" r="250"
                fill="{accent}" opacity="0.45"/>
        <rect x="65" y="65" width="1150"
              height="590" rx="40"
              fill="none" stroke="{accent}"
              stroke-width="10"/>
        """

    elif variation == 2:
        decoration = f"""
        <polygon
            points="900,0 1280,0 1280,720 700,720"
            fill="{accent}" opacity="0.85"/>
        <circle cx="1050" cy="350" r="160"
                fill="none" stroke="white"
                stroke-width="18"/>
        <path d="M1005 270 L1005 430 L1135 350 Z"
              fill="white"/>
        """

    else:
        decoration = f"""
        <circle cx="640" cy="360" r="340"
                fill="{accent}" opacity="0.18"/>
        <circle cx="640" cy="360" r="280"
                fill="none" stroke="{accent}"
                stroke-width="20"/>
        <path d="M80 105 L1200 105"
              stroke="{accent}" stroke-width="12"/>
        <path d="M80 615 L1200 615"
              stroke="{accent}" stroke-width="12"/>
        """

    # Short label near the top
    label = "NEW VIDEO"

    if "gaming" in topic.lower() or "game" in topic.lower():
        label = "GAMING"

    elif "tutorial" in topic.lower() or "how to" in topic.lower():
        label = "TUTORIAL"

    elif "review" in topic.lower():
        label = "REVIEW"

    elif "food" in topic.lower() or "recipe" in topic.lower():
        label = "FOOD & RECIPES"

    elif "tech" in topic.lower() or "ai" in topic.lower().split():
        label = "TECH"

    if variation in (1, 3):
        label_x = 640
        label_anchor = "middle"
    else:
        label_x = 110
        label_anchor = "start"

    # Adjust headline placement to avoid label
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="1280" height="720"
         viewBox="0 0 1280 720">

      <defs>
        <linearGradient id="background"
                        x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="{background}"/>
          <stop offset="100%" stop-color="#111827"/>
        </linearGradient>
      </defs>

      <rect width="1280" height="720"
            fill="url(#background)"/>

      {decoration}

      <text x="{label_x}" y="125"
            text-anchor="{label_anchor}"
            font-family="Arial"
            font-size="33"
            font-weight="bold"
            letter-spacing="5"
            fill="{accent}">
        {safe(label)}
      </text>

      {title_svg}

      <rect x="90" y="635" width="330"
            height="54" rx="15"
            fill="{accent}"/>

      <text x="255" y="672"
            text-anchor="middle"
            font-family="Arial"
            font-size="27"
            font-weight="bold"
            fill="#111827">
        WATCH NOW
      </text>

    </svg>
    """

    return svg_url(svg)


def make_thumbnails(answers, start=0):
    return [
        thumbnail_svg(answers, start),
        thumbnail_svg(answers, start + 1),
        thumbnail_svg(answers, start + 2)
    ]


# ------------------------------------
# FEATURE PROMPTS
# ------------------------------------

def feature_prompt(feature, answers):
    a = answers

    if feature == "brand-name":
        return f"""
Generate 12 original brand name ideas.

Industry: {a.get('q1', '')}
Target audience: {a.get('q2', '')}
Personality: {a.get('q3', '')}
Preferred themes: {a.get('q4', '')}
Words to avoid: {a.get('q5', '')}

Give memorable names, their meanings,
and explain the best three.
Do not claim names or domains are available.
"""

    if feature == "tagline":
        return f"""
Generate 12 creative taglines.

Brand: {a.get('q1', '')}
Brand promise: {a.get('q2', '')}
Preferred length: {a.get('q3', '')}
Tone: {a.get('q4', '')}
Keywords: {a.get('q5', '')}
Existing tagline: {a.get('q6', '')}

Make them catchy and relevant.
Recommend the best three.
"""

    if feature == "social-captions":
        return f"""
Create 5 high-quality social media captions.

Platform type: {a.get('q1', '')}
Brand: {a.get('q2', '')}
Product/category: {a.get('q3', '')}
Campaign goal: {a.get('q4', '')}
Tone: {a.get('q5', '')}
Specific platforms: {a.get('q6', '')}
Length: {a.get('q7', '')}

Include a hook, caption, call to action,
and relevant hashtags for each.
"""

    if feature == "content-writing":
        return f"""
Create polished marketing content.

Content type: {a.get('q1', '')}
Topic: {a.get('q2', '')}
Audience: {a.get('q3', '')}
Tone: {a.get('q4', '')}
Length: {a.get('q5', '')}
SEO keywords: {a.get('q6', '')}

Use suitable headings, natural wording,
and an engaging conclusion.
"""

    if feature == "full-brand":
        return f"""
Create a complete branding strategy.

Business: {a.get('q1', '')}
Audience: {a.get('q2', '')}
Brand values: {a.get('q3', '')}
Existing ideas: {a.get('q4', '')}
Inspiration: {a.get('q5', '')}
Main platforms: {a.get('q6', '')}
Budget and requirements: {a.get('q7', '')}

Include:
1. Brand positioning
2. Brand personality
3. Brand name ideas
4. Taglines
5. Color palette
6. Typography suggestions
7. Target audience
8. Marketing strategy
9. Social media ideas
10. Action plan
"""

    return f"""
Help with this branding request:
{a}
"""


# ------------------------------------
# API ROUTES
# ------------------------------------

@app.get("/")
def home():
    return {
        "message": "BrandCraft AI is running",
        "thumbnail_mode": "Free SVG designs"
    }


@app.get("/test-image")
def test_image():
    answers = {
        "q1": "Gaming Tutorial",
        "q2": "Exciting",
        "q3": "TOP 5 GAMING TRICKS",
        "q4": "Purple",
        "q5": "Bold"
    }

    return {
        "status": "success",
        "image_generated": True,
        "image_url": thumbnail_svg(answers)
    }


@app.post("/api/chat")
def chat(message: ChatMessage):
    text = message.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    session_id = message.session_id or str(uuid.uuid4())

    state = sessions.setdefault(
        session_id,
        {
            "history": [],
            "thumbnail_answers": None,
            "thumbnail_variation": 0
        }
    )

    feature = (message.feature or "").lower()
    answers = message.answers or {}

    try:
        # Thumbnail questionnaire completed
        if feature == "thumbnails" and answers:
            state["thumbnail_answers"] = answers.copy()
            state["thumbnail_variation"] = 0

            return {
                "reply": (
                    "Here are three YouTube thumbnail designs. "
                    "Choose your favorite and download it. "
                    "Type 'alternative' for more layouts."
                ),
                "image_urls": make_thumbnails(answers),
                "done": True,
                "session_id": session_id
            }

        # Another thumbnail variation
        if (
            re.fullmatch(
                r"(alternative|another|more|another thumbnail|"
                r"more thumbnails|different thumbnail|"
                r"new variation)[!. ]*",
                text.lower()
            )
            and state["thumbnail_answers"]
            and not feature
        ):
            state["thumbnail_variation"] += 1

            start = state["thumbnail_variation"]

            return {
                "reply": "Here are more thumbnail layouts.",
                "image_urls": make_thumbnails(
                    state["thumbnail_answers"],
                    start
                ),
                "done": True,
                "session_id": session_id
            }

        # All other guided features
        if feature and answers:
            prompt = feature_prompt(feature, answers)
            reply = ask_ai(prompt)

        else:
            reply = ask_ai(text, state["history"])

            state["history"].append({
                "role": "user",
                "content": text
            })

            state["history"].append({
                "role": "assistant",
                "content": reply
            })

            state["history"] = state["history"][-16:]

        return {
            "reply": reply,
            "image_urls": [],
            "done": bool(answers),
            "session_id": session_id
        }

    except HTTPException:
        raise

    except Exception as error:
        print(
            "BrandCraft error:",
            type(error).__name__
        )

        raise HTTPException(
            status_code=502,
            detail="Generation failed. Check backend terminal."
        )
