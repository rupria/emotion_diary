import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str = "emotion_diary") -> logging.Logger:
    # 현재 파일이 있는 프로젝트 폴더
    base_dir = Path(__file__).resolve().parent

    # logs 폴더 자동 생성
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Streamlit 재실행 시 핸들러 중복 등록 방지
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(message)s"
    )

    # 로그 파일 기록
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,  # 파일 최대 크기 5MB
        backupCount=3,             # 이전 로그 파일 3개 보관
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # VS Code 터미널에도 출력
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger