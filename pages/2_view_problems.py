import streamlit as st
from streamlit_ace import st_ace
import contextlib
from io import StringIO

# Configure page settings
st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
/* Navigation styling */
.nav-link {
    text-decoration: none;
    color: #666;
    margin-right: 20px;
    padding: 5px 10px;
}
.nav-link.active {
    color: #1a73e8;
    border-bottom: 2px solid #1a73e8;
}
/* Table styling */
.problem-table {
    width: 100%;
    border-collapse: collapse;
}
.problem-table th {
    background: #f8f9fa;
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #dee2e6;
}
.problem-table td {
    padding: 12px;
    border-bottom: 1px solid #dee2e6;
}
.problem-link {
    color: #1a73e8;
    text-decoration: none;
    cursor: pointer;
}
.difficulty-easy { color: #00b8a3; }
.difficulty-medium { color: #ffc01e; }
.difficulty-hard { color: #ff375f; }
.frequency-dot { color: #ffc01e; }
.solved-check { color: #00b8a3; }
/* Problem view styling */
.problem-description {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}
.example-block {
    background: white;
    padding: 15px;
    border-radius: 4px;
    margin: 10px 0;
    border: 1px solid #dee2e6;
}
.code-header {
    background: #f8f9fa;
    padding: 10px;
    border: 1px solid #dee2e6;
    border-bottom: none;
    border-radius: 4px 4px 0 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session states
if "problems" not in st.session_state:
    st.session_state["problems"] = []
if "selected_problem" not in st.session_state:
    st.session_state["selected_problem"] = None

def view_problem_list():
    # Filter row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    with col1:
        difficulty = st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"])
    with col2:
        status = st.selectbox("Status", ["All", "Solved", "Unsolved"])
    with col3:
        tags = st.selectbox("Tags", ["All", "Array", "String", "Binary Search", "Dynamic Programming"])
    with col4:
        search = st.text_input("🔍", placeholder="Search by problem title or id...")

    # Filter problems
    filtered_problems = st.session_state["problems"]
    if difficulty != "All":
        filtered_problems = [p for p in filtered_problems if p["difficulty"] == difficulty]
    if status != "All":
        is_solved = status == "Solved"
        filtered_problems = [p for p in filtered_problems if p.get("solved", False) == is_solved]
    if search:
        search = search.lower()
        filtered_problems = [p for p in filtered_problems if 
                           search in p["title"].lower() or 
                           search in str(p.get("id", "")).lower()]

    # Problems table
    st.markdown("""
    <table class="problem-table">
        <thead>
            <tr>
                <th style="width: 5%">#</th>
                <th style="width: 50%">Problems</th>
                <th style="width: 15%">Level</th>
                <th style="width: 30%">Frequency</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)
    
    for problem in filtered_problems:
        difficulty_class = f"difficulty-{problem['difficulty'].lower()}"
        check = "✓" if problem.get("solved", False) else ""
        
        # Make title clickable
        if st.markdown(f"""
        <tr>
            <td>{check} {problem.get('id', '')}</td>
            <td><a class="problem-link" onclick="handleProblemClick('{problem.get('id', '')}')">{problem['title']}</a></td>
            <td class="{difficulty_class}">{problem['difficulty']}</td>
            <td class="frequency-dot">{problem.get('frequency', '')}</td>
        </tr>
        """, unsafe_allow_html=True):
            st.session_state["selected_problem"] = problem

    st.markdown("</tbody></table>", unsafe_allow_html=True)

def view_problem_detail(problem):
    # Navigation tabs
    st.markdown("""
    <div style="display: flex; gap: 20px; margin-bottom: 20px; border-bottom: 1px solid #dee2e6; padding-bottom: 10px;">
        <a href="#" class="nav-link active">📝 Description</a>
        <a href="#" class="nav-link">💻 Solution</a>
        <a href="#" class="nav-link">📊 Submissions</a>
        <a href="#" class="nav-link">🎥 Video</a>
    </div>
    """, unsafe_allow_html=True)

    # Problem description
    st.markdown(f"""
    <div class="problem-description">
        <h2>{problem.get('id', '')}. {problem['title']} {problem.get('frequency', '')}</h2>
        <p>{problem.get('description', 'No description available.')}</p>
        
        <div class="example-block">
            <strong>Example 1:</strong><br>
            <strong>Input:</strong> {problem.get('example_input', 'N/A')}<br>
            <strong>Output:</strong> {problem.get('example_output', 'N/A')}<br>
            <strong>Explanation:</strong> {problem.get('example_explanation', 'N/A')}
        </div>
        
        <strong>Constraints:</strong>
        <ul>
            {''.join(f'<li>{constraint}</li>' for constraint in problem.get('constraints', ['No constraints specified.']))}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Code editor
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="code-header">', unsafe_allow_html=True)
        st.selectbox("Language", ["Python3"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        solution = st_ace(
            value=problem.get('solution_template', '# Write your solution here'),
            language="python",
            theme="github",
            keybinding="vscode",
            font_size=14,
            tab_size=4,
            show_gutter=True,
            show_print_margin=True,
            wrap=True,
            auto_update=True,
            height=400
        )

    with col2:
        st.markdown("### Test Cases")
        test_input = st.text_area("Test Input", height=100,
                                 value=problem.get('example_input', ''))
        expected_output = st.text_area("Expected Output", height=100,
                                      value=problem.get('example_output', ''))
        
        if st.button("Run Code"):
            if solution.strip():
                # Execute code and show results
                output_buffer = StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    try:
                        exec(solution)
                        st.success("Code executed successfully!")
                        st.code(output_buffer.getvalue())
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

# Main layout
if st.session_state["selected_problem"] is None:
    view_problem_list()
else:
    if st.button("← Back to Problems"):
        st.session_state["selected_problem"] = None
        st.experimental_rerun()
    else:
        view_problem_detail(st.session_state["selected_problem"])

# Right sidebar with companies
with st.sidebar:
    st.markdown("### Companies")
    company_search = st.text_input("🔍", placeholder="Search companies", key="company_search")
    
    companies = [
        ("Google", "683"),
        ("Amazon", "430"),
        ("Microsoft", "509"),
        ("Facebook", "486"),
        ("Apple", "447"),
        ("Bloomberg", "404"),
        ("Adobe", "317"),
        ("Oracle", "223")
    ]
    
    if company_search:
        companies = [(name, count) for name, count in companies 
                    if company_search.lower() in name.lower()]
    
    for company, count in companies:
        st.markdown(f"""
        <div style='background: #f1f1f1; padding: 5px 10px; margin: 5px 0; 
                    border-radius: 15px; display: inline-block; margin-right: 10px;'>
            {company} <span style='background: #e1e1e1; padding: 2px 8px; 
                                 border-radius: 10px;'>{count}</span>
        </div>
        """, unsafe_allow_html=True)
