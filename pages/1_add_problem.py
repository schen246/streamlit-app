import streamlit as st
from streamlit_ace import st_ace
import os
from datetime import datetime
import json
import sys
from io import StringIO
import contextlib
from typing import List
import ast

@contextlib.contextmanager
def capture_output():
    """Capture stdout and stderr"""
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

def parse_input(input_str):
    """Parse input string to Python objects"""
    try:
        return ast.literal_eval(input_str)
    except:
        return input_str

def execute_code(code, test_input):
    """Execute code with test input and return output"""
    with capture_output() as (out, err):
        try:
            # Create namespace for execution
            namespace = {'List': List}
            
            # Execute the function definition
            exec(code, namespace)
            
            # Get the function name (assuming it's the only function defined)
            func_name = [name for name, obj in namespace.items() 
                       if callable(obj) and name != 'List'][0]
            
            # Parse input and call function
            if isinstance(test_input, str):
                # Split by comma but respect brackets/parentheses
                args = []
                current = ""
                bracket_count = 0
                
                for char in test_input:
                    if char == ',' and bracket_count == 0:
                        if current.strip():
                            args.append(parse_input(current.strip()))
                        current = ""
                    else:
                        if char in '[({':
                            bracket_count += 1
                        elif char in '])}':
                            bracket_count -= 1
                        current += char
                
                if current.strip():
                    args.append(parse_input(current.strip()))
            else:
                args = [test_input]
            
            result = namespace[func_name](*args)
            return str(result), out.getvalue(), err.getvalue()
        except Exception as e:
            return None, out.getvalue(), str(e)

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
/* Solution styling */
.streamlit-ace {
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    margin-top: 0.75rem !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}
.streamlit-ace .ace_gutter {
    background: #f8f9fa !important;
    color: #6c757d !important;
}
.streamlit-ace .ace_print-margin {
    background: #e9ecef !important;
}
/* Language selector styling */
.stSelectbox [data-testid="stMarkdown"] {
    background: #f8f9fa;
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
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

# Solution
st.subheader("Solution")

# Language selector with improved styling
language = st.selectbox(
    "Programming Language",
    ["python", "javascript", "java", "cpp", "csharp", "golang"],
    format_func=lambda x: {
        "python": "Python",
        "javascript": "JavaScript",
        "java": "Java",
        "cpp": "C++",
        "csharp": "C#",
        "golang": "Go"
    }[x]
)

# Default templates for different languages
templates = {
    "python": """from typing import List, Optional

def solution_name(nums: List[int], target: int) -> int:
    '''
    Problem solving approach:
    1. Initialize variables
    2. Implement the solution logic
    3. Return the result
    
    Time complexity: O(?)
    Space complexity: O(?)
    '''
    # Your code here
    pass""",
    "javascript": """/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number}
 */
function solutionName(nums, target) {
    // Your code here
}""",
    "java": """class Solution {
    /**
     * @param nums Input array
     * @param target Target value
     * @return Result
     */
    public int solutionName(int[] nums, int target) {
        // Your code here
    }
}""",
    "cpp": """class Solution {
public:
    /**
     * @param nums Input array
     * @param target Target value
     * @return Result
     */
    int solutionName(vector<int>& nums, int target) {
        // Your code here
    }
};""",
    "csharp": """public class Solution {
    /// <summary>
    /// Solution method description
    /// </summary>
    /// <param name="nums">Input array</param>
    /// <param name="target">Target value</param>
    /// <returns>Result</returns>
    public int SolutionName(int[] nums, int target) {
        // Your code here
    }
}""",
    "golang": """// solutionName finds the target in the array
func solutionName(nums []int, target int) int {
    // Your code here
}"""
}

# Enhanced code editor with improved styling
solution_template = st_ace(
    value=templates[language],
    language=language,
    theme="tomorrow",  # Modern theme
    keybinding="vscode",
    font_size=14,
    tab_size=4,
    show_gutter=True,
    show_print_margin=True,
    wrap=True,
    auto_update=True,
    height=300,  # Taller editor
    annotations=[],
    key=f"ace_editor_{language}"
)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Test cases section
st.subheader("Test Cases")

# Test case inputs and outputs
col1, col2 = st.columns(2)
with col1:
    test_input = st.text_area("Test Input", 
                           placeholder="One test case per line, e.g.:\n[-1, 0, 3, 5, 9, 12], 9\n[-1, 0, 3, 5, 9, 12], 2",
                           height=100)
with col2:
    test_output = st.text_area("Expected Output",
                            placeholder="One result per line, corresponding to test inputs, e.g.:\n4\n-1",
                            height=100)

# Run tests button and results
if st.button("Run Tests", type="primary"):
    if not test_input or not test_output:
        st.warning("Please add test cases before running tests.")
    else:
        test_inputs = [i.strip() for i in test_input.split('\n') if i.strip()]
        test_outputs = [o.strip() for o in test_output.split('\n') if o.strip()]
        
        if len(test_inputs) != len(test_outputs):
            st.error("Number of test inputs and outputs don't match.")
        else:
            all_passed = True
            for i, (test_in, expected) in enumerate(zip(test_inputs, test_outputs)):
                result, stdout, stderr = execute_code(solution_template, test_in)
                
                # Display test case results
                with st.expander(f"Test Case {i + 1}", expanded=True):
                    cols = st.columns([0.3, 0.3, 0.3, 0.1])
                    cols[0].markdown("**Input:**")
                    cols[0].code(test_in)
                    cols[1].markdown("**Expected:**")
                    cols[1].code(expected)
                    cols[2].markdown("**Result:**")
                    cols[2].code(result if not stderr else "Error")
                    
                    if stderr:
                        cols[3].markdown("**Status:**")
                        cols[3].error("❌")
                        st.error(f"Error: {stderr}")
                        all_passed = False
                    else:
                        cols[3].markdown("**Status:**")
                        if str(result) == expected:
                            cols[3].success("✅")
                        else:
                            cols[3].error("❌")
                            all_passed = False
            
            if all_passed:
                st.success("🎉 All Tests Passed! You can now add this problem.")
            else:
                st.error("❌ Some tests failed. Please fix the solution before adding the problem.")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

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
