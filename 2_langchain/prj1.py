import streamlit as st

st.title("☑️나만의 챗GPT 테스트😂")

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")
# 만약 사용자 입력이 들어오면
if user_input:
    # 사용자 입력
    st.write(f"사용자 입력: {user_input}")
