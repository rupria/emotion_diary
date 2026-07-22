from datetime import date
import streamlit as st
from db import get_db_connection

EMOTIONS = {
    5: {"label": "완전 좋음", "emoji": "(^Δ^)"},
    4: {"label": "좋음", "emoji": "(^_^)"},
    3: {"label": "보통", "emoji": "(-_-)"},
    2: {"label": "나쁨", "emoji": "(>_<)"},
    1: {"label": "끔찍함", "emoji": "(T_T)"}
}

def render_create_page(change_page):
    st.markdown("<h2 style='text-align: center; color: #4E342E;'>📝 새 일기 쓰기</h2>", unsafe_allow_html=True)

    if st.button("< 뒤로", key="back_to_list"):
        change_page("list")

    st.write("---")

    input_date = st.date_input("오늘의 날짜", date.today())

    st.markdown("**오늘의 감정**")
    emotion_options = [5, 4, 3, 2, 1]
    selected_emotion = st.radio(
        "감정 선택",
        options=emotion_options,
        format_func=lambda x: f"{EMOTIONS[x]['emoji']} {EMOTIONS[x]['label']}",
        horizontal=True,
        label_visibility="collapsed"
    )

    input_content = st.text_area("오늘의 일기", placeholder="오늘의 감정과 하루를 기록해 보세요...", height=200)
    st.caption(f"{len(input_content)} / 2000")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("취소하기", use_container_width=True):
            change_page("list")
    with c2:
        if st.button("작성 완료", use_container_width=True, type="primary"):
            if not input_content.strip():
                st.error("내용을 입력해 주세요!")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                sql = "INSERT INTO diaries (diary_date, emotion_score, content) VALUES (%s, %s, %s)"
                cursor.execute(sql, (input_date, selected_emotion, input_content))
                conn.commit()
                cursor.close()
                conn.close()

                # 작성한 날짜의 연/월로 이동
                st.session_state.current_year = input_date.year
                st.session_state.current_month = input_date.month
                change_page("list")

                import streamlit as st

from logger_config import get_logger


logger = get_logger(__name__)


def render_create_page():
    logger.info("일기 작성 페이지 진입")

    content = st.text_area("일기 내용")

    if st.button("저장", key="create_diary"):
        logger.info(
            "일기 저장 버튼 클릭 | 글자 수=%d",
            len(content)
        )