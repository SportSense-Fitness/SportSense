import streamlit as st
import math

st.set_page_config(
    page_title="SportSense",
    page_icon="⚡",
    layout="wide"
)

# --- DARK SPORTS APP STYLING ---
st.markdown("""
<style>
    /* Dark background */
    .stApp { background-color: #0f1117; }
    section[data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2d3748; }

    /* Hide default streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Logo */
    .ss-logo { font-size: 28px; font-weight: 800; color: #00e676; letter-spacing: -1px; margin-bottom: 4px; }
    .ss-logo span { color: white; }
    .ss-tagline { font-size: 11px; color: #6b7280; margin-bottom: 20px; }

    /* Metric cards */
    .metric-card {
        background: #1a1d27;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-label { font-size: 11px; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .metric-value { font-size: 36px; font-weight: 800; color: white; line-height: 1; }
    .metric-unit { font-size: 14px; color: #6b7280; margin-top: 4px; }

    /* Risk badges */
    .badge-low { background: #064e3b; color: #10b981; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 13px; display: inline-block; }
    .badge-moderate { background: #78350f; color: #f59e0b; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 13px; display: inline-block; }
    .badge-high { background: #7f1d1d; color: #ef4444; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 13px; display: inline-block; }

    /* Section headers */
    .section-header { font-size: 13px; color: #00e676; text-transform: uppercase; letter-spacing: 2px; font-weight: 700; margin: 24px 0 12px 0; }

    /* Alert boxes */
    .alert-warning { background: #1c1a0f; border-left: 3px solid #f59e0b; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 8px; color: #d1d5db; font-size: 14px; }
    .alert-danger  { background: #1c0f0f; border-left: 3px solid #ef4444; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 8px; color: #d1d5db; font-size: 14px; }
    .alert-success { background: #0f1c14; border-left: 3px solid #10b981; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 8px; color: #d1d5db; font-size: 14px; }

    /* Incident cards */
    .incident-card { background: #1a1d27; border: 1px solid #2d3748; border-radius: 10px; padding: 16px; margin-bottom: 10px; }
    .incident-title { font-weight: 700; color: white; font-size: 15px; margin-bottom: 4px; }
    .incident-detail { color: #9ca3af; font-size: 13px; }

    /* Nav items */
    .stRadio label { color: #d1d5db !important; font-size: 14px; }

    /* Page title */
    h1 { color: white !important; font-weight: 800 !important; }
    h2, h3 { color: #e5e7eb !important; }
    p, li { color: #9ca3af; }

    /* Sport selector */
    .stSelectbox label { color: #6b7280 !important; font-size: 12px !important; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# --- DATA ---
sport_profiles = {
    "Gaelic Football": {
        "sprint_threshold": 25, "hi_threshold": 20, "typical_distance": 9000,
        "key_injuries": ["Hamstring", "Knee (ACL)", "Ankle"],
    },
    "Soccer": {
        "sprint_threshold": 25, "hi_threshold": 19, "typical_distance": 10000,
        "key_injuries": ["Hamstring", "Ankle", "Groin"],
    },
    "Rugby": {
        "sprint_threshold": 22, "hi_threshold": 18, "typical_distance": 7000,
        "key_injuries": ["Shoulder", "Knee", "Hamstring"],
    },
    "Basketball": {
        "sprint_threshold": 20, "hi_threshold": 16, "typical_distance": 4500,
        "key_injuries": ["Ankle", "Knee", "Back"],
    },
    "Athletics": {
        "sprint_threshold": 24, "hi_threshold": 18, "typical_distance": 12000,
        "key_injuries": ["Hamstring", "Achilles", "Shin splints"],
    },
}

session_history = [
    {"date": "01-Mar", "distance": 8200, "max_speed": 27.1, "sprints": 18, "training_stress": 320, "fatigue_minute": 58, "risk": "LOW",      "incidents": []},
    {"date": "03-Mar", "distance": 7800, "max_speed": 26.8, "sprints": 15, "training_stress": 280, "fatigue_minute": 55, "risk": "LOW",      "incidents": []},
    {"date": "08-Mar", "distance": 8900, "max_speed": 28.2, "sprints": 22, "training_stress": 410, "fatigue_minute": 50, "risk": "LOW",      "incidents": []},
    {"date": "12-Mar", "distance": 9100, "max_speed": 28.9, "sprints": 24, "training_stress": 390, "fatigue_minute": 47, "risk": "MODERATE", "incidents": ["Heavy landing — left knee"]},
    {"date": "15-Mar", "distance": 9400, "max_speed": 29.1, "sprints": 26, "training_stress": 420, "fatigue_minute": 44, "risk": "MODERATE", "incidents": ["Stumble — right ankle", "Sudden stop — hamstring spike"]},
    {"date": "19-Mar", "distance": 9800, "max_speed": 29.8, "sprints": 28, "training_stress": 600, "fatigue_minute": 38, "risk": "HIGH",     "incidents": ["Heavy landing — left knee", "Step imbalance detected — minute 38"]},
]

latest = session_history[-1]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="ss-logo">Sport<span>Sense</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="ss-tagline">AI-powered injury prevention</div>', unsafe_allow_html=True)
    st.markdown("---")
    sport = st.selectbox("Select sport", list(sport_profiles.keys()))
    st.markdown("---")
    page = st.radio("Navigate", [
        "⚡ Session Summary",
        "📈 Trend Graphs",
        "🛡 Injury Risk Dashboard",
        "⚠ Incident Log",
    ])
    st.markdown("---")
    st.markdown('<p style="color:#4b5563;font-size:11px;">SportSense v0.2 · Built by Oisin Whelan</p>', unsafe_allow_html=True)

profile = sport_profiles[sport]

def metric_card(label, value, unit=""):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>"""

def risk_badge(risk):
    cls = {"LOW": "badge-low", "MODERATE": "badge-moderate", "HIGH": "badge-high"}.get(risk, "badge-low")
    return f'<span class="{cls}">{risk}</span>'

# ================================================
# SESSION SUMMARY
# ================================================
if page == "⚡ Session Summary":
    st.markdown(f"# Session Summary")
    st.markdown(f'<p style="color:#6b7280;margin-top:-16px;">{latest["date"]} &nbsp;·&nbsp; {sport}</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(metric_card("Total Distance", f'{latest["distance"]:,}', "metres"), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("Max Speed", latest["max_speed"], "km/h"), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("Sprints", latest["sprints"], "detected"), unsafe_allow_html=True)
    with col4: st.markdown(metric_card("Training Stress", latest["training_stress"], "points"), unsafe_allow_html=True)

    st.markdown('<div class="section-header">Fatigue & Risk</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)

    with col5:
        fm = latest["fatigue_minute"]
        if fm < 40:
            st.markdown(f'<div class="alert-danger">⚡ Fatigue detected at minute <strong>{fm}</strong> — High injury risk in final quarter</div>', unsafe_allow_html=True)
        elif fm < 50:
            st.markdown(f'<div class="alert-warning">⚡ Fatigue detected at minute <strong>{fm}</strong> — Monitor recovery</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-success">⚡ Fatigue detected at minute <strong>{fm}</strong> — Good endurance</div>', unsafe_allow_html=True)

    with col6:
        st.markdown(f'<div style="background:#1a1d27;border:1px solid #2d3748;border-radius:12px;padding:20px;text-align:center"><div class="metric-label">Overall Injury Risk</div><div style="margin-top:12px">{risk_badge(latest["risk"])}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Areas to watch</div>', unsafe_allow_html=True)
    cols = st.columns(len(profile["key_injuries"]))
    for i, injury in enumerate(profile["key_injuries"]):
        with cols[i]:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Watch</div><div style="font-size:18px;font-weight:700;color:white;margin-top:8px">{injury}</div></div>', unsafe_allow_html=True)

    if latest["incidents"]:
        st.markdown('<div class="section-header">Incidents detected</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="alert-warning">⚠ <strong>{len(latest["incidents"])} incident(s)</strong> detected this session — tap each to see details</div>', unsafe_allow_html=True)
        for inc in latest["incidents"]:
            with st.expander(f"📋 {inc}"):
                st.markdown(f'<div class="incident-detail"><strong style="color:white">What happened:</strong> {inc}<br><br><strong style="color:white">Why it matters:</strong> Sudden movement spikes increase soft tissue injury risk, especially when combined with fatigue.<br><br><strong style="color:white">What to do:</strong> Monitor the affected area. If soreness persists beyond 24 hours, consult a physio.</div>', unsafe_allow_html=True)

# ================================================
# TREND GRAPHS
# ================================================
elif page == "📈 Trend Graphs":
    st.markdown("# Performance Trends")
    st.markdown('<p style="color:#6b7280;margin-top:-16px;">Your progress over time</p>', unsafe_allow_html=True)

    dates     = [s["date"] for s in session_history]
    distances = [s["distance"] for s in session_history]
    speeds    = [s["max_speed"] for s in session_history]
    sprints   = [s["sprints"] for s in session_history]
    stress    = [s["training_stress"] for s in session_history]
    fatigue   = [s["fatigue_minute"] for s in session_history]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Total distance (m)</div>', unsafe_allow_html=True)
        st.line_chart(dict(zip(dates, distances)), height=200)
        st.markdown('<div class="section-header">Sprint count</div>', unsafe_allow_html=True)
        st.bar_chart(dict(zip(dates, sprints)), height=200)
    with col2:
        st.markdown('<div class="section-header">Max speed (km/h)</div>', unsafe_allow_html=True)
        st.line_chart(dict(zip(dates, speeds)), height=200)
        st.markdown('<div class="section-header">Training stress (pts)</div>', unsafe_allow_html=True)
        st.bar_chart(dict(zip(dates, stress)), height=200)

    st.markdown('<div class="section-header">Fatigue onset (minute) — lower means tiring earlier</div>', unsafe_allow_html=True)
    st.line_chart(dict(zip(dates, fatigue)), height=200)

# ================================================
# INJURY RISK DASHBOARD
# ================================================
elif page == "🛡 Injury Risk Dashboard":
    st.markdown("# Injury Risk Dashboard")

    loads   = [s["training_stress"] for s in session_history]
    acute   = sum(loads[-4:])
    chronic = sum(loads) / (len(loads) / 4)
    ratio   = acute / chronic

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(metric_card("Acute Load", f"{acute}", "last 4 sessions"), unsafe_allow_html=True)
    with col2: st.markdown(metric_card("Chronic Load", f"{chronic:.0f}", "4 week average"), unsafe_allow_html=True)
    with col3: st.markdown(metric_card("A:C Ratio", f"{ratio:.2f}", "safe zone: 0.8 – 1.3"), unsafe_allow_html=True)

    st.markdown('<div class="section-header">Workload status</div>', unsafe_allow_html=True)
    if ratio > 1.5:
        st.markdown('<div class="alert-danger">🔴 <strong>HIGH RISK</strong> — Training load has spiked dangerously. Reduce intensity immediately.</div>', unsafe_allow_html=True)
    elif ratio > 1.3:
        st.markdown('<div class="alert-warning">🟡 <strong>CAUTION</strong> — Approaching the danger zone. Keep next session light.</div>', unsafe_allow_html=True)
    elif ratio >= 0.8:
        st.markdown('<div class="alert-success">🟢 <strong>SWEET SPOT</strong> — Training load is optimal. Keep it up.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-warning">🔵 <strong>UNDERTRAINING</strong> — Load is too low. Gradually increase intensity.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">What could get you injured</div>', unsafe_allow_html=True)
    fatigues = [s["fatigue_minute"] for s in session_history]
    all_incidents = [inc for s in session_history for inc in s["incidents"]]

    if fatigues[-1] < fatigues[0] - 10:
        st.markdown('<div class="alert-warning">⚠ <strong>Fatigue hitting earlier each session</strong> — Your body isn\'t recovering fully. Hamstring and ankle risk elevated in final quarter.</div>', unsafe_allow_html=True)
    if len(all_incidents) >= 3:
        st.markdown('<div class="alert-warning">⚠ <strong>Recurring incidents detected</strong> — Multiple movement spikes across recent sessions. This pattern often precedes soft tissue injury.</div>', unsafe_allow_html=True)
    if loads[-1] > sum(loads[:-1]) / len(loads[:-1]) * 1.3:
        st.markdown('<div class="alert-warning">⚠ <strong>Last session was a big spike</strong> — A sudden jump in training stress is the single biggest predictor of injury in GAA players.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Recommended next session</div>', unsafe_allow_html=True)
    target = round(sum(loads) / len(loads) * 0.8)
    st.markdown(f'<div class="alert-success">✓ Keep training stress below <strong>{target} pts</strong> in your next session to bring your ratio back into the safe zone.</div>', unsafe_allow_html=True)

# ================================================
# INCIDENT LOG
# ================================================
elif page == "⚠ Incident Log":
    st.markdown("# Incident Log")
    st.markdown('<p style="color:#6b7280;margin-top:-16px;">Every movement anomaly detected by SportSense</p>', unsafe_allow_html=True)

    total = sum(len(s["incidents"]) for s in session_history)
    st.markdown(metric_card("Total incidents logged", total, "across all sessions"), unsafe_allow_html=True)

    st.markdown('<div class="section-header">Session breakdown</div>', unsafe_allow_html=True)

    for s in reversed(session_history):
        if s["incidents"]:
            risk_col = {"LOW": "#10b981", "MODERATE": "#f59e0b", "HIGH": "#ef4444"}.get(s["risk"], "white")
            st.markdown(f'<div style="color:{risk_col};font-weight:700;font-size:16px;margin:20px 0 8px 0">{s["date"]} — {len(s["incidents"])} incident(s)</div>', unsafe_allow_html=True)
            for inc in s["incidents"]:
                with st.expander(f"📋 {inc}"):
                    st.markdown(f'<div class="incident-detail"><strong style="color:white">What happened:</strong> {inc}<br><br><strong style="color:white">Why it matters:</strong> Sudden movement spikes increase soft tissue injury risk, especially when combined with fatigue.<br><br><strong style="color:white">What to do:</strong> Monitor the affected area. If soreness persists beyond 24 hours, consult a physio.</div>', unsafe_allow_html=True)

    if total == 0:
        st.markdown('<div class="alert-success">✓ No incidents logged yet. Keep training!</div>', unsafe_allow_html=True)