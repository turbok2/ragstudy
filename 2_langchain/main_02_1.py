import streamlit as st
from langchain_core.messages.chat import ChatMessage

# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory


st.title("❤️챗GPT 테스트(ft.기억력)❤️")

# 세션 ID
session_id = "user-session-001"

# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대회기록을 저장하기 위한 용도로 생성한다.
    st.session_state["messages"] = []

# 사이드 바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")
    if clear_btn:
        # st.write("버튼이 눌렸습니다.")
        st.session_state["messages"] = []
        if "session_histories" in st.session_state:
            st.session_state["session_histories"].pop(session_id, None)
            
# 세션별 히스토리 저장소
if "session_histories" not in st.session_state:
    st.session_state["session_histories"] = {}

# 히스토리 반환 함수
def get_session_history(session_id):
    if session_id not in st.session_state["session_histories"]:
        st.session_state["session_histories"][session_id] = ChatMessageHistory()
    return st.session_state["session_histories"][session_id]

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 세로운 메시지를 추가
def add_messages(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))
    history = get_session_history(session_id)
    if role == "user":
        history.add_user_message(message)
    elif role == "assistant":
        history.add_ai_message(message)


# 체인 생성
def create_chain():
    # prompt | llm | output+parser
    # 프롬프트
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "당신은 친절한 AI 어시스턴트입니다"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "#Question:\n{question}"),
        ]
    )
    # 모델
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    # 출력파서
    output_parser = StrOutputParser()

    # Runnable 체인 구성
    chain = prompt | llm | output_parser
    
    # 히스토리 기반 체인 생성
    chat_chain = RunnableWithMessageHistory(
        chain,
        get_session_history=get_session_history,
        input_messages_key="question",        # 사용자 메시지 키
        history_messages_key="chat_history",  # 프롬프트에서 사용하는 히스토리 키
    )    
    return chat_chain


print_messages()
# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")
# 만약 사용자 입력이 들어오면
if user_input:
    # 사용자 입력
    st.chat_message("user").write(user_input)
    # AI의 답변
    chain = create_chain()
    response = chain.stream({"question": user_input}, config={"configurable": {"session_id": session_id}})
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # st.chat_message("assistant").write(ai_answer)
    # 대화기록을 저장한다.
    add_messages("user", user_input)
    add_messages("assistant", ai_answer)
