import streamlit as st
from streamlit_option_menu import option_menu
from logic import log_activity, load_data, get_ai_chat_response, set_api_key, get_api_key, add_task, load_tasks, update_task_status, delete_task
import logic # Ensure logic is imported for other functions like get_available_activities etc.
import pandas as pd
from datetime import datetime, timedelta # Added timedelta

# Helper to log activity and refresh data

def log_and_refresh(activity_desc: str, success_text: str = "✅ Logged!"):
    """Logs the activity, shows a success notification, then refreshes the app
    so that components relying on the dataset (e.g. Recent Activities) update
    immediately.
    """
    try:
        log_activity(activity_desc)
        # Store flash + celebration flag to display after rerun
        st.session_state["flash"] = success_text
        st.session_state["celebrate"] = True
        # Trigger UI refresh
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        elif hasattr(st, "rerun"):
            st.rerun()
    except Exception as e:
        st.error(f"Failed to log activity: {e}")

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LifeTrack",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- 2. LOAD CUSTOM CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# --- Flash message handling ---
if "flash" in st.session_state:
    st.toast(st.session_state.pop("flash"), icon="🎉")

# Show balloons animation if flagged (set before rerun)
if st.session_state.pop("celebrate", False):
    st.balloons()

# --- 3. INJECT CUSTOM HTML FOR BOTTOM NAV ---
# Since streamlit-option-menu doesn't properly support fixed positioning,
# we'll create our own navigation
st.markdown("""
<div class="bottom-nav-wrapper">
    <div class="bottom-nav-container">
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. NAVIGATION LOGIC ---
# Use streamlit-option-menu but style it to appear at bottom
selected = option_menu(
    menu_title=None,
    options=["Home", "Analysis", "Log", "Tasks", "Chat", "Settings"],
    icons=["house-fill", "bar-chart-fill", "plus-circle-fill", "check2-square", "chat-dots-fill", "gear-fill"],
    default_index=0,
    orientation="horizontal",
    key="navigation",
    styles={
        "container": {"padding": "0", "background-color": "transparent"},
        "icon": {"color": "white", "font-size": "22px"},
        "nav-link": {
            "color": "rgba(255, 255, 255, 0.8)",
            "font-size": "13px",
            "text-align": "center",
            "margin": "0px",
            "padding": "12px 16px",
            "border-radius": "12px",
        },
        "nav-link-selected": {
            "background-color": "rgba(255, 255, 255, 0.25)",
            "color": "white",
            "font-weight": "600",
        },
    }
)

# --- 5. PAGE CONTENT ---
if selected == "Home":
    # User Profile Section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 👋 Welcome back!")
        st.markdown("### Keep up the great work!")
    with col2:
        st.markdown("""
        <div style='text-align: right; padding: 10px;'>
            <h2>🏆 1,250</h2>
            <p style='margin: 0; color: rgba(255,255,255,0.8);'>Points</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Load data
    df = load_data()

    # Dashboard Stats Card
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 📊 Today's Progress")
        
        if df is not None and not df.empty:
            today_df = df[df['timestamp'].dt.date == datetime.today().date()]
            
            # Progress metrics with better styling
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h3>🎯 Activities</h3>
                    <h1>{}</h1>
                    <p>Today</p>
                </div>
                """.format(len(today_df)), unsafe_allow_html=True)
            
            with col2:
                # Calculate activities for the current week
                today = datetime.now().date()
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)

                this_week_df = df[(df['timestamp'].dt.date >= start_of_week) & (df['timestamp'].dt.date <= end_of_week)]
                st.markdown("""
                <div class="metric-card">
                    <h3>📈 Activities</h3>
                    <h1>{}</h1>
                    <p>This Week</p>
                </div>
                """.format(len(this_week_df)), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <h3>🔥 Streak</h3>
                    <h1>3</h1>
                    <p>Days</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🚀 Start tracking to see your progress!")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Quick Actions Section
    st.markdown("## ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            if st.button("💧 Log Water", use_container_width=True, key="home_water"):
                log_and_refresh("Drank a glass of water")
            
            if st.button("🏃 Add Exercise", use_container_width=True, key="home_exercise"):
                log_and_refresh("Completed workout session")
            
            if st.button("🍎 Track Meal", use_container_width=True, key="home_meal"):
                log_and_refresh("Had a healthy meal")
    
    with col2:
        with st.container():
            if st.button("😴 Log Sleep", use_container_width=True, key="home_sleep"):
                log_and_refresh("Got good sleep")
            
            if st.button("🧘 Add Meditation", use_container_width=True, key="home_meditation"):
                log_and_refresh("Meditated for 10 minutes")
            
            if st.button("📚 Track Study", use_container_width=True, key="home_study"):
                log_and_refresh("Studied for 30 minutes")

    # Recent Activities Card
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 📝 Recent Activities")
        
        if df is not None and not df.empty:
            recent = df.tail(5).iloc[::-1]  # Show last 5 activities
            for idx, activity in recent.iterrows():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{activity['activity']}**")
                with col2:
                    st.markdown(f"*{activity['timestamp'].strftime('%I:%M %p')}*")
                if idx < len(recent) - 1:
                    st.markdown("---")
        else:
            st.info("No activities yet. Start tracking above!")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Analysis":
    st.markdown("# 📊 Analytics")
    
    # Load data
    df = load_data()

    # Stats Overview
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 📈 Your Statistics")
        
        if df is not None and not df.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Activities", len(df), "+12%")
            with col2:
                st.metric("Active Days", df['timestamp'].dt.date.nunique(), "+3")
            with col3:
                st.metric("Best Streak", "7 days", "🔥") # Placeholder
            with col4:
                st.metric("Points Earned", "1,250", "+150") # Placeholder
        else:
            st.info("No data to analyze yet. Start tracking your activities!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts section
    if df is not None and not df.empty:
        # Totals chart
        with st.container():
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("### Total Quantities by Activity")
            totals_chart_data = logic.create_totals_chart_data(df)
            if totals_chart_data is not None and not totals_chart_data.empty:
                st.bar_chart(totals_chart_data)
            else:
                st.write("No data for totals chart.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Timeline chart
        with st.container():
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("### Activity Timeline")

            available_activities = logic.get_available_activities(df)
            if available_activities:
                selected_activity = st.selectbox(
                    "Select an activity:",
                    options=available_activities,
                    key="analysis_activity_select"
                )

                if selected_activity:
                    timeline_chart_data = logic.create_timeline_chart_data(df, selected_activity)
                    if timeline_chart_data is not None and not timeline_chart_data.empty:
                        st.line_chart(timeline_chart_data)
                    else:
                        st.write(f"No timeline data for {selected_activity}.")
            else:
                st.write("No activities available for timeline chart.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif df is None or df.empty: # Keep this condition to ensure the message shows if there's no data at all
        with st.container():
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown("## 📊 Activity Trends")
            st.info("No data to analyze yet. Start tracking your activities to see your trends!")
            st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Log":
    st.markdown("# ✍️ Quick Log")
    
    # Main logging form
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### 💭 What did you do?")
        
        with st.form(key="log_form", clear_on_submit=True):
            user_input = st.text_area(
                "Describe your activity",
                placeholder="e.g., Drank 2 glasses of water, walked for 30 minutes...",
                height=100,
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                submitted = st.form_submit_button(
                    "✨ Analyze & Save", 
                    use_container_width=True,
                    type="primary"
                )
            with col2:
                st.markdown("**+50** points", unsafe_allow_html=True)
            
            if submitted and user_input:
                log_and_refresh(user_input)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Quick action grid
    st.markdown("### ⚡ Quick Actions")
    
    # First row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💧 Water\n+10 pts", use_container_width=True, key="log_water"):
            log_and_refresh("Drank a glass of water")
    
    with col2:
        if st.button("🏃 Exercise\n+25 pts", use_container_width=True, key="log_exercise"):
            log_and_refresh("Completed exercise")
    
    with col3:
        if st.button("🧘 Meditate\n+15 pts", use_container_width=True, key="log_meditate"):
            log_and_refresh("Meditated")
    
    # Second row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍎 Healthy Meal\n+20 pts", use_container_width=True, key="log_meal"):
            log_and_refresh("Ate healthy meal")
    
    with col2:
        if st.button("📚 Study\n+30 pts", use_container_width=True, key="log_study"):
            log_and_refresh("Study session")
    
    with col3:
        if st.button("😴 Good Sleep\n+25 pts", use_container_width=True, key="log_sleep"):
            log_and_refresh("Got good sleep")
    
    # Quick Add Task section
    st.markdown("---")  # Separator
    st.markdown('<div class="glass-panel" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown("### ➕ Quick Add Task")
    
    with st.form(key="quick_add_task_form", clear_on_submit=True):
        new_task_description = st.text_input(
            "Enter new task description:", 
            key="new_task_input_field",
            placeholder="e.g., Buy groceries, Finish report", 
            label_visibility="collapsed"
        )
        
        add_task_button = st.form_submit_button("✨ Add Task to List", type="primary", use_container_width=True)
        
        if add_task_button:
            if new_task_description.strip():  # Check if not just whitespace
                try:
                    logic.add_task(new_task_description.strip())
                    st.session_state["flash"] = "✅ Task added successfully!"
                    # Rerun to clear form and update any dependent UI if needed
                    if hasattr(st, "rerun"):
                        st.rerun()
                    else:
                        st.experimental_rerun()
                except ValueError as e:
                    st.error(f"❌ Invalid input: {e}")
                except IOError as e:
                    st.error(f"❌ Could not save task: {e}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
            else:
                st.warning("⚠️ Please enter a task description.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Chat":
    st.markdown("# 💬 AI Assistant")

    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 🤖 Your Personal Health Coach")
        # Removed "Ask me anything..." as the chat interface implies this.

        st.markdown("#### Configure AI Response")
        
        # Sliders for temperature and max_tokens
        # Initialize with session_state.get to preserve values across reruns
        # Default to 0.7 for temperature and 250 for max_tokens if not in session_state
        temperature_slider = st.slider(
            "Temperature (Creativity)",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get('chat_temperature', 0.7),
            step=0.05,
            help="Lower values are more deterministic, higher values are more creative."
        )
        max_tokens_slider = st.slider(
            "Max Tokens (Response Length)",
            min_value=50,
            max_value=1000,
            value=st.session_state.get('chat_max_tokens', 250),
            step=50,
            help="Maximum number of tokens in the AI's response."
        )

        # Store current slider values in session state to persist them
        st.session_state.chat_temperature = temperature_slider
        st.session_state.chat_max_tokens = max_tokens_slider

        st.markdown("---") # Visual separator

        # Initialize chat history in session state if it doesn't exist
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display prior chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if user_input := st.chat_input("How can I help you stay healthy today?", key="chat_input"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Display user message immediately
            with st.chat_message("user"):
                st.write(user_input)

            # Get AI response using slider values from session state
            try:
                # Show a thinking indicator while waiting for AI
                with st.spinner("Thinking..."):
                    ai_response = get_ai_chat_response(
                        user_input,
                        temperature=st.session_state.chat_temperature,
                        max_tokens=st.session_state.chat_max_tokens
                    )

                if ai_response.startswith("Error:"):
                    st.error(ai_response)
                    # Optionally remove the last user message if AI fails, or keep it to show context of error
                    # For now, let's keep it. If AI fails, we add an error message to the chat.
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})

                # Rerun to update the chat display with the new AI message (or error)
                st.rerun()

            except ValueError as ve: # Catch API key validation errors from logic.py
                st.error(str(ve))
                # Add error to chat display
                st.session_state.messages.append({"role": "assistant", "content": str(ve)})
                st.rerun()
            except Exception as e: # Catch any other unexpected errors
                st.error(f"An unexpected error occurred: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"An unexpected error occurred: {e}"})
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Log":
    st.markdown("# ✍️ Quick Log")

    # Main logging form
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("### 💭 What did you do?")

        with st.form(key="log_form", clear_on_submit=True):
            user_input = st.text_area(
                "Describe your activity",
                placeholder="e.g., Drank 2 glasses of water, walked for 30 minutes...",
                height=100,
                label_visibility="collapsed"
            )

            col1, col2 = st.columns([3, 1])
            with col1:
                submitted = st.form_submit_button(
                    "✨ Analyze & Save",
                    use_container_width=True,
                    type="primary"
                )
            with col2:
                st.markdown("**+50** points", unsafe_allow_html=True)

            if submitted and user_input:
                log_and_refresh(user_input)

        st.markdown('</div>', unsafe_allow_html=True)

    # Quick action grid
    st.markdown("### ⚡ Quick Actions")

    # First row
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💧 Water\n+10 pts", use_container_width=True, key="log_water"):
            log_and_refresh("Drank a glass of water")

    with col2:
        if st.button("🏃 Exercise\n+25 pts", use_container_width=True, key="log_exercise"):
            log_and_refresh("Completed exercise")

    with col3:
        if st.button("🧘 Meditate\n+15 pts", use_container_width=True, key="log_meditate"):
            log_and_refresh("Meditated")

    # Second row
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🍎 Healthy Meal\n+20 pts", use_container_width=True, key="log_meal"):
            log_and_refresh("Ate healthy meal")

    with col2:
        if st.button("📚 Study\n+30 pts", use_container_width=True, key="log_study"):
            log_and_refresh("Study session")

    with col3:
        if st.button("😴 Good Sleep\n+25 pts", use_container_width=True, key="log_sleep"):
            log_and_refresh("Got good sleep")
    
    # Quick Add Task section
    st.markdown("---")  # Separator
    st.markdown('<div class="glass-panel" style="margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown("### ➕ Quick Add Task")

    with st.form(key="quick_add_task_form", clear_on_submit=True):
        new_task_description = st.text_input(
            "Enter new task description:",
            key="new_task_input_field_log_page", # Ensure unique key
            placeholder="e.g., Buy groceries, Finish report",
            label_visibility="collapsed"
        )

        add_task_button = st.form_submit_button("✨ Add Task to List", type="primary", use_container_width=True)

        if add_task_button:
            if new_task_description.strip():  # Check if not just whitespace
                try:
                    # Updated to pass None for due_date and priority
                    logic.add_task(description=new_task_description.strip(), due_date=None, priority=None)
                    st.session_state["flash"] = "✅ Task added successfully!"
                    if hasattr(st, "rerun"): st.rerun()
                    else: st.experimental_rerun()
                except ValueError as e:
                    st.error(f"❌ Invalid input: {e}")
                except IOError as e:
                    st.error(f"❌ Could not save task: {e}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {e}")
            else:
                st.warning("⚠️ Please enter a task description.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Chat":
    st.markdown("# 💬 AI Assistant")

    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 🤖 Your Personal Health Coach")
        # Removed "Ask me anything..." as the chat interface implies this.

        st.markdown("#### Configure AI Response")

        # Sliders for temperature and max_tokens
        # Initialize with session_state.get to preserve values across reruns
        # Default to 0.7 for temperature and 250 for max_tokens if not in session_state
        temperature_slider = st.slider(
            "Temperature (Creativity)",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.get('chat_temperature', 0.7),
            step=0.05,
            help="Lower values are more deterministic, higher values are more creative."
        )
        max_tokens_slider = st.slider(
            "Max Tokens (Response Length)",
            min_value=50,
            max_value=1000,
            value=st.session_state.get('chat_max_tokens', 250),
            step=50,
            help="Maximum number of tokens in the AI's response."
        )

        # Store current slider values in session state to persist them
        st.session_state.chat_temperature = temperature_slider
        st.session_state.chat_max_tokens = max_tokens_slider

        st.markdown("---") # Visual separator

        # Initialize chat history in session state if it doesn't exist
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display prior chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if user_input := st.chat_input("How can I help you stay healthy today?", key="chat_input"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Display user message immediately
            with st.chat_message("user"):
                st.write(user_input)

            # Get AI response using slider values from session state
            try:
                # Show a thinking indicator while waiting for AI
                with st.spinner("Thinking..."):
                    ai_response = get_ai_chat_response(
                        user_input,
                        temperature=st.session_state.chat_temperature,
                        max_tokens=st.session_state.chat_max_tokens
                    )

                if ai_response.startswith("Error:"):
                    st.error(ai_response)
                    # Optionally remove the last user message if AI fails, or keep it to show context of error
                    # For now, let's keep it. If AI fails, we add an error message to the chat.
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})

                # Rerun to update the chat display with the new AI message (or error)
                st.rerun()

            except ValueError as ve: # Catch API key validation errors from logic.py
                st.error(str(ve))
                # Add error to chat display
                st.session_state.messages.append({"role": "assistant", "content": str(ve)})
                st.rerun()
            except Exception as e: # Catch any other unexpected errors
                st.error(f"An unexpected error occurred: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"An unexpected error occurred: {e}"})
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# This is the first "Chat" block. The duplicated "Log" and "Chat" blocks that follow it will be removed.
elif selected == "Tasks":
    st.markdown("# ✅ Your Tasks")

    # Initialize session state for modal
    if 'show_task_modal' not in st.session_state:
        st.session_state.show_task_modal = False
    if 'editing_task_id' not in st.session_state:
        st.session_state.editing_task_id = None

    # "Add New Task" button
    if st.button("➕ Add New Task", use_container_width=True, type="primary"):
        st.session_state.editing_task_id = None
        st.session_state.show_task_modal = True
        st.rerun()

    # Load tasks (pending by default, but load_tasks itself handles the filter)
    # We need all tasks if we are to find one by ID for editing,
    # but display will filter to pending.
    all_tasks_df = logic.load_tasks(status_filter=None) # Load all for editing purposes
    display_tasks_df = all_tasks_df[all_tasks_df['status'] == 'pending'].copy()


    # Sorting options for display_tasks_df
    sort_option = st.selectbox(
        "Sort tasks by:",
        ["Creation Date (Newest First)", "Due Date (Earliest First)", "Priority (High to Low)"],
        key="task_sort_option"
    )

    if display_tasks_df is not None and not display_tasks_df.empty:
        if sort_option == "Due Date (Earliest First)":
            display_tasks_df = display_tasks_df.sort_values(by='due_date', ascending=True, na_position='last')
        elif sort_option == "Priority (High to Low)":
            priority_order = ["high", "medium", "low"]
            display_tasks_df['priority_sort'] = pd.Categorical(
                display_tasks_df['priority'].fillna('z_other'),
                categories=priority_order + ['z_other'],
                ordered=True
            )
            display_tasks_df = display_tasks_df.sort_values(by='priority_sort', ascending=True)
            display_tasks_df = display_tasks_df.drop(columns=['priority_sort'])
        else: # Default: Creation Date (Newest First)
            display_tasks_df = display_tasks_df.sort_values(by='created_at', ascending=False)
    
    # Task display section
    st.markdown('<div class="glass-panel" style="margin-top: 20px;">', unsafe_allow_html=True)
    if display_tasks_df.empty:
        st.info("No pending tasks! Add one above or enjoy your clear list! 👍")
    else:
        st.markdown("### 📋 Pending Tasks")
        for idx, task_row in display_tasks_df.iterrows():
            task_display_parts = []
            if pd.notna(task_row['priority']) and task_row['priority']:
                task_display_parts.append(f"[{task_row['priority'].capitalize()}]")
            task_display_parts.append(task_row['description'])
            if pd.notna(task_row['due_date']) and hasattr(task_row['due_date'], 'strftime'):
                task_display_parts.append(f"- Due: {task_row['due_date'].strftime('%Y-%m-%d')}")
            task_text = " ".join(task_display_parts)

            # Adjusted columns for Delete button: Description | Done | Edit | Delete
            col1, col_done, col_edit, col_delete = st.columns([0.55, 0.15, 0.15, 0.15])
            
            with col1:
                st.markdown(f"**{task_text}**")
                st.caption(f"Added: {task_row['created_at'].strftime('%Y-%m-%d %H:%M') if hasattr(task_row['created_at'], 'strftime') else task_row['created_at']}")
            
            with col_done:
                if st.button("Done", key=f"done_button_{task_row['task_id']}", use_container_width=True):
                    try:
                        logic.update_task_status(task_row['task_id'], 'completed')
                        st.session_state["flash"] = "🎉 Task marked as complete!"
                        st.session_state["celebrate"] = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error updating task: {e}")

            with col_edit:
                if st.button("Edit", key=f"edit_button_{task_row['task_id']}", use_container_width=True):
                    st.session_state.editing_task_id = task_row['task_id']
                    st.session_state.show_task_modal = True
                    st.rerun()

            with col_delete:
                if st.button("Delete", key=f"delete_button_{task_row['task_id']}", use_container_width=True):
                    try:
                        logic.delete_task(task_id=task_row['task_id'])
                        st.toast("🗑️ Task deleted successfully!")
                        st.rerun()
                    except ValueError as e:
                        st.error(f"❌ Error deleting task: {e}")
                    except IOError as e:
                        st.error(f"❌ Error deleting task (IO): {e}")
                    except Exception as e:
                        st.error(f"❌ Unexpected error deleting task: {e}")
            st.markdown("---")
    st.markdown('</div>', unsafe_allow_html=True)

    # Task Add/Edit Modal
    if st.session_state.show_task_modal:
        modal_title = "Add New Task"
        task_to_edit = None
        default_desc, default_due_date, default_priority_idx = "", None, 0 # Default for new task

        priority_options = ["None", "low", "medium", "high"]

        if st.session_state.editing_task_id:
            modal_title = "Edit Task"
            # Find the task in the full DataFrame
            task_to_edit_series = all_tasks_df[all_tasks_df['task_id'] == st.session_state.editing_task_id].iloc[0]
            if not task_to_edit_series.empty:
                default_desc = task_to_edit_series['description']
                # st.date_input handles None or datetime.date object
                default_due_date = task_to_edit_series['due_date'] if pd.notna(task_to_edit_series['due_date']) else None

                current_priority = task_to_edit_series['priority']
                if pd.notna(current_priority) and current_priority in priority_options:
                    default_priority_idx = priority_options.index(current_priority)
                else: # Handles None, pd.NA or empty string for priority
                    default_priority_idx = 0 # "None"

        # Using st.dialog for the modal
        with st.dialog(title=modal_title, dismissed=(not st.session_state.show_task_modal)):
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True) # Apply glass panel style to modal content
            with st.form("task_form"):
                description = st.text_area("Description", value=default_desc)
                due_date_val = st.date_input("Due Date (Optional)", value=default_due_date)
                priority_val_str = st.selectbox("Priority", options=priority_options, index=default_priority_idx)

                submitted = st.form_submit_button("💾 Save Task")
                if submitted:
                    final_due_date_str = due_date_val.isoformat() if due_date_val else None
                    final_priority_str = priority_val_str if priority_val_str != "None" else None

                    try:
                        if st.session_state.editing_task_id:
                            # Editing existing task
                            # Ensure status is preserved if not changed by this form (it isn't)
                            current_status = task_to_edit_series['status'] if task_to_edit_series is not None else 'pending'
                            logic.edit_task(
                                task_id=st.session_state.editing_task_id,
                                description=description,
                                status=current_status, # Pass existing status
                                due_date=final_due_date_str,
                                priority=final_priority_str
                            )
                            st.toast("✅ Task updated successfully!", icon="🎉")
                        else:
                            # Adding new task
                            logic.add_task(
                                description=description,
                                due_date=final_due_date_str,
                                priority=final_priority_str
                            )
                            st.toast("✅ Task added successfully!", icon="🎉")

                        st.session_state.show_task_modal = False
                        st.session_state.editing_task_id = None
                        st.rerun()
                    except ValueError as e:
                        st.error(f"❌ Validation Error: {e}")
                    except IOError as e:
                        st.error(f"❌ IO Error: Could not save task. {e}")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {e}")
            
            if st.button("Cancel", key="cancel_task_modal"):
                st.session_state.show_task_modal = False
                st.session_state.editing_task_id = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


elif selected == "Settings":
    st.markdown("# ⚙️ Settings")
    
    # API Key Management Section
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 🔑 API Configuration")

        # Get current API key for status display (do this before input field)
        current_api_key = get_api_key()
        if current_api_key:
            if len(current_api_key) > 4:
                 st.caption(f"Current status: API Key is set (ending with ...{current_api_key[-4:]})")
            else:
                 st.caption("Current status: API Key is set (but too short to mask).")
        else:
            st.caption("Current status: API Key not set.")

        # Initialize api_key_input from session_state if it exists, otherwise empty string
        if 'api_key_input' not in st.session_state:
            st.session_state.api_key_input = ''

        api_key_value_from_input = st.text_input(
            "OpenRouter API Key",
            value=st.session_state.api_key_input,
            type="password",
            key="api_key_input_field",  # Use this key to retrieve value
            help="Enter your OpenRouter API key. This is stored locally in config.json."
        )
        # Update session state for the input field immediately if it changes
        st.session_state.api_key_input = api_key_value_from_input

        if st.button("Save API Key", key="save_api_key_button"):
            # Use the value from the input field's dedicated session state key
            api_key_to_save = st.session_state.api_key_input_field
            if set_api_key(api_key_to_save):
                st.success("API Key saved successfully!")
                # Clear the input field in session_state after successful save
                st.session_state.api_key_input = ''
                # Rerun to update the status caption and clear the visible input if desired by Streamlit's default behavior
                st.rerun()
            else:
                st.error("Failed to save API Key. Check file permissions for config.json.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Notification Settings Section
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 🔔 Notifications")
        
        daily_reminders = st.toggle(
            "Daily Reminders",
            value=st.session_state.get('settings_daily_reminders', True),
            key="toggle_daily_reminders"
        )
        st.session_state.settings_daily_reminders = daily_reminders

        achievement_alerts = st.toggle(
            "Achievement Alerts",
            value=st.session_state.get('settings_achievement_alerts', True),
            key="toggle_achievement_alerts"
        )
        st.session_state.settings_achievement_alerts = achievement_alerts

        weekly_summary = st.toggle(
            "Weekly Summary",
            value=st.session_state.get('settings_weekly_summary', True),
            key="toggle_weekly_summary"
        )
        st.session_state.settings_weekly_summary = weekly_summary
        
        st.markdown('</div>', unsafe_allow_html=True)

# Add some padding at the bottom for the navigation
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) 