import streamlit as st
from calculate_distance import haversine, total_distance
from speed import analyse_session, classify_zone

st.set_page_config(page_title="SportSense", page_icon="⚡", layout="wide")

# ── THEME ─────────────────────────────────────────────────────────────────────

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Barlow+Condensed:wght@600;700&display=swap" rel="stylesheet">
<style>
  .stApp { background: #F5F7FA !important; }
  section[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 0.5px solid rgba(0,0,0,0.08); }
  #MainMenu, footer, header { visibility: hidden; }

  * { font-family: 'DM Sans', system-ui, sans-serif !important; }

  :root {
    --blue:       #1565C0;
    --blue-light: #E3F0FF;
    --blue-mid:   #1976D2;
    --blue-acc:   #2196F3;
    --text:       #0D1B2A;
    --muted:      #6B7A8D;
    --card:       #FFFFFF;
    --border:     rgba(0,0,0,0.08);
    --red:        #C62828;
    --red-bg:     #FFEBEE;
    --amber:      #E65100;
    --amber-bg:   #FFF3E0;
    --green:      #2E7D32;
    --green-bg:   #E8F5E9;
  }

  h1, h2, h3 { color: var(--text) !important; font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important; }
  p, li { color: var(--muted); font-size: 13px; }

  /* Sidebar nav */
  .css-1d391kg, [data-testid="stSidebarNav"] a {
    color: var(--text) !important;
  }

  .top-bar {
    background: var(--blue);
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 12px;
    margin-bottom: 20px;
  }
  .logo {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    letter-spacing: 1px;
  }
  .logo span { color: #90CAF9; }
  .top-tag {
    font-size: 11px;
    color: #90CAF9;
    background: rgba(255,255,255,0.12);
    padding: 3px 12px;
    border-radius: 20px;
    font-weight: 500;
  }

  .metric-card {
    background: var(--card);
    border: 0.5px solid var(--border);
    border-radius: 12px;
    padding: 16px 14px;
    text-align: center;
    margin-bottom: 10px;
  }
  .metric-label {
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
    margin-bottom: 6px;
  }
  .metric-value {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 36px;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
  }
  .metric-unit { font-size: 11px; color: var(--muted); margin-top: 4px; }
  .metric-up   { font-size: 12px; color: var(--green); font-weight: 600; margin-top: 4px; }
  .metric-down { font-size: 12px; color: var(--red);   font-weight: 600; margin-top: 4px; }

  .section-label {
    font-size: 10px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 20px 0 8px;
  }

  .badge { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; }
  .badge-red    { background: var(--red-bg);   color: var(--red);   }
  .badge-amber  { background: var(--amber-bg); color: var(--amber); }
  .badge-green  { background: var(--green-bg); color: var(--green); }
  .badge-blue   { background: var(--blue-light); color: var(--blue); }

  .alert-card {
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 500;
    line-height: 1.5;
  }
  .alert-red   { background: var(--red-bg);    color: #7B1010; border-left: 3px solid var(--red);   }
  .alert-amber { background: var(--amber-bg);  color: #7B3000; border-left: 3px solid var(--amber); }
  .alert-green { background: var(--green-bg);  color: #1A4D1D; border-left: 3px solid var(--green); }
  .alert-blue  { background: var(--blue-light); color: #0D3470; border-left: 3px solid var(--blue); }

  .sense-hero {
    background: var(--blue);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .sense-score {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 64px;
    font-weight: 700;
    color: #fff;
    line-height: 1;
  }
  .sense-sub { font-size: 12px; color: #90CAF9; margin-top: 2px; }

  .session-card {
    background: var(--card);
    border: 0.5px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
  }
  .incident-card {
    background: var(--card);
    border-radius: 10px;
    border: 0.5px solid var(--border);
    padding: 12px 16px;
    margin-bottom: 8px;
  }
  .incident-card.red   { border-left: 3px solid var(--red);   }
  .incident-card.amber { border-left: 3px solid var(--amber); }
  .incident-card.blue  { border-left: 3px solid var(--blue);  }

  .pb-card {
    background: var(--card);
    border: 0.5px solid var(--border);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
  }
  .pb-num {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 28px;
    font-weight: 700;
    color: var(--text);
  }
  .pb-lbl { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

  .step-track {
    background: var(--blue-light);
    border-radius: 5px;
    height: 10px;
    overflow: hidden;
    margin: 4px 0 10px;
  }
  .step-fill-l { background: var(--blue);    height: 100%; border-radius: 5px 0 0 5px; }
  .step-fill-r { background: #90CAF9; height: 100%; border-radius: 0 5px 5px 0; }

  .ac-track {
    width: 100%;
    height: 8px;
    background: var(--blue-light);
    border-radius: 4px;
    position: relative;
    margin: 10px 0 4px;
  }
  .ac-safe {
    position: absolute;
    left: 40%;
    width: 25%;
    top: 0; height: 100%;
    background: rgba(46,125,50,0.2);
    border-radius: 2px;
  }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────

sessions = [
    {"date":"19 Mar","type":"Match",    "distance":9800, "max_speed":29.8,
     "sprints":28,"hi_distance":2890,"stress":600,"fatigue_min":38,
     "risk":"HIGH","accels":35,"decels":33,"left_foot":56,"right_foot":44,
     "incidents":["Heavy landing — left knee","Step imbalance — minute 38"]},
    {"date":"14 Mar","type":"Training", "distance":6200, "max_speed":26.1,
     "sprints":14,"hi_distance":1540,"stress":380,"fatigue_min":44,
     "risk":"MODERATE","accels":21,"decels":20,"left_foot":51,"right_foot":49,
     "incidents":["Speed drop >15% — fatigue flagged"]},
    {"date":"7 Mar", "type":"Match",    "distance":9400, "max_speed":28.7,
     "sprints":24,"hi_distance":2610,"stress":560,"fatigue_min":52,
     "risk":"MODERATE","accels":30,"decels":29,"left_foot":53,"right_foot":47,
     "incidents":["Workload spike — 1.2× weekly average"]},
    {"date":"1 Mar", "type":"Training", "distance":5800, "max_speed":24.9,
     "sprints":11,"hi_distance":1230,"stress":320,"fatigue_min":58,
     "risk":"LOW","accels":17,"decels":16,"left_foot":50,"right_foot":50,
     "incidents":[]},
]

profile = {
    "name":        "Gaelic Football",
    "sprint_kmh":  25,
    "hi_kmh":      20,
    "match_km":    10,
    "injuries":    ["Hamstring","Knee","Ankle","Groin"],
}

def average(key):
    vals = [s[key] for s in sessions]
    return sum(vals) / len(vals)

def metric(label, value, unit="", change_html=""):
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-unit">{unit}</div>
      {change_html}
    </div>"""

def arrow(now, avg, fmt=".0f", suffix=""):
    diff = now - avg
    sym  = "▲" if diff >= 0 else "▼"
    cls  = "metric-up" if diff >= 0 else "metric-down"
    return f'<div class="{cls}">{sym} {abs(diff):{fmt}}{suffix} vs avg</div>'

# ── SIDEBAR NAV ───────────────────────────────────────────────────────────────

st.sidebar.markdown("""
<div style="padding:12px 0 20px;">
  <div style="font-family:'Barlow Condensed',sans-serif;font-size:20px;font-weight:700;color:#1565C0;letter-spacing:1px;">
    SPORT<span style="color:#6B7A8D;">SENSE</span>
  </div>
  <div style="font-size:11px;color:#6B7A8D;margin-top:2px;">Gaelic Football</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["🏠  Home", "📋  Activity", "🛡  Injury Risk", "⚠  Incidents"],
    label_visibility="collapsed",
)

# ── HOME ──────────────────────────────────────────────────────────────────────

if page == "🏠  Home":
    s = sessions[-1]

    # Sense Score
    loads   = [x["stress"] for x in sessions]
    acute   = sum(loads[-4:])
    chronic = sum(loads) / (len(loads) / 4)
    ratio   = round(acute / chronic, 2)
    sense   = min(100, max(0, round(
        (s["distance"] / 100) +
        (s["max_speed"] * 0.5) +
        (s["sprints"]   * 1.2) -
        max(0, (ratio - 1.3) * 40)
    )))

    risk_badge = {
        "HIGH":     '<span class="badge badge-red">HIGH RISK</span>',
        "MODERATE": '<span class="badge badge-amber">MODERATE RISK</span>',
        "LOW":      '<span class="badge badge-green">LOW RISK</span>',
    }.get(s["risk"], "")

    st.markdown(f"""
    <div class="sense-hero">
      <div>
        <div style="font-size:12px;color:#90CAF9;font-weight:500;margin-bottom:2px;">Sense Score</div>
        <div class="sense-score">{sense}</div>
        <div class="sense-sub">Good performance · {s['date']} {s['type']}</div>
        <div style="margin-top:10px;">{risk_badge}</div>
      </div>
      <svg width="80" height="80" viewBox="0 0 80 80">
        <circle cx="40" cy="40" r="32" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="6"/>
        <circle cx="40" cy="40" r="32" fill="none" stroke="#90CAF9" stroke-width="6"
          stroke-dasharray="201" stroke-dashoffset="{int(201 * (1 - sense/100))}"
          stroke-linecap="round" transform="rotate(-90 40 40)"/>
        <text x="40" y="44" text-anchor="middle" fill="#fff" font-size="18"
          font-family="Barlow Condensed" font-weight="700">{sense}</text>
      </svg>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Last session</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(metric("Distance",  f'{s["distance"]/1000:.1f}', "km"),  unsafe_allow_html=True)
    with c2: st.markdown(metric("Max Speed", s["max_speed"], "km/h"),              unsafe_allow_html=True)
    with c3: st.markdown(metric("Sprints",   s["sprints"],   "total"),             unsafe_allow_html=True)
    with c4: st.markdown(metric("A:C Ratio", ratio, "workload",
        f'<div class="{"metric-down" if ratio > 1.3 else "metric-up"}">'
        f'{"DANGER" if ratio > 1.5 else "CAUTION" if ratio > 1.3 else "SAFE"}</div>'),
        unsafe_allow_html=True)

    st.markdown('<div class="section-label">Personal bests</div>', unsafe_allow_html=True)
    pb_speed    = max(s["max_speed"]    for s in sessions)
    pb_dist     = max(s["distance"]     for s in sessions)
    pb_sprints  = max(s["sprints"]      for s in sessions)
    pb_hi       = max(s["hi_distance"]  for s in sessions)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f'<div class="pb-card"><div class="pb-lbl">Max Speed</div><div class="pb-num">{pb_speed}</div><div class="pb-lbl">km/h</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="pb-card"><div class="pb-lbl">Distance</div><div class="pb-num">{pb_dist/1000:.1f}</div><div class="pb-lbl">km</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="pb-card"><div class="pb-lbl">Sprints</div><div class="pb-num">{pb_sprints}</div><div class="pb-lbl">session</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="pb-card"><div class="pb-lbl">HI Distance</div><div class="pb-num">{pb_hi/1000:.1f}</div><div class="pb-lbl">km</div></div>', unsafe_allow_html=True)

# ── ACTIVITY ──────────────────────────────────────────────────────────────────

elif page == "📋  Activity":
    st.markdown("# Activity")

    selected = st.selectbox("Session", [f"{s['date']} — {s['type']}" for s in reversed(sessions)])
    s = next(x for x in sessions if f"{x['date']} — {x['type']}" == selected)

    tab = st.radio("", ["Volume", "Speed", "Load"], horizontal=True)

    avg_dist   = average("distance")
    avg_speed  = average("max_speed")
    avg_sprint = average("sprints")
    avg_hi     = average("hi_distance")
    avg_accels = average("accels")
    avg_decels = average("decels")

    if tab == "Volume":
        st.markdown('<div class="section-label">Volume</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.markdown(metric("Total Distance",   f'{s["distance"]/1000:.1f}', "km", arrow(s["distance"], avg_dist, ".0f", " m")), unsafe_allow_html=True)
        with c2: st.markdown(metric("HI Distance",      f'{s["hi_distance"]/1000:.2f}', "km", arrow(s["hi_distance"], avg_hi, ".0f", " m")), unsafe_allow_html=True)

        dist_per_min = round(s["distance"] / 70)
        st.markdown(metric("Distance Per Min", dist_per_min, "m/min"), unsafe_allow_html=True)

        st.markdown('<div class="section-label">5-min breakdown</div>', unsafe_allow_html=True)
        blocks = [820,790,870,810,760,840,800,750,780,820,710,680,650,600]
        max_b  = max(blocks)
        bars   = "".join(
            f'<div style="flex:1;background:{"#1565C0" if b>=750 else "#E65100" if b>=650 else "#C62828"};'
            f'height:{int(b/max_b*72)}px;border-radius:3px 3px 0 0;min-height:4px;"></div>'
            for b in blocks
        )
        labels = "".join(
            f'<div style="flex:1;font-size:8px;color:#6B7A8D;text-align:center;">{(i+1)*5}</div>'
            for i in range(len(blocks))
        )
        st.markdown(f"""
        <div style="background:#fff;border:0.5px solid rgba(0,0,0,0.08);border-radius:12px;padding:16px;">
          <div style="display:flex;align-items:flex-end;gap:3px;height:72px;">{bars}</div>
          <div style="display:flex;gap:3px;margin-top:4px;">{labels}</div>
          <div style="font-size:9px;color:#6B7A8D;text-align:center;margin-top:2px;">Minutes</div>
          <div style="display:flex;gap:14px;margin-top:8px;font-size:10px;">
            <span style="display:flex;align-items:center;gap:4px;">
              <span style="width:8px;height:8px;border-radius:2px;background:#1565C0;display:inline-block;"></span>Normal
            </span>
            <span style="display:flex;align-items:center;gap:4px;">
              <span style="width:8px;height:8px;border-radius:2px;background:#C62828;display:inline-block;"></span>High intensity
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

    elif tab == "Speed":
        st.markdown('<div class="section-label">Speed</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.markdown(metric("Max Speed", s["max_speed"], "km/h", arrow(s["max_speed"], avg_speed, ".1f")), unsafe_allow_html=True)
        with c2: st.markdown(metric("Sprints",   s["sprints"],   "total", arrow(s["sprints"], avg_sprint, ".0f")), unsafe_allow_html=True)

        st.markdown('<div class="section-label">Accelerations & decelerations</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3: st.markdown(metric("Accels", s["accels"], "over 3 m/s²", arrow(s["accels"], avg_accels, ".0f")), unsafe_allow_html=True)
        with c4: st.markdown(metric("Decels", s["decels"], "over 3 m/s²", arrow(s["decels"], avg_decels, ".0f")), unsafe_allow_html=True)

        st.markdown('<div class="section-label">Step balance</div>', unsafe_allow_html=True)
        lf, rf = s["left_foot"], s["right_foot"]
        diff   = abs(lf - rf)
        note   = "Balanced" if diff <= 2 else f"{'Left' if lf > rf else 'Right'} dominant — monitor if it grows"
        alert_cls = "alert-green" if diff <= 2 else "alert-amber" if diff <= 8 else "alert-red"
        st.markdown(f"""
        <div style="background:#fff;border:0.5px solid rgba(0,0,0,0.08);border-radius:12px;padding:14px 16px;">
          <div style="display:flex;justify-content:space-between;font-size:12px;color:#6B7A8D;margin-bottom:4px;">
            <span>Left foot <strong style="color:#0D1B2A;">{lf}%</strong></span>
            <span>Right foot <strong style="color:#0D1B2A;">{rf}%</strong></span>
          </div>
          <div class="step-track"><div class="step-fill-l" style="width:{lf}%;display:inline-block;"></div></div>
          <div class="alert-card {alert_cls}">{note}. Ideal is 50:50. Differences &gt; 4% may indicate an issue.</div>
        </div>""", unsafe_allow_html=True)

    elif tab == "Load":
        st.markdown('<div class="section-label">Training stress</div>', unsafe_allow_html=True)
        avg_stress  = average("stress")
        avg_fatigue = average("fatigue_min")
        c1, c2 = st.columns(2)
        with c1: st.markdown(metric("Stress Load",   s["stress"],      "points", arrow(s["stress"],      avg_stress,  ".0f")), unsafe_allow_html=True)
        with c2: st.markdown(metric("Fatigue Onset", f'Min {s["fatigue_min"]}', "", arrow(s["fatigue_min"], avg_fatigue, ".0f", " min")), unsafe_allow_html=True)

        if s["fatigue_min"] < 40:
            st.markdown('<div class="alert-card alert-red">Fatigue set in early — elevated injury risk in the final quarter. Prioritise recovery.</div>', unsafe_allow_html=True)
        elif s["fatigue_min"] < 50:
            st.markdown('<div class="alert-card alert-amber">Fatigue in the second half — monitor recovery before your next session.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-card alert-green">Good endurance — fatigue only in the final minutes.</div>', unsafe_allow_html=True)

# ── INJURY RISK ───────────────────────────────────────────────────────────────

elif page == "🛡  Injury Risk":
    st.markdown("# Injury Risk")

    loads   = [s["stress"] for s in sessions]
    acute   = sum(loads[-4:])
    chronic = sum(loads) / (len(loads) / 4)
    ratio   = round(acute / chronic, 2)

    if ratio > 1.5:
        status_html = '<div class="alert-card alert-red">HIGH RISK — Load has spiked dangerously. Reduce intensity immediately.</div>'
        badge_html  = '<span class="badge badge-red">DANGER ZONE</span>'
    elif ratio > 1.3:
        status_html = '<div class="alert-card alert-amber">CAUTION — Approaching the danger zone. Keep next session light.</div>'
        badge_html  = '<span class="badge badge-amber">CAUTION</span>'
    elif ratio >= 0.8:
        status_html = '<div class="alert-card alert-green">SWEET SPOT — Training load is optimal. Keep it up.</div>'
        badge_html  = '<span class="badge badge-green">OPTIMAL</span>'
    else:
        status_html = '<div class="alert-card alert-blue">UNDERTRAINING — Load is too low. Gradually increase intensity.</div>'
        badge_html  = '<span class="badge badge-blue">LOW</span>'

    # A:C ratio gauge
    needle_pct = min(100, round(ratio / 2.0 * 100))
    st.markdown(f"""
    <div style="background:#fff;border:0.5px solid rgba(0,0,0,0.08);border-radius:12px;padding:16px 18px;margin-bottom:12px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div>
          <div style="font-family:'Barlow Condensed',sans-serif;font-size:36px;font-weight:700;color:{'#C62828' if ratio>1.5 else '#E65100' if ratio>1.3 else '#2E7D32'};line-height:1;">{ratio}</div>
          <div style="font-size:11px;color:#6B7A8D;">A:C Ratio</div>
        </div>
        {badge_html}
      </div>
      <div class="ac-track">
        <div class="ac-safe"></div>
        <div style="position:absolute;top:-4px;left:{needle_pct}%;width:16px;height:16px;background:#1565C0;border:2px solid #fff;border-radius:50%;transform:translateX(-50%);box-shadow:0 1px 4px rgba(0,0,0,0.2);"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:9px;color:#6B7A8D;margin-top:4px;">
        <span>0.0</span><span>0.8</span><span>1.3</span><span>1.5</span><span>2.0</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(metric("Acute Load",   acute,          "last 4 sessions"), unsafe_allow_html=True)
    with c2: st.markdown(metric("Chronic Load", f"{chronic:.0f}", "4-week avg"),      unsafe_allow_html=True)
    with c3: st.markdown(metric("Spike",        f"+{round((loads[-1] / (sum(loads[:-1])/len(loads[:-1])) - 1)*100)}%", "vs avg session"), unsafe_allow_html=True)

    st.markdown('<div class="section-label">Workload status</div>', unsafe_allow_html=True)
    st.markdown(status_html, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Injury risk zones</div>', unsafe_allow_html=True)
    zones = [
        ("#C62828", "Hamstring",       "22–24% of GAA injuries"),
        ("#E65100", "Knee (non-contact)", "flagged this session"),
        ("#F9A825", "Ankle",           "risk rises after minute 47"),
        ("#1565C0", "Groin / hip",     "monitor step balance"),
    ]
    cols = st.columns(len(zones))
    for col, (colour, name, note) in zip(cols, zones):
        with col:
            st.markdown(f"""
            <div style="background:#fff;border:0.5px solid rgba(0,0,0,0.08);border-radius:10px;padding:12px;text-align:center;">
              <div style="width:10px;height:10px;border-radius:50%;background:{colour};margin:0 auto 6px;"></div>
              <div style="font-size:12px;font-weight:600;color:#0D1B2A;">{name}</div>
              <div style="font-size:10px;color:#6B7A8D;margin-top:2px;">{note}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Recommended next session</div>', unsafe_allow_html=True)
    target = round(sum(loads) / len(loads) * 0.8)
    st.markdown(f'<div class="alert-card alert-blue">Keep stress load below <strong>{target} pts</strong>. Light recovery only — no sprint work until ratio drops below 1.3.</div>', unsafe_allow_html=True)

# ── INCIDENTS ─────────────────────────────────────────────────────────────────

elif page == "⚠  Incidents":
    st.markdown("# Incident Log")
    total = sum(len(s["incidents"]) for s in sessions)
    st.markdown(f'<p>{total} incidents logged across all sessions</p>', unsafe_allow_html=True)

    for s in reversed(sessions):
        if not s["incidents"]:
            continue
        sev_cls = {"HIGH": "red", "MODERATE": "amber", "LOW": "blue"}.get(s["risk"], "blue")
        st.markdown(f"""
        <div style="font-size:10px;font-weight:600;color:#6B7A8D;text-transform:uppercase;letter-spacing:1px;margin:16px 0 6px;">
          {s['date']} · {s['type']} · {len(s['incidents'])} incident(s)
          &nbsp;<span class="badge badge-{sev_cls}">{s['risk']}</span>
        </div>""", unsafe_allow_html=True)
        for inc in s["incidents"]:
            with st.expander(inc):
                st.markdown(f"""
                <div style="font-size:13px;color:#6B7A8D;line-height:1.8;">
                  <strong style="color:#0D1B2A;">What happened:</strong> {inc}<br>
                  <strong style="color:#0D1B2A;">Why it matters:</strong> Sudden movement spikes increase soft tissue injury risk, especially combined with fatigue.<br>
                  <strong style="color:#0D1B2A;">What to do:</strong> Monitor the area. If soreness persists beyond 24 hours, consult a physio.
                </div>""", unsafe_allow_html=True)

    if total == 0:
        st.markdown('<div class="alert-card alert-green">No incidents logged yet. Keep training!</div>', unsafe_allow_html=True)
