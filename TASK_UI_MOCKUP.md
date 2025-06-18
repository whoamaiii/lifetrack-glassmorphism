# 🎨 Task Management UI Mockup & Code Examples

## 📱 Visual Layout

### Home Page with Floating Action Button
```
┌─────────────────────────────────────┐
│  👋 Welcome back!                   │
│  Keep up the great work!     🏆1,250│
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │ 📊 Today's Progress         │   │
│  │  🎯 Activities: 5           │   │
│  │  ✅ Tasks: 3/7             │   │
│  │  🔥 Streak: 3 days         │   │
│  └─────────────────────────────┘   │
│                                     │
│  ⚡ Quick Actions                   │
│  [💧 Water] [🏃 Exercise]          │
│  [🍎 Meal]  [😴 Sleep]            │
│                                     │
│  📝 Recent Activities & Tasks       │
│  ┌─────────────────────────────┐   │
│  │ ☑ Buy groceries      2:30pm │   │
│  │ ☐ Call dentist       3:00pm │   │
│  │ 💧 Water - 500ml     1:45pm │   │
│  │ ☑ Morning workout    9:00am │   │
│  └─────────────────────────────┘   │
│                                     │
│                              [➕]    │ ← Floating Action Button
└─────────────────────────────────────┘
```

### Quick Add Modal (After clicking ➕)
```
┌─────────────────────────────────────┐
│                              [➕]    │
│                    ┌───────────────┐ │
│                    │ ✨ Quick Add  │ │
│                    │               │ │
│                    │ [What needs  ]│ │
│                    │ [to be done? ]│ │
│                    │               │ │
│                    │ 📅 Today  🔴  │ │
│                    │               │ │
│                    │ [Add Task]    │ │
│                    └───────────────┘ │
└─────────────────────────────────────┘
```

### Task Edit Modal
```
┌─────────────────────────────────────┐
│  ┌─────────────────────────────┐   │
│  │ ✏️ Edit Task         [✕]    │   │
│  │                             │   │
│  │ Title                       │   │
│  │ [Buy groceries.............]│   │
│  │                             │   │
│  │ Description                 │   │
│  │ [Get milk, eggs, bread     ]│   │
│  │ [and vegetables for dinner ]│   │
│  │                             │   │
│  │ Due Date        Priority    │   │
│  │ [📅 Today 5pm] [🔴 High ▼] │   │
│  │                             │   │
│  │ Category        Points      │   │
│  │ [🛒 Shopping ▼] [15 pts]    │   │
│  │                             │   │
│  │ Tags                        │   │
│  │ [#grocery #weekly]         │   │
│  │                             │   │
│  │ ☑ Recurring Task           │   │
│  │ Pattern: [Weekly ▼]        │   │
│  │                             │   │
│  │ [💾 Save] [❌ Cancel]       │   │
│  │         [🗑️ Delete Task]    │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Task Card with Action Menu
```
┌─────────────────────────────────────┐
│  ☐ Buy groceries                [⋮]│
│    📅 Today 5pm  🏆 15pts           │
│    ┌──────────────┐                 │
│    │ ✏️ Edit      │ ← Action Menu   │
│    │ 📁 Archive   │                 │
│    │ 🗑️ Delete    │                 │
│    │ 📌 Pin       │                 │
│    │ 🔄 Duplicate │                 │
│    └──────────────┘                 │
└─────────────────────────────────────┘
```

### Expanded Task Card (with Description)
```
┌─────────────────────────────────────┐
│  ☐ Buy groceries               [⋮] │
│    📅 Today 5pm  🏆 15pts           │
│  ┌─────────────────────────────┐   │
│  │ Get milk, eggs, bread and    │   │
│  │ vegetables for dinner tonight│   │
│  └─────────────────────────────┘   │
│    #grocery #weekly                 │
└─────────────────────────────────────┘
```

### Tasks Page Layout
```
┌─────────────────────────────────────┐
│  ✅ Tasks                           │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │ 📊 Task Stats               │   │
│  │ Today: 3/7  Week: 15/23    │   │
│  │ Points: 150  Rate: 65%     │   │
│  └─────────────────────────────┘   │
│                                     │
│  🔍 [Search tasks...]               │
│  [All] [Today] [Upcoming] [Done]    │
│  [▼ Priority] [▼ Category] [▼ Tags]│
│                                     │
│  📌 High Priority                   │
│  ┌─────────────────────────────┐   │
│  │ ☐ Finish project report     │   │
│  │   📅 Today 5pm  🏆 50pts    │   │
│  └─────────────────────────────┘   │
│                                     │
│  📋 Today's Tasks                   │
│  ┌─────────────────────────────┐   │
│  │ ☑ Morning meditation        │   │
│  │   ✓ Completed  🏆 20pts     │   │
│  ├─────────────────────────────┤   │
│  │ ☐ Call mom                  │   │
│  │   📅 3pm  🏆 10pts          │   │
│  ├─────────────────────────────┤   │
│  │ ☐ Buy groceries            │   │
│  │   📅 6pm  🏆 15pts          │   │
│  └─────────────────────────────┘   │
│                                     │
│  📂 No tasks due today!             │ ← Empty State
│     [➕ Add your first task]        │
│                                     │
└─────────────────────────────────────┘
[🏠][📊][➕][💬][⚙️] ← Bottom Nav
```

## 💻 Code Examples

### 1. Task Model (task_logic.py)
```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Literal
from enum import Enum
import uuid
import json

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Task:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    points: int = 10
    recurring: dict = field(default_factory=lambda: {
        "enabled": False,
        "pattern": None,
        "next_due": None
    })
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status.value,
            "priority": self.priority.value,
            "category": self.category,
            "tags": self.tags,
            "points": self.points,
            "recurring": self.recurring
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            created_at=datetime.fromisoformat(data["created_at"]),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
            status=TaskStatus(data["status"]),
            priority=TaskPriority(data["priority"]),
            category=data.get("category", "general"),
            tags=data.get("tags", []),
            points=data.get("points", 10),
            recurring=data.get("recurring", {"enabled": False, "pattern": None, "next_due": None})
        )
```

### 2. Task UI Component (streamlit_app.py addition)
```python
def render_task_card(task: Task, expanded: bool = False):
    """Render a glassmorphic task card"""
    with st.container():
        # Apply priority-based styling
        priority_colors = {
            TaskPriority.LOW: "rgba(16, 185, 129, 0.3)",
            TaskPriority.MEDIUM: "rgba(245, 158, 11, 0.3)",
            TaskPriority.HIGH: "rgba(239, 68, 68, 0.3)",
            TaskPriority.URGENT: "rgba(239, 68, 68, 0.5)"
        }
        
        # Create columns for task layout
        col1, col2, col3 = st.columns([0.5, 4, 1])
        
        with col1:
            # Checkbox for completion
            completed = st.checkbox(
                "",
                value=task.status == TaskStatus.COMPLETED,
                key=f"task_check_{task.id}"
            )
            if completed and task.status != TaskStatus.COMPLETED:
                complete_task(task.id)
                st.toast(f"✅ +{task.points} points!", icon="🎉")
                st.balloons()
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
                else:
                    st.rerun()
        
        with col2:
            # Task title and details
            if task.status == TaskStatus.COMPLETED:
                st.markdown(f"~~**{task.title}**~~")
            else:
                # Make title clickable to expand
                if st.button(f"**{task.title}**", key=f"task_title_{task.id}"):
                    st.session_state[f"expanded_{task.id}"] = not st.session_state.get(f"expanded_{task.id}", False)
            
            # Due date and points
            details = []
            if task.due_date:
                due_str = task.due_date.strftime("%b %d, %I:%M %p")
                if task.due_date < datetime.now() and task.status != TaskStatus.COMPLETED:
                    details.append(f"🚨 Overdue: {due_str}")
                else:
                    details.append(f"📅 {due_str}")
            details.append(f"🏆 {task.points} pts")
            st.caption(" • ".join(details))
            
            # Show description if expanded
            if st.session_state.get(f"expanded_{task.id}", False) and task.description:
                st.markdown(f"<div class='task-description'>{task.description}</div>", unsafe_allow_html=True)
                if task.tags:
                    st.caption(" ".join([f"#{tag}" for tag in task.tags]))
        
        with col3:
            # Action menu
            if st.button("⋮", key=f"task_menu_{task.id}"):
                st.session_state[f"show_menu_{task.id}"] = not st.session_state.get(f"show_menu_{task.id}", False)
            
            # Show action menu if toggled
            if st.session_state.get(f"show_menu_{task.id}", False):
                render_task_action_menu(task)

def render_task_action_menu(task: Task):
    """Render the action menu for a task"""
    with st.container():
        st.markdown('<div class="task-action-menu">', unsafe_allow_html=True)
        
        if st.button("✏️ Edit", key=f"edit_{task.id}"):
            st.session_state['editing_task'] = task
            st.session_state['show_edit_modal'] = True
        
        if task.status != TaskStatus.ARCHIVED:
            if st.button("📁 Archive", key=f"archive_{task.id}"):
                archive_task(task.id)
                st.toast("Task archived", icon="📁")
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
                else:
                    st.rerun()
        else:
            if st.button("♻️ Restore", key=f"restore_{task.id}"):
                restore_task(task.id)
                st.toast("Task restored", icon="♻️")
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
                else:
                    st.rerun()
        
        if st.button("🗑️ Delete", key=f"delete_{task.id}"):
            st.session_state[f"confirm_delete_{task.id}"] = True
        
        if st.button("📌 Pin", key=f"pin_{task.id}"):
            pin_task(task.id)
            st.toast("Task pinned", icon="📌")
        
        if st.button("🔄 Duplicate", key=f"duplicate_{task.id}"):
            duplicate_task(task.id)
            st.toast("Task duplicated", icon="🔄")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Delete confirmation
    if st.session_state.get(f"confirm_delete_{task.id}", False):
        st.warning("⚠️ Are you sure you want to permanently delete this task?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, delete", key=f"confirm_yes_{task.id}"):
                delete_task(task.id)
                st.toast("Task deleted", icon="🗑️")
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
                else:
                    st.rerun()
        with col2:
            if st.button("Cancel", key=f"confirm_no_{task.id}"):
                st.session_state[f"confirm_delete_{task.id}"] = False

def render_task_edit_modal():
    """Render the task edit modal"""
    if st.session_state.get('show_edit_modal', False) and st.session_state.get('editing_task'):
        task = st.session_state['editing_task']
        
        st.markdown("""
        <div class="edit-modal-backdrop">
            <div class="edit-modal">
                <h3>✏️ Edit Task</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("edit_task_form"):
            # Title
            title = st.text_input("Title", value=task.title)
            
            # Description
            description = st.text_area("Description", value=task.description, height=100)
            
            # Due date and priority in columns
            col1, col2 = st.columns(2)
            with col1:
                due_date = st.date_input(
                    "Due Date", 
                    value=task.due_date.date() if task.due_date else None
                )
                due_time = st.time_input(
                    "Due Time",
                    value=task.due_date.time() if task.due_date else datetime.now().replace(hour=17, minute=0).time()
                )
            
            with col2:
                priority = st.selectbox(
                    "Priority",
                    options=[p.value for p in TaskPriority],
                    index=[p.value for p in TaskPriority].index(task.priority.value)
                )
                points = st.number_input("Points", value=task.points, min_value=0, step=5)
            
            # Category and tags
            col3, col4 = st.columns(2)
            with col3:
                category = st.selectbox(
                    "Category",
                    options=["general", "work", "personal", "health", "study"],
                    index=["general", "work", "personal", "health", "study"].index(task.category)
                )
            
            with col4:
                tags_str = st.text_input("Tags (comma separated)", value=", ".join(task.tags))
                tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
            
            # Recurring task options
            recurring_enabled = st.checkbox("Recurring Task", value=task.recurring.get("enabled", False))
            if recurring_enabled:
                pattern = st.selectbox(
                    "Repeat Pattern",
                    options=["daily", "weekly", "monthly"],
                    index=["daily", "weekly", "monthly"].index(task.recurring.get("pattern", "weekly"))
                )
            else:
                pattern = None
            
            # Form buttons
            col5, col6, col7 = st.columns([2, 2, 3])
            with col5:
                if st.form_submit_button("💾 Save", type="primary"):
                    # Update task
                    task.title = title
                    task.description = description
                    if due_date and due_time:
                        task.due_date = datetime.combine(due_date, due_time)
                    task.priority = TaskPriority(priority)
                    task.points = points
                    task.category = category
                    task.tags = tags
                    task.recurring = {
                        "enabled": recurring_enabled,
                        "pattern": pattern,
                        "next_due": None
                    }
                    
                    update_task(task)
                    st.session_state['show_edit_modal'] = False
                    st.toast("Task updated!", icon="✅")
                    if hasattr(st, "experimental_rerun"):
                        st.experimental_rerun()
                    else:
                        st.rerun()
            
            with col6:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state['show_edit_modal'] = False
                    if hasattr(st, "experimental_rerun"):
                        st.experimental_rerun()
                    else:
                        st.rerun()
            
            with col7:
                if st.form_submit_button("🗑️ Delete Task", type="secondary"):
                    st.session_state[f"confirm_delete_{task.id}"] = True

def render_quick_add_modal():
    """Render the quick add task modal"""
    st.markdown("""
    <div class="quick-add-modal">
        <h3>✨ Quick Add Task</h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("quick_add_form", clear_on_submit=True):
        # Natural language input
        task_input = st.text_input(
            "What needs to be done?",
            placeholder="e.g., Buy milk tomorrow 5pm !high #shopping",
            label_visibility="collapsed"
        )
        
        # Show parsed preview if input exists
        if task_input:
            parsed_preview = parse_natural_language_task(task_input)
            st.caption(f"📝 Title: {parsed_preview.title}")
            if parsed_preview.due_date:
                st.caption(f"📅 Due: {parsed_preview.due_date.strftime('%b %d, %I:%M %p')}")
            st.caption(f"🎯 Priority: {parsed_preview.priority.value.title()}")
        
        # Quick options
        col1, col2 = st.columns(2)
        with col1:
            due_today = st.checkbox("📅 Due Today")
        with col2:
            high_priority = st.checkbox("🔴 High Priority")
        
        # Submit button
        if st.form_submit_button("Add Task", use_container_width=True):
            if task_input:
                # Parse and create task
                task = parse_natural_language_task(task_input)
                if due_today:
                    task.due_date = datetime.now().replace(hour=17, minute=0)
                if high_priority:
                    task.priority = TaskPriority.HIGH
                
                save_task(task)
                st.session_state["flash"] = f"✅ Task added! +{task.points} points"
                st.session_state["celebrate"] = True
                st.session_state['show_quick_add'] = False
                if hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
                else:
                    st.rerun()
            else:
                st.error("Please enter a task description")

def render_empty_state(section: str):
    """Render empty state messages for different sections"""
    empty_states = {
        "today": {
            "icon": "📋",
            "message": "No tasks due today!",
            "action": "Add your first task for today"
        },
        "overdue": {
            "icon": "✅",
            "message": "Great! No overdue tasks",
            "action": "Keep up the good work!"
        },
        "upcoming": {
            "icon": "📅",
            "message": "No upcoming tasks",
            "action": "Plan ahead by adding future tasks"
        },
        "completed": {
            "icon": "🎯",
            "message": "No completed tasks yet",
            "action": "Complete your first task to see it here"
        },
        "all": {
            "icon": "📝",
            "message": "No tasks yet!",
            "action": "Create your first task to get started"
        }
    }
    
    state = empty_states.get(section, empty_states["all"])
    
    st.markdown(f"""
    <div class="empty-state">
        <h2>{state['icon']}</h2>
        <p>{state['message']}</p>
        <p class="empty-state-action">{state['action']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if section != "completed":
        if st.button("➕ Add Task", key=f"empty_add_{section}"):
            st.session_state['show_quick_add'] = True
```

### 3. Floating Action Button CSS (style.css addition)
```css
/* Floating Action Button */
.floating-add-button {
    position: fixed;
    bottom: 100px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
    z-index: 1000;
}

.floating-add-button:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 30px rgba(102, 126, 234, 0.6);
}

.floating-add-button:active {
    transform: scale(0.95);
}

/* Quick Add Modal */
.quick-add-modal {
    position: fixed;
    bottom: 180px;
    right: 20px;
    width: 350px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    animation: slideIn 0.3s ease;
}

/* Edit Modal */
.edit-modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
}

.edit-modal {
    width: 90%;
    max-width: 500px;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
}

/* Task Action Menu */
.task-action-menu {
    position: absolute;
    right: 0;
    top: 100%;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 0.5rem;
    min-width: 150px;
    box-shadow: 0 4px 20px rgba(31, 38, 135, 0.3);
    z-index: 100;
}

.task-action-menu button {
    display: block;
    width: 100%;
    text-align: left;
    padding: 0.5rem;
    margin: 0.25rem 0;
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    border-radius: 5px;
    transition: background 0.2s ease;
}

.task-action-menu button:hover {
    background: rgba(255, 255, 255, 0.1);
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Task Card Styles */
.task-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1rem;
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.task-card:hover {
    transform: translateX(5px);
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 20px rgba(31, 38, 135, 0.2);
}

.task-card.completed {
    opacity: 0.7;
    background: rgba(255, 255, 255, 0.05);
}

/* Task Description */
.task-description {
    background: rgba(255, 255, 255, 0.05);
    padding: 0.75rem;
    border-radius: 10px;
    margin-top: 0.5rem;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.9rem;
    line-height: 1.5;
}

/* Priority Indicators */
.task-priority-urgent {
    border-left: 4px solid #ef4444;
}

.task-priority-high {
    border-left: 4px solid #f59e0b;
}

.task-priority-medium {
    border-left: 4px solid #3b82f6;
}

.task-priority-low {
    border-left: 4px solid #10b981;
}

/* Empty States */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: rgba(255, 255, 255, 0.7);
}

.empty-state h2 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.empty-state p {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.empty-state-action {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.5);
}

/* Task completion animation */
@keyframes completeTask {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
    100% {
        transform: scale(1);
        opacity: 0.7;
    }
}

.task-completing {
    animation: completeTask 0.5s ease;
}

/* Accessibility improvements */
.task-card:focus-within {
    outline: 2px solid rgba(255, 255, 255, 0.5);
    outline-offset: 2px;
}

button:focus-visible {
    outline: 2px solid rgba(255, 255, 255, 0.5);
    outline-offset: 2px;
}

/* Keyboard navigation helpers */
.task-action-menu button:focus {
    background: rgba(255, 255, 255, 0.2);
}

/* Screen reader only text */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

### 4. Natural Language Parser (task_logic.py addition)
```python
import re
from datetime import datetime, timedelta
from dateutil import parser as date_parser

def parse_natural_language_task(input_text: str) -> Task:
    """
    Parse natural language input into a Task object.
    
    Examples:
    - "Buy milk tomorrow 5pm !high #shopping"
    - "Call dentist next monday urgent"
    - "Finish report by friday @work"
    
    If parsing fails, returns a basic task with the input as title.
    """
    # Start with a basic task
    task = Task(title=input_text.strip())
    
    try:
        # Extract priority (!high, !urgent, etc)
        priority_match = re.search(r'!(\w+)', input_text)
        if priority_match:
            priority_text = priority_match.group(1).lower()
            priority_map = {
                'low': TaskPriority.LOW,
                'medium': TaskPriority.MEDIUM,
                'high': TaskPriority.HIGH,
                'urgent': TaskPriority.URGENT
            }
            task.priority = priority_map.get(priority_text, TaskPriority.MEDIUM)
            input_text = input_text.replace(priority_match.group(0), '')
        
        # Extract tags (#tag)
        tags = re.findall(r'#(\w+)', input_text)
        task.tags = tags
        for tag in tags:
            input_text = input_text.replace(f'#{tag}', '')
        
        # Extract category (@category)
        category_match = re.search(r'@(\w+)', input_text)
        if category_match:
            task.category = category_match.group(1)
            input_text = input_text.replace(category_match.group(0), '')
        
        # Parse due date
        due_date = extract_due_date(input_text)
        if due_date:
            task.due_date = due_date
            # Remove date text from title
            date_patterns = [
                'tomorrow', 'today', 'next week', 'next month',
                'monday', 'tuesday', 'wednesday', 'thursday', 
                'friday', 'saturday', 'sunday',
                r'\d{1,2}[ap]m', r'\d{1,2}:\d{2}',
                r'by\s+\w+', r'on\s+\w+', r'at\s+\w+'
            ]
            for pattern in date_patterns:
                input_text = re.sub(rf'\b{pattern}\b', '', input_text, flags=re.IGNORECASE)
        
        # Clean up the title
        task.title = ' '.join(input_text.split()).strip()
        
        # If title is empty after parsing, use original input
        if not task.title:
            task.title = input_text.strip()
        
        # Assign points based on priority
        points_map = {
            TaskPriority.LOW: 5,
            TaskPriority.MEDIUM: 10,
            TaskPriority.HIGH: 20,
            TaskPriority.URGENT: 30
        }
        task.points = points_map[task.priority]
        
    except Exception as e:
        # If any parsing error occurs, log it and return basic task
        print(f"Error parsing task: {e}")
        # Task already has original input as title
        pass
    
    return task

def extract_due_date(text: str) -> Optional[datetime]:
    """Extract due date from natural language"""
    now = datetime.now()
    
    # Time extraction pattern
    time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*([ap]m)?'
    time_match = re.search(time_pattern, text, re.IGNORECASE)
    
    # Default time (5pm)
    hour = 17
    minute = 0
    
    if time_match:
        hour_str = time_match.group(1)
        minute_str = time_match.group(2) or "0"
        am_pm = time_match.group(3)
        
        hour = int(hour_str)
        minute = int(minute_str)
        
        if am_pm:
            if am_pm.lower() == 'pm' and hour != 12:
                hour += 12
            elif am_pm.lower() == 'am' and hour == 12:
                hour = 0
    
    # Common patterns
    text_lower = text.lower()
    
    if 'today' in text_lower:
        return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    elif 'tomorrow' in text_lower:
        return (now + timedelta(days=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    elif 'next week' in text_lower:
        return (now + timedelta(weeks=1)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # Day of week patterns
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for i, day in enumerate(days):
        if day in text_lower:
            days_ahead = i - now.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return (now + timedelta(days=days_ahead)).replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    # Try to parse with dateutil
    try:
        # Extract potential date strings
        date_match = re.search(r'(by|on|at|until)\s+(.+?)(?:\s+|$)', text, re.IGNORECASE)
        if date_match:
            date_str = date_match.group(2)
            parsed_date = date_parser.parse(date_str, fuzzy=True)
            # If no time was specified in the parse, use our extracted/default time
            if parsed_date.hour == 0 and parsed_date.minute == 0:
                parsed_date = parsed_date.replace(hour=hour, minute=minute)
            return parsed_date
    except:
        pass
    
    return None

def handle_parse_error(input_text: str, error: Exception) -> Task:
    """
    Handle parsing errors gracefully.
    Returns a basic task and logs the error for improvement.
    """
    # Log error for analysis and improvement
    with open("parse_errors.log", "a") as f:
        f.write(f"{datetime.now().isoformat()} - Input: '{input_text}' - Error: {error}\n")
    
    # Return basic task with full input as title
    return Task(
        title=input_text,
        priority=TaskPriority.MEDIUM,
        points=10
    )
```

### 5. Integration with Existing Home Page
```python
# Add to Home page in streamlit_app.py
if selected == "Home":
    # ... existing code ...
    
    # Recent Activities & Tasks Card (modified)
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 📝 Recent Activities & Tasks")
        
        # Load both activities and tasks
        df = load_data()
        tasks = load_tasks(status_filter=[TaskStatus.PENDING, TaskStatus.IN_PROGRESS])
        
        # Combine and sort by time
        combined_items = []
        
        # Add activities
        if df is not None and not df.empty:
            for _, activity in df.tail(3).iterrows():
                combined_items.append({
                    'type': 'activity',
                    'time': activity['timestamp'],
                    'data': activity
                })
        
        # Add tasks
        for task in tasks[:3]:
            combined_items.append({
                'type': 'task',
                'time': task.due_date or task.created_at,
                'data': task
            })
        
        # Sort by time
        combined_items.sort(key=lambda x: x['time'], reverse=True)
        
        # Display combined list
        if combined_items:
            for item in combined_items[:5]:
                if item['type'] == 'activity':
                    activity = item['data']
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{activity['activity']}** - {activity['quantity']} {activity['unit']}")
                    with col2:
                        st.markdown(f"*{activity['timestamp'].strftime('%I:%M %p')}*")
                else:
                    task = item['data']
                    render_task_card(task)
        else:
            render_empty_state("all")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Floating Action Button (always visible)
    if st.button("➕", key="floating_add", help="Quick add task"):
        st.session_state['show_quick_add'] = True
    
    # Quick Add Modal
    if st.session_state.get('show_quick_add', False):
        render_quick_add_modal()
    
    # Edit Modal
    if st.session_state.get('show_edit_modal', False):
        render_task_edit_modal()

# Keyboard shortcut handler (add to every page)
# Note: Streamlit doesn't natively support keyboard shortcuts,
# but you can add this JavaScript component
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    // Ctrl+T or Cmd+T
    if ((e.ctrlKey || e.metaKey) && e.key === 't') {
        e.preventDefault();
        // Trigger the floating add button click
        document.querySelector('[data-testid="stButton"][aria-label="Quick add task"]').click();
    }
    // Escape to close modals
    if (e.key === 'Escape') {
        // Close any open modals
        window.parent.postMessage({type: 'closeModals'}, '*');
    }
});
</script>
""", unsafe_allow_html=True)
```

## 🎯 Key Features Demonstrated

1. **Seamless Integration**: Tasks appear alongside activities
2. **Quick Access**: Floating button on all pages
3. **Smart Parsing**: Natural language understanding with error handling
4. **Visual Feedback**: Completion animations and celebrations
5. **Glassmorphic Design**: Consistent with existing UI
6. **Points System**: Integrated gamification
7. **Priority System**: Visual indicators for urgency
8. **Responsive**: Works on mobile and desktop
9. **Full CRUD**: Create, Read, Update, Delete operations
10. **Archive System**: Soft delete with restore capability
11. **Empty States**: Helpful messages when no tasks exist
12. **Accessibility**: Keyboard navigation and screen reader support

## 🚀 Implementation Notes

- Start with basic task CRUD operations
- Add UI components incrementally
- Test natural language parser thoroughly
- Ensure smooth animations
- Maintain consistent glassmorphic styling
- Keep performance optimal with lazy loading
- Add keyboard shortcuts for power users
- Implement comprehensive error handling
- Test with various screen sizes
- Ensure accessibility compliance

---

*This mockup provides a clear vision of how task management will enhance the LifeTrack experience while maintaining the beautiful glassmorphic aesthetic.* 