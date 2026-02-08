import streamlit as st
import pandas as pd
import google.generativeai as genai
from gtts import gTTS
import os

# 1. 보안을 위해 API 키를 직접 적지 않고 'Secrets' 기능을 사용하도록 변경합니다.
# (잠시 후 2단계에서 설정하는 법을 알려드릴게요)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API 키가 설정되지 않았습니다. Streamlit 설정에서 GEMINI_API_KEY를 입력해 주세요.")

# 모델 이름을 더 명확하게 'models/gemini-1.5-flash'로 수정했습니다.
model = genai.GenerativeModel('models/gemini-1.5-flash')

# (이후 시트 연결 및 앱 화면 코드는 이전과 동일하게 유지하시면 됩니다)
