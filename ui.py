
# import streamlit as st
# import os
# from app import generate_scenes, build_video_from_scenes


# def main():
#     st.set_page_config(page_title="AI Lesson Video Generator", layout="wide")
#     st.title("🎥 AI-powered e-Learning Video Generator")

#     st.markdown(
#         "Give me **keywords**, and I’ll generate a full **lesson video** with structured explanation, AI images, and voiceover."
#     )

#     with st.sidebar:
#         st.header("⚙️ Settings")
#         keywords = st.text_area(
#             "Topic Keywords",
#             "CPU, registers, instruction cycle",
#             help="Write 2–5 keywords or a small topic description.",
#         )
#         level = st.selectbox(
#             "Target Level",
#             ["School", "B.Tech 1st year", "B.Tech 2nd year", "Beginner", "Intermediate"],
#             index=1,
#         )
#         language = st.selectbox("Language", ["English"])
#         duration = st.slider("Approx. Duration (minutes)", 1, 10, 3)
#         style = st.selectbox(
#             "Style",
#             ["Whiteboard explainer", "Infographic", "Simple slideshow"],
#             index=1,
#         )

#         bg_music = st.checkbox("Add Background Music (assets/bg_music.mp3)", value=False)

#         generate_btn = st.button("🚀 Generate Video")

#     col1, col2 = st.columns([2, 1])

#     with col1:
#         if generate_btn:
#             if not keywords.strip():
#                 st.error("Please enter some keywords.")
#                 return

#             with st.spinner("✍️ Generating lesson script with AI..."):
#                 try:
#                     scenes = generate_scenes(keywords, level, language, duration, style)
#                 except Exception as e:
#                     st.error(f"Script Error: {e}")
#                     return

#             with st.spinner("🎬 Generating slides, images & video..."):
#                 try:
#                     music_path = "assets/bg_music.mp3" if bg_music else None
#                     video_path = build_video_from_scenes(
#                         scenes,
#                         out_path="output/final_video.mp4",
#                         lang="en",
#                         bg_music_path=music_path,
#                     )
#                 except Exception as e:
#                     st.error(f"Video Error: {e}")
#                     return

#             if video_path and os.path.exists(video_path):
#                 st.success("✅ Video generated successfully!")
#                 st.video(video_path)
#             else:
#                 st.error("Video could not be generated.")
#         else:
#             st.info("Fill in the details in the sidebar and click **Generate Video**.")

#     with col2:
#         st.subheader("ℹ️ What this app does")
#         st.markdown(
#             """
# 1. **Understands your topic** from keywords  
# 2. Breaks it into **4–6 scenes**  
# 3. For each scene, creates:
#    - Title  
#    - Definition  
#    - Explanation  
#    - Example  
#    - Analogy  
#    - Visual hint  
# 4. Generates **AI images** per scene  
# 5. Designs **infographic-style slides**  
# 6. Converts text to **voiceover**  
# 7. Stitches everything into a **single MP4 video**  
# """
#         )
#         video_file = "output/final_video.mp4"
#         if os.path.exists(video_file):
#             with open(video_file, "rb") as f:
#                 st.download_button("⬇ Download Last Video", f, "lesson_video.mp4")


# if __name__ == "__main__":
#     os.makedirs("output", exist_ok=True)
#     main()
import streamlit as st
from app import generate_scenes, build_video_from_scenes

st.set_page_config(page_title="AI eLearning Video Generator", layout="wide")
st.title("🎓 AI e-Learning Video Generator")

keywords = st.text_area(
    "Enter topic keywords",
    "CPU, registers, instruction cycle"
)
level = st.selectbox(
    "Target Level",
    ["School", "B.Tech 1st year", "Beginner"]
)
duration = st.slider("Video Length (minutes)", 3, 6, 4)
style = st.selectbox("Style", ["Infographic", "Whiteboard"])

if st.button("Generate Video"):
    with st.spinner("Generating detailed script..."):
        scenes = generate_scenes(keywords, level, "English", duration, style)

    with st.spinner("Rendering video (this takes ~10 seconds)..."):
        video_path = build_video_from_scenes(scenes)

    st.success("✅ Video generated successfully")
    st.video(video_path)

    with open(video_path, "rb") as f:
        st.download_button("⬇ Download Video", f, "lesson_video.mp4")
