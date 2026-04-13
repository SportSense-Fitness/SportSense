import streamlit as st
import math

st.set_page_config(page_title="SportSense", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; }
    section[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #1f1f1f; }
    #MainMenu, footer, header { visibility: hidden; }
    h1, h2, h3 { color: white !important; font-weight: 900 !important; letter-spacing: -0.5px; }
    p, li { color: #888; }

    .top-bar {
        background: #000;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #1f1f1f;
        margin-bottom: 24px;
    }
    .logo { font-size: 22px; font-weight: 900; color: #00e676; letter-spacing: -1px; }
    .logo span { color: white; }

    .metric-block {
        background: #111;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-label {
        font-size: 10px;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 42px;
        font-weight: 900;
        color: white;
        line-height: 1;
        letter-spacing: -2px;
    }
    .metric-unit {
        font-size: 12px;
        color: #444;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-change-up {
        font-size: 13px;
        color: #00e676;
        font-weight: 700;
        margin-top: 8px;
    }
    .metric-change-down {
        font-size: 13px;
        color: #ef4444;
        font-weight: 700;
        margin-top: 8px;
    }
    .metric-change-neutral {
        font-size: 13px;
        color: #555;
        font-weight: 700;
        margin-top: 8px;
    }

    .session-card {
        background: #111;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 12px;
        cursor: pointer;
    }
    .session-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .session-date { font-size: 13px; color: #555; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .session-type { font-size: 13px; color: #00e676; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }

    .pill {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 2px solid;
    }
    .pill-low    { border-color: #00e676; color: #00e676; }
    .pill-mod    { border-color: #f59e0b; color: #f59e0b; }
    .pill-high   { border-color: #ef4444; color: #ef4444; }
    .pill-green  { border-color: #00e676; color: #00e676; }
    .pill-amber  { border-color: #f59e0b; color: #f59e0b; }

    .sense-score-ring {
        background: #111;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
    }
    .score-number {
        font-size: 72px;
        font-weight: 900;
        color: #00e676;
        line-height: 1;
        letter-spacing: -4px;
    }
    .score-label {
        font-size: 10px;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 8px;
    }

    .section-title {
        font-size: 10px;
        color: #555;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        margin: 28px 0 12px 0;
    }

    .balance-bar-container {
        background: #111;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 12px;
    }
    .balance-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .balance-foot { font-size: 11px; color: #555; text-transform: uppercase; letter-spacing: 1px; }
    .balance-value { font-size: 36px; font-weight: 900; color: white; }
    .bar-track {
        background: #1f1f1f;
        border-radius: 4px;
        height: 8px;
        display: flex;
        overflow: hidden;
        margin: 8px 0 16px 0;
    }
    .bar-left  { background: #00e676; height: 100%; }
    .bar-right { background: #3b82f6; height: 100%; }

    .incident-card {
        background: #111;
        border: 1px solid #2a1a1a;
        border-left: 3px solid #ef4444;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .incident-title { font-size: 14px; font-weight: 700; color: white; margin-bottom: 4px; }
    .incident-body  { font-size: 12px; color: #555; }

    .tab-row {
        display: flex;
        gap: 8px;
        margin-bottom: 24px;
        border-bottom: 1px solid #1f1f1f;
        padding-bottom: 0;
    }
    .tab-active   { font-size: 13px; font-weight: 800; color: white; padding: 8px 0; border-bottom: 2px solid #00e676; margin-right: 20px; cursor: pointer; }
    .tab-inactive { font-size: 13px; font-weight: 600; color: #444; padding: 8px 0; margin-right: 20px; cursor: pointer; }

    .alert-bar {
        background: #1a0f0f;
        border: 1px solid #3a1a1a;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 13px;
        color: #ccc;
    }
    .alert-bar-green {
        background: #0a1a0f;
        border: 1px solid #1a3a1f;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        font-size: 13px;
        color: #ccc;
    }

    .pb-card {
        background: #111;
        border: 1px solid #1f1f1f;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }
    .pb-icon { font-size: 28px; margin-bottom: 8px; }
    .pb-metric { font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 1px; }
    .pb-value { font-size: 28px; font-weight: 900; color: #00e676; }
    .pb-unit { font-size: 11px; color: #444; }

    .five-min-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        gap: 4px;
        margin: 16px 0;
    }
    .five-min-bar {
        flex: 1;
        border-radius: 4px 4px 0 0;
        min-height: 4px;
    }
    .five-min-label {
        font-size: 9px;
        color: #444;
        text-align: center;
        margin-top: 4px;
    }

    .stRadio label { color: #888 !important; font-size: 13px !important; }
    .stSelectbox label { color: #444 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 1px; }
    div[data-testid="stSelectbox"] > div { background: #111 !important; border-color: #1f1f1f !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────

sport_profiles = {
    "Gaelic Football": {"sprint": 25, "hi": 20, "typical": 9000, "injuries": ["Hamstring", "Knee (ACL)", "Ankle"]},
    "Soccer":          {"sprint": 25, "hi": 19, "typical": 10000,"injuries": ["Hamstring", "Ankle", "Groin"]},
    "Rugby":           {"sprint": 22, "hi": 18, "typical": 7000, "injuries": ["Shoulder", "Knee", "Hamstring"]},
    "Basketball":      {"sprint": 20, "hi": 16, "typical": 4500, "injuries": ["Ankle", "Knee", "Back"]},
    "Athletics":       {"sprint": 24, "hi": 18, "typical": 12000,"injuries": ["Hamstring", "Achilles", "Shin splints"]},
}

sessions = [
    {"date":"01 Mar","type":"Training","distance":8200,"max_speed":27.1,"sprints":18,"hi_distance":1840,"stress":320,"fatigue_min":58,"risk":"LOW",     "accels":24,"decels":22,"left_foot":51,"right_foot":49,"incidents":[]},
    {"date":"03 Mar","type":"Training","distance":7800,"max_speed":26.8,"sprints":15,"hi_distance":1620,"stress":280,"fatigue_min":55,"risk":"LOW",     "accels":21,"decels":20,"left_foot":50,"right_foot":50,"incidents":[]},
    {"date":"08 Mar","type":"Training","distance":8900,"max_speed":28.2,"sprints":22,"hi_distance":2100,"stress":410,"fatigue_min":50,"risk":"LOW",     "accels":28,"decels":27,"left_foot":52,"right_foot":48,"incidents":[]},
    {"date":"12 Mar","type":"Match",   "distance":9100,"max_speed":28.9,"sprints":24,"hi_distance":2340,"stress":390,"fatigue_min":47,"risk":"MODERATE","accels":30,"decels":29,"left_foot":53,"right_foot":47,"incidents":["Heavy landing — left knee"]},
    {"date":"15 Mar","type":"Training","distance":9400,"max_speed":29.1,"sprints":26,"hi_distance":2580,"stress":420,"fatigue_min":44,"risk":"MODERATE","accels":32,"decels":30,"left_foot":54,"right_foot":46,"incidents":["Stumble — right ankle","Sudden stop — hamstring spike"]},
    {"date":"19 Mar","type":"Match",   "distance":9800,"max_speed":29.8,"sprints":28,"hi_distance":2890,"stress":600,"fatigue_min":38,"risk":"HIGH",    "accels":35,"decels":33,"left_foot":56,"right_foot":44,"incidents":["Heavy landing — left knee","Step imbalance — minute 38"]},
]

latest  = sessions[-1]
prev    = sessions[-2]
average = lambda key: sum(s[key] for s in sessions[:-1]) / len(sessions[:-1])

def change(key, fmt=".0f", suffix=""):
    now = latest[key]
    avg = average(key)
    diff = now - avg
    arrow = "▲" if diff > 0 else "▼"
    colour = "metric-change-up" if diff > 0 else "metric-change-down"
    return f'<div class="{colour}">{arrow} {abs(diff):{fmt}}{suffix} vs avg</div>'

def sense_score(s):
    d_score = min(s["distance"] / 9000, 1) * 30
    sp_score = min(s["max_speed"] / 32, 1) * 25
    sprint_score = min(s["sprints"] / 30, 1) * 20
    fatigue_score = min(s["fatigue_min"] / 60, 1) * 15
    risk_penalty = {"LOW": 0, "MODERATE": 5, "HIGH": 10}.get(s["risk"], 0)
    return max(0, min(100, round(d_score + sp_score + sprint_score + fatigue_score - risk_penalty + 10)))

def pill(text, colour):
    return f'<span class="pill pill-{colour}">{text}</span>'

def metric(label, value, unit, change_html=""):
    return f"""<div class="metric-block">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
        {change_html}
    </div>"""

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="logo">Sport<span>Sense</span></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px;color:#333;margin-top:2px">AI injury prevention</p>', unsafe_allow_html=True)
    st.markdown("---")
    sport = st.selectbox("Sport", list(sport_profiles.keys()))
    st.markdown("---")
    page = st.radio("", ["🏠  Home", "📋  Activity", "🛡  Injury Risk", "⚠  Incidents"])
    st.markdown("---")
    st.markdown('<p style="font-size:10px;color:#333;">SportSense v0.1 · Built by Oisin</p>', unsafe_allow_html=True)

profile = sport_profiles[sport]
score   = sense_score(latest)

# ── HOME ──────────────────────────────────────────────────────────────────────

if page == "🏠  Home":
    st.markdown('<div class="logo" style="font-size:32px;margin-bottom:4px">Sport<span>Sense</span></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#333;font-size:12px;margin-top:0">LAST SESSION &nbsp;·&nbsp; {latest["date"].upper()} &nbsp;·&nbsp; {latest["type"].upper()}</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""<div class="sense-score-ring">
            <div class="score-label">Sense Score</div>
            <div class="score-number">{score}</div>
            <div class="score-label" style="margin-top:4px">/ 100</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        risk_colour = {"LOW":"low","MODERATE":"mod","HIGH":"high"}.get(latest["risk"],"low")
        fatigue_colour = "green" if latest["fatigue_min"] >= 50 else "amber" if latest["fatigue_min"] >= 40 else "high"
        st.markdown(f"""<div class="session-card">
            <div class="session-card-header">
                <span class="session-date">{latest["date"]}</span>
                <span class="session-type">{latest["type"]}</span>
            </div>
            <div style="display:flex;gap:12px;margin-bottom:16px">
                <div>
                    <div class="metric-label">Injury Risk</div>
                    {pill(latest["risk"], risk_colour)}
                </div>
                <div>
                    <div class="metric-label">Fatigue</div>
                    {pill(f'Min {latest["fatigue_min"]}', fatigue_colour)}
                </div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;text-align:center">
                <div><div class="metric-label">Distance</div><div style="font-size:22px;font-weight:900;color:white">{latest["distance"]:,}</div><div class="metric-unit">m</div></div>
                <div><div class="metric-label">Max Speed</div><div style="font-size:22px;font-weight:900;color:white">{latest["max_speed"]}</div><div class="metric-unit">km/h</div></div>
                <div><div class="metric-label">Sprints</div><div style="font-size:22px;font-weight:900;color:white">{latest["sprints"]}</div><div class="metric-unit">total</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Personal Bests
    st.markdown('<div class="section-title">Personal Bests</div>', unsafe_allow_html=True)
    pb_speed    = max(s["max_speed"]    for s in sessions)
    pb_distance = max(s["distance"]     for s in sessions)
    pb_sprints  = max(s["sprints"]      for s in sessions)
    pb_hi       = max(s["hi_distance"]  for s in sessions)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'<div class="pb-card"><div class="pb-icon">⚡</div><div class="pb-metric">Max Speed</div><div class="pb-value">{pb_speed}</div><div class="pb-unit">km/h</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="pb-card"><div class="pb-icon">📍</div><div class="pb-metric">Distance</div><div class="pb-value">{pb_distance:,}</div><div class="pb-unit">m</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="pb-card"><div class="pb-icon">🏃</div><div class="pb-metric">Sprints</div><div class="pb-value">{pb_sprints}</div><div class="pb-unit">session</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="pb-card"><div class="pb-icon">🔥</div><div class="pb-metric">Hi Intensity</div><div class="pb-value">{pb_hi:,}</div><div class="pb-unit">m</div></div>', unsafe_allow_html=True)

# ── ACTIVITY ─────────────────────────────────────────────────────────────────

elif page == "📋  Activity":
    st.markdown("# Activity")
    st.markdown('<p style="color:#333;font-size:12px">YOUR SESSIONS</p>', unsafe_allow_html=True)

    selected = st.selectbox("View session", [f"{s['date']} — {s['type']}" for s in reversed(sessions)])
    s = next(x for x in sessions if f"{x['date']} — {x['type']}" == selected)

    tab = st.radio("", ["Volume", "Speed", "Cardio"], horizontal=True)

    avg_dist   = average("distance")
    avg_speed  = average("max_speed")
    avg_sprint = average("sprints")
    avg_hi     = average("hi_distance")
    avg_accels = average("accels")
    avg_decels = average("decels")

    def arrow(now, avg, fmt=".0f", suffix=""):
        diff = now - avg
        sym = "▲" if diff >= 0 else "▼"
        cls = "metric-change-up" if diff >= 0 else "metric-change-down"
        return f'<div class="{cls}">{sym} {abs(diff):{fmt}}{suffix} vs avg</div>'

    if tab == "Volume":
        st.markdown('<div class="section-title">Volume</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: st.markdown(metric("Total Distance", f'{s["distance"]:,}', "m", arrow(s["distance"], avg_dist, ".0f")), unsafe_allow_html=True)
        with c2: st.markdown(metric("Hi Intensity Dist", f'{s["hi_distance"]:,}', "m", arrow(s["hi_distance"], avg_hi, ".0f")), unsafe_allow_html=True)

        dist_per_min = round(s["distance"] / 70)
        st.markdown(metric("Distance Per Min", dist_per_min, "m/min"), unsafe_allow_html=True)

        # 5 min breakdown
        st.markdown('<div class="section-title">5 Min Breakdown</div>', unsafe_allow_html=True)
        blocks = [820, 790, 870, 810, 760, 840, 800, 750, 780, 820, 710, 680, 650, 600]
        max_b  = max(blocks)
        bars   = ""
        labels = ""
        for i,b in enumerate(blocks):
            h = int((b/max_b)*80)
            colour = "#00e676" if b >= 750 else "#f59e0b" if b >= 650 else "#ef4444"
            bars   += f'<div style="flex:1;background:{colour};height:{h}px;border-radius:4px 4px 0 0"></div>'
            labels += f'<div style="flex:1;font-size:8px;color:#444;text-align:center">{(i+1)*5}</div>'
        st.markdown(f'<div style="background:#111;border:1px solid #1f1f1f;border-radius:16px;padding:20px"><div style="display:flex;align-items:flex-end;gap:3px;height:80px">{bars}</div><div style="display:flex;gap:3px;margin-top:6px">{labels}</div><div style="font-size:10px;color:#333;margin-top:4px;text-align:center">Minutes</div></div>', unsafe_allow_html=True)

    elif tab == "Speed":
        st.markdown('<div class="section-title">Speed</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1: st.markdown(metric("Max Speed", s["max_speed"], "km/h", arrow(s["max_speed"], avg_speed, ".1f")), unsafe_allow_html=True)
        with c2: st.markdown(metric("Sprints", s["sprints"], "total", arrow(s["sprints"], avg_sprint, ".0f")), unsafe_allow_html=True)

        st.markdown('<div class="section-title">Accelerations & Decelerations</div>', unsafe_allow_html=True)
        c3,c4 = st.columns(2)
        with c3: st.markdown(metric("Accels", s["accels"], "over 3m/s²", arrow(s["accels"], avg_accels, ".0f")), unsafe_allow_html=True)
        with c4: st.markdown(metric("Decels", s["decels"], "over 3m/s²", arrow(s["decels"], avg_decels, ".0f")), unsafe_allow_html=True)

        st.markdown('<div class="section-title">Step Balance</div>', unsafe_allow_html=True)
        lf = s["left_foot"]
        rf = s["right_foot"]
        balance_diff = abs(lf - rf)
        balance_note = "Perfect balance" if balance_diff <= 2 else f"{'Left' if lf > rf else 'Right'} foot dominant — monitor if difference grows" 
        st.markdown(f"""<div class="balance-bar-container">
            <div class="balance-row">
                <div><div class="balance-foot">Left Foot</div><div class="balance-value">{lf}</div></div>
                <div style="text-align:right"><div class="balance-foot">Right Foot</div><div class="balance-value">{rf}</div></div>
            </div>
            <div class="bar-track">
                <div class="bar-left" style="width:{lf}%"></div>
                <div class="bar-right" style="width:{rf}%"></div>
            </div>
            <p style="font-size:12px;color:#555;margin:8px 0 0 0">ℹ {balance_note}. Ideal is 50:50. Differences of +/- 4 may indicate an underlying issue.</p>
        </div>""", unsafe_allow_html=True)

    elif tab == "Cardio":
        st.markdown('<div class="section-title">Training Stress</div>', unsafe_allow_html=True)
        avg_stress = average("stress")
        st.markdown(metric("Training Stress", s["stress"], "points", arrow(s["stress"], avg_stress, ".0f")), unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#444">Training Stress measures the overall physical demand of a session — combining duration and intensity into a single score. Higher = more demanding.</p>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Fatigue</div>', unsafe_allow_html=True)
        avg_fatigue = average("fatigue_min")
        st.markdown(metric("Fatigue Onset", f'Min {s["fatigue_min"]}', "", arrow(s["fatigue_min"], avg_fatigue, ".0f", " min")), unsafe_allow_html=True)
        if s["fatigue_min"] < 40:
            st.markdown('<div class="alert-bar">⚠ Fatigue set in early — elevated injury risk in the final quarter. Prioritise recovery before your next session.</div>', unsafe_allow_html=True)
        elif s["fatigue_min"] < 50:
            st.markdown('<div class="alert-bar">⚠ Fatigue detected in the second half — monitor recovery.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-bar-green">✓ Good endurance — fatigue only in the final minutes.</div>', unsafe_allow_html=True)

# ── INJURY RISK ───────────────────────────────────────────────────────────────

elif page == "🛡  Injury Risk":
    st.markdown("# Injury Risk")

    loads   = [s["stress"] for s in sessions]
    acute   = sum(loads[-4:])
    chronic = sum(loads) / (len(loads) / 4)
    ratio   = acute / chronic

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(metric("Acute Load", acute, "last 4 sessions"), unsafe_allow_html=True)
    with c2: st.markdown(metric("Chronic Load", f"{chronic:.0f}", "4 week avg"), unsafe_allow_html=True)
    with c3: st.markdown(metric("A:C Ratio", f"{ratio:.2f}", "safe: 0.8–1.3"), unsafe_allow_html=True)

    st.markdown('<div class="section-title">Workload Status</div>', unsafe_allow_html=True)
    if ratio > 1.5:
        st.markdown('<div class="alert-bar">🔴 HIGH RISK — Training load has spiked dangerously. Reduce intensity immediately.</div>', unsafe_allow_html=True)
    elif ratio > 1.3:
        st.markdown('<div class="alert-bar">🟡 CAUTION — Approaching the danger zone. Keep next session light.</div>', unsafe_allow_html=True)
    elif ratio >= 0.8:
        st.markdown('<div class="alert-bar-green">🟢 SWEET SPOT — Training load is optimal. Keep it up.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-bar">🔵 UNDERTRAINING — Load is too low. Gradually increase intensity.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">What Could Get You Injured</div>', unsafe_allow_html=True)
    fatigues = [s["fatigue_min"] for s in sessions]
    all_incidents = [i for s in sessions for i in s["incidents"]]

    if fatigues[-1] < fatigues[0] - 10:
        st.markdown('<div class="alert-bar">⚠ <strong style="color:white">Fatigue hitting earlier each session</strong> — Your body isn\'t recovering fully. Hamstring and ankle risk elevated in the final quarter.</div>', unsafe_allow_html=True)
    if len(all_incidents) >= 3:
        st.markdown('<div class="alert-bar">⚠ <strong style="color:white">Recurring incidents detected</strong> — Multiple movement spikes across recent sessions. This pattern often precedes soft tissue injury.</div>', unsafe_allow_html=True)
    if loads[-1] > sum(loads[:-1]) / len(loads[:-1]) * 1.3:
        st.markdown('<div class="alert-bar">⚠ <strong style="color:white">Last session was a big spike</strong> — A sudden jump in training stress is the single biggest predictor of injury in GAA players.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Areas to Watch</div>', unsafe_allow_html=True)
    cols = st.columns(len(profile["injuries"]))
    for i, inj in enumerate(profile["injuries"]):
        with cols[i]:
            st.markdown(f'<div class="metric-block"><div class="metric-label">Watch</div><div style="font-size:20px;font-weight:900;color:white;margin-top:8px">{inj}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Recommended Next Session</div>', unsafe_allow_html=True)
    target = round(sum(loads) / len(loads) * 0.8)
    st.markdown(f'<div class="alert-bar-green">✓ Keep training stress below <strong style="color:#00e676">{target} pts</strong> in your next session.</div>', unsafe_allow_html=True)

# ── INCIDENTS ─────────────────────────────────────────────────────────────────

elif page == "⚠  Incidents":
    st.markdown("# Incident Log")
    total = sum(len(s["incidents"]) for s in sessions)
    st.markdown(f'<p style="color:#555;font-size:12px">{total} INCIDENTS LOGGED ACROSS ALL SESSIONS</p>', unsafe_allow_html=True)

    for s in reversed(sessions):
        if s["incidents"]:
            risk_colour = {"LOW":"#00e676","MODERATE":"#f59e0b","HIGH":"#ef4444"}.get(s["risk"],"white")
            st.markdown(f'<div style="color:{risk_colour};font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin:20px 0 8px">{s["date"]} · {s["type"]} · {len(s["incidents"])} incident(s)</div>', unsafe_allow_html=True)
            for inc in s["incidents"]:
                with st.expander(f"📋 {inc}"):
                    st.markdown(f"""
                    <div style="font-size:13px;color:#888;line-height:1.8">
                        <strong style="color:white">What happened:</strong> {inc}<br>
                        <strong style="color:white">Why it matters:</strong> Sudden movement spikes increase soft tissue injury risk, especially when combined with fatigue.<br>
                        <strong style="color:white">What to do:</strong> Monitor the affected area. If soreness persists beyond 24 hours, consult a physio.
                    </div>""", unsafe_allow_html=True)

    if total == 0:
        st.markdown('<div class="alert-bar-green">✓ No incidents logged yet. Keep training!</div>', unsafe_allow_html=True)