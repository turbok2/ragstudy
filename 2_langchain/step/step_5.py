import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
# API KEY 정보로드
load_dotenv()
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

# 체인 생성
def create_chain():
    # prompt | llm | output+parser
    # 프롬프트
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트입니다"),
            ("user", "#Question:\n{question}"),
        ]
    )
    # 모델
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    # 출력파서
    output_parser = StrOutputParser()
    # 체인생성
    chain = prompt | llm | output_parser
    return chain

#이전 대화를 출력
print_messages()
# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")
# 만약 사용자 입력이 들어오면
if user_input:
    # 사용자 입력
    st.chat_message("user").write(user_input)
    # AI의 답변
    chain = create_chain()
    ai_answer = chain.invoke({"question": user_input})
    st.chat_message("assistant").write(ai_answer)
    # 대화기록을 저장
    add_messages("user", user_input)
    add_messages("assistant", ai_answer)
