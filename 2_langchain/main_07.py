import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
# API KEY 정보로드```
load_dotenv()

# 언어 설정
langs = ["Korean", "English", "Japanese", "Chinese"]
lang_codes = {"Korean": "ko", "English": "en", "Japanese": "ja", "Chinese": "zh"}

# Streamlit 앱 구성
st.set_page_config(page_title="번역기")
st.title("🎇번역기♻️")

# Streamlit Session State 초기화 (입력 필드 관리)
if "original_text" not in st.session_state:
    st.session_state["original_text"] = ""
    
with st.sidebar:
    # 번역할 언어 선택 (라디오 버튼)
    target_lang = st.radio("번역할 언어 선택", langs)

    # 초기화 버튼 생성
    clear_btn = st.button("입력 초기화")
    if clear_btn:
        st.session_state["original_text"] = ""
        st.rerun()  # 페이지를 다시 로드하여 입력창을 비웁니다.

# LangChain과 OpenAI 설정
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.3)

# 프롬프트 템플릿 정의
# prompt_template = """
# Translate this text to {target_lang}:
# {original_text}
# """
prompt_template = """
As a professional translator, please provide an accurate and contextually appropriate translation of the following text into {target_lang}. Ensure that the nuances and technical details are preserved:
{original_text}
"""
output_parser = StrOutputParser()

# 번역 함수
def translate_text(original_text, target_lang):
    # 프롬프트 템플릿 정의
    prompt = PromptTemplate.from_template(prompt_template)
    # 새로운 방식의 RunnableSequence 사용
    chain = prompt | llm | output_parser
    # 번역 결과 생성
    translation = chain.invoke(
        {"target_lang": target_lang, "original_text": original_text}
    )
    return translation

# 원본 텍스트 입력
st.session_state["original_text"] = st.text_area(
    "번역할 텍스트를 입력하세요:", value=st.session_state["original_text"], 
    height=150)

# 번역 버튼
if st.button("번역"):
    if st.session_state["original_text"]:
        # 번역 실행
        translated_text = translate_text(st.session_state["original_text"], target_lang)
        st.info(f"번역 결과:\n{translated_text}")
    else:
        st.warning("번역할 텍스트를 입력하세요.")