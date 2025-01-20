import streamlit as st

st.title("LeetCode Learning Tracker")
st.write("Track your progress and document your solutions for LeetCode problems.")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Problem", "View Problems"])

if "problems" not in st.session_state:
    st.session_state["problems"] = []

if page == "Home":
    st.header("Welcome to LeetCode Learning Tracker")
    st.write("Use this app to document your problem-solving journey on LeetCode.")

elif page == "Add Problem":
    st.header("Add a New Problem")
    title = st.text_input("Problem Title")
    description = st.text_area("Problem Description")
    solution = st.text_area("Solution")

    if st.button("Add Problem"):
        st.session_state["problems"].append({
            "title": title,
            "description": description,
            "solution": solution
        })
        st.success("Problem added successfully!")

elif page == "View Problems":
    st.header("Documented Problems")
    if st.session_state["problems"]:
        for i, problem in enumerate(st.session_state["problems"], 1):
            st.subheader(f"{i}. {problem['title']}")
            st.write("**Description:**")
            st.write(problem['description'])
            st.write("**Solution:**")
            st.code(problem['solution'], language="python")
    else:
        st.write("No problems added yet.")