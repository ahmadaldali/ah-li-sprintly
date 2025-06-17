# AH-LI Sprintly

A Django-based project designed to assist with sprint planning and intelligent issue assignment.

---

## 📦 Repository

You can clone the project from the following repository:

```python
git clone https://github.com/ahmadaldali/ah-li-sprintly
```

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- Django
- Other dependencies in `requirements.txt`

### Setup

```python
# Clone the repository
git clone https://github.com/ahmadaldali/ah-li-sprintly
cd ah-li-sprintly

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the development server
python manage.py runserver
```

---

## 🧠 AI App

### 🔍 Suggest an Assignee

**Endpoint:**
POST /ai/{planning_service}/suggest-assigner/<issue_id>

**Example:**
http://127.0.0.1:8000/ai/jira/suggest-assigner/35231

```python
{
  "assigner": "<name of the most suitable developer>",
  "assigner_id": "<id of the most suitable developer>",
  "issue": "<title of the issue to be assigned>",
  "reason": "<brief explanation of why this developer is a good fit>",
  "story_points": "<The estimated effort for this task>"
}
```

## 📋 Planning App

### 🧾 Get Unassigned Issues in Current Sprint

**Endpoint:**
GET /planning/{planning_service}/unassigned-current-issues

**Example:**
http://127.0.0.1:8000/planning/jira/unassigned-current-issues

```python
[
    {
      "id": "<issue_id>",
      "title": "<issue_title>",
      "description": "<issue_description>",
      "story_points": "<effort_estimate>",
      "epic": "<issue_topic>"
    }
]
```

## ✅  Testing
```python
python3 manage.py test
```

---

## 📫 Contact
For questions or suggestions, feel free to open an issue or submit a pull request.
