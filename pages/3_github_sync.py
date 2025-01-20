import streamlit as st
import subprocess

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
