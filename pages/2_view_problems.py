import streamlit as st

st.header("Documented Problems")

# Filter options
col1, col2 = st.columns(2)
with col1:
    difficulty_filter = st.multiselect("Filter by Difficulty", ["Easy", "Medium", "Hard"])
with col2:
    search_term = st.text_input("Search by title or tags")

if "problems" not in st.session_state:
    st.session_state["problems"] = []

if st.session_state["problems"]:
    filtered_problems = st.session_state["problems"]
    
    # Apply difficulty filter
    if difficulty_filter:
        filtered_problems = [p for p in filtered_problems if p["difficulty"] in difficulty_filter]
    
    # Apply search filter
    if search_term:
        search_term = search_term.lower()
        filtered_problems = [p for p in filtered_problems if 
                           search_term in p["title"].lower() or 
                           any(search_term in tag.lower() for tag in p["tags"])]
    
    for i, problem in enumerate(filtered_problems, 1):
        with st.expander(f"{i}. {problem['title']} ({problem['difficulty']})"):
            st.write(f"**Date Added:** {problem['date_added']}")
            if problem['tags']:
                st.write("**Tags:** " + ", ".join(problem['tags']))
            st.write("**Description:**")
            st.write(problem['description'])
            st.write("**Solution:**")
            st.code(problem['solution'], language="python")
else:
    st.write("No problems added yet.")
