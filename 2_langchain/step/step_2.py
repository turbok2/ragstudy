import streamlit as st

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()
st.title("☑️나만의 챗GPT 테스트😂")

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")
# 만약 사용자 입력이 들어오면
if user_input:
    # 사용자 입력
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)
