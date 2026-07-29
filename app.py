import streamlit as st

from samwoo_prototype.database import create_tables
from samwoo_prototype.repositories.notes import NoteRepository
from samwoo_prototype.schemas.notes import NoteCreate
from samwoo_prototype.services.notes import create_note, list_notes

st.set_page_config(page_title="삼우 업무 프로토타입", page_icon="🧩", layout="wide")
create_tables()
repository = NoteRepository()

st.title("삼우 업무 프로토타입")
st.caption("화면은 Streamlit, 업무 로직과 데이터 처리는 별도 모듈에 작성합니다.")

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

st.subheader("저장된 항목")
for note in list_notes(repository):
    with st.container(border=True):
        st.markdown(f"**{note.title}**")
        st.write(note.content)
