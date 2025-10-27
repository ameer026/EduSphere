import streamlit as st

# Page configuration
st.set_page_config(
    page_title="EduSphere",
    page_icon="📂",
    layout="centered"
)

# Sidebar
import os
import streamlit as st
from PIL import UnidentifiedImageError

with st.sidebar:
    img_path = os.path.join("images", "head.jpeg")
    if os.path.exists(img_path):
        try:
            st.image(img_path)
        except UnidentifiedImageError:
            st.warning("Logo file exists but is not a valid image. Replace with a valid JPEG/PNG.")
        except Exception as e:
            st.warning(f"Could not display logo: {e}")
    else:
        st.info("Logo not found. Add `images/head.jpeg` to the repository to show the logo.")
# Custom CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] > .main {
    background-color: #F8F9FA;
    background-size: 180%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
}

[data-testid="stSidebar"] {
    background-color: #E3F2FD;
}

[data-testid="stHeader"] {
    background-color: rgba(0, 131, 184, 0.1);
}

.stButton > button {
    background-color: #0083B8;
    color: white;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #006B99;
    transform: translateY(-2px);
}

.card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    margin: 1rem 0;
    border: 1px solid rgba(0, 131, 184, 0.1);
}

.feature-item {
    padding: 12px 20px;
    margin: 8px 0;
    background: rgba(0, 131, 184, 0.04);
    border-radius: 8px;
    transition: all 0.2s ease;
    border-left: 3px solid #0083B8;
}

.feature-item:hover {
    background: rgba(0, 131, 184, 0.08);
    transform: translateX(5px);
}

h1, h2, h3 {
    color: #0083B8;
}

p {
    color: #2C3E50;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.title("🎓 EduSphere")
st.markdown("### Empowering educators with AI-powered document interaction")

# Main Content
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h3>About EduSphere</h3>
        <p>EduSphere is an innovative AI-powered educational platform designed to assist teaching and learning experience. 
    Built with Streamlit and integrated with Google's Gemini, it is a set of comprehensive tools including document 
    analysis, data visualization, virtual whiteboarding, and YouTube video summarization. The platform helps educators and 
    students interact with educational content more effectively through features like intelligent PDF chat, Excel data analysis, 
    air-drawn explanations, and automated video transcription. Whether you're preparing lessons, analyzing data, or seeking 
    quick comprehension of educational content, EduSphere provides an intuitive and powerful solution.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>How it Works</h3>
        <div class="feature-item">📄 Upload your educational documents</div>
        <div class="feature-item">💬 Ask questions and get instant solution</div>
        <div class="feature-item">🔍 Get AI-powered insights</div>
        <div class="feature-item">📊 Visualize key information</div>
        <div class="feature-item">📈 Get Summarized Content from Video</div>
        <div class="feature-item">🎬 Summarize YouTube videos for quick learning</div>
    </div>
    """, unsafe_allow_html=True)

# Features Section
st.markdown("""
<div class="card">
    <h3>Key Features</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        <div class="feature-item">🤖 Advanced AI Integration</div>
        <div class="feature-item">🌍 Last minute Study Support</div>
        <div class="feature-item">📱 Responsive Design</div>
        <div class="feature-item">🔒 Secure Document Handling</div>
        <div class="feature-item">⚡ Real-time Processing</div>
        <div class="feature-item">📊 Data Visualization</div>
    </div>
</div>

<div style="text-align: center; margin-top: 3rem; padding: 1rem; background: rgba(0, 131, 184, 0.04); border-radius: 8px;">
    <p style="margin: 0;">Made with ❤️ for Educators</p>
</div>
""", unsafe_allow_html=True)
