import streamlit as st
import os
from datetime import datetime
import subprocess

st.header("Add a New Problem")
title = st.text_input("Problem Title")
difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
description = st.text_area("Problem Description")
solution = st.text_area("Solution (Python code)")
tags = st.text_input("Tags (comma-separated)", "")

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

if "problems" not in st.session_state:
    st.session_state["problems"] = []

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
