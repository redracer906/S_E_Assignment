import requests
import streamlit as st

API_URL = "http://127.0.0.1:5001"
st.set_page_config(page_title="Student Management", page_icon="🎓", layout="wide")
st.title("Student Management System")
st.caption("Streamlit frontend connected to the Flask and SQLite API")


def get_students():
    try:
        response = requests.get(f"{API_URL}/students", timeout=4)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Cannot connect to Flask API. Start app.py first. Details: {exc}")
        return None


def show_result(response):
    if response.ok:
        st.success(response.json().get("message", "Operation successful"))
        st.rerun()
    else:
        st.error(response.json().get("error", "Request failed"))

students = get_students()
if students is not None:
    st.subheader("All students")
    st.dataframe(students, use_container_width=True, hide_index=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Add student")
        with st.form("add_student_form", clear_on_submit=True):
            name = st.text_input("Name", key="add_name")
            department = st.text_input("Department", key="add_department")
            email = st.text_input("Email", key="add_email")
            submitted = st.form_submit_button("Add student")
        if submitted:
            try:
                response = requests.post(
                    f"{API_URL}/students",
                    json={"name": name, "department": department, "email": email}, timeout=4
                )
                show_result(response)
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")

    with right:
        st.subheader("Update student")
        if students:
            student_map = {f'{s["id"]} — {s["name"]}': s for s in students}
            selected_label = st.selectbox("Select student", list(student_map))
            selected = student_map[selected_label]
            with st.form("update_student_form"):
                new_name = st.text_input("Name", value=selected["name"])
                new_department = st.text_input("Department", value=selected["department"])
                new_email = st.text_input("Email", value=selected["email"])
                updated = st.form_submit_button("Update student")
            if updated:
                try:
                    response = requests.put(
                        f'{API_URL}/students/{selected["id"]}',
                        json={"name": new_name, "department": new_department, "email": new_email}, timeout=4
                    )
                    show_result(response)
                except requests.RequestException as exc:
                    st.error(f"Request failed: {exc}")

            st.subheader("Delete student")
            if st.button(f'Delete {selected["name"]}', type="secondary"):
                try:
                    response = requests.delete(f'{API_URL}/students/{selected["id"]}', timeout=4)
                    show_result(response)
                except requests.RequestException as exc:
                    st.error(f"Request failed: {exc}")
        else:
            st.info("Add a student first to enable update and delete.")

    if st.button("Refresh records"):
        st.rerun()
