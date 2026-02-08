# 질문을 뽑는 부분을 더 똑똑하게 수정했습니다.
if st.button('🎯 새로운 질문 받기'):
    try:
        # 컬럼 이름 대신 '위치'로 가져오도록 수정 (0번은 첫번째 칸, 1번은 두번째 칸)
        selected = df.sample(n=1).iloc[0]
        st.session_state.question = selected.iloc[0] # 첫 번째 열 (질문)
        st.session_state.ideal = selected.iloc[1]    # 두 번째 열 (모범답안)
        
        st.subheader(f"면접관의 질문:")
        st.write(st.session_state.question)
        
        # 음성 출력
        tts = gTTS(text=st.session_state.question, lang='ja')
        tts.save("q.mp3")
        st.audio("q.mp3", format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"질문을 불러오는 중 에러가 발생했습니다. 시트 구성을 확인해 주세요: {e}")
