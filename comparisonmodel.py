import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("SPEV Comparative Dashboard 🚙⚡️")

scenario_data = {
    "Best": pd.DataFrame({
        "Vehicle": ["SPEV", "E-Rick", "Fuel"],
        "Initial Cost (₹, in K)": [110, 80, 200],
        "Range per tank/charge (km)": [140, 120, 250],
        "Cost per Km (₹/100km)": [35, 48, 250],
        "Life span (in months)": [72, 48, 84],
        "Operational CO2 (g/km)": [42, 56, 54]
    }),
    "Average": pd.DataFrame({
        "Vehicle": ["SPEV", "E-Rick", "Fuel"],
        "Initial Cost (₹, in K)": [135, 95, 220],
        "Range per tank/charge (km)": [120, 100, 200],
        "Cost per Km (₹/100km)": [48, 64, 275],
        "Life span (in months)": [66, 30, 78],
        "Operational CO2 (g/km)": [48, 64, 57.5]
    }),
    "Worst": pd.DataFrame({
        "Vehicle": ["SPEV", "E-Rick", "Fuel"],
        "Initial Cost (₹, in K)": [160, 110, 230],
        "Range per tank/charge (km)": [100, 80, 150],
        "Cost per Km (₹/100km)": [60, 80, 300],
        "Life span (in months)": [60, 18, 60],
        "Operational CO2 (g/km)": [52, 68, 64]
    })
}

col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    st.subheader("Scenario")
    scenario = st.radio("Choose scenario:", ["Best", "Average", "Worst"], index=1)

with col2:
    st.subheader("Parameters")
    all_params = list(scenario_data["Average"].columns[1:]) 
    selected_params = []
    for i, param in enumerate(all_params):
        default = param in ["Range (km)", "Cost per km (₹)"]  # Pre-select 2 params
        if st.checkbox(param, value=default, key=f"chk_{i}_{param}"):
            selected_params.append(param)

with col3:
    st.subheader("Comparison Chart")

    if not selected_params:
        st.warning("Select at least one parameter (middle column) to display the chart.")
    else:
        temp = scenario_data[scenario].copy()

        n_params = len(selected_params)
        n_vehicles = len(temp["Vehicle"])
        x = np.arange(n_vehicles)

        max_total_bar_width = 0.8
        bar_width = max_total_bar_width / n_params

        fig_w = max(6, 1.5 * n_params + 4)
        fig_h = 5
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))

        offsets = (np.arange(n_params) - (n_params - 1) / 2) * bar_width

        for i, p in enumerate(selected_params):
            ax.bar(x + offsets[i], temp[p], width=bar_width, label=p)

        ax.set_xticks(x)
        ax.set_xticklabels(temp["Vehicle"])
        ax.set_title(f"{scenario} Case Scenario")
        ax.set_xlabel("Vehicle")
        ax.set_ylabel("Value (units vary by parameter)")
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        st.pyplot(fig)
