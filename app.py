import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi, VideoUnavailable, TranscriptsDisabled
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for Gemini
prompt = """Analyze the provided YouTube transcript and extract the most valuable information into a structured, scannable summary under 250 words.

Required Output Structure:
**MAIN TOPIC:** [Single sentence capturing video's core purpose]

**KEY POINTS:**
• [Most important insight/takeaway]
• [Second most important point]
• [Third key point]
• [Additional points as needed, max 5 total]

**ACTIONABLE ITEMS:** [If any - steps, recommendations, or calls-to-action]

**NOTABLE DETAILS:** [Statistics, examples, or supporting facts worth remembering]

Processing Instructions:
1. Identify the video's primary objective and target audience
2. Extract information in order of importance/impact
3. Prioritize actionable content over theoretical discussion
4. Preserve specific data points (numbers, percentages, dates)
5. Eliminate transcript artifacts (filler words, repetitions, "um," "uh")
6. Focus on "what the viewer should know/do after watching"

Transcript to summarize: """

# extract video ID form url
def extract_video_id(yt_url):
    parsed_url = urlparse(yt_url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    return None

# transcript from YouTube
def transcriber(yt_url):
    video_id = extract_video_id(yt_url)
    if not video_id:
        return None, "❌Invalid YouTube URL."

    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Converting the List into str
        transcript_text = " ".join([i["text"] for i in transcript_list])
        return transcript_text, None
    except VideoUnavailable:
        return None, "❌ Video is unavailable or private."
    except TranscriptsDisabled:
        return None, "❌ Transcripts are disabled for this video."
    except Exception as e:
        return None, f"⚠️ Unexpected error: {e}"

# Generate summary using Gemini
def geminiContentGenerator(transcript_text, prompt):
    model = genai.GenerativeModel("models/gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit
st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="📺",
    layout="wide"
)

st.title("📺 YouTube Video Summarizer")
st.markdown("Get AI-powered summaries of YouTube videos instantly!")

yt_link = st.text_input("Enter YouTube Video Link Here:")

if yt_link:
    video_id = extract_video_id(yt_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    else:
        st.warning("⚠️ Please enter a valid YouTube link.")

# Generate summary
if st.button("🚀 Generate Summary", type="primary"):
    if not yt_link:
        st.error("Please enter a YouTube URL first!")
    else:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: Extract transcript
        status_text.text("📝 Extracting transcript...")
        progress_bar.progress(33)

        transcriptText, error = transcriber(yt_link)

        if error:
            st.error(error)
        elif transcriptText:
            # Step 2: Generate summary
            status_text.text("🤖 Generating AI summary...")
            progress_bar.progress(66)

            summary = geminiContentGenerator(transcriptText, prompt)

            # Step 3: Display results
            status_text.text("✅ Complete!")
            progress_bar.progress(100)

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Display summary
            st.markdown("## 📋 Summary")
            st.markdown(summary)
