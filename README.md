# LeetCode Learning Tracker

A Streamlit application to help track and document your LeetCode problem-solving journey. The app allows you to save your solutions and automatically sync them to GitHub.

## Features

- Add solved LeetCode problems with descriptions and solutions
- Categorize problems by difficulty (Easy, Medium, Hard)
- Add tags to problems for better organization
- Filter problems by difficulty and search by title/tags
- Automatic GitHub synchronization
- Track your progress over time

## Setup Instructions

1. Install the required dependencies:
```bash
python3 -m pip install streamlit
```

2. Create a new repository on GitHub for your LeetCode solutions

3. Clone your repository and copy these files into it, or initialize git in this directory:
```bash
git init
git remote add origin YOUR_REPOSITORY_URL
```

4. Run the Streamlit app:
```bash
python3 -m streamlit run app.py
```

## Using the App

1. **Add a Problem**
   - Click "Add Problem" in the sidebar
   - Enter the problem title, difficulty, description, and your solution
   - Add relevant tags (comma-separated)
   - Click "Add Problem" to save and sync to GitHub

2. **View Problems**
   - Click "View Problems" in the sidebar
   - Filter problems by difficulty
   - Search problems by title or tags
   - Click on any problem to expand and view details

3. **GitHub Sync**
   - Click "GitHub Sync" in the sidebar
   - Check repository status
   - Manually sync all solutions if needed
   - View setup instructions

## Directory Structure

- `/solutions`: Contains individual Python files for each solution
- `app.py`: Main Streamlit application file
