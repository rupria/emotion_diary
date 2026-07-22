import streamlit as st
from db import get_db_connection

EMOTIONS = {
    5: {"label": "완전 좋음", "emoji": "(^Δ^)"},
    4: {"label": "좋음", "emoji": "(^_^)"},
    3: {"label": "보통", "emoji": "(-_-)"},
    2: {"label": "나쁨", "emoji": "(>_<)"},
    1: {"label": "끔찍함", "emoji": "(T_T)"}
}

def render_edit_page(change_page):
    st.markdown("<h2 style='text-align: center; color: #4E342E;'>🔍 일기 수정 및 삭제</h2>", unsafe_allow_html=True)

    if st.button("< 목록으로", key="back_from_edit"):
        change_page("list")

    st.write("---")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM diaries WHERE id = %s", (st.session_state.selected_diary_id,))
    diary_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if not diary_data:
        st.error("존재하지 않거나 삭제된 일기입니다.")
        if st.button("목록으로 돌아가기"):
            change_page("list")
    else:
        edit_date = st.date_input("날짜 수정", diary_data['diary_date'])

        st.markdown("**감정 수정**")
        emotion_options = [5, 4, 3, 2, 1]
        edit_emotion = st.radio(
            "감정 수정 선택",
            options=emotion_options,
            index=emotion_options.index(diary_data['emotion_score']),
            format_func=lambda x: f"{EMOTIONS[x]['emoji']} {EMOTIONS[x]['label']}",
            horizontal=True,
            label_visibility="collapsed"
        )

        edit_content = st.text_area("내용 수정", value=diary_data['content'], height=200)

        col_submit, col_delete, col_cancel = st.columns([2, 2, 1])

        with col_submit:
            if st.button("수정 완료", use_container_width=True, type="primary"):
                if not edit_content.strip():
                    st.error("내용을 입력해 주세요.")
                else:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    sql = "UPDATE diaries SET diary_date=%s, emotion_score=%s, content=%s WHERE id=%s"
                    cursor.execute(sql, (edit_date, edit_emotion, edit_content, diary_data['id']))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    change_page("list")

        with col_delete:
            if st.button("🗑️ 일기 삭제", use_container_width=True):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM diaries WHERE id = %s", (diary_data['id'],))
                conn.commit()
                cursor.close()
                conn.close()
                change_page("list")

        with col_cancel:
            if st.button("취소", use_container_width=True):
                change_page("list")