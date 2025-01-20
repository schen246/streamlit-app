import streamlit as st
from streamlit_ace import st_ace
import os
from datetime import datetime
import json

# Configure page settings
st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
/* Input field styling */
.stTextInput input, .stTextArea textarea, div[data-baseweb="select"] {
    background-color: #f8f9fa !important;
    border: 1px solid #dee2e6 !important;
    border-radius: 4px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #1a73e8 !important;
    box-shadow: none !important;
}
/* Remove padding from main container */
.main .block-container {
    padding: 2rem 1rem !important;
    max-width: 1000px;
}
/* Section spacing */
.stMarkdown {
    margin-top: 1.5rem;
}
.section-divider {
    border-top: 1px solid #dee2e6;
    margin: 2rem 0;
}
/* Solution template styling */
.streamlit-ace {
    border: 1px solid #dee2e6;
    border-radius: 4px;
    margin-top: 0.5rem;
}
/* Button styling */
.stButton button {
    background-color: #1a73e8;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    float: right;
    margin-top: 1rem;
}
/* Hide fullscreen button */
button[title="View fullscreen"] {
    display: none;
}
/* Multiselect styling */
div[data-baseweb="select"] > div {
    background-color: #f8f9fa !important;
}
/* Title styling */
h1 {
    font-size: 1.5rem !important;
    margin-bottom: 2rem !important;
}
/* Label styling */
label {
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Add New Problem")

# Basic information
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    title = st.text_input("Problem Title", placeholder="e.g., Binary Search")
with col2:
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
with col3:
    frequency = st.selectbox("Frequency", ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"])

# Problem description
description = st.text_area("Problem Description", 
                         placeholder="Describe the problem here...",
                         height=120)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Examples section
st.markdown("### Examples")
col1, col2 = st.columns(2)
with col1:
    example_input = st.text_area("Example Input", 
                                placeholder="e.g., nums = [-1, 0, 3, 5, 9, 12], target = 9",
                                height=100)
    example_output = st.text_input("Example Output", placeholder="e.g., 4")

with col2:
    example_explanation = st.text_area("Example Explanation",
                                     placeholder="Explain why this is the correct output...",
                                     height=150)

# Constraints and Tags
col1, col2 = st.columns([3, 2])
with col1:
    constraints = st.text_area("Constraints (one per line)",
                             placeholder="e.g.,\n1 <= nums.length <= 10^4\n-10^4 <= nums[i] <= 10^4",
                             height=100)
with col2:
    tags = st.multiselect("Tags", 
                         ["Array", "String", "Hash Table", "Dynamic Programming", 
                          "Math", "Sorting", "Greedy", "Binary Search"])

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Solution Template
st.subheader("Solution Template")
solution_template = st_ace(
    value="""def solution_name(param1: type) -> return_type:
    pass""",
    language="python",
    theme="github",
    keybinding="vscode",
    font_size=14,
    tab_size=4,
    show_gutter=True,
    show_print_margin=True,
    wrap=True,
    auto_update=True,
    height=150
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Test cases in a container
st.subheader("Test Cases")
test_container = st.container()
with test_container:
    col1, col2 = st.columns(2)
    with col1:
        test_input = st.text_area("Test Input", 
                                 placeholder="One test case per line, e.g.:\n[-1, 0, 3, 5, 9, 12], 9\n[-1, 0, 3, 5, 9, 12], 2",
                                 height=100)
    with col2:
        test_output = st.text_area("Expected Output",
                                  placeholder="One result per line, corresponding to test inputs, e.g.:\n4\n-1",
                                  height=100)

# Submit button
if st.button("Add Problem"):
    if not title or not description:
        st.error("Please fill in at least the title and description.")
    else:
        # Create problem object
        problem = {
            "id": len(st.session_state.get("problems", [])) + 1,
            "title": title,
            "difficulty": difficulty,
            "frequency": frequency,
            "description": description,
            "example_input": example_input,
            "example_output": example_output,
            "example_explanation": example_explanation,
            "constraints": [c for c in constraints.split('\n') if c.strip()],
            "tags": tags,
            "solution_template": solution_template,
            "test_cases": {
                "inputs": [i.strip() for i in test_input.split('\n') if i.strip()],
                "outputs": [o.strip() for o in test_output.split('\n') if o.strip()]
            },
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        def save_problems(problems):
            """Save problems to the JSON file"""
            if not os.path.exists('data'):
                os.makedirs('data')
            with open('data/problems.json', 'w') as f:
                json.dump(problems, f, indent=2)

        # Add to session state and save to file
        if "problems" not in st.session_state:
            st.session_state.problems = []
        
        # Set problem ID
        problem["id"] = str(len(st.session_state.problems) + 1)
        
        # Add to session state
        st.session_state.problems.append(problem)
        
        # Save to JSON file
        save_problems(st.session_state.problems)
        
        st.success(f"Problem '{title}' added successfully!")
