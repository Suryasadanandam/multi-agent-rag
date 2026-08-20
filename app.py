import streamlit as st
from agent import search_agent, summarize_agent, report_agent
from utils import format_report

st.set_page_config(
    page_title="ARIA — Research Intelligence",
    page_icon="⬡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Outfit:wght@300;400;600;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body { background: #030712; }

[data-testid="stAppViewContainer"] {
    background: #030712;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(56,189,248,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(99,102,241,0.06) 0%, transparent 50%);
    font-family: 'Outfit', sans-serif;
    color: #f1f5f9;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stMain"] > div { padding-top: 2rem; }

.hero-wrap { text-align: center; padding: 3rem 0 1.5rem; }

.aria-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 4px;
    color: #38bdf8;
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 100px;
    padding: 6px 18px;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 900;
    font-size: 5rem;
    letter-spacing: -4px;
    line-height: 1;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #f8fafc 30%, #38bdf8 65%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: #475569;
    letter-spacing: 1px;
    margin-bottom: 2.5rem;
}

.pipeline {
    display: flex;
    align-items: stretch;
    gap: 0;
    margin: 2.5rem 0;
}

.pipe-node {
    flex: 1;
    background: #0c1526;
    border: 1px solid #1e293b;
    padding: 1.8rem 1.5rem;
    position: relative;
    transition: all 0.4s ease;
}

.pipe-node:first-child { border-radius: 16px 0 0 16px; }
.pipe-node:last-child { border-radius: 0 16px 16px 0; }

.pipe-node::after {
    content: '›';
    position: absolute;
    right: -14px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.8rem;
    color: #1e293b;
    z-index: 2;
}
.pipe-node:last-child::after { display: none; }

.pipe-node.s1 { border-top: 2px solid #0ea5e9; }
.pipe-node.s2 { border-top: 2px solid #6366f1; }
.pipe-node.s3 { border-top: 2px solid #10b981; }

.pipe-node.active {
    background: #0f1f38;
    box-shadow: 0 0 40px rgba(56,189,248,0.08), inset 0 1px 0 rgba(56,189,248,0.15);
    transform: translateY(-4px);
    z-index: 1;
}
.pipe-node.s2.active { box-shadow: 0 0 40px rgba(99,102,241,0.08), inset 0 1px 0 rgba(99,102,241,0.15); }
.pipe-node.s3.active { box-shadow: 0 0 40px rgba(16,185,129,0.08), inset 0 1px 0 rgba(16,185,129,0.15); }
.pipe-node.done { opacity: 0.55; }

.node-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #334155;
    letter-spacing: 3px;
    margin-bottom: 1rem;
}

.node-icon { font-size: 1.6rem; margin-bottom: 0.8rem; display: block; }

.node-title { font-weight: 700; font-size: 1.05rem; margin-bottom: 0.5rem; }
.pipe-node.s1 .node-title { color: #38bdf8; }
.pipe-node.s2 .node-title { color: #818cf8; }
.pipe-node.s3 .node-title { color: #34d399; }

.node-desc {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #475569;
    line-height: 1.6;
}

.node-status {
    margin-top: 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #334155;
    display: flex;
    align-items: center;
    gap: 6px;
}

.dot { width: 6px; height: 6px; border-radius: 50%; background: #1e293b; flex-shrink: 0; }
.dot.active { background: #38bdf8; box-shadow: 0 0 6px #38bdf8; animation: blink 1s infinite; }
.dot.done-s1 { background: #38bdf8; }
.dot.done-s2 { background: #6366f1; }
.dot.done-s3 { background: #10b981; }

@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.input-shell {
    background: #0c1526;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin: 1.5rem 0;
}

.input-shell::before {
    content: '// RESEARCH QUERY';
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #334155;
    letter-spacing: 2px;
    display: block;
    margin-bottom: 1rem;
}

[data-testid="stTextInput"] input {
    background: #030712 !important;
    border: 1px solid #1e293b !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.9rem 1.2rem !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 0 2px rgba(56,189,248,0.1) !important;
}

[data-testid="stTextInput"] label { display: none !important; }

[data-testid="stButton"] button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.5rem !important;
    border: none !important;
}

[data-testid="stButton"]:first-of-type button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.25) !important;
}

[data-testid="stButton"]:not(:first-of-type) button {
    background: #0c1526 !important;
    color: #64748b !important;
    border: 1px solid #1e293b !important;
}

.terminal {
    background: #020810;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1.2rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
}

.terminal-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid #0f172a;
}

.t-dot { width: 10px; height: 10px; border-radius: 50%; }
.t-dot.r { background: #ef4444; }
.t-dot.y { background: #f59e0b; }
.t-dot.g { background: #22c55e; }
.terminal-title { font-size: 0.65rem; color: #334155; letter-spacing: 2px; margin-left: 6px; }

.log-entry { padding: 3px 0; display: flex; gap: 10px; align-items: flex-start; }
.log-time { color: #334155; flex-shrink: 0; }
.log-tag { flex-shrink: 0; }
.log-tag.s1 { color: #38bdf8; }
.log-tag.s2 { color: #818cf8; }
.log-tag.s3 { color: #34d399; }
.log-tag.sys { color: #475569; }
.log-msg { color: #94a3b8; }
.log-msg.s1 { color: #7dd3fc; }
.log-msg.s2 { color: #a5b4fc; }
.log-msg.s3 { color: #6ee7b7; }

.report-shell {
    background: #0c1526;
    border: 1px solid #1e293b;
    border-radius: 16px;
    overflow: hidden;
    margin-top: 2rem;
}

.report-topbar {
    background: #0f1f38;
    border-bottom: 1px solid #1e293b;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.report-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #34d399;
    letter-spacing: 3px;
}

.report-body {
    padding: 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.9;
    color: #94a3b8;
    white-space: pre-wrap;
    max-height: 520px;
    overflow-y: auto;
}

.footer-strip {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 3rem 0 1rem;
    flex-wrap: wrap;
}

.footer-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #1e293b;
    letter-spacing: 2px;
    border: 1px solid #1e293b;
    padding: 4px 12px;
    border-radius: 100px;
}

[data-testid="stDownloadButton"] button {
    background: rgba(16,185,129,0.1) !important;
    color: #34d399 !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

if "report" not in st.session_state:
    st.session_state.report = None
if "status" not in st.session_state:
    st.session_state.status = {"s1": "idle", "s2": "idle", "s3": "idle"}
if "logs" not in st.session_state:
    st.session_state.logs = []
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

st.markdown("""
<div class="hero-wrap">
    <div class="aria-badge">⬡ ARIA — AUTONOMOUS RESEARCH INTELLIGENCE AGENT</div>
    <div class="hero-title">Research,<br>Redefined.</div>
    <div class="hero-sub">type a topic · 3 agents activate · full report in seconds</div>
</div>
""", unsafe_allow_html=True)

def render_pipeline(s):
    def status_html(key, done_dot):
        st_ = s[key]
        if st_ == "active":
            return '<div class="node-status"><div class="dot active"></div> PROCESSING...</div>'
        elif st_ == "done":
            return f'<div class="node-status"><div class="dot {done_dot}"></div> COMPLETE</div>'
        return '<div class="node-status"><div class="dot"></div> STANDBY</div>'

    def card(key, base):
        st_ = s[key]
        if st_ == "active": return f"{base} active"
        if st_ == "done": return f"{base} done"
        return base

    return f"""
    <div class="pipeline">
        <div class="{card('s1', 'pipe-node s1')}">
            <div class="node-id">AGENT · 01</div>
            <span class="node-icon">🔍</span>
            <div class="node-title">Search Agent</div>
            <div class="node-desc">Queries Tavily API<br>Collects 5 top sources<br>Real-time web data</div>
            {status_html('s1', 'done-s1')}
        </div>
        <div class="{card('s2', 'pipe-node s2')}">
            <div class="node-id">AGENT · 02</div>
            <span class="node-icon">🧠</span>
            <div class="node-title">Summarize Agent</div>
            <div class="node-desc">Reads all sources<br>Extracts key insights<br>Groq LLM powered</div>
            {status_html('s2', 'done-s2')}
        </div>
        <div class="{card('s3', 'pipe-node s3')}">
            <div class="node-id">AGENT · 03</div>
            <span class="node-icon">📋</span>
            <div class="node-title">Report Agent</div>
            <div class="node-desc">Writes full report<br>Structured sections<br>Download ready</div>
            {status_html('s3', 'done-s3')}
        </div>
    </div>"""

pipeline_slot = st.empty()
pipeline_slot.markdown(render_pipeline(st.session_state.status), unsafe_allow_html=True)

st.markdown('<div class="input-shell">', unsafe_allow_html=True)
topic = st.text_input("", placeholder="e.g.  Artificial Intelligence in Healthcare 2025", key="topic_input")
col1, col2, col3 = st.columns([1.4, 0.8, 5])
with col1:
    run_btn = st.button("⚡  Run Agents", use_container_width=True)
with col2:
    reset_btn = st.button("↺  Reset", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if reset_btn:
    st.session_state.report = None
    st.session_state.status = {"s1": "idle", "s2": "idle", "s3": "idle"}
    st.session_state.logs = []
    st.session_state.last_topic = ""
    st.rerun()

def render_logs():
    if not st.session_state.logs:
        return ""
    rows = ""
    for l in st.session_state.logs:
        rows += f'<div class="log-entry"><span class="log-time">{l["time"]}</span><span class="log-tag {l["tag"]}">{l["label"]}</span><span class="log-msg {l["tag"]}">{l["msg"]}</span></div>'
    return f'<div class="terminal"><div class="terminal-header"><div class="t-dot r"></div><div class="t-dot y"></div><div class="t-dot g"></div><span class="terminal-title">AGENT ACTIVITY LOG</span></div>{rows}</div>'

import datetime
def ts():
    return datetime.datetime.now().strftime("%H:%M:%S")

log_slot = st.empty()

if run_btn and topic:
    st.session_state.report = None
    st.session_state.logs = []
    st.session_state.last_topic = topic
    st.session_state.status = {"s1": "idle", "s2": "idle", "s3": "idle"}

    def add_log(tag, label, msg):
        st.session_state.logs.append({"time": ts(), "tag": tag, "label": label, "msg": msg})

    st.session_state.status["s1"] = "active"
    pipeline_slot.markdown(render_pipeline(st.session_state.status), unsafe_allow_html=True)
    add_log("sys", "[SYS]", f'Initializing pipeline → "{topic}"')
    add_log("s1", "[A01]", "Connecting to Tavily search API...")
    log_slot.markdown(render_logs(), unsafe_allow_html=True)

    search_data = search_agent(topic)
    st.session_state.status["s1"] = "done"
    add_log("s1", "[A01]", "✓ Sources collected")

    st.session_state.status["s2"] = "active"
    pipeline_slot.markdown(render_pipeline(st.session_state.status), unsafe_allow_html=True)
    add_log("s2", "[A02]", "Summarizing source content...")
    log_slot.markdown(render_logs(), unsafe_allow_html=True)

    summary = summarize_agent(search_data, topic)
    st.session_state.status["s2"] = "done"
    add_log("s2", "[A02]", "✓ Summary generated")

    st.session_state.status["s3"] = "active"
    pipeline_slot.markdown(render_pipeline(st.session_state.status), unsafe_allow_html=True)
    add_log("s3", "[A03]", "Composing research report...")
    log_slot.markdown(render_logs(), unsafe_allow_html=True)

    report = report_agent(summary, topic)
    st.session_state.status["s3"] = "done"
    add_log("s3", "[A03]", "✓ Report complete")
    add_log("sys", "[SYS]", "Pipeline finished — all 3 agents done ✓")

    st.session_state.report = format_report(topic, report)
    pipeline_slot.markdown(render_pipeline(st.session_state.status), unsafe_allow_html=True)
    log_slot.markdown(render_logs(), unsafe_allow_html=True)

elif run_btn and not topic:
    st.warning("Please enter a research topic first!")

if st.session_state.logs and not run_btn:
    log_slot.markdown(render_logs(), unsafe_allow_html=True)

if st.session_state.report:
    report_html = st.session_state.report.replace("\n", "<br>")
    st.markdown(f"""
    <div class="report-shell">
        <div class="report-topbar">
            <span class="report-label">RESEARCH REPORT · OUTPUT</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#334155;">LLAMA-3.3-70B · GROQ</span>
        </div>
        <div class="report-body">{report_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        label="⬇  Download Report (.txt)",
        data=st.session_state.report,
        file_name=f"ARIA_{st.session_state.last_topic[:25].replace(' ','_')}.txt",
        mime="text/plain"
    )

st.markdown("""
<div class="footer-strip">
    <span class="footer-tag">Python</span>
    <span class="footer-tag">Groq · Llama 3.3 70B</span>
    <span class="footer-tag">Tavily Search</span>
    <span class="footer-tag">Streamlit</span>
    <span class="footer-tag">Multi-Agent AI</span>
</div>
""", unsafe_allow_html=True)