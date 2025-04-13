import gradio as gr
from app.handlers.gpt_handler import analyze_error
from app.handlers.ocr_handler import extract_text
from app.handlers.web_search import fetch_web_sol

custom_css = """
#markdown_box {
  height: 400px;
  max-height: 600px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 6px;
}
"""

def showtime(image = None, error_text = ""):
    extracted_error = ""

    if image is not None:
        extracted_error = extract_text(image)
    elif image is None:
        extracted_error = error_text

    final_error = extracted_error or extract_text #use ocr first if possible

    if not final_error:
        return "Please upload a screenshot of your error or enter the error message"

    llm_result = analyze_error(final_error)
    web_result = fetch_web_sol(final_error)
    return f"LLM Response: {llm_result} \n\n Web Response: {web_result}"

with gr.Blocks(title="Bugnix Code Assistant", css=custom_css) as demo:
    gr.Markdown('Welcome to Bugnix!\n Upload a screenshot of your error or paste your complicated chunk of errors here- and watch Bugfix make it easier for you')

    with gr.Row():
        image_input = gr.Image(label="Upload Screenshot", type="filepath")
        text_input = gr.Textbox(label="Paste Error Message")
    
    analyse_btn = gr.Button("Analyse Error!")
    output = gr.Markdown(elem_id="markdown_box")
    #gr.Textbox(label="Response", lines=10, max_lines=20, interactive=False)

    analyse_btn.click(
        fn=showtime,
        inputs=[image_input, text_input],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(share = True)
       
        