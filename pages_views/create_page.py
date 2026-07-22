from datetime import date
from typing import Callable

import streamlit as st

from db import get_db_connection
from logger_config import get_logger


logger = get_logger(__name__)


EMOTIONS = {
    5: {
        "label": "완전 좋음",
        "emoji": "(^Δ^)"
    },
    4: {
        "label": "좋음",
        "emoji": "(^_^)"
    },
    3: {
        "label": "보통",
        "emoji": "(-_-)"
    },
    2: {
        "label": "나쁨",
        "emoji": "(>_<)"
    },
    1: {
        "label": "끔찍함",
        "emoji": "(T_T)"
    }
}


def render_create_page(change_page: Callable) -> None:
    """
    새 일기를 작성하는 페이지를 표시합니다.
    """

    logger.info("일기 작성 페이지 진입")

    st.markdown(
        """
        <h2 style="text-align: center; color: #4E342E;">
            📝 새 일기 쓰기
        </h2>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "< 뒤로",
        key="back_to_list"
    ):
        logger.info("일기 작성 페이지 뒤로 버튼 클릭")
        change_page("list")

    st.divider()

    input_date = st.date_input(
        "오늘의 날짜",
        value=date.today(),
        key="create_diary_date"
    )

    st.markdown("**오늘의 감정**")

    emotion_options = [5, 4, 3, 2, 1]

    selected_emotion = st.radio(
        "감정 선택",
        options=emotion_options,
        format_func=lambda score: (
            f"{EMOTIONS[score]['emoji']} "
            f"{EMOTIONS[score]['label']}"
        ),
        horizontal=True,
        label_visibility="collapsed",
        key="create_diary_emotion"
    )

    input_content = st.text_area(
        "오늘의 일기",
        placeholder="오늘의 감정과 하루를 기록해 보세요...",
        height=200,
        max_chars=2000,
        key="create_diary_content"
    )

    st.caption(f"{len(input_content)} / 2000")

    cancel_column, save_column = st.columns(2)

    with cancel_column:
        cancel_button = st.button(
            "취소하기",
            use_container_width=True,
            key="cancel_create_diary"
        )

    with save_column:
        save_button = st.button(
            "작성 완료",
            use_container_width=True,
            type="primary",
            key="save_create_diary"
        )

    if cancel_button:
        logger.info("일기 작성 취소 버튼 클릭")
        change_page("list")

    if save_button:
        logger.info(
            "일기 작성 완료 버튼 클릭 | 날짜=%s | 감정=%d | 글자 수=%d",
            input_date,
            selected_emotion,
            len(input_content)
        )

        if not input_content.strip():
            logger.warning("일기 저장 중단 | 내용 미입력")
            st.error("내용을 입력해 주세요!")
            return

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO diaries (
                    diary_date,
                    emotion_score,
                    content
                )
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                insert_query,
                (
                    input_date,
                    selected_emotion,
                    input_content.strip()
                )
            )

            connection.commit()

            logger.info(
                "일기 저장 성공 | 날짜=%s | 감정=%d",
                input_date,
                selected_emotion
            )

            # 작성한 날짜의 연도와 월로 목록 화면 이동
            st.session_state.current_year = input_date.year
            st.session_state.current_month = input_date.month

            change_page("list")

        except Exception as error:
            logger.exception(
                "일기 저장 실패 | 날짜=%s | 감정=%d",
                input_date,
                selected_emotion
            )

            if connection is not None:
                try:
                    connection.rollback()

                except Exception:
                    logger.exception("일기 저장 실패 후 rollback 오류")

            st.error("일기를 저장하는 중 오류가 발생했습니다.")
            st.exception(error)

        finally:
            if cursor is not None:
                try:
                    cursor.close()

                except Exception:
                    logger.exception("DB cursor 종료 실패")

            if connection is not None:
                try:
                    connection.close()

                except Exception:
                    logger.exception("DB connection 종료 실패")