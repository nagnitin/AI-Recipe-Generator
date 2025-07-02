# 🥗 AI Recipe Assistant with Chatbot

A comprehensive AI-powered recipe assistant that combines chat functionality, image analysis, and camera integration to help you create delicious meals from your available ingredients.

## ✨ Features

### 💬 Chat Assistant
- **Real-time AI Chat**: Have conversations with your AI cooking assistant
- **Cooking Advice**: Get personalized cooking tips and recipe suggestions
- **Ingredient Questions**: Ask about ingredients, substitutions, and cooking techniques
- **Quick Action Buttons**: Pre-defined buttons for common requests (Recipe Ideas, Healthy Options, Quick Meals)

### 📷 Image Analysis
- **Upload Images**: Upload photos of your fridge or ingredients
- **Camera Capture**: Take photos directly in the app using your device's camera
- **Ingredient Recognition**: AI identifies ingredients in your photos
- **Recipe Generation**: Get personalized recipes based on available ingredients

### 🍽️ Recipe Generator
- **Multiple Input Methods**: Upload images, take photos, or chat with images
- **Complete Recipes**: Get full recipes with ingredients, instructions, and cooking steps
- **Interactive Chat**: Ask specific questions about your ingredients

## 🚀 Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google API key**:
   - Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set it as an environment variable:
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     ```
   - Or the app will use the default key (not recommended for production)

4. **Run the application**:
   ```bash
   streamlit run recipe_from_fridge.py
   ```

## 📱 How to Use

### Chat Assistant
1. Select "Chat Assistant" from the sidebar
2. Type your cooking questions in the chat input
3. Use the image upload or camera buttons to include photos
4. Try the quick action buttons for instant recipe ideas

### Recipe Generator
1. Select "Recipe Generator" from the sidebar
2. Choose from three tabs:
   - **Upload Image**: Upload existing photos
   - **Take Photo**: Use your camera to capture ingredients
   - **Chat with Image**: Upload/take photos and ask specific questions

### Camera Features
- **Chat Camera**: Take photos during conversations
- **Recipe Camera**: Capture ingredients for recipe generation
- **Chat with Image Camera**: Take photos and ask questions about them

## 🎯 Example Use Cases

### Chat Examples:
- "What can I make for dinner tonight?"
- "How do I cook quinoa properly?"
- "What's a good substitute for eggs in baking?"
- "Give me some healthy meal prep ideas"

### Image Analysis Examples:
- Take a photo of your fridge contents
- Upload a picture of vegetables from your garden
- Share a photo of pantry items
- Ask "What can I make with these ingredients?"

## 🔧 Technical Details

- **Framework**: Streamlit
- **AI Model**: Google Gemini 1.5 Flash
- **Image Processing**: PIL (Python Imaging Library)
- **Session Management**: Streamlit session state for chat history

## 📁 File Structure

```
├── recipe_from_fridge.py    # Main application file
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🛠️ Customization

### Adding New Quick Actions
Edit the quick action buttons in the `chat_page()` function:

```python
if st.button("Your New Action"):
    # Add your custom logic here
    pass
```

### Modifying AI Prompts
Update the prompts in the `chat_with_ai()` and `extract_ingredients_and_recipes()` functions to customize AI responses.

### Styling
The app uses Streamlit's built-in styling. You can customize colors and layout by modifying the `st.set_page_config()` call.

## 🔒 Privacy & Security

- Images are processed locally and sent to Google's AI service for analysis
- No images are stored permanently on the server
- Chat history is maintained only during the session
- Consider using environment variables for API keys in production

## 🐛 Troubleshooting

### Common Issues:

1. **API Key Error**: Make sure your Google API key is valid and has access to Gemini models
2. **Camera Not Working**: Ensure your browser has camera permissions
3. **Image Upload Issues**: Check that images are in supported formats (JPG, PNG)
4. **Slow Responses**: Large images may take longer to process

### Performance Tips:
- Compress large images before uploading
- Use the camera feature for better performance
- Clear chat history if the app becomes slow

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application!

## 📄 License

This project is open source and available under the MIT License.

---

**Enjoy cooking with your AI assistant! 🍳✨** 