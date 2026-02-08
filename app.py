import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import os

# 1. API 키 설정 (가장 확실한 방법: 직접 입력 또는 Secrets 사용)
# 만약 에러가 계속되면 " " 사이에 영태님의 API 키를 직접 넣어보세요.
API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyAV9mCyS7fJFj4d671o-SEO2ccPAH4JjQc")

if not API_KEY or API_KEY == "AIzaSyAV9mCyS7fJFj4d671o-SEO2ccPAH4JjQc":
    st.error("⚠️ API 키가 설정되지 않았습니다. 코드에 직접 넣거나 Streamlit Secrets에 입력해 주세요.")
else:
    genai.configure(api_key=API_KEY)

# 모델 설정 (가장 최신이며 안정적인 flash 모델 사용)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. 구글 시트 ID (영태님의 ID 적용)
SHEET_ID = "17DOk-zLFHhlwMgL_wiPYYXS-tLAoSYvZpWoLwcP6Mu8"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.title("🏯 나고야 취업 성공! AI 모의 면접관")
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv(url, encoding='utf-8')

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ 시트 데이터를 불러오지 못했습니다: {e}")
    st.stop()

# 면접 질문 섹션
if st.button('🎯 새로운 질문 받기'):
    try:
        selected = df.sample(n=1).iloc[0]
        st.session_state.question = selected.iloc[0]
        st.session_state.ideal = selected.iloc[1]
        
        st.subheader("📢 면접관의 질문:")
        st.info(st.session_state.question)
        
        tts = gTTS(text=st.session_state.question, lang='ja')
        tts.save("q.mp3")
        st.audio("q.mp3", format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"질문 추출 에러: {e}")

# 답변 입력 섹션
user_input = st.text_area("✍️ 일본어 답변을 입력하세요 (또는 스마트폰 음성 입력 사용):", height=150)

# 피드백 섹션 (에러 진단 기능 강화)
if st.button('🤖 AI 피드백 받기'):
    if not user_input:
        st.warning("먼저 답변을 입력해 주세요.")
    elif 'question' not in st.session_state:
        st.warning("먼저 [질문 받기] 버튼을 눌러주세요.")
    else:
        with st.spinner('🔍 나고야 현지 면접관이 분석 중입니다...'):
            try:
                prompt = f"""
                당신은 나고야 지역 대기업의 인사 담당자입니다. 
                아래 면접 질문에 대한 사용자의 답변을 평가해 주세요.
                사용자는 한국 금융권 20년 경력의 베테랑입니다.
                
                질문: {st.session_state.question}
                사용자 답변: {user_input}
                
                평가 가이드:
                1. 나고야의 보수적인 기업 문화를 고려한 정중한 일본어 표현 제안
                2. 20년 경력의 전문성이 신뢰감 있게 전달되는지 확인
                3. 한국어로 친절하고 전문적인 피드백 제공
                """
                response = model.generate_content(prompt)
                st.success("✅ 분석 완료!")
                st.markdown(response.text)
            except Exception as e:
                # 에러가 나면 화면에 빨간색으로 에러 원인을 보여줍니다.
                st.error(f"❌ AI 분석 중 에러가 발생했습니다: {str(e)}")
                st.info("💡 팁: API 키가 유효한지, 혹은 할당량이 초과되지 않았는지 확인해 보세요.")
