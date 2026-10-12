import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Paste your real prototype / demo link here. Leave empty to show "coming soon".
DEMO_URL = ""

# set_page_config must be the first Streamlit call
st.set_page_config(
    page_title="PreCrash AI - Predictive Vehicle Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Styling (colors chosen to stay readable in both light and dark themes)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main-title { font-size: 42px; font-weight: 700; color: #2563EB; margin-bottom: 5px; }
    .subtitle { font-size: 20px; opacity: 0.75; margin-bottom: 25px; }
    .section-header {
        font-size: 28px; font-weight: 600; color: #2563EB;
        border-bottom: 2px solid rgba(128, 128, 128, 0.3);
        padding-bottom: 8px; margin-top: 30px; margin-bottom: 15px;
    }
    .metric-box {
        background-color: rgba(37, 99, 235, 0.08);
        padding: 15px; border-radius: 8px; border-left: 5px solid #2563EB;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def section_header(text: str) -> None:
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_overview() -> None:
    st.markdown('<div class="main-title">PreCrash AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predictive AI for Safer Roads</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(
            "**PreCrash AI** is an advanced, AI-powered vehicle-safety system designed to "
            "identify developing collision risks long before impact, giving drivers the "
            "crucial early window needed to respond safely."
        )
        st.write(
            "Unlike traditional safety mechanisms that react only when an accident is imminent or "
            "already occurring, PreCrash AI continuously analyzes driver physiology and "
            "environmental telemetry to catch threats earlier."
        )
    with col2:
        link = (
            f'<a href="{DEMO_URL}" target="_blank">🔗 View PreCrash AI Prototype / Demo</a>'
            if DEMO_URL
            else "🔗 Prototype demo link coming soon"
        )
        st.markdown(
            f"""
            <div class="metric-box">
            <h4>Project Status</h4>
            <p>🔄 Initial prototype & technical demo development phase.</p>
            <p>{link}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_problem() -> None:
    section_header("The Structural Problem")
    st.error(
        "🚨 **The Vulnerability Window:** Road accidents develop in mere seconds, "
        "leaving drivers with highly compressed reaction timelines."
    )
    st.markdown(
        """
        Critical vulnerabilities globally include:
        - **Driver Fatigue & Distraction:** Inattention caused by mobile phone usage or dangerous driving behavior.
        - **External Hazards:** Unexpected objects or road issues.
        - **Sensor Failures:** Real-time sensor drops that leave automated systems blind.
        """
    )
    st.warning(
        "⚠️ **Traditional Approach:** Existing options focus heavily on *reactive* warnings or "
        "post-collision alerts. They miss the active development window of an accident."
    )

    section_header("Our Strategic Mission")
    st.info(
        "🎯 **Mission Statement:** To drastically reduce and prevent avoidable road accidents by "
        "identifying dangerous situations earlier, giving vehicle operators a structured, timely "
        "window for appropriate corrections."
    )


def page_solution() -> None:
    section_header("The PreCrash Architecture")
    st.write("Our planned safety engine combines 9 critical technical components:")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("🔹 **1. Driver Monitoring:** Deep-learning computer vision to track fatigue, eye aspect ratio (EAR), and mobile-device distractions.")
        st.markdown("🔹 **2. Driving-Behavior Analysis:** Algorithmic tracking of telemetry and vehicle mechanics.")
        st.markdown("🔹 **3. Predictive Risk Assessment:** Fusing multi-channel temporal streams into a proactive collision-risk index.")
        st.markdown("🔹 **4. Real-Time Intelligent Alerts:** Context-aware, progressive early warnings.")
        st.markdown("🔹 **5. Sensor-Failure Detection:** Safe fallback modes when core sensors become uncalibrated.")
    with c2:
        st.markdown("🔹 **6. Vehicle-to-Vehicle (V2V):** Networks allowing nearby vehicles to exchange hazard data.")
        st.markdown("🔹 **7. Emergency Notification:** Automatic crash diagnostics and telemetry routing to first responders.")
        st.markdown("🔹 **8. Digital-Twin Simulation:** Isolated testing against extreme driving scenarios.")
        st.markdown("🔹 **9. Active Safety Intervention:** Controlled automatic deceleration where legally permissible.")

    section_header("Technical Stack & Milestones")
    st.code(
        "Stack candidates: Python, OpenCV, MediaPipe, YOLO models, "
        "low-latency edge hardware telemetry",
        language="text",
    )
    st.markdown("**Key Milestones Ahead:**")
    st.markdown(
        "- Lock and document baseline software prototypes.\n"
        "- Fuse driver computer-vision layers into the central temporal risk engine.\n"
        "- Start B2B customer discovery for corporate logistics and enterprise fleets."
    )


FUNDING_ROWS = [
    ("AI, computer vision models, and predictive risk logic", 18000),
    ("Prototype hardware engineering and vehicle/sensor telemetry integration", 16000),
    ("Sensor-failure tracking software and fail-safe modes", 10000),
    ("Controlled testing and safety verification routines", 12000),
    ("V2V communications planning and emergency-response API integration", 8000),
    ("Digital-twin driving-scene simulation environment", 6000),
    ("Core data pipeline, logging storage, and developer licenses", 4000),
    ("Customer discovery and stakeholder network development", 3000),
    ("Engineering buffers, testing adjustments, and contingency", 3000),
]


def page_business() -> None:
    section_header("Business Strategy & Commercialization")
    st.write(
        "PreCrash AI operates on a pre-revenue, pre-seed B2B model. The immediate focus is "
        "securing **enterprise fleet logistics and transit operator partnerships** to run "
        "validation pilots in controlled real-world scenarios."
    )

    section_header("Funding Target & Capital Allocation")

    df = pd.DataFrame(FUNDING_ROWS, columns=["Focus Area", "Allocation (USD)"])
    total = int(df["Allocation (USD)"].sum())
    df["Share"] = df["Allocation (USD)"] / total

    st.metric(label="Pre-Seed Capital Required", value=f"${total:,.0f} USD")
    st.write("Indicative fund allocation across focus areas:")

    st.dataframe(
        df,
        hide_index=True,
        column_config={
            "Allocation (USD)": st.column_config.NumberColumn(format="$%d"),
            "Share": st.column_config.ProgressColumn(
                "Share of total", format="percent", min_value=0.0, max_value=1.0
            ),
        },
    )
    st.bar_chart(df.set_index("Focus Area")["Allocation (USD)"], horizontal=True)


def page_team() -> None:
    section_header("Founding Team")

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("### 👩‍💼 Esraa")
        st.markdown("**Founder & Product Lead**")
        st.write(
            "Directs overall product vision, defines functional requirements, coordinates "
            "roadmap priorities, and shapes early-stage commercialization strategy."
        )
    with t2:
        st.markdown("### 👨‍💻 Ahmed Sabry")
        st.markdown("**Co-founder & Technical Lead**")
        st.write(
            "Leads technical development of the initial prototype and software demo, exploring "
            "computer-vision scripts and models for tracking operator fatigue."
        )

    st.markdown("---")
    st.markdown("### Long-Term Vision")
    st.info(
        "To scale PreCrash AI into a robust vehicle-safety technology company, introducing "
        "predictive capabilities that mitigate road risks early and support safer mobility "
        "across Egypt and the wider region."
    )


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
PAGES = {
    "Overview": page_overview,
    "The Problem & Mission": page_problem,
    "Our Solution & Tech Roadmap": page_solution,
    "Business Plan & Funding": page_business,
    "Our Team": page_team,
}

st.sidebar.title("🛡️ PreCrash AI")
st.sidebar.markdown("*Predictive AI for Safer Roads*")
st.sidebar.write("---")
choice = st.sidebar.radio("Go to Section:", list(PAGES))
st.sidebar.write("---")
st.sidebar.info("📍 Founded: Egypt\n\n🚀 Stage: Initial Prototype")

PAGES[choice]()
