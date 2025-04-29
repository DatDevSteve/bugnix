import streamlit as st
from app.handlers import ocr_handler
from app.handlers import gpt_handler

#web app config
st.set_page_config(layout="wide",page_title="Bugnix: AI Debugging")
hide_streamlit_style = """
    <style>
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {
        display: none;
    }
    /* Hide sidebar collapse < button */
    [data-testid="collapsedControl"] {
        display: none;
    }
    /* Additional fix: hide the expand/collapse floating button */
    .css-1fttcpj.e1fqkh3o3 {
        visibility : hidden;
    }
    header, footer {
        visibility: hidden ;
    }
    </style>
    """
#st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#hardcode for debugging:
error_sample = """Traceback (most recent call last):
  File "/mnt/.../main.py", line 3, in <module>
    from app.handlers.ocr_handler import extract_text
  File "/mnt/.../ocr_handler.py", line 24
    ^
SyntaxError: expected 'except' or 'finally' block""" 

st.title(":gear: :blue[BUGNIX CODE ASSISTANT]")
empty = st.container(height=50, border=False)
input, output = st.columns(2)

random_error = """**Error:**
```js
Uncaught ReferenceError: x is not defined
    at script.js:3
```"""
with input:
    st.subheader("INSERT A SCREENSHOT:")
    error_image = st.file_uploader(" ")
    if error_image is not None:
        bin_error = error_image.getvalue()
        extracted_error = ocr_handler.extract_text(bin_error)


    st.subheader("ENTER OR PASTE YOUR CODE ERROR:")
    erroVal = ""
    error_text = st.text_area(label=" ",placeholder="Copy & Paste your error here", height=350, value=erroVal, key="user_input") 
    
    analyze_btn = st.button(type="primary",label="Analyze Error", icon="⏩", use_container_width=True )
    random_btn = st.button(type="primary", label="Try a Test Error", icon="❔", use_container_width=True)



with output:
    #empty = st.container(height=40, border=False)
    st.subheader("CODE ERROR ANALYSIS: ")
    container = st.container(border=True, height=610)
    newUI = st.button("Go back to New UI", use_container_width= True)
    st.write("version 1.0 MVP")
    if analyze_btn:
        if error_image is None:
            if error_text is not None:
                container.write_stream(gpt_handler.analyze_error(error_text))
        else:
            if error_text is not None:
               st.write(":red[PROVIDING ANALYSIS FOR CODE SNIPPET IMAGE OVER TEXT SNIPPET]")
               container.write_stream(gpt_handler.analyze_error(extracted_error)) #prefers image input over text input
            elif error_text is None:
                container.write_stream(gpt_handler.analyze_error(extracted_error))
        
    if random_btn:
        container.write_stream(gpt_handler.analyze_error(random_error))
    
    if newUI:
        st.switch_page("pages/Interactive.py")