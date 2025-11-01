import os
import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx

# --- Видео тайрах функц ---
def trim_video(input_path, output_path, start_time, end_time):
    try:
        clip = VideoFileClip(input_path).subclip(start_time, end_time)
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        clip.close()
        print(f"🎬 Video trimmed and saved to: {output_path}")
    except Exception as e:
        print(f"⚠️ Алдаа гарлаа: {e}")

# --- Хоёр видео нэгтгэх функц ---
def merge_videos(video_list, output_path):
    try:
        clips = [VideoFileClip(v) for v in video_list]
        final = concatenate_videoclips(clips)
        final.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print(f"🎞️ Videos merged into: {output_path}")
    except Exception as e:
        print(f"⚠️ Алдаа гарлаа: {e}")

# --- Эффект нэмэх (жишээ: хар цагаан болгож хадгалах) ---
def apply_effects(input_path, output_path):
    try:
        clip = VideoFileClip(input_path).fx(vfx.blackwhite)
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        clip.close()
        print(f"✨ Effect applied and saved to: {output_path}")
    except Exception as e:
        print(f"⚠️ Алдаа гарлаа: {e}")

# --- Streamlit UI хэсэг ---
def media_edit_ui():
    st.title("🎬 Видео / Зураг засварлагч")
    st.write("Доорх хэрэгслүүдийн аль нэгийг сонгоно уу 👇")

    choice = st.radio("Сонгох:", ["✂️ Хасах", "➕ Нэгтгэх", "🎨 Эффект нэмэх"])

    # ✂️ Видео тайрах хэсэг
    if choice == "✂️ Хасах":
        uploaded_file = st.file_uploader("🎞️ Видео оруулна уу", type=["mp4", "mov", "avi"])
        start = st.number_input("Эхлэх секунд:", min_value=0)
        end = st.number_input("Дуусах секунд:", min_value=0)

        if uploaded_file and st.button("✂️ Хасах"):
            os.makedirs("outputs", exist_ok=True)
            output = f"outputs/trimmed_{uploaded_file.name}"

            # Түр хадгалах
            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.read())

            input_path = os.path.abspath(f"temp_{uploaded_file.name}")
            trim_video(input_path, output, start, end)

            st.video(output)
            st.success("🎬 Видео амжилттай тайрагдлаа!")

    # ➕ Видео нэгтгэх хэсэг
    elif choice == "➕ Нэгтгэх":
        st.write("Олон видео файлыг дараалан оруулна уу.")
        uploaded_files = st.file_uploader("Видеонуудыг сонго", accept_multiple_files=True, type=["mp4", "mov"])
        if uploaded_files and st.button("🎞️ Нэгтгэх"):
            os.makedirs("outputs", exist_ok=True)
            video_list = []
            for file in uploaded_files:
                temp_path = f"temp_{file.name}"
                with open(temp_path, "wb") as f:
                    f.write(file.read())
                video_list.append(os.path.abspath(temp_path))
            output = "outputs/merged_output.mp4"
            merge_videos(video_list, output)
            st.video(output)
            st.success("🎞️ Видеонууд амжилттай нэгтгэгдлээ!")

    # 🎨 Эффект нэмэх хэсэг
    elif choice == "🎨 Эффект нэмэх":
        uploaded_file = st.file_uploader("🎞️ Видео оруулна уу", type=["mp4", "mov"])
        if uploaded_file and st.button("✨ Эффект хэрэглэх"):
            os.makedirs("outputs", exist_ok=True)
            output = f"outputs/effect_{uploaded_file.name}"

            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.read())

            input_path = os.path.abspath(f"temp_{uploaded_file.name}")
            apply_effects(input_path, output)

            st.video(output)
            st.success("✨ Эффект амжилттай хэрэглэгдлээ!")

