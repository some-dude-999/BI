# Project Development & Documentation Rules

## 🚨 FIRST PRIORITY: DOCUMENTATION CHECK
**BEFORE doing ANYTHING else:**
1. Check if documentation exists for the project/files you're working with
2. **IF NO DOCUMENTATION EXISTS → CREATE IT IMMEDIATELY**
3. Analyze the existing code to understand:
   - Data structures and flow
   - Program objectives and functionality
   - API endpoints and data sources
   - User interactions and outputs
4. Create comprehensive documentation BEFORE making any changes

### For New LLMs Joining a Project
**Your first task is ALWAYS:**
1. Read all existing documentation files
2. Quickly analyze the codebase to understand the system architecture
3. Map out the data flow and program objectives
4. If documentation is missing or incomplete, create/update it first
5. Only then proceed with requested tasks

## 📝 MANDATORY DOCUMENTATION SYSTEM
**Every HTML file MUST have a corresponding .txt documentation file**

### Documentation Naming Convention
- HTML file: `Some Program.html` → Documentation: `Some Program.txt`
- HTML file: `dashboard.html` → Documentation: `dashboard.txt`
- Documentation must be in the same directory as its HTML file

### Documentation Contents (Required)
Each .txt file MUST include:
1. **PROJECT OVERVIEW** - What this component does and its purpose
2. **DATA SOURCES** - Where all data comes from (APIs, files, databases, user input)
3. **SCRIPT FUNCTIONALITY** - How the HTML/JavaScript works, key functions explained
4. **DEPENDENCIES** - External libraries, APIs, or other files this depends on
5. **LAST UPDATED** - Date and what changed
6. **INTEGRATION NOTES** - How this connects with other project components

### Update Protocol
**CRITICAL: Update documentation EVERY time you:**
- Create a new HTML file
- Modify existing functionality
- Add new data sources
- Change API endpoints
- Integrate new features
- Fix bugs or issues
- **DISCOVER YOUR INITIAL UNDERSTANDING WAS INCORRECT**

### Documentation Accuracy Rule
**If your understanding of the project turns out to be incorrect:**
1. IMMEDIATELY update the documentation with the correct information
2. Note what was misunderstood and why (helps future LLMs avoid same mistake)
3. Ensure documentation is maximally accurate and helpful for future versions
4. Think of documentation as a message to your future self - be thorough!

**Remember: Bad documentation = confused future LLMs = broken projects**

**This documentation is essential for future LLMs to understand and continue the project as it grows in complexity.**

---

## 🔄 Git Rules
**If it's not on main branch, it FAILED.**

### Commit Requirements
- Always commit and push immediately after any code change
- Always work directly on main branch
- Only branch if GitHub technically requires it, then immediately merge to main
- Verify changes are on main before considering task complete

### Verification Steps
1. Make changes
2. Update corresponding .txt documentation
3. Git add, commit, push
4. Verify on GitHub that changes appear on main
5. Update LINK.txt if HTML files were created/modified

**MANDATORY: End every response with a link to create the pull request for the changes just made. No link = task not done.**

---

## 🔗 HTML File Tracking (LINK.txt)
**After each run, check LINK.txt:**
- If any .html file was created/modified and not in LINK.txt, add it
- If the path changed, update it
- If already listed, leave it alone
- Applies to ALL .html files in any folder

### LINK.txt Format
```
path/to/file.html - Brief description
another/path/page.html - What this page does
```

---

## ⚠️ Remember
1. **NO DOCUMENTATION = STOP! Create it first before ANY other work**
2. **Not on main = useless code**
3. **Incorrect understanding = update documentation immediately**
4. **Every change needs:**
   - Documentation check/update FIRST
   - Code update
   - Documentation update (if understanding changed)
   - Git push to main
   - LINK.txt update (if HTML)
   - Pull request link in response
5. **Documentation is a message to your future self - make it count!**

## Documentation Template Example
```text
=== [Component Name].txt ===
PROJECT: [Project Name]
COMPONENT: [This Component's Purpose]
CREATED: [Date]
LAST UPDATED: [Date] - [What Changed]

DATA SOURCES:
- API: [endpoint URL] - [what data it provides]
- File: [filename] - [what data it contains]
- User Input: [form fields] - [what users provide]

FUNCTIONALITY:
- Main Purpose: [What this does]
- Key Functions:
  * functionName() - [what it does]
  * anotherFunction() - [its purpose]
- Event Handlers: [user interactions handled]

DEPENDENCIES:
- External Libraries: [library names and versions]
- Project Files: [other files this needs]
- APIs Required: [external services]

INTEGRATION:
- Receives data from: [other components]
- Sends data to: [other components]
- Triggers: [what causes this to run]

CORRECTIONS & CLARIFICATIONS:
[Document any initial misunderstandings that were corrected]
- Initially thought: [wrong assumption]
- Actually: [correct understanding]
- Why this matters: [impact on functionality]

NOTES:
[Any special considerations, known issues, or future improvements needed]
[Tips for future LLMs working on this]
===
```

## 🧠 Documentation Philosophy
**Think of documentation as a conversation with your future self:**
- What would you want to know if you saw this code for the first time?
- What mistakes might you make without proper context?
- What's the quickest path to understanding the entire system?
- Document not just WHAT the code does, but WHY it does it that way

This documentation system ensures that as projects grow, any new LLM can quickly understand the entire codebase, data flow, and system architecture.
