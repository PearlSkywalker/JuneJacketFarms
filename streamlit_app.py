"""
Garden Command Center
streamlit_app.py — Botanical Modern UI · Seattle Weather · Daily Briefing
"""

import streamlit as st
import requests
from datetime import datetime

# ─── Page config (must be the very first Streamlit call) ─────────────────────
st.set_page_config(
    page_title="Garden Command Center",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Botanical Modern Design System (CSS) ─────────────────────────────────────
BOTANICAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --sage:         #718355;
    --sage-light:   #9aab74;
    --sage-muted:   #b8c9a0;
    --sage-dark:    #4f5e3a;
    --cream:        #F9F7F2;
    --cream-deep:   #edeade;
    --cream-border: #e0dbd0;
    --charcoal:     #2F2F2F;
    --charcoal-mid: #5a5a52;
    --muted:        #9a9a8a;
    --warning:      #b85c2a;
    --warning-bg:   #fdf0e8;
    --info-bg:      #f0f4ec;
    --white:        #ffffff;
    --radius:       14px;
    --radius-sm:    9px;
    --radius-pill:  99px;
    --shadow-sm:    0 1px 6px rgba(47,47,47,0.06);
    --shadow:       0 3px 18px rgba(47,47,47,0.09);
    --shadow-lg:    0 8px 40px rgba(47,47,47,0.13);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream) !important;
    color: var(--charcoal);
}

.main .block-container {
    padding: 2rem 2.5rem 5rem;
    max-width: 1100px;
}

h1, h2, h3, h4 {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 300;
    letter-spacing: 0.02em;
}

#MainMenu, header, footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

[data-testid="stSidebar"] {
    background: var(--charcoal) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 0 !important;
}

.brand-lockup {
    display: flex;
    align-items: center;
    gap: 11px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

.brand-hex {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, var(--sage) 0%, var(--sage-light) 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}

.brand-text-top {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: var(--cream) !important;
    line-height: 1;
}

.brand-text-sub {
    font-size: 0.58rem;
    letter-spacing: 0.22em;
    color: var(--sage-muted) !important;
    text-transform: uppercase;
    margin-top: 3px;
}

.nav-label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.3) !important;
    padding: 0 0.75rem;
    margin-bottom: 0.4rem;
    margin-top: 0.2rem;
}

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: rgba(249,247,242,0.65) !important;
    text-align: left !important;
    padding: 0.6rem 0.8rem !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.84rem !important;
    font-weight: 400 !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(113,131,85,0.2) !important;
    color: var(--cream) !important;
}

.sidebar-footer-text {
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    color: rgba(255,255,255,0.2) !important;
    padding: 0 0.5rem;
    margin-top: auto;
    padding-top: 2rem;
}

.page-eyebrow {
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--sage);
    margin-bottom: 6px;
}

.page-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.6rem;
    font-weight: 300;
    color: var(--charcoal);
    margin: 0 0 0.2rem 0;
    line-height: 1.05;
}

.page-subtitle {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 0;
    letter-spacing: 0.01em;
}

.page-divider {
    border: none;
    border-top: 1px solid var(--cream-border);
    margin: 1.2rem 0 2rem 0;
}

.weather-card {
    background: linear-gradient(145deg, #4f5e3a 0%, #718355 55%, #8a9e66 100%);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
    margin-bottom: 0;
}

.weather-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}

.weather-card::after {
    content: '';
    position: absolute;
    bottom: -60px; right: 40px;
    width: 220px; height: 220px;
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
}

.weather-location {
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.65);
    margin-bottom: 0.6rem;
}

.weather-main {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
}

.weather-emoji-large {
    font-size: 3rem;
    line-height: 1;
    margin-top: 4px;
}

.weather-temp {
    font-family: 'Cormorant Garamond', serif;
    font-size: 4rem;
    font-weight: 300;
    color: white;
    line-height: 1;
}

.weather-desc {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.85);
    margin-top: 2px;
    font-weight: 300;
}

.weather-meta {
    display: flex;
    gap: 1.4rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.15);
}

.weather-meta-item {
    display: flex;
    flex-direction: column;
}

.weather-meta-val {
    font-size: 0.88rem;
    color: white;
    font-weight: 500;
}

.weather-meta-lbl {
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-top: 1px;
}

.rain-banner {
    background: rgba(113,131,85,0.1);
    border: 1px solid rgba(113,131,85,0.25);
    border-left: 3px solid var(--sage);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: var(--sage-dark);
    display: flex;
    align-items: center;
    gap: 8px;
}

.warn-banner {
    background: var(--warning-bg);
    border: 1px solid rgba(184,92,42,0.2);
    border-left: 3px solid var(--warning);
    border-radius: var(--radius-sm);
    padding: 0.75rem 1rem;
    font-size: 0.82rem;
    color: var(--warning);
}

.section-heading {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.25rem;
    font-weight: 400;
    color: var(--charcoal);
    margin: 0 0 1rem 0;
    letter-spacing: 0.02em;
}

.task-card {
    background: var(--white);
    border: 1px solid var(--cream-border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 0.65rem;
}

.task-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.35rem;
}

.task-name {
    font-weight: 500;
    font-size: 0.9rem;
    color: var(--charcoal);
}

.task-badge {
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    background: var(--info-bg);
    color: var(--sage-dark);
    padding: 3px 10px;
    border-radius: var(--radius-pill);
    border: 1px solid rgba(113,131,85,0.2);
}

.task-badge.urgent {
    background: var(--warning-bg);
    color: var(--warning);
    border-color: rgba(184,92,42,0.2);
}

.task-meta {
    font-size: 0.75rem;
    color: var(--muted);
}

.task-placeholder {
    background: var(--white);
    border: 1.5px dashed var(--cream-border);
    border-radius: var(--radius);
    padding: 2rem 1.4rem;
    text-align: center;
}

.task-placeholder-icon {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}

.task-placeholder-text {
    font-size: 0.82rem;
    color: var(--muted);
}

.task-placeholder-sub {
    font-size: 0.72rem;
    color: var(--cream-border);
    margin-top: 4px;
}

.stats-strip {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 0;
}

.stat-tile {
    background: var(--white);
    border: 1px solid var(--cream-border);
    border-radius: var(--radius);
    padding: 1.1rem 1.25rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
}

.stat-icon { font-size: 1.2rem; margin-bottom: 0.4rem; }

.stat-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 400;
    color: var(--sage-dark);
    line-height: 1;
}

.stat-label {
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 4px;
}

.coming-soon {
    background: var(--white);
    border: 1px solid var(--cream-border);
    border-radius: var(--radius);
    padding: 3rem 2rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
}

.coming-soon-icon { font-size: 2.5rem; margin-bottom: 1rem; }

.coming-soon-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 300;
    color: var(--charcoal);
    margin-bottom: 0.5rem;
}

.coming-soon-text { font-size: 0.82rem; color: var(--muted); }
"""

st.markdown(f"<style>{BOTANICAL_CSS}</style>", unsafe_allow_html=True)


# ─── Weather helper (Open-Meteo — free, no API key required) ─────────────────
WMO_CODES = {
    0:  ("Clear sky", "☀️"),
    1:  ("Mainly clear", "🌤️"),
    2:  ("Partly cloudy", "⛅"),
    3:  ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Icy fog", "🌫️"),
    51: ("Light drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy drizzle", "🌧️"),
    61: ("Light rain", "🌧️"),
    63: ("Rain", "🌧️"),
    65: ("Heavy rain", "🌧️"),
    71: ("Light snow", "🌨️"),
    73: ("Snow", "❄️"),
    75: ("Heavy snow", "❄️"),
    80: ("Rain showers", "🌦️"),
    81: ("Showers", "🌧️"),
    82: ("Violent showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    99: ("Severe thunderstorm", "⛈️"),
}


@st.cache_data(ttl=1800)
def fetch_seattle_weather():
    """Fetch today's Seattle weather from Open-Meteo. Cached for 30 minutes."""
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=47.6062&longitude=-122.3321"
            "&daily=weathercode,temperature_2m_max,temperature_2m_min"
            ",precipitation_sum,windspeed_10m_max"
            "&temperature_unit=fahrenheit"
            "&precipitation_unit=inch"
            "&windspeed_unit=mph"
            "&timezone=America%2FLos_Angeles"
            "&forecast_days=1"
        )
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        d = r.json()["daily"]
        code = d["weathercode"][0]
        desc, emoji = WMO_CODES.get(code, ("Unknown", "🌡️"))
        precip = d["precipitation_sum"][0] or 0.0
        return {
            "temp_high":   d["temperature_2m_max"][0],
            "temp_low":    d["temperature_2m_min"][0],
            "precip_in":   round(precip, 2),
            "wind_mph":    d["windspeed_10m_max"][0],
            "description": desc,
            "emoji":       emoji,
            "rain_heavy":  precip >= 0.5,
        }
    except Exception:
        return None


# ─── Session state ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "briefing"


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
            <div class="brand-hex">🌿</div>
            <div>
                <div class="brand-text-top">GARDEN</div>
                <div class="brand-text-sub">Command Center</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)

    nav = {
        "briefing": ("🏠", "Daily Briefing"),
        "vault":    ("🌱", "Plant Vault"),
        "map":      ("🗺️", "Garden Map"),
        "harvest":  ("🌾", "Harvest Log"),
    }

    for key, (icon, label) in nav.items():
        if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown(
        f'<div class="sidebar-footer-text">Seattle, WA · {datetime.now().strftime("%b %d, %Y")}</div>',
        unsafe_allow_html=True,
    )


# ─── Route to the active page ─────────────────────────────────────────────────
page = st.session_state.page


# ══════════════════════════════════════════════════════════════════════════════
# DAILY BRIEFING
# ══════════════════════════════════════════════════════════════════════════════
if page == "briefing":

    today = datetime.now()
    hour = today.hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    st.markdown(
        f"""
        <div class="page-eyebrow">{greeting} · {today.strftime("%A, %B %-d, %Y")}</div>
        <h1 class="page-title">Daily Briefing</h1>
        <p class="page-subtitle">Your garden at a glance — weather, tasks, and what needs attention today.</p>
        <hr class="page-divider">
        """,
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1.65, 1], gap="large")

    # ── Left column ───────────────────────────────────────────────────────────
    with col_left:

        weather = fetch_seattle_weather()

        if weather:
            st.markdown(
                f"""
                <div class="weather-card">
                    <div class="weather-location">📍 Seattle, Washington</div>
                    <div class="weather-main">
                        <div class="weather-emoji-large">{weather['emoji']}</div>
                        <div>
                            <div class="weather-temp">{weather['temp_high']:.0f}°F</div>
                            <div class="weather-desc">{weather['description']}</div>
                        </div>
                    </div>
                    <div class="weather-meta">
                        <div class="weather-meta-item">
                            <span class="weather-meta-val">↓ {weather['temp_low']:.0f}°F</span>
                            <span class="weather-meta-lbl">Low</span>
                        </div>
                        <div class="weather-meta-item">
                            <span class="weather-meta-val">{weather['precip_in']:.2f}"</span>
                            <span class="weather-meta-lbl">Precipitation</span>
                        </div>
                        <div class="weather-meta-item">
                            <span class="weather-meta-val">{weather['wind_mph']:.0f} mph</span>
                            <span class="weather-meta-lbl">Wind</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if weather["rain_heavy"]:
                st.markdown(
                    """
                    <div class="rain-banner" style="margin-top:0.75rem">
                        🌧️ <strong>Watering suppressed</strong> — ≥0.5" of rain forecast.
                        Outdoor watering tasks pushed back 48 hours automatically.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="warn-banner">⚡ Could not reach weather service. Check your connection.</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Tasks section
        st.markdown('<p class="section-heading">📋 Today\'s Tasks</p>', unsafe_allow_html=True)

        # Placeholder tasks — replaced by live DB queries in the next sprint
        PLACEHOLDER_TASKS = [
            {
                "name":   "Water raised bed A",
                "type":   "Water",
                "meta":   "Kale · Beets · Lettuce",
                "urgent": False,
            },
            {
                "name":   "Fertilize Monstera deliciosa",
                "type":   "Fertilize",
                "meta":   "Living room · Node 7",
                "urgent": False,
            },
            {
                "name":   "Check Peperomia cuttings",
                "type":   "Propagation",
                "meta":   "Started 14 days ago · Water medium",
                "urgent": False,
            },
            {
                "name":   "Treat aphids — Strawberries",
                "type":   "Pest",
                "meta":   "Bed C · Overdue 1 day",
                "urgent": True,
            },
        ]

        for task in PLACEHOLDER_TASKS:
            badge_class = "task-badge urgent" if task["urgent"] else "task-badge"
            st.markdown(
                f"""
                <div class="task-card">
                    <div class="task-header">
                        <span class="task-name">{task['name']}</span>
                        <span class="{badge_class}">{task['type']}</span>
                    </div>
                    <div class="task-meta">{task['meta']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="task-placeholder">
                <div class="task-placeholder-icon">🗓️</div>
                <div class="task-placeholder-text">Live tasks will load from your database once connected.</div>
                <div class="task-placeholder-sub">Plant Vault → Care Engine → Daily Briefing</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Right column ──────────────────────────────────────────────────────────
    with col_right:

        st.markdown('<p class="section-heading">📊 Garden at a Glance</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="stats-strip">
                <div class="stat-tile">
                    <div class="stat-icon">🌱</div>
                    <div class="stat-value">—</div>
                    <div class="stat-label">Plants</div>
                </div>
                <div class="stat-tile">
                    <div class="stat-icon">✂️</div>
                    <div class="stat-value">—</div>
                    <div class="stat-label">Cuttings</div>
                </div>
                <div class="stat-tile">
                    <div class="stat-icon">🌾</div>
                    <div class="stat-value">—</div>
                    <div class="stat-label">Lbs Harvested</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-heading">⚠️ Needs Attention</p>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="warn-banner">
                🐾 <strong>Pothos aureus</strong> is <em>toxic to dogs.</em> Keep out of reach.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="task-placeholder" style="padding:1.5rem 1rem">
                <div class="task-placeholder-icon">🩺</div>
                <div class="task-placeholder-text">No active health alerts.</div>
                <div class="task-placeholder-sub">Alerts populate from Health Diagnostic Log</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p class="section-heading">🌿 Quick Note</p>', unsafe_allow_html=True)
        note = st.text_area(
            label="quick_note",
            placeholder="Jot something down… noticed new growth on the Monstera, need more perlite…",
            height=110,
            label_visibility="collapsed",
        )
        if st.button("Save Note", type="primary", use_container_width=True):
            if note.strip():
                st.success("Note saved! (Connect to database to persist.)")
            else:
                st.warning("Nothing to save — write something first.")


# ══════════════════════════════════════════════════════════════════════════════
# PLANT VAULT (stub — built out in next sprint)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "vault":
    st.markdown(
        """
        <div class="page-eyebrow">Module 1</div>
        <h1 class="page-title">Plant Vault</h1>
        <hr class="page-divider">
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="coming-soon">
            <div class="coming-soon-icon">🌱</div>
            <div class="coming-soon-title">Plant Vault</div>
            <div class="coming-soon-text">
                Full seed and plant library with dog-safety indicators, sun-spec tags,
                and variety tracking. Coming in the next sprint.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# GARDEN MAP (stub — built out in next sprint)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "map":
    st.markdown(
        """
        <div class="page-eyebrow">Module 2</div>
        <h1 class="page-title">Garden Map</h1>
        <hr class="page-divider">
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="coming-soon">
            <div class="coming-soon-icon">🗺️</div>
            <div class="coming-soon-title">Tactical Bed Planner</div>
            <div class="coming-soon-text">
                Visual grid bed mapper with drag-and-drop plant placement
                and sun-compatibility alerts. Coming soon.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# HARVEST LOG (stub — built out in next sprint)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "harvest":
    st.markdown(
        """
        <div class="page-eyebrow">Module 3</div>
        <h1 class="page-title">Harvest Log</h1>
        <hr class="page-divider">
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="coming-soon">
            <div class="coming-soon-icon">🌾</div>
            <div class="coming-soon-title">Harvest Dashboard</div>
            <div class="coming-soon-text">
                Weight logger for kale, beets, strawberries and more —
                plus an ROI calculator showing money saved vs. local organic prices.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
