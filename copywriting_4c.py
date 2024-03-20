import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
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

def sidebar():
    st.sidebar.title("Clear-Concise-Credible-Compelling")
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")


def title_and_description():
    st.title("✍️ Alwrity - AI Generator for CopyWriting 4C's Formula")
    with st.expander("What is **Copywriting 4C's formula** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's 4C's copywriting Formula, How to use this AI generator 🗣️
            ---
            #### 4C's Copywriting Formula

            4C's stands for Clear, Concise, Credible, and Compelling. It's a copywriting formula that emphasizes:

            1. **Clear**: Presenting information in a straightforward and understandable manner.
            2. **Concise**: Communicating the message succinctly without unnecessary details.
            3. **Credible**: Providing trustworthy and reliable information supported by evidence.
            4. **Compelling**: Creating content that captivates and persuades the audience to take action.

            The 4C's formula ensures that copy is effective, engaging, and impactful.

            #### 4C's Copywriting Formula: Simple Example

            - **Clear**: Our product is designed to simplify your daily tasks.
            - **Concise**: Save time and effort with our user-friendly solution.
            - **Credible**: Backed by years of research and customer testimonials.
            - **Compelling**: Transform your productivity and streamline your workflow today!

            ---
        ''')

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

    page_bottom()


def generate_four_cs_copy(brand_name, description, ad_details):
    prompt = f"""As an expert copywriter, I need your help in creating a marketing campaign for {brand_name},
        which is a {description}. Your task is to use the 4C's (Clear, Concise, Credible, and Compelling) formula to craft compelling copy. The details of the ad campaign are {ad_details}. 
        Make sure your message is easy to understand.
        Keep your message short and to the point.
        Back up your claims with evidence or testimonials.
        Make your content interesting and persuasive.
    """
    return openai_chatgpt(prompt)


def page_bottom():
    """ """
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using 4C's formula - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Problem:
    Are you struggling to create compelling marketing campaigns that grab your audience's attention and drive them to take action?

    ### Agitate:
    Imagine spending hours crafting a message, only to find it doesn't resonate with your audience or compel them to engage with your brand. Your campaigns may lack the attention-grabbing headlines, compelling details, and persuasive calls-to-action needed to stand out in today's crowded digital landscape.

    ### Conviction:
    Introducing Alwrity - Your AI Generator for Copywriting 4C's Formula.
    """)



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=1):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()

