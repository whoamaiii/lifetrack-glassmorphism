import streamlit as st
from streamlit_option_menu import option_menu
from logic import log_activity, load_data
import pandas as pd
from datetime import datetime

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
    options=["Home", "Analysis", "Log", "Chat", "Settings"],
    icons=["house-fill", "bar-chart-fill", "plus-circle-fill", "chat-dots-fill", "gear-fill"],
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
                st.markdown("""
                <div class="metric-card">
                    <h3>📈 Total</h3>
                    <h1>{}</h1>
                    <p>This Week</p>
                </div>
                """.format(len(df)), unsafe_allow_html=True)
            
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
                log_activity("Drank a glass of water")
                st.success("✅ Water logged!")
                st.balloons()
            
            if st.button("🏃 Add Exercise", use_container_width=True, key="home_exercise"):
                log_activity("Completed workout session")
                st.success("✅ Exercise logged!")
                st.balloons()
            
            if st.button("🍎 Track Meal", use_container_width=True, key="home_meal"):
                log_activity("Had a healthy meal")
                st.success("✅ Meal tracked!")
                st.balloons()
    
    with col2:
        with st.container():
            if st.button("😴 Log Sleep", use_container_width=True, key="home_sleep"):
                log_activity("Got good sleep")
                st.success("✅ Sleep logged!")
                st.balloons()
            
            if st.button("🧘 Add Meditation", use_container_width=True, key="home_meditation"):
                log_activity("Meditated for 10 minutes")
                st.success("✅ Meditation logged!")
                st.balloons()
            
            if st.button("📚 Track Study", use_container_width=True, key="home_study"):
                log_activity("Studied for 30 minutes")
                st.success("✅ Study session logged!")
                st.balloons()

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
    
    # Stats Overview
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 📈 Your Statistics")
        
        df = load_data()
        if df is not None and not df.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Activities", len(df), "+12%")
            with col2:
                st.metric("Active Days", df['timestamp'].dt.date.nunique(), "+3")
            with col3:
                st.metric("Best Streak", "7 days", "🔥")
            with col4:
                st.metric("Points Earned", "1,250", "+150")
        else:
            st.info("No data to analyze yet. Start tracking your activities!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts placeholder
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 📊 Activity Trends")
        st.markdown("Charts and visualizations coming soon!")
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
                log_activity(user_input)
                st.success(f"✅ Logged successfully!")
                st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Quick action grid
    st.markdown("### ⚡ Quick Actions")
    
    # First row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💧 Water\n+10 pts", use_container_width=True, key="log_water"):
            log_activity("Drank a glass of water")
            st.success("✅ +10 points!")
    
    with col2:
        if st.button("🏃 Exercise\n+25 pts", use_container_width=True, key="log_exercise"):
            log_activity("Completed exercise")
            st.success("✅ +25 points!")
    
    with col3:
        if st.button("🧘 Meditate\n+15 pts", use_container_width=True, key="log_meditate"):
            log_activity("Meditated")
            st.success("✅ +15 points!")
    
    # Second row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍎 Healthy Meal\n+20 pts", use_container_width=True, key="log_meal"):
            log_activity("Ate healthy meal")
            st.success("✅ +20 points!")
    
    with col2:
        if st.button("📚 Study\n+30 pts", use_container_width=True, key="log_study"):
            log_activity("Study session")
            st.success("✅ +30 points!")
    
    with col3:
        if st.button("😴 Good Sleep\n+25 pts", use_container_width=True, key="log_sleep"):
            log_activity("Got good sleep")
            st.success("✅ +25 points!")

elif selected == "Chat":
    st.markdown("# 💬 AI Assistant")
    
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 🤖 Your Personal Health Coach")
        st.markdown("Ask me anything about your health and wellness journey!")
        
        # Chat interface placeholder
        st.text_input("Type your message...", placeholder="How can I improve my water intake?")
        st.button("Send →", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Settings":
    st.markdown("# ⚙️ Settings")
    
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 👤 Profile")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### 🎯")
        with col2:
            st.text_input("Name", value="User", label_visibility="visible")
            st.text_input("Email", value="user@example.com", label_visibility="visible")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown("## 🔔 Notifications")
        
        st.toggle("Daily Reminders", value=True)
        st.toggle("Achievement Alerts", value=True)
        st.toggle("Weekly Summary", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Add some padding at the bottom for the navigation
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) 