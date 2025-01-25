import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os
import subprocess
import tempfile

# Page config
st.set_page_config(page_title="Flowchart Generator", page_icon="🔀", layout="wide")

# Load environment variables
load_dotenv()
    
# Configure Google API
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    st.error("GOOGLE_API_KEY is not set")
    st.stop()
    
genai.configure(api_key=google_api_key)

# Prompt template
prompt = ["""Create a simple flowchart using Mermaid.js syntax:
1. Start with 'flowchart TD'
2. Use simple node IDs (A, B, C, etc.)
3. Node format: A[Description]
4. Use --> for connections
5. Keep it simple and clear

Example:
flowchart TD
    A[Start] --> B[Process]
    B --> C[Decision]
    C --> D[End]"""]

def get_gemiml_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([*prompt, question])
        return response.text if response else None
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return None

def remove_triple_backticks(text):
    text = text.replace("```mermaid", "").replace("```", "")
    return text.strip()

def validate_mermaid_code(code):
    if not code.startswith('flowchart TD'):
        return False
    lines = code.split('\n')
    for line in lines[1:]:
        if line.strip() and not ('-->' in line or ']' in line):
            return False
    return True

def generate_image(mermaid_code):
    try:
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        input_file = os.path.join(temp_dir, "flowchart.mmd")
        output_file = os.path.join(temp_dir, "flowchart.png")
        
        # Write Mermaid code
        with open(input_file, "w", encoding='utf-8') as f:
            f.write(mermaid_code)
        
        # Generate image
        mmdc_path = "C:\\Users\\syedt\\AppData\\Roaming\\npm\\mmdc.cmd"
        result = subprocess.run(
            [mmdc_path, "-i", input_file, "-o", output_file],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            st.error(f"Mermaid CLI error: {result.stderr}")
            return None
        
        # Return image if successful
        if os.path.exists(output_file):
            image = Image.open(output_file)
            image_copy = image.copy()
            image.close()
            return image_copy
            
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
    finally:
        try:
            os.remove(input_file)
            os.remove(output_file)
            os.rmdir(temp_dir)
        except:
            pass
    return None

def app():
    st.title("🔀 Flowchart Generator")
    st.markdown("### Transform text descriptions into flowcharts using AI")

    # Templates
    examples = {
        "Login Process": "Create a flowchart for user login process",
        "Data Processing": "Create a flowchart for basic data processing steps",
        "Order System": "Create a flowchart for order processing system"
    }

    selected_template = st.selectbox(
        "Choose a template or create your own:",
        ["Custom"] + list(examples.keys())
    )

    description = st.text_area(
        "Enter your flowchart description:",
        value=examples[selected_template] if selected_template != "Custom" else "",
        height=150
    )

    if st.button("Generate Flowchart"):
        if description:
            with st.spinner("Generating flowchart..."):
                mermaid_code = get_gemiml_response(description, prompt)
                if mermaid_code:
                    mermaid_code = remove_triple_backticks(mermaid_code)
                    if validate_mermaid_code(mermaid_code):
                        with st.expander("View Mermaid Code"):
                            st.code(mermaid_code, language="mermaid")
                        
                        image = generate_image(mermaid_code)
                        if image:
                            st.image(image, caption="Generated Flowchart", use_column_width=True)
                            
                            # Save for download
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                                image.save(tmp_file.name)
                                with open(tmp_file.name, 'rb') as f:
                                    st.download_button(
                                        "Download Flowchart",
                                        f,
                                        file_name="flowchart.png",
                                        mime="image/png"
                                    )
                                os.unlink(tmp_file.name)
                        else:
                            st.error("Failed to generate flowchart image")
                    else:
                        st.error("Invalid Mermaid syntax generated")
                else:
                    st.error("Failed to generate flowchart code")
        else:
            st.warning("Please enter a description")

if __name__ == "__main__":
    app()
