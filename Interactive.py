import streamlit as st
from app.handlers.gpt_handler import analyze_error
from app.handlers.ocr_handler import extract_text
## Page Config:
st.set_page_config(layout="wide",initial_sidebar_state="collapsed",page_title="Bugnix Error Assistant"
    )
image = "app/assets/LogoTitle.png"

errorText = st.session_state.get("error_message")

#UI:

col0, col1, col2 = st.columns([5,5,5])
logo = col1.image(image, use_container_width=True)
st.markdown("####")

col3, col4 = st.columns([5,1])
errorTitle = col3.markdown("### ⚙  Your Error:")
errorText = col3.code("YOUR ERROR TEXT WILL APPEAR HERE", height=100)

col5, ratio = st.columns([7,1])
explainTitle = col5.markdown("### ✅ Error Explaination: ")
textCont = col5.container(height=500, border=True)


contain = st.container(border=False)
with contain:
    col6, col7, col8 = st.columns([5,2,2])
    errorInput = col6.text_area(" ", height= 78, placeholder="Enter or paste your error code here")
    ssButton = col7.file_uploader(" ",accept_multiple_files=False)
    col8.write("")
    col8.write("")
    col8.write("")
    analyseBtn = col8.button("ANALYSE ERROR >", type="primary" )
    if ssButton is not None:
        bin_error = ssButton.getvalue()
        extracted_error = extract_text(bin_error)
    if analyseBtn:
        error_image = extracted_error
        error_text = errorInput
        if error_image is None:
            if error_text is not None:
                errorText.code(errorText)
                textCont.write_stream(analyze_error(error_text))
                
        else:
            if error_text is not None:
               errorText.code(error_image)
               textCont.write_stream(analyze_error(error_image)) #prefers image input over text input
               
            elif error_text is None:
               errorText.code(error_image)
               textCont.write_stream(analyze_error(error_image))
