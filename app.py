import streamlit as st

from samwoo_prototype.config import allows_local_demo_data, get_settings
from samwoo_prototype.repositories.notes import NoteRepository
from samwoo_prototype.schemas.notes import NoteCreate
from samwoo_prototype.services.notes import create_note, list_notes

st.set_page_config(page_title="삼우 업무 프로토타입", page_icon="🧩", layout="wide")
repository = NoteRepository()

st.title("삼우 업무 프로토타입")
st.caption("화면은 Streamlit, 업무 로직과 데이터 처리는 별도 모듈에 작성합니다.")
st.warning(
    "이 템플릿 앱은 기본 공개입니다. 앱 자체 인증·인가를 구현하기 전에는 "
    "개인정보나 업무상 민감정보를 입력하지 마세요."
)

local_demo = allows_local_demo_data(get_settings().database_url)

if local_demo:
    with st.form("new-note", clear_on_submit=True):
        title = st.text_input("제목")
        content = st.text_area("내용")
        submitted = st.form_submit_button("저장")

    if submitted:
        try:
            create_note(repository, NoteCreate(title=title, content=content))
            st.success("저장했습니다.")
        except ValueError as error:
            st.error(str(error))
else:
    st.info(
        "공개 배포에서는 익명 저장이 비활성화되어 있습니다. 앱 자체 인증·인가와 "
        "서버 측 권한 검사를 구현한 뒤 저장 기능을 연결하세요."
    )

if local_demo:
    st.subheader("최근 저장 항목")
    st.caption("로컬 화면의 메모리 사용을 제한하기 위해 최근 100개만 표시합니다.")
    for note in list_notes(repository):
        with st.container(border=True):
            st.markdown(f"**{note.title}**")
            st.write(note.content)
else:
    st.subheader("운영 데이터")
    st.caption(
        "앱 자체 인증·인가를 구현하기 전에는 PostgreSQL 레코드를 공개 화면에서 조회하지 않습니다."
    )
