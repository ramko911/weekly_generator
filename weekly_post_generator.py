import streamlit as st
from datetime import date, timedelta
import re
import pandas as pd
import os

st.set_page_config(page_title="Wantumeni Weekly Post Generator", layout="centered")
st.title("🎧 Wantumeni Post Generator")

# Files to store history
HISTORY_FILE = "post_history.csv"
ANALYTICS_FILE = "analytics.csv"

# Helper to delete rows
def delete_row(df, index):
    return df.drop(index=index).reset_index(drop=True)

# Calculate date ranges
today = date.today()
start_of_week = today - timedelta(days=today.weekday())
end_of_week = start_of_week + timedelta(days=6)
last_week_start = start_of_week - timedelta(days=7)
last_week_end = start_of_week - timedelta(days=1)

# Tabs for navigation
tab0, tab1, tab2, tab3 = st.tabs(["🏠 Home", "📄 Description", "📜 History", "📊 Analytics"])

with tab0:
    st.subheader("📊 Weekly Digest – This Week's Performance")
    if os.path.exists(ANALYTICS_FILE):
        df = pd.read_csv(ANALYTICS_FILE, parse_dates=["Date"])

        df_this_week = df[(df["Date"] >= pd.Timestamp(start_of_week)) & (df["Date"] <= pd.Timestamp(end_of_week))]
        df_last_week = df[(df["Date"] >= pd.Timestamp(last_week_start)) & (df["Date"] <= pd.Timestamp(last_week_end))]

        if not df_this_week.empty:
            top = df_this_week.sort_values("Reach", ascending=False).head(1).iloc[0]
            st.markdown(f"**🏆 Top Performer:** {top['Track Title']} on {top['Platform']} — {top['Reach']} Reach")

            totals = df_this_week.groupby("Platform")[["Reach", "Likes", "Saves"]].sum()
            st.markdown("**📈 Totals This Week by Platform:**")
            st.dataframe(totals)

            if not df_last_week.empty:
                reach_this = df_this_week["Reach"].sum()
                reach_last = df_last_week["Reach"].sum()
                growth = reach_this - reach_last
                pct = (growth / reach_last * 100) if reach_last > 0 else 0
                arrow = "⬆️" if growth >= 0 else "⬇️"
                st.markdown(f"**📊 Reach Growth vs Last Week:** {arrow} {growth} ({pct:.1f}%)")

            df_recent = df[df["Date"] >= pd.Timestamp(today - timedelta(days=28))].copy()
            df_recent["Week"] = df_recent["Date"].dt.to_period("W").astype(str)
            trend = df_recent.groupby("Week")["Reach"].sum()
            st.markdown("**📉 Reach Trend (Past 4 Weeks):**")
            st.line_chart(trend)
        else:
            st.info("No analytics entries found for this week.")
    else:
        st.info("No analytics data available yet.")
