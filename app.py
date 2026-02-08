import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import os

# 1. API 키 설정 (Secrets 사용 권장)
API_KEY = st.secrets.get("GEMINI_API_KEY", "여기에_키를_직접_넣어도_됩니다")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 2. 구글 시트 ID (영태님의 시트 ID로 꼭 확인하세요)
# 주소창에서 /d/ 와 /edit 사이에 있는 긴 문자열입니다.
SHEET_ID = "17DOk-zLFHhlwMgL_wiPYYXS-tLAoSYvZpWoLwcP6Mu8 "
# URL을 더 안정적인 export 방식으로 변경했습니다.
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("🏯 나고야 취업 성공! AI 모의 면접관")

@st.cache_data
def load_data():
    # encoding='utf-8'을 명시하여 한글/일본어 깨짐을 방지합니다.
    return pd.read_csv(url, encoding='utf-8')

try:
    df = load_data()
except Exception as e:
    st.error(f"시트 데이터를 불러오지 못했습니다. 시트가 '링크가 있는 모든 사용자에게 공개' 상태인지 확인해 주세요. 에러 내용: {e}")
    st.stop()

# (이후 질문 받기 및 피드백 버튼 코드는 동일하게 유지)
