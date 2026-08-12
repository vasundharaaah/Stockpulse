import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


from backend import (
    fetch_stock_data,
    get_latest_price,
    get_change_percent,
    process_multiple_stocks,
    format_ticker,
)
from features import (
    check_price_alert,
    export_to_csv,
    get_app_instructions,
)

# PAGE CONFIG

st.set_page_config(
    page_title="StockPulse",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@300;400;500;600&display=swap');

/* ── Variables ── */
:root {
    --bg:        #0e0f13;
    --bg2:       #13141a;
    --bg3:       #1a1b23;
    --border:    rgba(255,255,255,0.07);
    --border2:   rgba(255,255,255,0.12);
    --text:      #e8e3d8;
    --muted:     rgba(232,227,216,0.35);
    --gold:      #e8a435;
    --gold2:     #f5c26b;
    --up:        #4ade97;
    --down:      #f87171;
    --accent:    #e8a435;
}

/* ── Base ── */
html, body, [class*="css"], .stApp {
    font-family: 'IBM Plex Mono', monospace !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background-image:
        radial-gradient(ellipse 60% 40% at 80% 0%, rgba(232,164,53,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 10% 100%, rgba(74,222,151,0.04) 0%, transparent 50%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 1px;
    color: var(--muted) !important;
    padding: 6px 0 !important;
    transition: color 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover { color: var(--gold) !important; }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stSelectbox > div > div, .stTextArea textarea {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(232,164,53,0.12) !important;
    outline: none !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--gold) !important;
    border-radius: 4px !important;
    color: var(--gold) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    padding: 10px 24px !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: var(--gold) !important;
    color: var(--bg) !important;
    box-shadow: 0 4px 20px rgba(232,164,53,0.25) !important;
}

/* ── Download Button ── */
.stDownloadButton > button {
    background: var(--gold) !important;
    border: none !important;
    border-radius: 4px !important;
    color: var(--bg) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton > button:hover {
    background: var(--gold2) !important;
    box-shadow: 0 6px 24px rgba(232,164,53,0.35) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 22px;
}
[data-testid="metric-container"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.6rem !important;
    color: var(--text) !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: var(--muted) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    padding: 12px 24px !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--gold) !important; }

/* ── Toggle / Checkbox ── */
.stToggle label { font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; }

/* ── Segmented control ── */
[data-testid="stSegmentedControl"] button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 1px;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-thumb { background: rgba(232,164,53,0.25); border-radius: 2px; }

/* ── Expander ── */
.streamlit-expanderHeader {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--muted) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px;
}

/* ── Alert Boxes ── */
.alert-up {
    background: rgba(74,222,151,0.07);
    border: 1px solid rgba(74,222,151,0.3);
    border-left: 3px solid var(--up);
    border-radius: 8px;
    padding: 16px 20px;
}
.alert-down {
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.3);
    border-left: 3px solid var(--down);
    border-radius: 8px;
    padding: 16px 20px;
}
.alert-neutral {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--muted);
    border-radius: 8px;
    padding: 16px 20px;
}

/* ── Stock card ── */
.scard {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    transition: border-color 0.25s, transform 0.2s;
    cursor: default;
    margin-bottom: 12px;
}
.scard:hover { border-color: rgba(232,164,53,0.35); transform: translateY(-2px); }
.scard-ticker {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: var(--gold);
    letter-spacing: 0.5px;
}
.scard-name { font-size: 9px; letter-spacing: 2px; color: var(--muted); margin-top: 2px; text-transform: uppercase; }
.scard-price { font-family: 'DM Serif Display', serif; font-size: 1.6rem; color: var(--text); margin-top: 14px; }
.scard-chg-up   { font-size: 11px; color: var(--up);   letter-spacing: 0.5px; }
.scard-chg-down { font-size: 11px; color: var(--down);  letter-spacing: 0.5px; }
.scard-vol { font-size: 10px; color: var(--muted); margin-top: 6px; }

/* ── Section Label ── */
.slabel {
    font-size: 9px;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: var(--muted);
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 18px;
}

/* ── Price pill ── */
.pill-up   { display:inline-block; padding:3px 12px; border-radius:20px; font-size:11px; font-weight:600; background:rgba(74,222,151,0.12); color:var(--up); border:1px solid rgba(74,222,151,0.25); }
.pill-down { display:inline-block; padding:3px 12px; border-radius:20px; font-size:11px; font-weight:600; background:rgba(248,113,113,0.12); color:var(--down); border:1px solid rgba(248,113,113,0.25); }
</style>
""", unsafe_allow_html=True)

# COLOUR CONSTANTS 
 
C_BG    = "#0e0f13"
C_BG2   = "#13141a"
C_GRID  = "rgba(255,255,255,0.05)"
C_UP    = "#4ade97"
C_DOWN  = "#f87171"
C_GOLD  = "#e8a435"
C_TEXT  = "#e8e3d8"
C_MUTED = "rgba(232,227,216,0.35)"


# CHART BUILDER 

def build_chart(df: pd.DataFrame, ticker: str, show_sma: bool, show_volume: bool) -> go.Figure:
    if df is None or df.empty:
        return go.Figure()

    is_up  = df["Close"].iloc[-1] >= df["Close"].iloc[0]
    accent = C_UP if is_up else C_DOWN

    # SMA helper
    def sma(n):
        return df["Close"].rolling(window=min(n, len(df))).mean()

    rows    = [0.72, 0.28] if show_volume else [1.0]
    n_rows  = 2 if show_volume else 1

    fig = make_subplots(
        rows=n_rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=rows,
    )

    # Candles
    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"],
        increasing_line_color=C_UP,  increasing_fillcolor=C_UP,
        decreasing_line_color=C_DOWN, decreasing_fillcolor=C_DOWN,
        line=dict(width=1),
        name="OHLC",
    ), row=1, col=1)

    if show_sma:
        fig.add_trace(go.Scatter(
            x=df.index, y=sma(20),
            mode="lines", name="SMA 20",
            line=dict(color="rgba(232,164,53,0.75)", width=1.5, dash="dot"),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df.index, y=sma(50),
            mode="lines", name="SMA 50",
            line=dict(color="rgba(160,210,255,0.6)", width=1.5, dash="dash"),
        ), row=1, col=1)

    if show_volume:
        vol_colors = [
            C_UP if df["Close"].iloc[i] >= df["Open"].iloc[i] else C_DOWN
            for i in range(len(df))
        ]
        fig.add_trace(go.Bar(
            x=df.index, y=df["Volume"],
            marker_color=vol_colors, marker_opacity=0.45,
            name="Volume", showlegend=False,
        ), row=2, col=1)

    ax = dict(
        gridcolor=C_GRID, showgrid=True, zeroline=False,
        showline=False,
        tickfont=dict(family="IBM Plex Mono", size=9, color=C_MUTED),
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        font=dict(family="IBM Plex Mono", color=C_MUTED),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=C_BG2, bordercolor=accent,
            font=dict(family="IBM Plex Mono", size=11, color=C_TEXT),
        ),
        legend=dict(
            orientation="h", x=0, y=1.04,
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=9, family="IBM Plex Mono", color=C_MUTED),
        ),
        xaxis=dict(**ax, showticklabels=False if show_volume else True),
        yaxis=dict(**ax),
        **({"xaxis2": dict(**ax), "yaxis2": dict(**ax, title="")} if show_volume else {}),
    )
    return fig



# MINI SPARKLINE  (for portfolio cards)

def mini_sparkline(df: pd.DataFrame, is_up: bool) -> go.Figure:
    color = C_UP if is_up else C_DOWN
    fig = go.Figure(go.Scatter(
        x=df.index, y=df["Close"],
        mode="lines",
        line=dict(color=color, width=1.5),
        fill="tozeroy",
        fillcolor=f"rgba({'74,222,151' if is_up else '248,113,113'},0.08)",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0), height=55,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        showlegend=False, hovermode=False,
    )
    return fig

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:32px;padding-bottom:20px;border-bottom:1px solid rgba(255,255,255,0.06);">
        <div style="font-family:'DM Serif Display',serif;font-size:1.55rem;color:#e8a435;letter-spacing:0.5px;">
            ◈ StockPulse
        </div>
        <div style="font-size:8px;letter-spacing:4px;color:rgba(232,227,216,0.25);margin-top:4px;text-transform:uppercase;">
            Market Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="slabel">Navigate</div>', unsafe_allow_html=True)
    page = st.radio(
        "",
        ["◎  Single Stock", "⚑  Price Alerts", "↓  Export Data", "?  Help"],
        label_visibility="collapsed",
    )



#TITLE


st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:36px;
            padding-bottom:24px;border-bottom:1px solid rgba(255,255,255,0.06);">
    <div>
        <div style="font-family:'DM Serif Display',serif;font-size:2.6rem;
                    line-height:1.05;color:#e8e3d8;letter-spacing:-1px;">
            Market <em style="color:#e8a435;">Intelligence</em>
        </div>
    
</div>
""", unsafe_allow_html=True)


# PAGE: SINGLE STOCK 
if "Single" in page:
    st.markdown('<div class="slabel">Ticker Lookup</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([5, 1])
    with c1:
        raw_ticker = st.text_input(
            "", value="TCS", placeholder="Enter ticker — e.g. TCS, INFY,etc",
            label_visibility="collapsed",
        )
    with c2:
        go_btn = st.button("SEARCH", use_container_width=True)

    # Timeframe row
    tf_col, sma_col, vol_col = st.columns([3, 1, 1])
    with tf_col:
        TIMEFRAMES = {"1D": "5d", "1W": "5d", "1M": "1mo", "3M": "3mo", "1Y": "1y", "5Y": "5y"}
        tf_label = st.segmented_control("", list(TIMEFRAMES.keys()), default="1M", label_visibility="collapsed")
    with sma_col:
        show_sma = st.toggle("SMA", value=True)
    with vol_col:
        show_vol = st.toggle("Volume", value=True)

    period = TIMEFRAMES.get(tf_label or "1M", "1mo")

    if raw_ticker:
        with st.spinner(""):
            data   = fetch_stock_data(raw_ticker, period=period)  
            latest = get_latest_price(data)                        
            chg_pct = get_change_percent(data)                    

        if data is None or latest is None:
            st.markdown("""
            <div class="alert-neutral" style="margin-top:12px;">
                <div style="font-size:10px;letter-spacing:2px;color:rgba(232,227,216,0.3);">ERROR</div>
                <div style="margin-top:4px;font-size:13px;">
                    Ticker not found. Try <code style="color:#e8a435;">TCS</code>,
                    <code style="color:#e8a435;">INFY</code>, <code style="color:#e8a435;">AAPL</code>
                </div>
                <div style="margin-top:6px;font-size:10px;color:rgba(232,227,216,0.3);">
                    Indian stocks are auto-appended with .NS (e.g. TCS → TCS.NS)
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            chg_pct    = chg_pct if chg_pct is not None else 0.0
            is_up      = chg_pct >= 0
            arrow      = "▲" if is_up else "▼"
            pill       = "pill-up" if is_up else "pill-down"
            chg_c      = C_UP if is_up else C_DOWN
            ticker_fmt = format_ticker(raw_ticker)

            # ── Price Hero ──
            st.markdown(f"""
            <div style="margin:24px 0 20px;">
                <div style="font-size:10px;letter-spacing:3px;color:{C_MUTED};text-transform:uppercase;">
                    {ticker_fmt}
                </div>
                <div style="display:flex;align-items:baseline;gap:16px;margin-top:6px;flex-wrap:wrap;">
                    <span style="font-family:'DM Serif Display',serif;font-size:3rem;color:{C_TEXT};">
                        ₹{latest['price']:,.2f}
                    </span>
                    <span class="{pill}">
                        {arrow} {abs(chg_pct):.2f}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Metric Strip ──
            m1, m2, m3 = st.columns(3)
            m1.metric("Day High",  f"₹{latest['high']:,.2f}")
            m2.metric("Day Low",   f"₹{latest['low']:,.2f}")
            m3.metric("Volume",    f"{latest['volume']:,}")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Chart ──
            fig = build_chart(data, ticker_fmt, show_sma, show_vol)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # ── Quick Stats Table ──
            with st.expander("RAW DATA PREVIEW"):
                st.dataframe(
                    data.tail(10)[["Open","High","Low","Close","Volume"]].round(2),
                    use_container_width=True,
                )


# PAGE: PRICE ALERTS 
elif "Alert" in page:
    st.markdown('<div class="slabel">Price Alert Checker</div>', unsafe_allow_html=True)

    a1, a2, a3, a4 = st.columns([2, 2, 2, 1])
    with a1:
        alert_ticker = st.text_input("", "TCS", label_visibility="collapsed", placeholder="Ticker")
    with a2:
        alert_price  = st.number_input("", min_value=0.0, value=3500.0, step=10.0, label_visibility="collapsed", format="%.2f")
    with a3:
        alert_cond   = st.selectbox("", ["above", "below"], label_visibility="collapsed")
    with a4:
        check_btn    = st.button("CHECK", use_container_width=True)

    if check_btn:
        with st.spinner(""):
            data   = fetch_stock_data(alert_ticker, period="1d") 
            latest = get_latest_price(data)                       

        if latest is None:
            st.markdown('<div class="alert-neutral"><b>Invalid ticker.</b></div>', unsafe_allow_html=True)
        else:
            curr = latest["price"]
        
            triggered, message = check_price_alert(curr, alert_price, alert_cond)

            css_cls = "alert-up" if triggered else "alert-neutral"
            icon    = "🚨" if triggered else "⏳"
            status  = "TRIGGERED" if triggered else "MONITORING"
            status_c = C_UP if triggered else C_MUTED

            st.markdown(f"""
            <div class="{css_cls}" style="margin-top:12px;">
                <div style="font-size:9px;letter-spacing:3px;color:{C_MUTED};text-transform:uppercase;">
                    {alert_ticker.upper()} · ALERT STATUS
                </div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.6rem;
                            color:{status_c};margin-top:8px;">
                    {icon} {status}
                </div>
                <div style="font-size:12px;color:{C_MUTED};margin-top:10px;line-height:2;">
                    Current &nbsp;→ <span style="color:{C_TEXT};">₹{curr:,.2f}</span><br>
                    Target &nbsp;&nbsp;→ <span style="color:{C_TEXT};">₹{alert_price:,.2f} ({alert_cond})</span><br>
                    <span style="color:rgba(232,227,216,0.45);">{message}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)



# PAGE: EXPORT DATA 
elif "Export" in page:
    st.markdown('<div class="slabel">Export Historical Data</div>', unsafe_allow_html=True)
 
    e1, e2, e3 = st.columns([2, 2, 1])
    with e1:
        exp_ticker = st.text_input("", "TCS", label_visibility="collapsed", placeholder="Ticker")
    with e2:
        EXP_TF = {"1 Month":"1mo","3 Months":"3mo","6 Months":"6mo","1 Year":"1y","5 Years":"5y"}
        exp_tf_label = st.selectbox("", list(EXP_TF.keys()), label_visibility="collapsed")
    with e3:
        exp_btn = st.button("FETCH", use_container_width=True)
 
    if exp_btn:
        with st.spinner(""):
            data = fetch_stock_data(exp_ticker, period=EXP_TF[exp_tf_label])  # ← Member 1
 
        if data is None or data.empty:
            st.markdown('<div class="alert-neutral">No data found for this ticker.</div>', unsafe_allow_html=True)
        else:
            ticker_fmt = format_ticker(exp_ticker)
            # ← Member 4's function (saves locally)
            ok, msg = export_to_csv(data, ticker_fmt)
 
            csv_bytes = data.to_csv().encode("utf-8")
            fname     = f"{ticker_fmt}_{exp_tf_label.replace(' ','')}.csv"
 
            st.markdown(f"""
            <div class="alert-up" style="margin-bottom:16px;">
                <div style="font-size:9px;letter-spacing:3px;color:{C_MUTED};">READY</div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.2rem;
                            color:{C_UP};margin-top:6px;">✓ {fname}</div>
                <div style="font-size:11px;color:{C_MUTED};margin-top:6px;">
                    {len(data)} rows · OHLCV data
                </div>
            </div>
            """, unsafe_allow_html=True)
 
            st.download_button(
                label="↓  DOWNLOAD CSV",
                data=csv_bytes,
                file_name=fname,
                mime="text/csv",
            )
 
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="slabel">Data Preview — Last 10 Rows</div>', unsafe_allow_html=True)
            st.dataframe(data.tail(10).round(2), use_container_width=True)
 

# ── PAGE: HELP ──
elif "Help" in page:
    st.markdown('<div class="slabel">Documentation</div>', unsafe_allow_html=True)

    instructions = get_app_instructions()  

    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:12px;
                padding:32px;line-height:2;font-size:13px;color:{C_TEXT};">
        {instructions.replace('##', '<br><br><span style="font-family:DM Serif Display,serif;font-size:1.2rem;color:#e8a435;">').replace('###', '<br><span style="font-size:10px;letter-spacing:2px;color:rgba(232,227,216,0.5);text-transform:uppercase;">').replace('*', '').replace('`', '')}
    </div>
    """, unsafe_allow_html=True)