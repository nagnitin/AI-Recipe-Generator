import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import base64
from datetime import datetime
import io

# Configure Gemini API key (no fallback public key)
api_key = os.getenv("AIzaSyCPWOOzVt8mvjqxNH1ym2gDloVzELtVWDE")
if not api_key:
    st.error("No Google API key found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()
else:
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")
        st.stop()

# Initialize Gemini model with error handling
try:
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    chat_model = genai.GenerativeModel("models/gemini-1.5-flash")
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {e}")
    st.stop()

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_image" not in st.session_state:
        st.session_state.current_image = None

def extract_ingredients_and_recipes(image):
    """Extract ingredients and generate recipes from image"""
    prompt = """
You are a smart kitchen assistant.

1. First, list all identifiable ingredients from this image.
2. Then, suggest 2–3 easy recipes using those ingredients.
Each recipe should have:
- Title
- Ingredient list
- Steps (in bullet points)
"""
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return "Sorry, I couldn't process the image. Please try again later."

def chat_with_ai(message, image=None):
    """Chat with AI about recipes and cooking"""
    try:
        if image:
            prompt = f"""
You are a helpful cooking assistant. The user said: "{message}"

Please analyze this image and respond to their question. If they're asking about ingredients or recipes, 
provide helpful cooking advice, recipe suggestions, or ingredient information based on what you see in the image.
"""
            response = chat_model.generate_content([prompt, image])
        else:
            prompt = f"""
You are a helpful cooking assistant. The user said: "{message}"

Please provide helpful cooking advice, recipe suggestions, cooking tips, or answer any culinary questions they might have.
Be friendly and informative in your response.
"""
            response = chat_model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return "Sorry, I couldn't process your request. Please try again later."

def display_chat_message(role, content, image=None):
    """Display a chat message with optional image"""
    with st.chat_message(role):
        if image:
            # Responsive image display
            st.image(image, caption="Uploaded Image", width=min(300, st.get_option("server.maxUploadSize") or 200))
        st.write(content)

def main():
    # Responsive page configuration
    st.set_page_config(
        page_title="AI Recipe Assistant", 
        page_icon="🥗",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for responsive design
    st.markdown("""
    <style>
    /* Responsive design improvements */
    .main > div {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Mobile-friendly sidebar */
    @media (max-width: 768px) {
        .css-1d391kg {
            padding: 1rem 0.5rem;
        }
        .stButton > button {
            width: 100%;
            margin: 0.25rem 0;
        }
        .stRadio > div {
            flex-direction: column;
        }
        .stRadio > div > label {
            margin: 0.25rem 0;
        }
    }
    
    /* Tablet and desktop improvements */
    @media (min-width: 769px) {
        .main > div {
            max-width: 1200px;
            margin: 0 auto;
        }
    }
    
    /* Better spacing for all devices */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: #f0f2f6 !important;
        border-radius: 0.5rem 0.5rem 0 0;
        gap: 1rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        color: #222 !important;
        font-weight: 600;
        opacity: 1 !important;
        border: 2px solid #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #fff !important;
        color: #111 !important;
        border-bottom: 2px solid #ff4b4b !important;
        opacity: 1 !important;
    }
    
    .stTabs [aria-selected="false"] {
        background: #f0f2f6 !important;
        color: #333 !important;
        opacity: 1 !important;
    }
    
    /* Responsive columns */
    .row-widget.stHorizontal {
        gap: 1rem;
    }
    
    /* Mobile-friendly chat input */
    .stChatInput {
        margin-bottom: 1rem;
    }
    
    /* Better image display */
    .stImage > img {
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Responsive buttons */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 500;
    }
    
    /* Mobile-friendly file uploader */
    .stFileUploader {
        margin: 0.5rem 0;
    }
    
    /* Better spacing for camera inputs */
    .stCameraInput {
        margin: 0.5rem 0;
    }
    
    /* Responsive info boxes */
    .stAlert {
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    /* Mobile-friendly radio buttons */
    .stRadio > div {
        gap: 0.5rem;
    }
    
    /* Better chat message display */
    .stChatMessage {
        margin: 0.5rem 0;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    
    /* Responsive sidebar */
    .css-1d391kg {
        padding: 1rem;
    }
    
    /* Mobile optimization */
    @media (max-width: 480px) {
        .main > div {
            padding: 0.5rem;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.25rem !important;
        }
        h3 {
            font-size: 1.1rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    # Responsive sidebar
    with st.sidebar:
        st.title("🥗 AI Recipe Assistant")
        st.markdown("---")
        
        # Mobile-friendly navigation
        page = st.selectbox(
            "Choose a feature:",
            ["Chat Assistant", "Recipe Generator", "About"],
            help="Select the feature you want to use"
        )
        
        # Device info (for debugging)
        if st.checkbox("Show Device Info", help="Check this to see responsive layout info"):
            st.info(f"Screen width: {st.get_option('server.maxUploadSize') or 'Unknown'}")
    
    # Main content area
    if page == "Chat Assistant":
        chat_page()
    elif page == "Recipe Generator":
        recipe_generator_page()
    else:
        about_page()

def chat_page():
    """Main chat interface with responsive design"""
    st.title("💬 AI Cooking Assistant")
    st.markdown("Chat with your AI cooking assistant! Ask questions, get recipe advice, or upload images for analysis.")
    
    # Responsive info box
    st.info("📱 **Mobile Tip**: Use your browser's camera icon to switch between front and rear cameras.")
    
    # Chat interface with responsive container
    chat_container = st.container()
    
    # Display chat history with responsive design
    with chat_container:
        for message in st.session_state.messages:
            display_chat_message(message["role"], message["content"], message.get("image"))
    
    # Responsive input area
    if st.get_option("server.maxUploadSize") and st.get_option("server.maxUploadSize") < 768:
        # Mobile layout - stacked
        user_input = st.chat_input("Ask me about cooking, recipes, or upload an image...")
        uploaded_image = st.file_uploader(
            "📷 Upload image for chat",
            type=["jpg", "jpeg", "png"],
            key="chat_image_upload",
            help="Upload an image to discuss with AI"
        )
        st.markdown("**📸 Camera Controls**")
        if "chat_camera_on" not in st.session_state:
            st.session_state.chat_camera_on = False
        if not st.session_state.chat_camera_on:
            if st.button("Turn On Camera", key="chat_camera_on_btn", use_container_width=True):
                st.session_state.chat_camera_on = True
                st.rerun()
            return
            camera_image = None
        else:
            camera_image = st.camera_input("📸 Take photo", key="chat_camera_default")
            if st.button("Turn Off Camera", key="chat_camera_off_btn", use_container_width=True):
                st.session_state.chat_camera_on = False
                st.rerun()
            return
    else:
        # Desktop layout - side by side
        col1, col2 = st.columns([3, 1])
        with col1:
            user_input = st.chat_input("Ask me about cooking, recipes, or upload an image...")
        with col2:
            uploaded_image = st.file_uploader(
                "📷 Upload image for chat",
                type=["jpg", "jpeg", "png"],
                key="chat_image_upload",
                help="Upload an image to discuss with AI"
            )
            if "chat_camera_on" not in st.session_state:
                st.session_state.chat_camera_on = False
            if not st.session_state.chat_camera_on:
                if st.button("Turn On Camera", key="chat_camera_on_btn"):
                    st.session_state.chat_camera_on = True
                    st.rerun()
                return
                camera_image = None
            else:
                camera_image = st.camera_input("📸 Take photo", key="chat_camera_default")
                if st.button("Turn Off Camera", key="chat_camera_off_btn"):
                    st.session_state.chat_camera_on = False
                    st.rerun()
                return
    # Handle user input
    if user_input or uploaded_image or ("chat_camera_on" in st.session_state and st.session_state.chat_camera_on and camera_image):
        current_image = None
        if uploaded_image:
            current_image = Image.open(uploaded_image)
            st.session_state.current_image = current_image
        elif ("chat_camera_on" in st.session_state and st.session_state.chat_camera_on and camera_image):
            current_image = Image.open(camera_image)
            st.session_state.current_image = current_image
        elif st.session_state.current_image:
            current_image = st.session_state.current_image
        if user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "image": current_image
            })
            with st.spinner("Thinking..."):
                ai_response = chat_with_ai(user_input, current_image)
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response,
                "image": None
            })
            st.session_state.current_image = None
            st.rerun()
    
    # Responsive quick action buttons
    st.markdown("---")
    st.subheader("Quick Actions")
    
    # Responsive button layout
    if st.get_option("server.maxUploadSize") and st.get_option("server.maxUploadSize") < 768:
        # Mobile - stacked buttons
        if st.button("🍳 Recipe Ideas", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "Give me some quick recipe ideas for dinner",
                "image": None
            })
            with st.spinner("Generating recipe ideas..."):
                response = chat_with_ai("Give me some quick recipe ideas for dinner")
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "image": None
            })
            st.rerun()
        
        if st.button("🥬 Healthy Options", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "What are some healthy meal options?",
                "image": None
            })
            with st.spinner("Finding healthy options..."):
                response = chat_with_ai("What are some healthy meal options?")
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "image": None
            })
            st.rerun()
        
        if st.button("⏰ Quick Meals", use_container_width=True):
            st.session_state.messages.append({
                "role": "user",
                "content": "What are some meals I can make in under 30 minutes?",
                "image": None
            })
            with st.spinner("Finding quick meals..."):
                response = chat_with_ai("What are some meals I can make in under 30 minutes?")
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "image": None
            })
            st.rerun()
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.current_image = None
            st.rerun()
    else:
        # Desktop - side by side buttons
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🍳 Recipe Ideas"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "Give me some quick recipe ideas for dinner",
                    "image": None
                })
                with st.spinner("Generating recipe ideas..."):
                    response = chat_with_ai("Give me some quick recipe ideas for dinner")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "image": None
                })
                st.rerun()
        
        with col2:
            if st.button("🥬 Healthy Options"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What are some healthy meal options?",
                    "image": None
                })
                with st.spinner("Finding healthy options..."):
                    response = chat_with_ai("What are some healthy meal options?")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "image": None
                })
                st.rerun()
        
        with col3:
            if st.button("⏰ Quick Meals"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "What are some meals I can make in under 30 minutes?",
                    "image": None
                })
                with st.spinner("Finding quick meals..."):
                    response = chat_with_ai("What are some meals I can make in under 30 minutes?")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "image": None
                })
                st.rerun()
        
        with col4:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.session_state.current_image = None
                st.rerun()

def recipe_generator_page():
    """Recipe generator with responsive design"""
    st.title("📷 AI Recipe Generator")
    st.markdown("Upload a picture of your fridge or ingredients and get AI-generated recipe ideas!")
    st.info("📱 **Mobile Tip**: Use your browser's camera icon to switch between front and rear cameras.")
    
    # Responsive tabs
    tab1, tab2, tab3 = st.tabs(["📁 Upload Image", "📸 Take Photo", "💬 Chat with Image"])
    
    with tab1:
        uploaded_file = st.file_uploader(
            "Upload an image", 
            type=["jpg", "jpeg", "png"], 
            key="recipe_upload",
            help="Upload an image of your ingredients or fridge"
        )
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            if st.button("Generate Recipes", use_container_width=True):
                with st.spinner("Analyzing image and generating recipes..."):
                    response_text = extract_ingredients_and_recipes(image)
                    st.subheader("🍽️ Recipe Suggestions")
                    st.info(response_text)
    
    with tab2:
        st.markdown("**📸 Camera Capture (Mobile Supported)**")
        if "recipe_camera_on" not in st.session_state:
            st.session_state.recipe_camera_on = False
        if not st.session_state.recipe_camera_on:
            if st.button("Turn On Camera", key="recipe_camera_on_btn", use_container_width=True):
                st.session_state.recipe_camera_on = True
                st.rerun()
            return
            camera_photo = None
        else:
            camera_photo = st.camera_input("📸 Take photo", key="recipe_camera_default")
            if st.button("Turn Off Camera", key="recipe_camera_off_btn", use_container_width=True):
                st.session_state.recipe_camera_on = False
                st.rerun()
            return
        image = None
        if camera_photo is not None:
            image = Image.open(camera_photo)
            st.image(image, caption='Captured Photo', use_column_width=True)
            if st.button("Generate Recipes from Photo", use_container_width=True):
                with st.spinner("Analyzing photo and generating recipes..."):
                    response_text = extract_ingredients_and_recipes(image)
                    st.subheader("🍽️ Recipe Suggestions")
                    st.info(response_text)
    
    with tab3:
        st.markdown("Chat with your ingredients! Upload an image and ask questions about what you can make.")
        chat_image = st.file_uploader(
            "Upload image for chat", 
            type=["jpg", "jpeg", "png"], 
            key="recipe_chat_upload",
            help="Upload an image to ask questions about"
        )
        st.markdown("**📸 Camera Capture (Mobile Supported)**")
        if "recipe_chat_camera_on" not in st.session_state:
            st.session_state.recipe_chat_camera_on = False
        if not st.session_state.recipe_chat_camera_on:
            if st.button("Turn On Camera", key="recipe_chat_camera_on_btn", use_container_width=True):
                st.session_state.recipe_chat_camera_on = True
                st.rerun()
            return
            chat_camera = None
        else:
            chat_camera = st.camera_input("📸 Take photo", key="recipe_chat_camera_default")
            if st.button("Turn Off Camera", key="recipe_chat_camera_off_btn", use_container_width=True):
                st.session_state.recipe_chat_camera_on = False
                st.rerun()
            return
        current_image = None
        if chat_image:
            current_image = Image.open(chat_image)
        elif ("recipe_chat_camera_on" in st.session_state and st.session_state.recipe_chat_camera_on and chat_camera):
            current_image = Image.open(chat_camera)
        if current_image:
            st.image(current_image, caption="Your Ingredients", width=300)
            user_question = st.text_input("Ask about your ingredients (e.g., 'What can I make with these?', 'Are these ingredients fresh?')")
            if user_question and st.button("Ask AI", use_container_width=True):
                with st.spinner("Analyzing your ingredients..."):
                    response = chat_with_ai(user_question, current_image)
                    st.subheader("🤖 AI Response")
                    st.write(response)

def about_page():
    """About page with responsive design"""
    st.title("About AI Recipe Assistant")
    st.markdown("""
    ## 🥗 Your Smart Kitchen Companion
    
    This AI-powered recipe assistant helps you:
    
    - **💬 Chat with AI**: Get cooking advice, recipe suggestions, and culinary tips
    - **📷 Image Analysis**: Upload photos of your ingredients to get personalized recipe ideas
    - **📸 Camera Integration**: Take photos directly in the app for instant analysis
    - **🍽️ Recipe Generation**: Get complete recipes with ingredients and instructions
    
    ### 📱 How to Use:
    
    1. **Chat Assistant**: Have a conversation with your AI cooking assistant
    2. **Recipe Generator**: Upload images of your fridge/ingredients for recipe suggestions
    3. **Camera Features**: Use your device's camera to capture ingredients instantly
    
    ### ✨ Features:
    - Real-time chat with AI cooking assistant
    - Image recognition for ingredient identification
    - Personalized recipe recommendations
    - Quick action buttons for common requests
    - Camera integration for instant photo capture
    - **Responsive design** for all devices (mobile, tablet, laptop, desktop)
    
    ### 🔧 Technical Details:
    - **Framework**: Streamlit
    - **AI Model**: Google Gemini 1.5 Flash
    - **Image Processing**: PIL (Python Imaging Library)
    - **Session Management**: Streamlit session state for chat history
    - **Responsive Design**: Optimized for all screen sizes
    
    ### 📱 Mobile Features:
    - Touch-friendly interface
    - Optimized camera controls
    - Responsive button layouts
    - Mobile-optimized chat interface
    
    Powered by Google Gemini AI 🤖
    """)

if __name__ == "__main__":
    main()
