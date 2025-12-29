
# import os
# import json
# import textwrap
# import base64

# from dotenv import load_dotenv
# from openai import OpenAI
# from gtts import gTTS

# from moviepy.editor import (
#     ImageClip,
#     AudioFileClip,
#     concatenate_videoclips,
#     CompositeAudioClip,
# )
# from PIL import Image, ImageDraw, ImageFont

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# # ---------- 1. SCENE GENERATION (LLM) ----------

# def generate_scenes(keywords, level, language, duration_min, style):
#     """
#     Ask the LLM to return a richer, structured lesson:
#     - title
#     - definition
#     - explanation
#     - example
#     - analogy
#     - visual_hint
#     """
#     prompt = f"""
# You are an expert teacher. Create a {duration_min}-minute explainer script
# for {level} students in {language}.
# Topic keywords: {keywords}
# Video style: {style}.

# Break the lesson into 4–6 scenes.

# For EACH scene, return a JSON object with:
# - "scene": scene number (1, 2, 3, ...)
# - "title": a short title for this scene
# - "definition": 1–2 lines definition of the main concept in this scene
# - "explanation": 3–5 lines deeper explanation in simple language
# - "example": 2–3 lines real-life or practical example
# - "analogy": 1–2 lines analogy or comparison for intuition
# - "visual_hint": 1–2 lines describing what should be shown visually
# - "text": the full narration script for this scene (combined)

# Return STRICTLY a JSON array like:

# [
#   {{
#     "scene": 1,
#     "title": "Intro to CPU",
#     "definition": "...",
#     "explanation": "...",
#     "example": "...",
#     "analogy": "...",
#     "visual_hint": "simple diagram of a computer with CPU highlighted",
#     "text": "Full narration..."
#   }}
# ]

# Do NOT add backticks, markdown, or any explanation outside the JSON.
# """

#     response = client.responses.create(
#         model="gpt-4.1-mini",
#         input=prompt,
#     )

#     raw = response.output[0].content[0].text.strip()

#     # Handle case where model wraps JSON in ```json ... ```
#     if raw.startswith("```"):
#         raw = raw.strip("`")
#         # remove possible "json" language tag
#         if raw.lower().startswith("json"):
#             raw = raw[4:].strip()

#     scenes = json.loads(raw)
#     return scenes


# # ---------- 2. TEXT → SPEECH ----------

# def text_to_speech(text, out_path="output/scene1.mp3", lang="en"):
#     os.makedirs(os.path.dirname(out_path), exist_ok=True)
#     tts = gTTS(text=text, lang=lang)
#     tts.save(out_path)
#     return out_path


# # ---------- 3. AI IMAGE GENERATION PER SCENE ----------

# def generate_scene_image(scene, size="1024x1024"):
#     """
#     Generate an AI illustration based on visual_hint.
#     Uses OpenAI Images API (gpt-image-1).
#     """
#     scene_id = scene.get("scene", 0)
#     visual_hint = scene.get("visual_hint") or scene.get("title") or "educational diagram"

#     prompt = f"Clean, flat, educational infographic illustration. {visual_hint}"

#     try:
#         img_resp = client.images.generate(
#             model="gpt-image-1",
#             prompt=prompt,
#             size=size,
#             n=1,
#         )
#         b64_data = img_resp.data[0].b64_json
#         img_bytes = base64.b64decode(b64_data)

#         os.makedirs("output", exist_ok=True)
#         img_path = f"output/scene_{scene_id}_img.png"
#         with open(img_path, "wb") as f:
#             f.write(img_bytes)
#         return img_path
#     except Exception:
#         # If anything fails, return None, slide will just be text-based.
#         return None


# # ---------- 4. SLIDE GENERATION (INFOGRAPHIC LAYOUT) ----------

# def create_slide_image(scene, width=1920, height=1080):
#     """
#     Create an infographic-style slide:
#     - header bar with title
#     - AI-generated image on top/left (if available)
#     - structured bullet content on the right/bottom
#     """
#     scene_id = scene["scene"]
#     title = scene.get("title", f"Scene {scene_id}")
#     definition = scene.get("definition", "")
#     explanation = scene.get("explanation", "")
#     example = scene.get("example", "")
#     analogy = scene.get("analogy", "")

#     # --- COLORS ---
#     bg_color = (245, 247, 252)        # light background
#     header_color = (45, 96, 232)      # blue
#     box_color = (255, 255, 255)       # white
#     title_color = (255, 255, 255)     # white text
#     body_color = (30, 30, 30)         # dark text
#     accent_color = (90, 170, 90)      # green bullet dot

#     img = Image.new("RGB", (width, height), bg_color)
#     draw = ImageDraw.Draw(img)

#     # Fonts
#     try:
#         font_title = ImageFont.truetype("arial.ttf", 60)
#         font_section = ImageFont.truetype("arial.ttf", 32)
#         font_body = ImageFont.truetype("arial.ttf", 28)
#     except Exception:
#         font_title = ImageFont.load_default()
#         font_section = ImageFont.load_default()
#         font_body = ImageFont.load_default()

#     # --- HEADER ---
#     header_h = 130
#     draw.rectangle([(0, 0), (width, header_h)], fill=header_color)

#     title_text = f"Scene {scene_id}: {title}"
#     draw.text((60, 35), title_text, font=font_title, fill=title_color)

#     # --- MAIN LAYOUT ---
#     margin = 60
#     top = header_h + 40
#     bottom = height - 60
#     left = margin
#     right = width - margin

#     # Split area left/right: left for image, right for text
#     mid_x = left + int((right - left) * 0.45)

#     # IMAGE AREA
#     img_box_left = left
#     img_box_right = mid_x - 20
#     img_box_top = top
#     img_box_bottom = bottom

#     # TEXT AREA
#     text_box_left = mid_x + 20
#     text_box_right = right
#     text_box_top = top
#     text_box_bottom = bottom

#     # Draw rounded rectangles for both areas
#     radius = 30
#     try:
#         draw.rounded_rectangle(
#             [(img_box_left, img_box_top), (img_box_right, img_box_bottom)],
#             radius=radius,
#             fill=box_color,
#             outline=(220, 220, 220),
#             width=2,
#         )
#         draw.rounded_rectangle(
#             [(text_box_left, text_box_top), (text_box_right, text_box_bottom)],
#             radius=radius,
#             fill=box_color,
#             outline=(220, 220, 220),
#             width=2,
#         )
#     except Exception:
#         draw.rectangle(
#             [(img_box_left, img_box_top), (img_box_right, img_box_bottom)],
#             fill=box_color,
#             outline=(220, 220, 220),
#             width=2,
#         )
#         draw.rectangle(
#             [(text_box_left, text_box_top), (text_box_right, text_box_bottom)],
#             fill=box_color,
#             outline=(220, 220, 220),
#             width=2,
#         )

#     # --- AI IMAGE (inside left box) ---
#     image_path = generate_scene_image(scene)
#     if image_path and os.path.exists(image_path):
#         try:
#             ill = Image.open(image_path).convert("RGB")
#             box_w = img_box_right - img_box_left - 40
#             box_h = img_box_bottom - img_box_top - 40
#             ill.thumbnail((box_w, box_h), Image.Resampling.LANCZOS)
#             ill_x = img_box_left + (img_box_right - img_box_left - ill.width) // 2
#             ill_y = img_box_top + (img_box_bottom - img_box_top - ill.height) // 2
#             img.paste(ill, (ill_x, ill_y))
#         except Exception:
#             pass  # if anything fails, just show empty box

#     # --- STRUCTURED TEXT (inside right box) ---
#     padding = 35
#     cur_x = text_box_left + padding
#     cur_y = text_box_top + padding
#     text_area_width = (text_box_right - text_box_left) - 2 * padding
#     max_width_chars = max(30, text_area_width // 14)

#     def draw_section(title_label, body_text):
#         nonlocal cur_y
#         if not body_text.strip():
#             return
#         # Section title
#         draw.text((cur_x, cur_y), title_label, font=font_section, fill=header_color)
#         cur_y += 40

#         # Bullet content
#         wrapped = textwrap.wrap(body_text, width=max_width_chars)
#         for line in wrapped:
#             if cur_y > text_box_bottom - padding - 30:
#                 return
#             # bullet dot
#             draw.ellipse(
#                 (cur_x, cur_y + 8, cur_x + 10, cur_y + 18),
#                 fill=accent_color,
#                 outline=accent_color,
#             )
#             draw.text((cur_x + 20, cur_y), line, font=font_body, fill=body_color)
#             cur_y += 34
#         cur_y += 15  # small gap after section

#     draw_section("Definition", definition)
#     draw_section("Explanation", explanation)
#     draw_section("Example", example)
#     draw_section("Analogy", analogy)

#     out_path = f"output/scene_{scene_id}.png"
#     img.save(out_path)
#     return out_path


# # ---------- 5. CREATE SCENE CLIP ----------

# def create_scene_clip(scene, audio_path, width=1920, height=1080):
#     audio = AudioFileClip(audio_path)
#     duration = audio.duration

#     slide_path = create_slide_image(scene, width, height)
#     img_clip = ImageClip(slide_path).set_duration(duration)

#     # Simple fade-in for each scene
#     clip = img_clip.set_audio(audio).fadein(0.5)
#     return clip


# # ---------- 6. BUILD FINAL VIDEO (with optional background music) ----------

# def build_video_from_scenes(
#     scenes,
#     out_path="output/final_video.mp4",
#     lang="en",
#     bg_music_path="assets/bg_music.mp3",
# ):
#     os.makedirs("output", exist_ok=True)
#     clips = []

#     for scene in scenes:
#         scene_id = scene["scene"]
#         full_text = scene.get("text") or (
#             (scene.get("definition", "") + " " +
#              scene.get("explanation", "") + " " +
#              scene.get("example", "") + " " +
#              scene.get("analogy", ""))
#         )

#         audio_path = f"output/scene_{scene_id}.mp3"
#         text_to_speech(full_text, audio_path, lang)

#         clip = create_scene_clip(scene, audio_path)
#         clips.append(clip)

#     if not clips:
#         return None

#     # Crossfade between scenes
#     final = clips[0]
#     for clip in clips[1:]:
#         final = concatenate_videoclips([final, clip.crossfadein(0.6)])

#     # Optional background music if file exists
#     if bg_music_path and os.path.exists(bg_music_path):
#         try:
#             music = AudioFileClip(bg_music_path).volumex(0.15)
#             music = music.set_duration(final.duration)
#             final_audio = CompositeAudioClip([final.audio, music])
#             final = final.set_audio(final_audio)
#         except Exception:
#             # if anything fails, just keep original audio
#             pass

#     final.write_videofile(
#         out_path,
#         fps=30,
#         codec="libx264",
#         audio_codec="aac",
#         bitrate="3000k",
#     )
#     return out_path
import os
import json
import textwrap

from dotenv import load_dotenv
from openai import OpenAI
from gtts import gTTS

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont

# ---------------- SETUP ----------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
os.makedirs("output", exist_ok=True)


# ---------------- 1. DETAILED SCRIPT (4–5 MIN) ----------------
def generate_scenes(keywords, level, language, duration_min, style):
    prompt = f"""
You are an expert teacher.

Create a DETAILED {duration_min}-minute lesson for {level} students in {language}.
Topic: {keywords}

Rules:
- Create 4–6 scenes
- Each scene must be detailed
- Include explanation + examples
- Spoken English, easy to understand

Return ONLY valid JSON array:
[
  {{
    "scene": 1,
    "title": "Scene title",
    "text": "Detailed narration text"
  }}
]
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    raw = response.output_text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]

    return json.loads(raw)


# ---------------- 2. ONE FAST TTS CALL ----------------
def generate_full_audio(scenes, out_path="output/full_audio.mp3"):
    narration = " ".join(scene["text"] for scene in scenes)
    gTTS(text=narration, lang="en", slow=False).save(out_path)
    return out_path


# ---------------- 3. FAST SLIDE CREATION ----------------
def create_slide_image(scene, width=1280, height=720):
    img = Image.new("RGB", (width, height), (245, 247, 252))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 46)
        body_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()

    # Header
    draw.rectangle((0, 0, width, 100), fill=(45, 96, 232))
    draw.text((40, 30), scene["title"], font=title_font, fill=(255, 255, 255))

    # Body text
    wrapped = textwrap.fill(scene["text"], width=90)
    draw.text((60, 140), wrapped, font=body_font, fill=(30, 30, 30))

    path = f"output/scene_{scene['scene']}.png"
    img.save(path)
    return path


# ---------------- 4. FAST VIDEO BUILD ----------------
def build_video_from_scenes(scenes, out_path="output/final_video.mp4"):
    audio_path = generate_full_audio(scenes)
    audio = AudioFileClip(audio_path)

    scene_duration = audio.duration / len(scenes)

    clips = []
    for scene in scenes:
        img_path = create_slide_image(scene)
        clips.append(ImageClip(img_path).set_duration(scene_duration))

    video = concatenate_videoclips(clips).set_audio(audio)

    video.write_videofile(
        out_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        bitrate="1800k",
        preset="ultrafast",
        verbose=False,
        logger=None
    )

    video.close()
    audio.close()

    return out_path
