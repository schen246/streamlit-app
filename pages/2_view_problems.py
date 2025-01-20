import streamlit as st
import json
import os
from streamlit_ace import st_ace
import sys
from io import StringIO
import contextlib
from typing import List
import ast

# Configure page settings
st.set_page_config(
    page_title="View Problems",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
/* Global styling */
.main .block-container {
    padding: 1.5rem !important;
    max-width: 1400px;
}
div[data-testid="stToolbar"] {
    display: none;
}
div[data-testid="stDecoration"] {
    display: none;
}
div[data-testid="stStatusWidget"] {
    display: none;
}
/* Progress styling */
.progress-section {
    background: white;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    border: 1px solid #eee;
}
.progress-bar {
    height: 3px;
    background: #eee;
    border-radius: 1.5px;
    margin: 0.5rem 0;
}
.progress-fill {
    height: 100%;
    background: #3178c6;
    border-radius: 1.5px;
}
.progress-stats {
    display: flex;
    gap: 1.5rem;
    font-size: 13px;
}
.stat-easy { color: #00b8a3; }
.stat-medium { color: #ffc01e; }
.stat-hard { color: #ff375f; }
/* Filter styling */
div[data-testid="stSelectbox"] > div {
    background: #f8f9fa !important;
    border: 1px solid #eee !important;
    border-radius: 4px !important;
    min-height: 35px !important;
}
div[data-testid="stSelectbox"] > div:first-child {
    padding: 0 0.5rem !important;
}
div[data-testid="stSelectbox"] label {
    display: none !important;
}
/* Table styling */
div[data-testid="column"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
div[data-testid="column"]:first-child {
    color: #666;
    font-size: 14px;
    font-weight: 500;
}
div[data-testid="column"] button {
    color: #1a73e8;
    font-size: 14px;
    font-weight: 500;
    text-align: left;
    background: none;
    border: none;
    padding: 0;
    width: auto;
    min-width: 0;
}
div[data-testid="column"] button:hover {
    color: #1557b0;
    text-decoration: underline;
}
.problem-link {
    color: #1a73e8;
    text-decoration: none;
}
.difficulty-easy { color: #00b8a3; }
.difficulty-medium { color: #ffc01e; }
.difficulty-hard { color: #ff375f; }
/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    border-right: 1px solid #eee;
}
[data-testid="stSidebar"] button {
    width: 100%;
    text-align: left;
    padding: 0.5rem;
    background: none;
    border: 1px solid #eee;
    border-radius: 4px;
    margin: 0.2rem 0;
    font-size: 13px;
    transition: background-color 0.2s;
}
[data-testid="stSidebar"] button:hover {
    background-color: #e9ecef;
}
/* Search styling */
.search-box {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #eee;
    border-radius: 4px;
    margin-bottom: 1rem;
    font-size: 14px;
}
/* Code editor styling */
.streamlit-ace {
    border: 1px solid #eee;
    border-radius: 4px;
    margin: 1rem 0;
}
/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
}
.stTabs [data-baseweb="tab"] {
    height: 3rem;
    white-space: pre;
    font-size: 1rem;
}
/* Console styling */
[data-testid="stTextArea"] textarea {
    font-family: monospace;
    background: #f8f9fa;
}
/* Button styling */
.stButton button {
    width: 100%;
    margin: 0;
    border-radius: 4px;
    background-color: #f8f9fa;
    color: #333;
    border: 1px solid #dee2e6;
}
/* Split view styling */
[data-testid="column"] {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

def load_problems():
    """Load problems from JSON file"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists('data/problems.json'):
            with open('data/problems.json', 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        st.error(f"Error loading problems: {str(e)}")
        return []

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
                import re
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

# Initialize or load problems
if 'problems' not in st.session_state:
    st.session_state.problems = load_problems()

# Use all problems without filtering
filtered_problems = st.session_state.problems

# Main content area
if 'selected_problem' not in st.session_state:
    # Table header
    header_cols = st.columns([0.1, 0.4, 0.15, 0.15, 0.2])
    header_cols[0].markdown("<p style='color: #666; font-size: 14px; font-weight: 600;'>#</p>", unsafe_allow_html=True)
    header_cols[1].markdown("<p style='color: #666; font-size: 14px; font-weight: 600;'>Title</p>", unsafe_allow_html=True)
    header_cols[2].markdown("<p style='color: #666; font-size: 14px; font-weight: 600;'>Difficulty</p>", unsafe_allow_html=True)
    header_cols[3].markdown("<p style='color: #666; font-size: 14px; font-weight: 600;'>Status</p>", unsafe_allow_html=True)
    header_cols[4].markdown("<p style='color: #666; font-size: 14px; font-weight: 600;'>Frequency</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Table rows
    for problem in filtered_problems:
        cols = st.columns([0.1, 0.4, 0.15, 0.15, 0.2])
        
        # Problem ID
        cols[0].write(problem['id'])
        
        # Title with button
        if cols[1].button(problem['title'], key=f"btn_{problem['id']}"):
            st.session_state.selected_problem = problem
            st.rerun()
        
        # Difficulty with color
        cols[2].markdown(
            f"<span class='difficulty-{problem['difficulty'].lower()}'>{problem['difficulty']}</span>",
            unsafe_allow_html=True
        )
        
        # Status
        status_text = "✅ Solved" if problem.get("solved", False) else "Unsolved"
        cols[3].write(status_text)
        
        # Frequency
        cols[4].write(problem.get('frequency', ''))
        
        st.markdown("---")
else:
    problem = st.session_state.selected_problem
    
    # Back button
    st.markdown("""
        <style>
        div[data-testid="stButton"] button {
            background-color: #f8f9fa;
            color: #333;
            border: 1px solid #dee2e6;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            width: auto;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Problems"):
        del st.session_state.selected_problem
        st.rerun()
    
    # Title and metadata
    st.markdown(f"# {problem['title']}")
    st.markdown(f"**Difficulty:** <span class='difficulty-{problem['difficulty'].lower()}'>{problem['difficulty']}</span> | **Frequency:** {problem.get('frequency', '')}", unsafe_allow_html=True)
    
    # Create two columns for description and code, giving more space to code
    left_col, right_col = st.columns([0.4, 0.6])
    
    with left_col:
        # Description section
        st.markdown("### Description")
        st.write(problem.get('description', 'No description available.'))
        
        # Example section
        if problem.get('example_input'):
            st.markdown("### Example")
            st.markdown("**Input:**")
            st.code(problem['example_input'])
            st.markdown("**Output:**")
            st.code(problem['example_output'])
            if problem.get('example_explanation'):
                st.markdown("**Explanation:**")
                st.write(problem['example_explanation'])
        
        # Constraints section
        if problem.get('constraints'):
            st.markdown("### Constraints")
            for constraint in problem['constraints']:
                st.markdown(f"- {constraint}")
        
        # Tags section
        if problem.get('tags'):
            st.markdown("### Tags")
            st.write(", ".join(problem['tags']))
    
    with right_col:
        # Language selection with python3 as default
        language = st.selectbox(
            "Select Language",
            ["python3", "javascript", "java", "cpp", "typescript"],
            index=0,
            key="language_selector"
        )
        
        # Code editor with larger layout
        if "code" not in st.session_state:
            st.session_state.code = problem.get('solution_template', '')
            
        code = st_ace(
            value=st.session_state.code,
            language=language,
            theme="monokai",
            keybinding="vscode",
            font_size=14,
            tab_size=4,
            show_gutter=True,
            show_print_margin=True,
            wrap=True,
            auto_update=True,
            key="code_editor",
            height=700  # Increased height
        )
    
    # # Test Cases Section
    # st.markdown("""
    #     <style>
    #     .test-header {
    #         background-color: #f8f9fa;
    #         color: #333;
    #         padding: 0.75rem 1rem;
    #         border-radius: 4px 4px 0 0;
    #         margin: 2rem 0 0 0;
    #         border: 1px solid #dee2e6;
    #     }
    #     .test-content {
    #         border: 1px solid #e0e0e0;
    #         border-radius: 0 0 4px 4px;
    #         padding: 1rem;
    #         margin-top: 0;
    #     }
    #     .test-table {
    #         width: 100%;
    #         border-collapse: collapse;
    #     }
    #     .test-table th {
    #         background-color: #f8f9fa;
    #         padding: 0.5rem;
    #         text-align: left;
    #         border-bottom: 2px solid #dee2e6;
    #     }
    #     .test-table td {
    #         padding: 0.5rem;
    #         border-bottom: 1px solid #dee2e6;
    #     }
    #     </style>
    #     <div class="test-header">Test Cases</div>
    #     <div class="test-content">
    # """, unsafe_allow_html=True)
    
    # Initialize test cases in session state if not present
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = {
            'inputs': problem['test_cases']['inputs'].copy(),
            'outputs': problem['test_cases']['outputs'].copy(),
            'results': [''] * len(problem['test_cases']['inputs']),
            'status': [''] * len(problem['test_cases']['inputs'])
        }
    
    st.markdown("### Test Cases")
    
    # Run All Tests button
    if st.button("Run All Tests", type="primary"):
        st.session_state.code = code
        all_passed = True
        
        # Execute all test cases
        for i, (test_input, expected) in enumerate(zip(
            st.session_state.test_cases['inputs'],
            st.session_state.test_cases['outputs']
        )):
            result, stdout, stderr = execute_code(code, test_input)
            st.session_state.test_cases['results'][i] = result if not stderr else "Error"
            if stderr:
                st.session_state.test_cases['status'][i] = "❌"
                all_passed = False
            else:
                if str(result) == expected:
                    st.session_state.test_cases['status'][i] = "✅"
                else:
                    st.session_state.test_cases['status'][i] = "❌"
                    all_passed = False
        
        if all_passed:
            st.success("🎉 All Tests Passed!")
        else:
            st.error("❌ Some Tests Failed")
    
    # Test cases table
    cols = st.columns([0.05, 0.25, 0.25, 0.2, 0.1, 0.15])
    cols[0].markdown("**#**")
    cols[1].markdown("**Input**")
    cols[2].markdown("**Expected**")
    cols[3].markdown("**Result**")
    cols[4].markdown("**Status**")
    cols[5].markdown("**Actions**")
    
    # Temporary test case row
    temp_cols = st.columns([0.05, 0.25, 0.25, 0.2, 0.1, 0.15])
    temp_cols[0].markdown("*temp*")
    temp_input = temp_cols[1].text_input("Input", key="temp_input", placeholder="Enter input")
    temp_expected = temp_cols[2].text_input("Expected", key="temp_expected", placeholder="Enter expected output")
    temp_result = temp_cols[3].empty()
    temp_status = temp_cols[4].empty()
    
    # Test button for temporary test case
    if temp_cols[5].button("Test", key="temp_test"):
        if temp_input:
            result, stdout, stderr = execute_code(code, temp_input)
            temp_result.write(result if not stderr else "Error")
            if stderr:
                temp_status.write("❌")
            else:
                if str(result) == temp_expected:
                    temp_status.write("✅")
                else:
                    temp_status.write("❌")
    
    for i in range(len(st.session_state.test_cases['inputs'])):
        cols = st.columns([0.05, 0.25, 0.25, 0.2, 0.1, 0.15])
        
        # Test case number
        cols[0].write(f"{i + 1}")
        
        # Input field
        new_input = cols[1].text_input(
            "Input",
            value=st.session_state.test_cases['inputs'][i],
            key=f"input_{i}",
            label_visibility="collapsed"
        )
        st.session_state.test_cases['inputs'][i] = new_input
        
        # Expected output field
        new_output = cols[2].text_input(
            "Expected",
            value=st.session_state.test_cases['outputs'][i],
            key=f"output_{i}",
            label_visibility="collapsed"
        )
        st.session_state.test_cases['outputs'][i] = new_output
        
        # Result
        cols[3].write(st.session_state.test_cases['results'][i])
        
        # Status
        cols[4].write(st.session_state.test_cases['status'][i])
        
        # Action buttons
        action_cols = cols[5].columns(2)
        if action_cols[0].button("Test", key=f"test_{i}"):
            result, stdout, stderr = execute_code(code, new_input)
            st.session_state.test_cases['results'][i] = result if not stderr else "Error"
            if stderr:
                st.session_state.test_cases['status'][i] = "❌"
            else:
                if str(result) == new_output:
                    st.session_state.test_cases['status'][i] = "✅"
                else:
                    st.session_state.test_cases['status'][i] = "❌"
            st.rerun()
        
        if action_cols[1].button("🗑", key=f"delete_{i}"):
            st.session_state.test_cases['inputs'].pop(i)
            st.session_state.test_cases['outputs'].pop(i)
            st.session_state.test_cases['results'].pop(i)
            st.session_state.test_cases['status'].pop(i)
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
