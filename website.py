import streamlit as st
import pandas as pd

# Set page configuration for a professional corporate look
st.set_page_config(
    page_title="PreCrash AI - Predictive Vehicle Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for a polished UI
st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 20px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .section-header {
        font-size: 28px;
        font-weight: 600;
        color: #1E3A8A;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 8px;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .metric-box {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation Sidebar
st.sidebar.image("https://icons8.com", width=80)
st.sidebar.title("PreCrash AI")
st.sidebar.markdown("*Predictive AI for Safer Roads*")
st.sidebar.write("---")
page = st.sidebar.radio(
    "Go to Section:",
    ["Overview", "The Problem & Mission", "Our Solution & Tech Roadmap", "Business Plan & Funding", "Our Team"]
)

st.sidebar.write("---")
st.sidebar.info("📍 Founded: Egypt\n\n🚀 Stage: Initial Prototype")

# ----------------- PAGE 1: OVERVIEW -----------------
if page == "Overview":
    st.markdown('<div class="main-title">PreCrash AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predictive AI for Safer Roads</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(
            "**PreCrash AI** is an advanced, AI-powered vehicle-safety system designed to "
            "identify developing collision risks long before impact, empowering drivers with the "
            "crucial early windows needed to respond safely."
        )
        st.write(
            "Unlike traditional safety mechanisms that react only when an accident is imminent or already "
            "occurring, PreCrash AI continuously parses, cross-references, and metrics driver physiology "
            "and environmental telemetry to catch threats earlier."
        )
    with col2:
        st.markdown(
            """
            <div class="metric-box">
            <h4>Project Status</h4>
            <p>🔄 Initial prototype & technical demo development phase.</p>
            <a href="#" target="_blank">🔗 View PreCrash AI Prototype / Demo</a>
            </div>
            """, 
            unsafe_allow_html=True
        )

# ----------------- PAGE 2: THE PROBLEM & MISSION -----------------
elif page == "The Problem & Mission":
    st.markdown('<div class="section-header">The Structural Problem</div>', unsafe_allow_html=True)
    
    left_co, right_co = st.columns([2, 1])
    with left_co:
        st.error("🚨 **The Vulnerability Window:** Road accidents develop in mere seconds, leaving drivers with highly compressed reaction timelines.")
        st.markdown(
            """
            Critical system vulnerabilities globally include:
            - **Driver Fatigue & Distraction:** Inattention caused by mobile phone usage or dangerous driving behavior.
            - **External Hazards:** Unexpected objects or road issues.
            - **Sensor Failures:** Catastrophic real-time sensor drops that leave automated systems blind.
            """
        )
        st.warning("⚠️ **Traditional Approach:** Existing options focus heavily on *reactive* warnings or post-collision alerts. They completely miss the active development window of an accident.")

    st.markdown('<div class="section-header">Our Strategic Mission</div>', unsafe_allow_html=True)
    st.info("🎯 **Mission Statement:** To drastically reduce and prevent avoidable road accidents by identifying complex, dangerous situations earlier—equipping vehicle operators with a structured, timely window for appropriate corrections.")

# ----------------- PAGE 3: OUR SOLUTION & TECH ROADMAP -----------------
elif page == "Our Solution & Tech Roadmap":
    st.markdown('<div class="section-header">The PreCrash Architecture</div>', unsafe_allow_html=True)
    st.write("Our conceptually planned safety engine seamlessly synthesizes 9 critical technical vectors:")
    
    # Grid display of vectors
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("🔹 **1. Driver Monitoring:** Deep learning computer vision to track fatigue, eye-aspect ratios (EAR), and mobile device distractions.")
        st.markdown("🔹 **2. Driving-Behavior Analysis:** Algorithmic tracking of telemetry and active vehicle mechanics.")
        st.markdown("🔹 **3. Predictive Risk Assessment:** Fusing multi-channel temporal streams into a shifting proactive collision index.")
        st.markdown("🔹 **4. Real-Time Intelligent Alerts:** Context-aware, progressive early warnings.")
        st.markdown("🔹 **5. Sensor-Failure Detection:** Safe fallback modes when core arrays go uncalibrated.")
    with c2:
        st.markdown("🔹 **6. Vehicle-to-Vehicle (V2V):** Mesh networks allowing nearby transit vectors to exchange hazard logs.")
        st.markdown("🔹 **7. Emergency Notification:** Automatic crash diagnostics and telemetry routing to first responders.")
        st.markdown("🔹 **8. Digital-Twin Simulation:** Isolated environment testing against extreme driving anomalies.")
        st.markdown("🔹 **9. Active Safety Intervention:** Controlled autonomous deceleration protocols where legally permissible.")

    st.markdown('<div class="section-header">Technical Stack & Milestones</div>', unsafe_allow_html=True)
    st.code("Stack Candidates: Python, OpenCV, MediaPipe, YOLO Models, Low-latency Edge Hardware Telemetry Arrays", language="text")
    
    st.markdown("**Key Milestones Ahead:**")
    st.markdown(
        "- Lock & document baseline software prototypes.\n"
        "- Fuse driver computer vision layers into the central temporal risk scaling engine.\n"
        "- Initiate B2B customer discovery tailored for corporate logistics and enterprise fleets."
    )

# ----------------- PAGE 4: BUSINESS PLAN & FUNDING -----------------
elif page == "Business Plan & Funding":
    st.markdown('<div class="section-header">Business Strategy & Commercialization</div>', unsafe_allow_html=True)
    st.write(
        "PreCrash AI operates on a pre-revenue, pre-seed B2B framework. The immediate business focus "
        "is centered on securing active **enterprise fleet logistics and transit operator partnerships** "
        "to run validation pilot loops in controlled real-world scenarios."
    )

    st.markdown('<div class="section-header">Funding Target & Capital Allocation</div>', unsafe_allow_html=True)
    st.metric(label="Pre-Seed Capital Required", value="$80,000 USD")
    st.write("Indicative fund routing mapped across targeted functional focus areas:")

    # Interactive Table for allocation breakdown
    funding_data = {
        "Target Functional Focus Area": [
            "AI, Computer Vision models, and predictive risk scaling logic",
            "Prototype hardware engineering and vehicle/sensor telemetry integration",
            "Sensor-failure tracking software frameworks and fail-safe safety modes",
            "Isolated environment controlled testing and safety verification routines",
            "V2V communications planning and emergency response API integration",
            "Digital-twin driving scene simulation environment programming",
            "Core data pipeline infrastructure, logging storage, and developer licenses",
            "Structured customer discovery pipelines and stakeholder network development",
            "Rigorous engineering buffers, testing adjustments, and contingency funds"
        ],
        "Allocation (USD)": [18000, 16000, 10000, 12000, 8000, 6000, 4000, 3000, 3000]
    }
    
    df = pd.DataFrame(funding_data)
    df["Allocation (USD)"] = df["Allocation (USD)"].map('${:,.2f}'.format)
    st.table(df)

# ----------------- PAGE 5: OUR TEAM -----------------
elif page == "Our Team":
    st.markdown('<div class="section-header">Founding Team</div>', unsafe_allow_html=True)
    
    t1, t2 = st.columns(2)
    with t1:
        st.markdown("### 👩‍💼 Esraa")
        st.markdown("**Founder & Product Lead**")
        st.write("Directs overarching product vision, structures functional requirement standards, coordinates roadmap priorities, and defines early-stage commercialization strategies.")
        
    with t2:
        st.markdown("### 👨‍💻 Ahmed Sabry")
        st.markdown("**Co-founder & Technical Lead**")
        st.write("Drives technical development on the initial functional prototype and software demo, exploring computer-vision scripts and model framing for tracking operator fatigue.")

    st.markdown("---")
    st.markdown("### Long-Term Vision")
    st.info("To scale PreCrash AI into a highly robust vehicle-safety technology company, introducing premier predictive capabilities that mitigate early road risks and cultivate safer mobility across Egypt and future regional transport ecosystems.")
