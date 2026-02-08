import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import base64

# 1. API 키 설정 (보안을 위해 Secrets 기능을 권장합니다)
# 만약 에러가 계속되면 "키_직접_입력" 부분에 따옴표와 함께 키를 넣으셔도 됩니다.
API_KEY = st.secrets.get("GEMINI_API_KEY", "여기에_API_키를_직접_넣으셔도_됩니다")
genai.configure(api_key=API_KEY)

# 모델 이름을 가장 안정적인 버전으로 명시했습니다.
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 구글 시트 정보 (영태님의 시트 ID로 꼭 확인하세요)
SHEET_ID = "영태님의_시트_ID_입력"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.title("🏯 나고야 취업 성공! AI 모의 면접관")
st.markdown("20년 경력의 전문성을 일본어로 완벽하게 전달하세요.")

@st.cache_data
def load_data():
    return pd.read_csv(url)

try:
    df = load_data()
except Exception as e:
    st.error(f"시트 데이터를 불러오지 못했습니다: {e}")
    st.stop()

if st.button('🎯 새로운 질문 받기'):
    selected = df.sample(n=1).iloc[0]
    st.session_state.question = selected['面接官からの質問']
    st.session_state.ideal = selected['あなたの回答']
    st.subheader(f"면접관의 질문:")
    st.write(st.session_state.question)
    tts = gTTS(text=st.session_state.question, lang='ja')
    tts.save("q.mp3")
    st.audio("q.mp3", format="audio/mp3", autoplay=True)

user_input = st.text_area("일본어로 답변을 입력하세요:", height=150)

if st.button('🤖 AI 피드백 받기'):
    if user_input and 'question' in st.session_state:
        with st.spinner('나고야 현지 면접관이 분석 중입니다...'):
            prompt = f"""
            면접 질문: {st.session_state.question}
            사용자 답변: {user_input}
            나고야의 보수적인 기업 문화를 고려하여 정중한 일본어 표현과 
            한국 금융권 20년 경력이 잘 드러나도록 한국어로 피드백해 주세요.
            """
            try:
                response = model.generate_content(prompt)
                st.success("분석 완료!")
                st.write(response.text)
            except Exception as e:
                st.error(f"AI 분석 중 오류 발생: {e}")
    else:
        st.warning("질문을 먼저 받고 답변을 입력해 주세요.")
