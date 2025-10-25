# Microsoft 365 Copilot and Copilot Studio

## 🧠 Overview of M365 Copilot Chat

Microsoft 365 Copilot Chat is an AI-powered assistant integrated within the Microsoft 365 ecosystem.  
It leverages large language models (LLMs) with your organization’s Microsoft Graph data (emails, files, meetings, etc.) to deliver context-aware assistance securely within Word, Excel, Outlook, Teams, and SharePoint.

### ✨ Key Capabilities
- **Integrated experience** — works directly inside Word, Excel, Outlook, and Teams.
- **Graph-connected** — accesses your organizational data (emails, files, calendars, chats).
- **AI-powered productivity** — summarizes documents, drafts emails, generates insights, and automates workflows.
- **Governed & secure** — all data stays within your Microsoft 365 tenant and isn’t used to train public models.

---

## ⚙️ Copilot Studio (Agent Builder)

**Copilot Studio** is Microsoft’s low-code platform to **build and customize your own copilots** for business needs.  
It’s the control center where you define what your Copilot agents can do, what data they can access, and how they respond.

### 🔧 Features
- Build agents for internal workflows (e.g., HR Assistant, IT Helpdesk, Vendor Screening).
- Integrate with Microsoft 365 and external data sources.
- Configure conversational logic (topics, triggers, and actions).
- Extend with plugins, Power Automate, or APIs.
- Manage governance, permissions, and analytics centrally.

---

## 🪄 Steps to Create a New Agent

1. **Access Copilot Studio** via M365 Copilot.
2. **Describe your agent** — specify what it should do (e.g., “Screen companies using ACRA and Bloomberg LEI data”).
3. **Configure knowledge** — connect to data sources (SharePoint, OneDrive, APIs).
4. **Set instructions & tone** — define how the agent answers and behaves.
5. **Test & refine** — run conversations in preview.
6. **Publish** — deploy across Microsoft 365, Teams, or Outlook.

---

## 🌐 Why “All Websites” Does Not Enable Real-Time Web Search

Selecting “All websites” in Copilot Studio **does not grant live web access**.  
This option only allows the Copilot to **reference pre-indexed public web content** from Microsoft’s corpus (historical data), not perform live searches.

### 🚫 What It Means
- No real-time HTTP or API calls.
- No fetching of latest pages or press releases.
- Works only with cached or historical knowledge (e.g., up to Oct 2023).

---

## ✅ How to Enable or Work Around It

| Method | What It Does | Web Access |
|--------|---------------|------------|
| **Bing / Serper / Tavily Plugin** | Adds web search connector | ✅ |
| **Power Automate Flow** | Calls an external search API or endpoint | ✅ |
| **Graph Connectors** | Crawls approved domains (e.g., ACRA, Bloomberg) | 🟡 Partial |
| **Default “All websites”** | Uses cached public content | ❌ |

### Example (Power Automate)
You can define a flow:
1. Triggered by your Copilot.
2. Calls Serper or Tavily API.
3. Returns JSON results to Copilot.
4. Copilot summarizes and cites the sources.

---

## 🧩 Architecture Overview

```text
+------------------------------------------------------+
|                Microsoft 365 Environment             |
|------------------------------------------------------|
| Outlook | Teams | Word | Excel | SharePoint | Chat   |
+--------------------↓---------------------------------+
|             Microsoft 365 Copilot Chat               |
| (LLM + Microsoft Graph + Prompt Orchestration Layer) |
+--------------------↓---------------------------------+
|                Copilot Studio Agents                 |
|  - BSE_Generator                                     |
|  - MyHub                                              |
|  - Custom Flows / API Connectors                      |
+--------------------↓---------------------------------+
|          Data Sources & Integrations                 |
|  - Graph (Emails, Files, Calendar)                   |
|  - SharePoint / Dataverse                            |
|  - External APIs (e.g., ACRA, Bloomberg, Web Search) |
+------------------------------------------------------+