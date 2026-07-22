from datetime import datetime
import streamlit as st

from db import init_db
from pages_views.list_page import render_list_page
from pages_views.create_page import render_create_page
from pages_views.edit_page import render_edit_page

# 0. 페이지 기본 설정 및 스타일 정의
st.set_page_config(page_title="감성일기장", page_icon="📝", layout="centered")

st.markdown("""
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
""", unsafe_allow_html=True)

# DB 초기화
init_db()

# 세션 상태(Session State) 관리
if "page" not in st.session_state:
    st.session_state.page = "list"
if "current_year" not in st.session_state:
    st.session_state.current_year = datetime.now().year
if "current_month" not in st.session_state:
    st.session_state.current_month = datetime.now().month
if "selected_diary_id" not in st.session_state:
    st.session_state.selected_diary_id = None

def change_page(page_name, diary_id=None):
    st.session_state.page = page_name
    st.session_state.selected_diary_id = diary_id
    st.rerun()

def adjust_month(amount):
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
    st.rerun()

# 페이지 라우팅
if st.session_state.page == "list":
    render_list_page(change_page, adjust_month)
elif st.session_state.page == "create":
    render_create_page(change_page)
elif st.session_state.page == "edit":
    render_edit_page(change_page)

    import streamlit as st

from logger_config import get_logger


logger = get_logger(__name__)

logger.info("Streamlit 애플리케이션 실행")

st.title("감정 일기")

if st.button("클릭 테스트"):
    logger.info("클릭 테스트 버튼이 눌렸습니다.")
    st.success("클릭 이벤트가 기록되었습니다.")