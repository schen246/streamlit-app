import streamlit as st
import json
import os

# Configure page settings
st.set_page_config(
    page_title="LeetCode Practice",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for consistent styling across pages
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
/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    border-right: 1px solid #eee;
}
/* Button styling */
.stButton button {
    background-color: #1a73e8;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}
/* Input field styling */
.stTextInput input, .stTextArea textarea {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
}
/* Card styling */
.css-card {
    border-radius: 8px;
    padding: 1rem;
    background-color: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}
/* Difficulty colors */
.difficulty-easy { color: #00b8a3; }
.difficulty-medium { color: #ffc01e; }
.difficulty-hard { color: #ff375f; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'problems' not in st.session_state:
    # Load problems from JSON file
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        if os.path.exists('data/problems.json'):
            with open('data/problems.json', 'r') as f:
                st.session_state.problems = json.load(f)
        else:
            st.session_state.problems = []
    except Exception as e:
        st.error(f"Error loading problems: {str(e)}")
        st.session_state.problems = []

# Main page content
st.title("LeetCode Practice")

# Display quick stats in cards using columns
col1, col2, col3, col4 = st.columns(4)

total_problems = len(st.session_state.problems)
solved_problems = len([p for p in st.session_state.problems if p.get("solved", False)])
easy_problems = len([p for p in st.session_state.problems if p["difficulty"] == "Easy"])
medium_problems = len([p for p in st.session_state.problems if p["difficulty"] == "Medium"])
hard_problems = len([p for p in st.session_state.problems if p["difficulty"] == "Hard"])

with col1:
    st.markdown("""
    <div class="css-card">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem;">Total Problems</h3>
        <p style="font-size: 1.5rem; font-weight: bold; margin: 0;">{}</p>
    </div>
    """.format(total_problems), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="css-card">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem;">Problems Solved</h3>
        <p style="font-size: 1.5rem; font-weight: bold; margin: 0;">{} ({}%)</p>
    </div>
    """.format(solved_problems, int(solved_problems/total_problems*100) if total_problems > 0 else 0), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="css-card">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem;">Difficulty Distribution</h3>
        <p style="font-size: 1rem; margin: 0;">
            <span class="difficulty-easy">Easy: {}</span> • 
            <span class="difficulty-medium">Medium: {}</span> • 
            <span class="difficulty-hard">Hard: {}</span>
        </p>
    </div>
    """.format(easy_problems, medium_problems, hard_problems), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="css-card">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1rem;">Recent Activity</h3>
        <p style="font-size: 1rem; margin: 0;">Last 7 days: {} solved</p>
    </div>
    """.format(len([p for p in st.session_state.problems if p.get("solved", False) and 
                   p.get("solved_date", "").startswith("2024")])), unsafe_allow_html=True)

# Recent problems section
st.markdown("### Recent Problems")
recent_problems = sorted(
    st.session_state.problems,
    key=lambda x: x.get("date_added", ""),
    reverse=True
)[:5]

for problem in recent_problems:
    difficulty_class = f"difficulty-{problem['difficulty'].lower()}"
    st.markdown(f"""
    <div class="css-card" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h4 style="margin: 0; font-size: 1rem;">{problem['title']}</h4>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.875rem; color: #666;">
                Added {problem.get('date_added', 'N/A')}
            </p>
        </div>
        <span class="{difficulty_class}">{problem['difficulty']}</span>
    </div>
    """, unsafe_allow_html=True)

# Quick actions
st.markdown("### Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add New Problem"):
        st.switch_page("pages/1_add_problem.py")
with col2:
    if st.button("📚 View All Problems"):
        st.switch_page("pages/2_view_problems.py")
with col3:
    if st.button("🔄 Sync with GitHub"):
        st.switch_page("pages/3_github_sync.py")
