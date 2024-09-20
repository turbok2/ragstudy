import streamlit as st
from langchain_core.messages.chat import ChatMessage
st.title("☑️나만의 챗GPT 테스트😂")

# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대회기록을 저장하기 위한 용도로 생성한다.
    st.session_state["messages"] = []
# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)
# 세로운 메시지를 추가
def add_messages(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

#이전 대화를 출력
print_messages()
# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")
# 만약 사용자 입력이 들어오면
if user_input:
    # 웹에 대화를 출력
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)
    # 대화기록을 저장
    add_messages("user", user_input)
    add_messages("assistant", user_input)
