from datetime import datetime

import streamlit as st

from db import init_db
from logger_config import get_logger
from pages_views.list_page import render_list_page
from pages_views.create_page import render_create_page
from pages_views.edit_page import render_edit_page


# 로그 설정
logger = get_logger(__name__)


# 0. 페이지 기본 설정
st.set_page_config(
    page_title="감성일기장",
    page_icon="📝",
    layout="centered"
)


# 스타일
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAF6ED;
    }

    .diary-card {
        background-color: #FFFDF9;
        border: 2px solid #D5C5B5;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        box-shadow: 1px 2px 5px rgba(0,0,0,0.05);
    }

    .emotion-circle {
        width: 65px;
        height: 65px;
        border-radius: 50%;
        border: 3px solid #BCAAA4;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 16px;
        margin-right: 20px;
    }

    .em-5 { background-color: #FFD54F; color: #5D4037; }
    .em-4 { background-color: #A5D6A7; color: #2E7D32; }
    .em-3 { background-color: #AED581; color: #33691E; }
    .em-2 { background-color: #FFB74D; color: #E65100; }
    .em-1 { background-color: #EF9A9A; color: #C62828; }

    .diary-date {
        color: #8D6E63;
        font-size: 14px;
        font-weight: bold;
        margin-bottom: 4px;
    }

    .diary-content {
        color: #3E2723;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# DB 초기화
try:
    init_db()
    logger.info("DB 초기화 성공")

except Exception:
    logger.exception("DB 초기화 실패")
    st.error("데이터베이스 초기화 중 오류가 발생했습니다.")
    st.stop()


# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "list"

if "current_year" not in st.session_state:
    st.session_state.current_year = datetime.now().year

if "current_month" not in st.session_state:
    st.session_state.current_month = datetime.now().month

if "selected_diary_id" not in st.session_state:
    st.session_state.selected_diary_id = None


def change_page(page_name: str, diary_id=None):
    logger.info(
        "페이지 변경 | 기존=%s | 이동=%s | diary_id=%s",
        st.session_state.page,
        page_name,
        diary_id
    )

    st.session_state.page = page_name
    st.session_state.selected_diary_id = diary_id
    st.rerun()


def adjust_month(amount: int):
    month = st.session_state.current_month + amount
    year = st.session_state.current_year

    if month > 12:
        month = 1
        year += 1

    elif month < 1:
        month = 12
        year -= 1

    st.session_state.current_month = month
    st.session_state.current_year = year

    logger.info(
        "조회 월 변경 | year=%s | month=%s",
        year,
        month
    )

    st.rerun()


# 페이지 라우팅
current_page = st.session_state.page

logger.info(
    "페이지 렌더링 시작 | page=%s | selected_diary_id=%s",
    current_page,
    st.session_state.selected_diary_id
)

try:
    if current_page == "list":
        render_list_page(change_page, adjust_month)

    elif current_page == "create":
        render_create_page(change_page)

    elif current_page == "edit":
        render_edit_page(change_page)

    else:
        logger.warning("알 수 없는 페이지 값 | page=%s", current_page)
        st.session_state.page = "list"
        st.rerun()

except Exception:
    logger.exception(
        "페이지 렌더링 실패 | page=%s",
        current_page
    )

    st.error("페이지를 불러오는 중 오류가 발생했습니다.")

    # 개발 중에는 실제 오류 화면도 표시
    st.exception(Exception("자세한 오류는 logs/app.log를 확인하세요."))