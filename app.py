import streamlit as st
import requests
import mimetypes
import pathlib

# n8n webhook URL
WEBHOOK_URL = "https://n8n-3-rc8h.onrender.com/webhook-test/2f581f98-d5f0-435d-bb4b-2bc01913e240"

st.title("📤 Upload or Paste File to n8n Webhook")

# File uploader (supports drag and drop)
uploaded_file = st.file_uploader("Drag and drop a file here or click to select", type=["txt", "pdf", "docx", "jpg", "png", "csv", "json", "jpeg"])

# Text area for pasting raw text content
text_content = st.text_area("Or paste your text content here (it will be sent as a file)", height=200)

if uploaded_file is not None:
    # File upload logic
    file_name = uploaded_file.name
    file_bytes = uploaded_file.getvalue()

    # Guess MIME type
    guessed_mime, _ = mimetypes.guess_type(file_name)
    if not guessed_mime:
        ext = pathlib.Path(file_name).suffix.lower()
        fallback_mime = {
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".csv": "text/csv",
            ".json": "application/json",
        }
        mime_type = fallback_mime.get(ext, "application/unknown")
    else:
        mime_type = guessed_mime

    # Display file details
    st.write(f"**File Name:** {file_name}")
    st.write(f"**MIME Type:** {mime_type}")
    st.write(f"**Size:** {len(file_bytes) / 1024:.2f} KB")

    # Send button for file upload
    if st.button("Send File to n8n"):
        files = {
            "file": (file_name, file_bytes, mime_type),
        }
        try:
            response = requests.post(WEBHOOK_URL, files=files)
            if response.status_code == 200:
                st.success("✅ File successfully sent to n8n!")
            else:
                st.error(f"❌ Error: Status {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"Request failed: {e}")

elif text_content:
    # If text is provided, send it as a file
    if st.button("Send Text to n8n"):
        file_name = "pasted_text.txt"
        file_bytes = text_content.encode("utf-8")
        mime_type = "text/plain"

        files = {
            "file": (file_name, file_bytes, mime_type),
        }

        try:
            response = requests.post(WEBHOOK_URL, files=files)
            if response.status_code == 200:
                st.success("✅ Text successfully sent to n8n!")
            else:
                st.error(f"❌ Error: Status {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"Request failed: {e}")
