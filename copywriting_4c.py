import time #Iwish
import os
import json
import requests
import streamlit as st
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity Copywriting",
        layout="wide",
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)


def title_and_description():
    st.title("✍️ Alwrity - AI Generator for CopyWriting 4C's Formula")


def input_section():
    with st.expander("**PRO-TIP** - Campaign's Key features and benefits to build **Interest & Desire**", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            brand_name = st.text_input('**Enter Brand/Company Name**')
        with col2:
            description = st.text_input('**Describe What your company Does ?** (In 2-3 words)')

        ad_details = st.text_input('**Short Description of your Ad campaign ?**(In 3-4 words)', 
                           help="Guide: 'Provide main outcome of your campaign.'",
                           placeholder="Details of Ad campaign..")

        if st.button('**Get 4C\'s Copy**'):
            if ad_details.strip():
                with st.spinner("Generating 4C's Copy..."):
                    four_cs_copy = generate_four_cs_copy(brand_name, description, ad_details)
                    if four_cs_copy:
                        st.subheader('**👩🔬👩🔬 Your 4C Ad campaign copy:**')
                        st.markdown(four_cs_copy)
                    else:
                        st.error("💥 **Failed to generate 4C's copy. Please try again!**")
            else:
                st.error("Clear, Concise, Credible, and Compelling fields are required!")


def generate_four_cs_copy(brand_name, description, ad_details):
    prompt = f"""As an expert copywriter, I need your help in creating a marketing campaign for {brand_name},
        which is a {description}. Your task is to use the 4C's (Clear, Concise, Credible, and Compelling) formula to craft compelling copy. The details of the ad campaign are {ad_details}. 
        Make sure your message is easy to understand.
        Keep your message short and to the point.
        Back up your claims with evidence or testimonials.
        Make your content interesting and persuasive.
    """
    try:
        response = generate_text_with_exception_handling(prompt)
        return response
    except Exception as err:
        st.error(f"Exit: Failed to get response from LLM: {err}")
        exit(1)



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_text_with_exception_handling(prompt):
    """
    Generates text using the Gemini model with exception handling.

    Args:
        api_key (str): Your Google Generative AI API key.
        prompt (str): The prompt for text generation.

    Returns:
        str: The generated text.
    """

    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        return convo.last.text

    except Exception as e:
        st.exception(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    main()

