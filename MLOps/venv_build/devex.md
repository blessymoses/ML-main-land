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

# ✅ AWS Config File and Multiple Profiles

---

## 🔹 What is the AWS Config File?

The **AWS config file** (`~/.aws/config`) is used by the AWS CLI and SDKs to manage and switch between **multiple sets of credentials and region settings**. It works in tandem with the **credentials file** (`~/.aws/credentials`) to help you work with different AWS accounts or roles from the same machine.

---

## 📁 AWS Configuration Files

| File        | Path               | Purpose                                                |
|-------------|--------------------|--------------------------------------------------------|
| `config`    | `~/.aws/config`     | Stores profiles with region, output format, etc.       |
| `credentials` | `~/.aws/credentials` | Stores access keys (Access Key ID and Secret Access Key) |

---

## 🔹 Default Profile

When you run an AWS CLI command without specifying a profile, it uses the **default profile**:

```ini
[default]
region = ap-southeast-1
output = json
```

## 🔹 Named Profiles (Multiple Profiles)

You can create additional profiles to manage access to different AWS accounts or roles.

Example: ~/.aws/config

```ini
[default]
region = ap-southeast-1
output = json

[profile dev]
region = ap-southeast-1
output = json

[profile prod]
region = us-west-2
output = yaml
```

## 🔹 How to Use Profiles with AWS CLI
  - Use the --profile flag:
```bash
aws s3 ls --profile dev
```