# 📘 Smart Academic Milestone Tracker

Smart Academic Milestone Tracker is a web-based application designed to help students manage academic tasks, track deadlines, and monitor progress through a personalized dashboard.

This project provides a centralized platform for students to organize their academic milestones efficiently and visually.

---

## 🎯 Problem Statement

Students often manage academic work using notebooks or generic to-do applications that:
- Lack deadline awareness
- Do not provide progress tracking
- Are not personalized for academic workflows
- Do not offer visual insights into task completion

This makes it difficult for students to plan, prioritize, and track their academic progress effectively.

---

## 💡 Proposed Solution

The Smart Academic Milestone Tracker addresses these challenges by:
- Providing secure student authentication
- Allowing students to add, edit, delete, and complete academic tasks
- Automatically calculating task progress
- Displaying deadline status (Overdue / Due Soon / On Track)
- Visualizing progress using progress bars and statistics

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS

### Backend
- Python
- Flask

### Database
- SQLite

### Tools
- VS Code
- GitHub

---

## 🏗️ System Architecture

The application follows a **Client–Server Architecture**:

- The **client (browser)** handles user interaction.
- The **Flask backend** processes requests, applies business logic, and manages sessions.
- The **SQLite database** stores user and task data.

---

## 🗄️ Database Schema

### Users Table
| Field | Description |
|------|------------|
| id | Primary key |
| name | Student name |
| email | Login email |
| password | User password |

### Tasks Table
| Field | Description |
|------|------------|
| id | Primary key |
| user_id | Foreign key (User) |
| title | Task name |
| deadline | Submission date |
| completed | Task status (0 / 1) |

---

## ✨ Features

- Student registration and login
- Secure session-based authentication
- Add, edit, delete academic tasks
- Mark tasks as completed
- Deadline-based task status
- Progress bar visualization
- Task filtering (All / Completed / Pending)
- Logout functionality

---

## 📂 Project Structure

