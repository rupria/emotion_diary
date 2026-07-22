import streamlit as st
from db import get_db_connection

EMOTIONS = {
    5: {"label": "완전 좋음", "emoji": "(^Δ^)", "class": "em-5"},
    4: {"label": "좋음", "emoji": "(^_^)", "class": "em-4"},
    3: {"label": "보통", "emoji": "(-_-)", "class": "em-3"},
    2: {"label": "나쁨", "emoji": "(>_<)", "class": "em-2"},
    1: {"label": "끔찍함", "emoji": "(T_T)", "class": "em-1"}
}

def render_list_page(change_page, adjust_month):
    # 1. 상단 월 선택 바
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.button(" < ", on_click=adjust_month, args=(-1,), key="prev_month")
    with col2:
        st.markdown(
            f"<h2 style='text-align: center; color: #4E342E;'>"
            f"{st.session_state.current_year}년 {st.session_state.current_month}월</h2>",
            unsafe_allow_html=True
        )
    with col3:
        st.button(" > ", on_click=adjust_month, args=(1,), key="next_month")

    st.write("---")

    # 2. 정렬 조건 필터 및 새 일기 버튼
    filter_col, btn_col = st.columns([3, 1])
    with filter_col:
        sort_order = st.selectbox("정렬 기준", ["최신순", "오래된순"], label_visibility="collapsed")
    with btn_col:
        if st.button("+ 새 일기", use_container_width=True, type="primary"):
            change_page("create")

    # 3. 데이터베이스 데이터 조회
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    order_sql = "DESC" if sort_order == "최신순" else "ASC"
    query = f"""
        SELECT id, diary_date, emotion_score, content
        FROM diaries
        WHERE YEAR(diary_date) = %s AND MONTH(diary_date) = %s
        ORDER BY diary_date {order_sql}, id {order_sql}
    """
    cursor.execute(query, (st.session_state.current_year, st.session_state.current_month))
    diaries = cursor.fetchall()
    cursor.close()
    conn.close()

    # 4. 목록 출력
    if not diaries:
        st.info("이달에 작성된 일기가 없습니다. 새로운 하루를 기록해 보세요!")
    else:
        for diary in diaries:
            em_info = EMOTIONS.get(diary['emotion_score'], EMOTIONS[3])

            card_col1, card_col2, card_col3 = st.columns([1, 5, 1])

            with card_col1:
                st.markdown(f"""
                    <div class="emotion-circle {em_info['class']}">
                        {em_info['emoji']}
                    </div>
                """, unsafe_allow_html=True)

            with card_col2:
                st.markdown(f"<div class='diary-date'>{diary['diary_date']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='diary-content'>{diary['content']}</div>", unsafe_allow_html=True)

            with card_col3:
                if st.button(" 상세보기 ", key=f"view_{diary['id']}"):
                    change_page("edit", diary['id'])

            st.markdown("<hr style='margin: 8px 0; border-top: 1px dashed #D5C5B5;'>", unsafe_allow_html=True)