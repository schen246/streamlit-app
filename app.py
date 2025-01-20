import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="SCode",
    page_icon="📚",
    layout="wide"
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
/* Header styling */
.header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem 0;
    margin-bottom: 1.5rem;
}
.logo {
    font-size: 20px;
    font-weight: 600;
    color: #333;
}
.search-box {
    flex-grow: 1;
    padding: 0.5rem 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    font-size: 14px;
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
.problem-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
.problem-table th {
    background: #fafafa;
    padding: 0.6rem 0.75rem;
    text-align: left;
    border-bottom: 1px solid #eee;
    font-weight: 500;
    color: #666;
}
.problem-table td {
    padding: 0.6rem 0.75rem;
    border-bottom: 1px solid #eee;
}
.problem-link {
    color: #1a73e8;
    text-decoration: none;
}
.difficulty-easy { color: #00b8a3; }
.difficulty-medium { color: #ffc01e; }
.difficulty-hard { color: #ff375f; }
/* Company styling */
.companies-section {
    background: white;
    padding: 1rem;
    border-radius: 4px;
    border: 1px solid #eee;
}
.company-search {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    margin-bottom: 1rem;
    font-size: 14px;
}
.company-tag {
    display: inline-flex;
    align-items: center;
    background: #f5f5f5;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    margin: 0.25rem;
    font-size: 13px;
}
.company-count {
    background: #e8e8e8;
    padding: 0.1rem 0.5rem;
    border-radius: 8px;
    margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <span class="logo">SCode</span>
    <input type="text" class="search-box" placeholder="🔍 Search problems by title, tag, or company...">
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([3, 1])

with col1:
    # Progress section
    st.markdown("""
    <div class="progress-section">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>Progress</span>
            <span>317/986 problems solved</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: 32%;"></div>
        </div>
        <div class="progress-stats">
            <span class="stat-easy">Easy 63/174</span>
            <span class="stat-medium">Medium 204/592</span>
            <span class="stat-hard">Hard 50/220</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Difficulty", ["All", "Easy", "Medium", "Hard"], label_visibility="collapsed")
    with col2:
        st.selectbox("Status", ["All", "Solved", "Unsolved"], label_visibility="collapsed")
    with col3:
        st.selectbox("Tags", ["All", "Array", "String", "Dynamic Programming"], label_visibility="collapsed")

    # Problems table
    st.markdown("""
    <table class="problem-table">
        <thead>
            <tr>
                <th style="width: 5%">#</th>
                <th style="width: 60%">Title</th>
                <th style="width: 15%">Difficulty</th>
                <th style="width: 20%">Frequency</th>
            </tr>
        </thead>
        <tbody>
    """, unsafe_allow_html=True)
    
    # Sample problems
    problems = [
        {"id": "✓1", "title": "Binary Search", "difficulty": "Easy", "frequency": "⭐⭐⭐"},
        {"id": "2", "title": "Two Sum", "difficulty": "Medium", "frequency": "⭐⭐⭐⭐⭐"},
        {"id": "✓3", "title": "Design Hit Counter", "difficulty": "Medium", "frequency": "⭐⭐⭐⭐"}
    ]
    
    for problem in problems:
        difficulty_class = f"difficulty-{problem['difficulty'].lower()}"
        st.markdown(f"""
        <tr>
            <td>{problem['id']}</td>
            <td><a href="#" class="problem-link">{problem['title']}</a></td>
            <td class="{difficulty_class}">{problem['difficulty']}</td>
            <td>{problem['frequency']}</td>
        </tr>
        """, unsafe_allow_html=True)
    
    st.markdown("</tbody></table>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="companies-section">
        <h3 style="margin-top: 0; margin-bottom: 1rem; font-size: 16px;">Companies</h3>
        <input type="text" class="company-search" placeholder="🔍 Search companies">
        <div>
    """, unsafe_allow_html=True)
    
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
    
    for company, count in companies:
        st.markdown(f"""
        <span class="company-tag">
            {company}<span class="company-count">{count}</span>
        </span>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
