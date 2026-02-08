import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import base64

# 1. 환경 설정 (본인의 API 키와 시트 ID를 넣으세요)
GOOGLE_API_KEY = "AIzaSyAV9mCyS7fJFj4d671o-SEO2ccPAH4JjQc"
SHEET_ID = "17DOk-zLFHhlwMgL_wiPYYXS-tLAoSYvZpWoLwcP6Mu8"
SHEET_NAME = "Sheet1"  # 시트 하단 탭 이름이 다르면 수정하세요

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 구글 시트를 데이터프레임으로 가져오는 마법의 주소
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# 앱 화면 구성
st.title("🏯 나고야 취업 성공! AI 모의 면접관")
st.markdown("20년 경력의 전문성을 일본어로 완벽하게 전달하세요.")

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

# 면접 시작 버튼
if st.button('🎯 새로운 질문 받기'):
    # 랜덤 질문 선택
    selected = df.sample(n=1).iloc[0]
    st.session_state.question = selected['面接官からの質問']
    st.session_state.ideal = selected['あなたの回答']

    st.subheader(f"면접관의 질문:")
    st.write(st.session_state.question)

    # 음성 출력
    tts = gTTS(text=st.session_state.question, lang='ja')
    tts.save("q.mp3")
    st.audio("q.mp3", format="audio/mp3", autoplay=True)

# 답변 분석 (이미 녹음 파일이 있다고 가정하거나 텍스트 입력을 우선 테스트)
user_input = st.text_area("답변을 입력하거나 음성 인식을 시작하세요 (현재는 텍스트 입력으로 테스트 가능)")

if st.button('🤖 AI 피드백 받기'):
    if 'question' in st.session_state:
        with st.spinner('나고야 현지 면접관이 분석 중입니다...'):
            prompt = f"""
            질문: {st.session_state.question}
            모범답안: {st.session_state.ideal}
            사용자 답변: {user_input}

            나고야의 보수적이고 예의를 중시하는 대기업 면접관 관점에서
            한국어로 상세한 피드백을 주세요.
            """
            response = model.generate_content(prompt)
            st.success("분석 완료!")
            st.write(response.text)
    else:
        st.warning("먼저 질문을 받아주세요.")
