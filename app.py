import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import os

# --- 1. 보안 및 API 설정 ---
# Streamlit Secrets에서 키를 가져오거나, 없으면 에러 메시지를 띄웁니다.
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["AIzaSyAV9mCyS7fJFj4d671o-SEO2ccPAH4JjQc"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ API 키가 설정되지 않았습니다. Streamlit 'Settings > Secrets'에 GEMINI_API_KEY를 입력해 주세요.")
    st.stop()

# --- 2. 구글 시트 연결 ---
# 영태님의 시트 ID와 URL 설정
SHEET_ID = "17DOk-zLFHhlwMgL_wiPYYXS-tLAoSYvZpWoLwcP6Mu8"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="나고야 AI 면접관", page_icon="🏯")
st.title("🏯 나고야 취업 성공! AI 모의 면접관")
st.info("20년 경력의 전문성을 신뢰감 있는 일본어로 전달하는 연습을 시작하세요.")

@st.cache_data
def load_data():
    # encoding='utf-8'로 한글/일본어 깨짐 방지
    return pd.read_csv(url, encoding='utf-8')

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ 데이터를 불러오지 못했습니다. 시트 공유 설정을 확인하세요: {e}")
    st.stop()

# --- 3. 면접 기능 구현 ---
if st.button('🎯 새로운 질문 받기'):
    try:
        # 컬럼 이름과 상관없이 첫 번째, 두 번째 칸의 데이터를 가져옴
        selected = df.sample(n=1).iloc[0]
        st.session_state.question = selected.iloc[0] # 첫 번째 열: 질문
        st.session_state.ideal = selected.iloc[1]    # 두 번째 열: 답변 예시
        
        st.subheader("📢 면접관의 질문:")
        st.success(st.session_state.question)
        
        # 음성 파일 생성 및 자동 재생
        tts = gTTS(text=st.session_state.question, lang='ja')
        tts.save("q.mp3")
        st.audio("q.mp3", format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"질문 추출 중 오류: {e}")

# 답변 입력 섹션
user_input = st.text_area("✍️ 일본어로 답변을 입력하세요:", height=150, placeholder="여기에 답변을 입력하거나 스마트폰 음성 인식을 사용하세요.")

# 피드백 섹션
if st.button('🤖 AI 피드백 받기'):
    if user_input and 'question' in st.session_state:
        with st.spinner('🔍 나고야 현지 면접관의 시각으로 분석 중...'):
            try:
                prompt = f"""
                당신은 나고야 지역 대기업의 인사 담당자입니다.
                질문: {st.session_state.question}
                사용자 답변: {user_input}
                
                평가 항목:
                1. 한국 금융권 20년 경력의 신뢰감이 잘 느껴지는가?
                2. 나고야 특유의 정중하고 보수적인 표현(데스/마스 등)이 적절한가?
                3. 더 자연스러운 일본어 문장 추천 (한국어로 피드백)
                """
                response = model.generate_content(prompt)
                st.markdown("---")
                st.subheader("💡 AI 면접관의 조언")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI 분석 중 오류가 발생했습니다: {e}")
    else:
        st.warning("먼저 [질문 받기]를 누르고 답변을 입력해 주세요.")
