import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import os

# 1. API 키 설정 (본인의 키를 따옴표 안에 넣으세요)
API_KEY = "AIzaSyAV9mCyS7fJFj4d671o-SEO2ccPAH4JjQc" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 2. 구글 시트 설정 (영태님의 시트 ID 적용 완료)
SHEET_ID = "17DOk-zLFHhlwMgL_wiPYYXS-tLAoSYvZpWoLwcP6Mu8"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("🏯 나고야 취업 성공! AI 모의 면접관")
st.write("20년 경력의 전문성을 일본어로 완벽하게 전달하세요.")

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    return pd.read_csv(url, encoding='utf-8')

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
    st.stop()

# 면접 질문 받기 버튼
if st.button('🎯 새로운 질문 받기'):
    try:
        selected = df.sample(n=1).iloc[0]
        st.session_state.question = selected.iloc[0]
        st.session_state.ideal = selected.iloc[1]
        
        st.subheader("면접관의 질문:")
        st.write(st.session_state.question)
        
        # 음성 파일 생성 및 재생
        tts = gTTS(text=st.session_state.question, lang='ja')
        tts.save("q.mp3")
        st.audio("q.mp3", format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"질문을 뽑는 중 오류 발생: {e}")

# 답변 입력 칸
user_input = st.text_area("일본어로 답변을 입력하세요:", height=150)

# 피드백 버튼
if st.button('🤖 AI 피드백 받기'):
    if user_input and 'question' in st.session_state:
        with st.spinner('분석 중...'):
            prompt = f"""
            질문: {st.session_state.question}
            사용자 답변: {user_input}
            나고야의 보수적인 기업 문화를 고려하여 정중한 일본어 표현과 
            한국 금융권 20년 경력이 잘 드러나도록 한국어로 피드백해 주세요.
            """
            response = model.generate_content(prompt)
            st.success("분석 완료!")
            st.write(response.text)
    else:
        st.warning("먼저 질문을 받고 답변을 적어주세요.")
