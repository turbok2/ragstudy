# pdf를 한번 읽어서 임베딩했으면, 
# 다시 동일한 파일이 선택되면 임베딩 안하고 기존의 것을 사용하게 수정
# FAISS 파일에 저장 : 재실행해도 남아있음.(개인용으로 적합)
import streamlit as st
import os
import pdfplumber
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
import hashlib
import pickle
# API KEY를 환경변수로 관리하기 위한 설정 파일
from dotenv import load_dotenv
# API KEY 정보로드
load_dotenv()
# 웹페이지 탭 꾸미기
st.set_page_config(
    page_title="질의응답챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("❤️PDF 읽고 질문하기_V3❤️")
# 파일 해시를 생성하는 함수
def get_file_hash(uploaded_file):
    file_contents = uploaded_file.read()
    file_hash = hashlib.md5(file_contents).hexdigest()
    uploaded_file.seek(0)  # 파일 포인터를 처음으로 돌려서 이후 사용 가능하게 함
    return file_hash

def load_data(uploaded_file):
    # 파일이 업로드되었을 때만 처리
    documents = []
    if uploaded_file is not None:
        # 메모리 내 PDF 파일 읽기
        with pdfplumber.open(uploaded_file) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:  # 페이지에 텍스트가 있을 경우에만 처리
                    # 각 페이지의 텍스트와 해당 페이지 번호를 Document로 저장
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": uploaded_file.name,
                                "page": page_number  # 페이지 번호를 메타데이터에 추가
                            }
                        )
                    )
    return documents
# FAISS 인덱스를 로드하거나 저장하는 함수
def load_or_create_faiss_index(file_hash, documents, embeddings, embeddings_dir="embeddings"):
    faiss_file = os.path.join(embeddings_dir, f"{file_hash}.faiss")
    meta_file = os.path.join(embeddings_dir, f"{file_hash}_meta.pkl")

    if not os.path.exists(embeddings_dir):
        os.makedirs(embeddings_dir)

    if os.path.exists(faiss_file) and os.path.exists(meta_file):
        vectorstore = FAISS.load_local(faiss_file, embeddings, allow_dangerous_deserialization=True)
        with open(meta_file, "rb") as f:
            vectorstore.docstore._dict = pickle.load(f)
        st.success("기존 임베딩을 불러왔습니다.")
    else:
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_documents = text_splitter.split_documents(documents)
        vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
        vectorstore.save_local(faiss_file)
        with open(meta_file, "wb") as f:
            pickle.dump(vectorstore.docstore._dict, f)
        st.success("새로운 임베딩을 생성하고 저장했습니다.")
    
    return vectorstore
# 사이드 바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")
    if clear_btn:
        # st.write("버튼이 눌렸습니다.")
        st.session_state["messages"] = []
    reset_btn = st.button("임베딩 초기화")
    if reset_btn:
        st.session_state["file_hash"] = None  # 초기화 시 파일 해시도 초기화
    # CSV 파일 업로드
    uploaded_file = st.file_uploader("PDF 파일을 선택하세요", type=["pdf"])

# 임베딩이 이미 생성된 경우 이를 활용하도록 수정
if uploaded_file is not None:
    file_hash = get_file_hash(uploaded_file)
    
    if "file_hash" not in st.session_state or st.session_state["file_hash"] != file_hash:
        st.session_state["file_hash"] = file_hash
        documents = load_data(uploaded_file)
        embeddings = OpenAIEmbeddings()
        vectorstore = load_or_create_faiss_index(file_hash, documents, embeddings)
        st.session_state["retriever"] = vectorstore.as_retriever(search_kwargs={"k": 2})
else:
    st.session_state["file_hash"] = None
    st.session_state["retriever"] = None
        
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

# 세로운 메시지를 추가
def add_messages(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

def create_chain():
    system_template = """Use the following pieces of context to answer the users question shortly.
    Given the following summaries of a long document and a question, create a final answer with references ("SOURCES"), use "SOURCES" in capital letters regardless of the number of sources.
    If you don't know the answer, just say that "I don't know", don't try to make up an answer.
    ----------------
    {summaries}
    If you don't know the answer, just say that you don't know. 
    You MUST answer in Korean and in Markdown format:"""

    messages = [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{question}"),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chain_type_kwargs = {"prompt": prompt}

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, max_tokens=2000)

    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=st.session_state["retriever"],
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs,
    )
    return chain

print_messages()
# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")
# 만약 사용자 입력이 들어오면
if user_input:
    # 사용자 입력
    st.chat_message("user").write(user_input)
    if uploaded_file:
        # AI의 답변
        chain = create_chain()
        response = chain.invoke({"question": user_input})
        # 답변 추출
        ai_answer = response.get("answer", "")
        
        # 출처 문서 추출 (출처 정보에 페이지 정보가 포함됨)
        source_documents = response.get("source_documents", [])
        sources_info = ""
        
        for doc in source_documents:
            page_number = doc.metadata.get("page", "N/A")  # 페이지 정보를 추출
            sources_info += f"(출처: {doc.metadata.get('source')} - {page_number} 페이지)\n"
        
        # 답변과 출처 정보를 함께 표시
        with st.chat_message("assistant"):
            container = st.empty()
            if ai_answer=="I don't know.":
                container.markdown(f"{ai_answer}")  # 답변 출력
            else:
                container.markdown(f"{ai_answer}\n\n{sources_info}")  # 답변과 출처 출력
        # 대화기록을 저장한다.
        add_messages("user", user_input)
        add_messages("assistant", f"{ai_answer}\n\n{sources_info}")    
            
    else:
        msg = 'PDF파일을 먼저 선택해주세요.'
        st.chat_message("assistant") .write(msg)   
        # 대화기록을 저장한다.
        add_messages("user", user_input)
        add_messages("assistant", msg)    
    
# 질문
# 신경망처리 기반 인공지능 전용칩에 대해 설명해주세요.    (20페이지)
# 지능형 개인 맞춤 서비스 인공지능 기술의 요소기술은?     (22페이지)

# 소년이 소녀를 만난 곳은?
