# 📺 YouTube Video Summarizer

A Streamlit web app that extracts transcripts from YouTube videos and generates AI-powered summaries using Google Gemini. Instantly get structured, scannable summaries of video content in seconds!

---

## 🚀 Features

- 🤖 **AI-Powered Summarization**: Uses Google Gemini to create structured summaries  
- 📝 **Transcript Extraction**: Retrieves video captions using `youtube_transcript_api`  
- 🧠 **Insightful Highlights**: Extracts key points, actions, and notable details  
- 🖼️ **Video Thumbnail Preview**: Displays video thumbnail before summarization  
- ⚠️ **Robust Error Handling**: Covers unavailable videos, disabled captions, and invalid URLs  
- 🔢 **Multi-format URL Support**: Works with both full YouTube links and shortened ones  

---

## 🧠 How It Works

1. Paste a YouTube video link  
2. App fetches transcript using `youtube_transcript_api`  
3. Gemini processes the transcript and returns a concise summary  
4. Summary is displayed in a structured format with emojis for readability  

---

## 🔧 Technologies Used

- Python  
- Streamlit  
- Google Gemini API (`google.generativeai`)  
- youtube-transcript-api  
- dotenv  
- urllib  

---

## 🎥 Screen Recording

- [📺 Screen recording of Source Code](https://youtu.be/kITRzrvzdok)
 
- [📺 Screen recording of Live Demo](https://youtu.be/-dOhBuA8hS8)

---

## 📃 License

This project is open-source and free to use!

---

## 🙌 Acknowledgements

- Powered by [Google Gemini](https://ai.google.dev/)  
- Transcript extraction by [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)  
- Inspired by the need to save time on long-form video content 🎯  
