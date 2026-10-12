# Jira and Confluence Automation Ideas for Managers

## 1. Weekly Project Health Summary

**Problem it solves:** Managers often spend time gathering updates from multiple
Jira projects and Confluence pages. This automation provides a concise weekly
view of progress, blockers, overdue work, and upcoming milestones.

**Data needed:**
- Jira project and board identifiers
- Issue status, assignee, priority, due date, and labels
- Sprint dates and completion data
- Blocker links and dependencies
- Project milestones and status updates from Confluence

## 2. Blocker and Escalation Alerts

**Problem it solves:** Work can remain blocked without reaching the right
manager or team quickly. This automation detects stalled or blocked issues and
notifies the appropriate owner with context and suggested follow-up.

**Data needed:**
- Jira issue status and status-change history
- Blocker flags, issue links, and comments
- Assignee, team, and escalation contacts
- Time-in-status thresholds and notification preferences

## 3. Decision and Action Item Tracking

**Problem it solves:** Decisions and follow-up actions discussed in meetings
can be missed or become difficult to trace. This automation extracts agreed
actions from meeting notes, creates or updates Jira tasks, and links them to
the relevant Confluence page.

**Data needed:**
- Confluence meeting notes and page identifiers
- Decision and action-item text, owners, and due dates
- Jira project, issue type, and required fields
- Links between Jira issues, projects, and Confluence pages
