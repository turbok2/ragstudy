import streamlit as st


st.title("Streamlit 사용해보기")

if st.button("버튼"):
    st.write("눌림")
else:
    st.write("아직 안 눌림")

st.divider()

check = st.checkbox("Check or Not")

if check:
    st.write("Check!!!")
else:
    st.write("Not!!!")

st.divider()

animal = st.radio("좋아하는 동물을 선택해주세요.", ("고양이", "강아지", "토끼"))

if animal == "고양이":
    st.write("야옹야옹")
elif animal == "강아지":
    st.write("멍멍")
else:
    st.write("깡총~~")

animal = st.selectbox("좋아하는 동물을 선택해주세요.", ("고양이", "강아지", "토끼"))

st.write("당신이 좋아하는 동물은 :", animal)

animals = st.multiselect("좋아하는 동물을 선택해주세요.", ("고양이", "강아지", "토끼"))

st.write("당신이 좋아하는 동물은 :", animals)

from datetime import datetime
from datetime import time


## 정수
age = st.slider("몇살인가요?", 0, 130, 25)
st.write(age, "살 입니다.")


## 실수
values = st.slider("값을 선택해주세요.", 0.0, 100.0, (25.0, 75.0))
st.write("값 : ", values)


## 시간
appointment = st.slider("몇시에 일어났나요?", value=(time(9, 30), time(12, 45)))
st.write("일어난 시간 :", appointment)


## 날짜
start_time = st.slider(
    "기분이 좋았던 날은 언제인가요?",
    value=datetime(2023, 6, 16, 9, 30),
    format="MM/DD/YY - hh:mm",
)
st.write("날짜 :", start_time)

## 특정 컬러 선택
color = st.select_slider(
    "컬러를 선택해주세요.",
    options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
)
st.write("선택한 컬러 : ", color)


## 범위 선택
start_color, end_color = st.select_slider(
    "컬러를 선택해주세요.",
    options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
    value=("red", "blue"),
)
st.write("선택한 색상 범위 : ", start_color, ",", end_color)


name = st.text_input("이름을 입력해주세요.", "ex) ComgongNuNa")
st.write("내 이름은 바로 ", name)

number = st.number_input("숫자를 입력하세요.", step=2)
st.write("현재 숫자 : ", number)

txt = st.text_area(
    "긴 텍스트를 입력하는 창입니다.",
    """
    안녕하세요. 
    streamlit을 테스트하고 있습니다.
    
    """,
)
st.write("입력된 문장 :", txt)

import datetime

d = st.date_input("당신의 생일은?", datetime.date(2023, 6, 16))
st.write("나의 생일 :", d)


t = st.time_input(
    "알람을 설정해주세요.", datetime.time(8, 30), step=datetime.timedelta(minutes=30)
)
st.write("당신의 알람 시간 : ", t)

import pandas as pd

uploaded_file = st.file_uploader("파일을 선택해주세요.")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file, encoding="cp949")
    st.write(dataframe)

color = st.color_picker("색깔을 골라주세요.", "#00f900")
st.write("현재 색깔 : ", color)
