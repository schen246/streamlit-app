import streamlit as st
import os
import subprocess
from datetime import datetime

st.title("LeetCode Learning Tracker")
st.write("Track your progress and document your solutions for LeetCode problems.")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Add Problem", "View Problems", "GitHub Sync"])

if "problems" not in st.session_state:
    st.session_state["problems"] = []

def save_to_file(problem):
    if not os.path.exists("solutions"):
        os.makedirs("solutions")
    
    filename = f"solutions/{problem['title'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    
    # Write solution to file
    with open(filename, "w") as f:
        f.write(f"# {problem['title']}\n")
        f.write(f"# Description: {problem['description']}\n\n")
        f.write(problem['solution'])
    
    return filename

def commit_to_github(filename, problem_title):
    try:
        # Add the file
        subprocess.run(["git", "add", filename])
        
        # Commit with problem title
        commit_message = f"Add solution: {problem_title}"
        subprocess.run(["git", "commit", "-m", commit_message])
        
        # Push to GitHub
        subprocess.run(["git", "push"])
        return True
    except Exception as e:
        st.error(f"Error syncing with GitHub: {str(e)}")
        return False

if page == "Home":
    st.header("Welcome to LeetCode Learning Tracker")
    st.write("Use this app to document your problem-solving journey on LeetCode.")
    st.write("Features:")
    st.write("- Add your solved LeetCode problems")
    st.write("- Document your solutions with descriptions")
    st.write("- Automatically sync solutions to GitHub")
    st.write("- Track your progress over time")

elif page == "Add Problem":
    st.header("Add a New Problem")
    title = st.text_input("Problem Title")
    difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
    description = st.text_area("Problem Description")
    solution = st.text_area("Solution (Python code)")
    tags = st.text_input("Tags (comma-separated)", "")

    if st.button("Add Problem"):
        if title and description and solution:
            problem = {
                "title": title,
                "difficulty": difficulty,
                "description": description,
                "solution": solution,
                "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            filename = save_to_file(problem)
            st.session_state["problems"].append(problem)
            
            if commit_to_github(filename, title):
                st.success("Problem added and synced to GitHub successfully!")
            else:
                st.warning("Problem added locally but GitHub sync failed.")
        else:
            st.error("Please fill in all required fields (Title, Description, and Solution)")

elif page == "View Problems":
    st.header("Documented Problems")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        difficulty_filter = st.multiselect("Filter by Difficulty", ["Easy", "Medium", "Hard"])
    with col2:
        search_term = st.text_input("Search by title or tags")
    
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

elif page == "GitHub Sync":
    st.header("GitHub Repository Status")
    
    if st.button("Check Git Status"):
        try:
            status = subprocess.check_output(["git", "status"]).decode()
            st.code(status, language="bash")
        except Exception as e:
            st.error(f"Error checking git status: {str(e)}")
    
    st.subheader("Manual Sync")
    if st.button("Force Sync All Solutions"):
        try:
            subprocess.run(["git", "add", "solutions/*"])
            subprocess.run(["git", "commit", "-m", "Sync all solutions"])
            subprocess.run(["git", "push"])
            st.success("Successfully synced all solutions to GitHub!")
        except Exception as e:
            st.error(f"Error during manual sync: {str(e)}")
    
    st.subheader("Repository Setup Instructions")
    st.write("""
    1. Create a new repository on GitHub
    2. Initialize git in this directory (if not already done):
       ```
       git init
       ```
    3. Add your GitHub repository as remote:
       ```
       git remote add origin YOUR_REPOSITORY_URL
       ```
    4. Set up your git credentials
    5. Make sure you have write permissions to the repository
    """)
