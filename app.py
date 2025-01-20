import streamlit as st

st.title("LeetCode Learning Tracker")
st.write("Track your progress and document your solutions for LeetCode problems.")

st.header("Welcome to LeetCode Learning Tracker")
st.write("Use this app to document your problem-solving journey on LeetCode.")
st.write("Features:")
st.write("- Add your solved LeetCode problems")
st.write("- Document your solutions with descriptions")
st.write("- Automatically sync solutions to GitHub")
st.write("- Track your progress over time")

# Initialize session state for problems if it doesn't exist
if "problems" not in st.session_state:
    st.session_state["problems"] = []
