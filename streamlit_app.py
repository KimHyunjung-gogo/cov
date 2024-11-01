import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import st_folium

st.title("1. 5G Coverage Hole DU List")
st.write(
    "csv파일을 import하여 5g coverage hole값을 map으로 볼수있습니다"
)

# 파일 업로드 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

# 파일이 업로드되었을 때만 아래 코드 실행
if uploaded_file is not None:
    # CSV 파일을 읽어 데이터프레임 생성
    df = pd.read_csv(uploaded_file)
    
    # latitude와 longitude에 NaN 값이 있는 행 제거
    df = df.dropna(subset=['latitude', 'longitude'])

    # 데이터프레임의 첫 10줄을 표시
    st.subheader("업로드된 파일의 첫 10줄")
    st.write(df.head(10))
    
    # 지도의 중심 위치 설정 (데이터프레임의 평균 좌표 값 기준)
    center_latitude = df['latitude'].mean()
    center_longitude = df['longitude'].mean()

    # Folium 지도 생성
    m = folium.Map(location=[center_latitude, center_longitude], zoom_start=11, tiles="cartodb positron")

    # 데이터프레임의 각 행을 순회하며 마커 추가
    for _, row in df.iterrows():
        color = 'red' if row['5g_covhole_july'] >= 0.3 else 'blue'
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=2,  # 가장 작은 점 크기
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=(
                f"Cell_name_pci: {row['cell_name_pci']}<br>"
                f"enb_name: {row['enb_name']}<br>"
                f"5G_CH(%): {row['5g_covhole_july']}"
            ),
        ).add_to(m)
    
    # Streamlit에 Folium 지도 표시
    st.title("2. 5G Coverage Hole DU MAP")
    st.write("5G 커버리지 홀이 0.3 이상일 때 빨간색 마커로 표시됩니다.")
    st_folium(m)

    # 5g_covhole_july 값이 0.3 이상인 행 필터링
    filtered_df = df[df['5g_covhole_july'] >= 0.3]

    # 사용자로부터 몇 개의 데이터를 볼지 입력받기
    num_rows = st.number_input("보고 싶은 데이터 개수를 입력하세요:", min_value=1, max_value=len(filtered_df), value=5, step=1)

    # 입력받은 개수만큼 데이터 출력
    st.write(f"5g_covhole_july 값이 0.3 이상인 데이터 중 상위 {num_rows}개:")
    st.table(filtered_df.head(num_rows))
else:
    st.write("CSV 파일을 업로드하세요.")


################################
import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load OpenAI API Key from .env file
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = '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'
st.title("3.ChatGPT와 대화하기")

# 대화를 저장할 리스트 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력 받기
user_input = st.text_input("질문을 입력하세요:")

# 사용자가 질문을 입력하고 Enter를 눌렀을 때
if user_input:
    # OpenAI API에 질문을 보내고 응답 받기
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150,
        temperature=0.5,
    )
    
    # ChatGPT의 응답
    answer = response.choices[0].message['content'].strip()

    # 대화 저장
    st.session_state.chat_history.append({"user": user_input, "bot": answer})

# 대화 내용 표시
for chat in st.session_state.chat_history:
    st.write(f"**User**: {chat['user']}")
    st.write(f"**ChatGPT**: {chat['bot']}")