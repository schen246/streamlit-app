import streamlit as st
from streamlit_ace import st_ace
import os
from datetime import datetime
import subprocess
import sys
from io import StringIO
import contextlib
import json

# Configure page to use wide layout
st.set_page_config(layout="wide")

def execute_code(code, test_input=None):
    # Create string buffer to capture output
    output_buffer = StringIO()
    error_buffer = StringIO()
    
    # Create a namespace for execution
    namespace = {}
    
    # Redirect stdout and stderr
    with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
        try:
            # Execute the code to define the function
            exec(code, namespace)
            
            # If test input is provided, try to execute the function
            if test_input:
                try:
                    # Parse test input as Python literal
                    input_data = eval(test_input)
                    
                    # Find the function to call
                    function_name = None
                    for name, obj in namespace.items():
                        if callable(obj) and not name.startswith('__'):
                            function_name = name
                            break
                    
                    if function_name:
                        if isinstance(input_data, tuple):
                            result = namespace[function_name](*input_data)
                        elif isinstance(input_data, dict):
                            result = namespace[function_name](**input_data)
                        else:
                            result = namespace[function_name](input_data)
                        
                        print(f"Input: {test_input}")
                        print(f"Output: {result}")
                except Exception as e:
                    print(f"Error running test case: {str(e)}")
            
            output = output_buffer.getvalue()
            error = error_buffer.getvalue()
            return output, error, None
        except Exception as e:
            return output_buffer.getvalue(), error_buffer.getvalue(), str(e)

# Navigation bar
st.markdown("""
<div style='padding: 1rem; background-color: #f8f9fa; margin-bottom: 1rem'>
    <span style='font-size: 1.2em; margin-right: 2rem; color: #0366d6;'>📝 Description</span>
    <span style='font-size: 1.2em; margin-right: 2rem; color: #0366d6;'>💻 Solution</span>
    <span style='font-size: 1.2em; color: #0366d6;'>📊 Submissions</span>
</div>
""", unsafe_allow_html=True)

# Problem details
with st.expander("Problem Details", expanded=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        title = st.text_input("Problem Title", value="Binary Search")
        description = st.text_area("Problem Description", height=100, value="""Given a sorted array of integers nums and a target value, return the index of target in nums. If target is not found, return -1.

Example 1:
Input: nums = [-1, 0, 3, 5, 9, 12], target = 9
Output: 4
Explanation: 9 exists in nums and its index is 4

Example 2:
Input: nums = [-1, 0, 3, 5, 9, 12], target = 2
Output: -1
Explanation: 2 does not exist in nums so return -1

Constraints:
- nums is sorted in ascending order
- All values in nums are unique
- 1 <= nums.length <= 10^4
- -10^4 <= nums[i], target <= 10^4""")
    
    with col2:
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        tags = st.text_input("Tags (comma-separated)", "")

# Main coding interface with improved layout
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        background-color: #0366d6;
        color: white;
    }
    .output-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

col_main, col_side = st.columns([3, 1])

with col_main:
    # Language selector and code editor
    st.selectbox("Language", ["Python3"], key="language")
    solution = st_ace(
        value="""def binary_search(nums: list[int], target: int) -> int:
    # Write your binary search implementation here
    left = 0
    right = len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1""",
        placeholder="Write your Python solution here...",
        language="python",
        theme="monokai",
        keybinding="vscode",
        font_size=14,
        tab_size=4,
        show_gutter=True,
        show_print_margin=True,
        wrap=True,
        auto_update=True,
        height=400
    )

with col_side:
    # Test cases section
    st.markdown("### Test Cases")
    test_input = st.text_area("Test Input", height=100, 
                             value="([-1, 0, 3, 5, 9, 12], 9)",
                             placeholder="Example: [1, 2, 3] for a single argument\n(1, 2, 3) for multiple arguments")
    expected_output = st.text_area("Expected Output", height=100, 
                                  value="4",
                                  placeholder="Expected return value")
    
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("Run Code")
    with col2:
        submit_button = st.button("Submit")

    if run_button:
        if solution.strip():
            output, error, exception = execute_code(solution, test_input if test_input.strip() else None)
            
            st.markdown("### Test Case Console")
            with st.container():
                st.markdown('<div class="output-container">', unsafe_allow_html=True)
                if output:
                    st.code(output, language="text")
                if error or exception:
                    st.error(error if error else exception)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Compare with expected output if provided
                if expected_output.strip() and output.strip():
                    try:
                        actual_output = output.strip().split("Output: ")[1].strip()
                        if actual_output == expected_output.strip():
                            st.success("✅ Test case passed!")
                        else:
                            st.error("❌ Test case failed")
                    except:
                        st.error("❌ Could not verify test case")
        else:
            st.warning("Please enter some code to run")

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
