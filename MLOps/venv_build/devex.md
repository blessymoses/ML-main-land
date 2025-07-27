# Developer Experience (DevEx) Setup Guide

This guide will help you set up your development environment with Amazon Q, AWS CodeCommit, AWS Toolkit, and EMR extension.

---

## 1. Start with Amazon Q Setup
Ensure the proxy is configured correctly by starting with Amazon Q.

**Documentation:**  
[Amazon Q Setup for VSCode](https://confluence.income.com.sg/display/DATA/Amazon+Q+Set+up+-+VSCode)

---

## 2. AWS CodeCommit Setup
Follow the steps in the CodeCommit documentation:

- [CodeCommit Setup for Windows](https://confluence.income.com.sg/display/DEVOPS/CodeCommit+Setup+for+Windows)  
- [AWS Configurations](https://confluence.income.com.sg/display/DEVOPS/Configurations)

> **Note:** If you're on AVD, Python and Git Bash are pre-installed. Begin from Step 3 in the page above.

By the end of this setup, you will have an AWS config file ready.

---

## 3. AWS Config File & Profiles
Understand the **AWS config file** and how to set up **multiple profiles** for different environments.

---

## 4. AWS Toolkit Extension
Follow this documentation for the AWS Toolkit extension:

[AWS Toolkit Extension Setup](https://confluence.income.com.sg/display/DATA/AWS+Toolkit+Extension)

---

## 5. EMR Extension
Follow this documentation for the EMR extension:

[Amazon EMR Extension Setup](https://confluence.income.com.sg/display/DATA/Amazon+EMR+Extension)

---

## 6. GitLens Inspect
Enable GitLens for inspecting repositories directly in your IDE.

---

## 7. Git Cheatsheet – Top Commands & Best Practices

| Command | Purpose |
|--------|---------|
| `git clone <repo>` | Clone a remote repo to your local machine |
| `git status` | Check the current state of your working directory |
| `git pull` | Fetch and merge changes from the remote branch |
| `git add .` | Stage all modified files for commit |
| `git commit -m "message"` | Commit staged changes with a message |
| `git push origin <branch>` | Push local commits to the remote branch |
| `git checkout <branch>` | Switch to an existing branch |
| `git checkout -b <new-branch>` | Create and switch to a new branch |
| `git log --oneline --graph` | Visualize the commit history as a graph |
| `git stash` / `git stash pop` | Temporarily store and retrieve local changes |

### Best Practices:
- Always `pull` before `push` to avoid conflicts.
- Use clear, descriptive commit messages.
- Use `feature/`, `bugfix/`, or `hotfix/` prefixes for branch names.
- Avoid pushing directly to `main`/`master` unless authorized.
- Review your changes using `git diff` before committing.

---

### **Next Steps**
- Confirm all configurations by testing a sample AWS connection.
- Explore the [GitLens Inspect tool](https://gitlens.amod.io/) for version control insights.

---

**Author:** DevEx Team  
**Last Updated:** July 2025