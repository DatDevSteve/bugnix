import streamlit as st
from app.handlers import ocr_handler
from app.handlers import gpt_handler

#Set Configuration for the App:
st.set_page_config(
    layout="wide",
    page_title="Bugnix Error Assistant")

col1, col2, col3 = st.columns([3,4,5])
col1.image("app/assets/LogoTitle.png", use_container_width=True)
empty = st.container(height=50, border=False)
input, output = st.columns([2,3])

#Hardcoded error for sample error analysis to test:
random_error = """**Error:**
```js
Uncaught ReferenceError: x is not defined
    at script.js:3
```"""

#Column with input for Error Screenshot or Pasted Code
with input:
    #Error Screenshot Analysis" 
    st.subheader("INSERT A SCREENSHOT:")
    error_image = st.file_uploader(" ")
    if error_image is not None:
        bin_error = error_image.getvalue()
        extracted_error = ocr_handler.extract_text(bin_error) #Use Azure Computer Vision to extract text from screenshot
    
    #Error Pasting Textbox:
    st.subheader("ENTER OR PASTE YOUR CODE ERROR:")
    erroVal = ""
    error_text = st.text_area(label=" ",placeholder="Copy & Paste your error here", height=350, value=erroVal, key="user_input") 
    
    #Buttons:
    analyze_btn = st.button(type="primary",label="Analyze Error", icon="⏩", use_container_width=True )
    random_btn = st.button(type="secondary", label="Try a Sample Error", icon="❔", use_container_width=True)

#Column with Code Interpretation Output
with output:
    st.subheader("CODE ERROR ANALYSIS: ")
    container = st.container(border=True, height=610)
    st.write("version 1.0 for Microsoft AI Agents Hackathon 2025")
    if analyze_btn:
        if error_image is None:
            if error_text is not None:
                container.write_stream(gpt_handler.analyze_error(error_text))
        else:
            if error_text is not None:
               st.write(":red[PROVIDING ANALYSIS FOR CODE SNIPPET IMAGE OVER TEXT SNIPPET]")
               container.write_stream(gpt_handler.analyze_error(extracted_error)) #PREFERENCE OF IMAGE SNIP OF CODE RATHER THAN TEXT
            elif error_text is None:
                container.write_stream(gpt_handler.analyze_error(extracted_error))
        
    if random_btn:
        container.write_stream(gpt_handler.analyze_error(random_error))