import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("SPEV Comparative Dashboard 🚙⚡️")

data = {
    "Vehicle": ["SPEV", "Commercial E-Rickshaw", "Petrol Auto"],
    "Range (km)": [120, 80, 200],
    "Charging Time (hrs)": [4, 6, 0.2],
    "Top Speed (km/h)": [50, 45, 60],
    "Cost per km (₹)": [0.5, 1.2, 3.5],
    "CO₂ Avoided (kg/100km)": [25, 15, 0]
}
df = pd.DataFrame(data)

scenario_factors = {
    "Range (km)": {"Best": 1.1, "Average": 1.0, "Worst": 0.85},
    "Charging Time (hrs)": {"Best": 0.8, "Average": 1.0, "Worst": 1.3},
    "Top Speed (km/h)": {"Best": 1.05, "Average": 1.0, "Worst": 0.9},
    "Cost per km (₹)": {"Best": 0.7, "Average": 1.0, "Worst": 1.5},
    "CO₂ Avoided (kg/100km)": {"Best": 1.2, "Average": 1.0, "Worst": 0.75}
}

col1, col2, col3 = st.columns([1, 1, 3])

with col1:
    st.subheader("Scenario")
    scenario = st.radio("Choose scenario:", ["Best", "Average", "Worst"], index=1)

with col2:
    st.subheader("Parameters")
    all_params = list(df.columns[1:]) 
    selected_params = []
    for i, param in enumerate(all_params):
        default = param in ["Range (km)", "Cost per km (₹)"]
        if st.checkbox(param, value=default, key=f"chk_{i}_{param}"):
            selected_params.append(param)

with col3:
    st.subheader("Comparison Chart")

    if not selected_params:
        st.warning("Select at least one parameter (middle column) to display the chart.")
    else:
        temp = df.copy()
        for p in selected_params:
            factor = scenario_factors.get(p, {}).get(scenario, 1.0)
            temp[p] = temp[p] * factor

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
        ax.set_title(f"Vehicles — {scenario} scenario")
        ax.set_xlabel("Vehicle")
        ax.set_ylabel("Value (units vary by parameter)")
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1)) 
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        st.pyplot(fig)
