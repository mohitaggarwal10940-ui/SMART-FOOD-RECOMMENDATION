import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# -----------------------------
# Load dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("food_dataset_big.csv")

df = load_data()

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="Smart Food Recommendation", page_icon="🥗")
st.title("🥗 Smart Food Recommendation System for Health")
st.write("This app suggests whether a food is good or bad for a given health condition.")

# User inputs
disease = st.selectbox("Select your health condition:", sorted(df["Disease"].unique()))
food = st.text_input("Enter a food item:")

# Check recommendation
if st.button("Check Recommendation"):
    result = df[(df["Disease"] == disease) & (df["Food"].str.lower() == food.lower())]
    if not result.empty:
        rec = result.iloc[0]
        if rec['Recommendation'] == "Recommend":
            st.success(f"✅ {rec['Food']} is RECOMMENDED for {disease}.")
        else:
            st.error(f"❌ {rec['Food']} should be AVOIDED for {disease}.")
        st.write(f"**Reason:** {rec['Reason']}")
        st.write(f"**Biomarker Impact:** {rec['Biomarker']}")
    else:
        st.warning("Food not found in dataset. Try another food.")

# Suggest healthy foods
if st.button("Suggest Healthy Foods"):
    recs = df[(df["Disease"] == disease) & (df["Recommendation"] == "Recommend")]
    if not recs.empty:
        st.subheader(f"🌟 Suggested foods for {disease}:")
        for _, row in recs.iterrows():
            st.write(f"- **{row['Food']}** → {row['Reason']} (Biomarker: {row['Biomarker']})")
    else:
        st.warning("No healthy foods found in dataset.")

# Show pie chart
if st.button("Show Food Chart"):
    counts = df[df["Disease"] == disease]["Recommendation"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(f"Food Recommendations for {disease}")
    st.pyplot(fig)

# Generate 1-day diet plan
if st.button("Generate 1-Day Diet Plan"):
    recs = df[(df["Disease"] == disease) & (df["Recommendation"] == "Recommend")]
    if not recs.empty:
        choices = random.sample(list(recs["Food"]), min(3, len(recs)))
        st.subheader(f"🍽️ 1-Day Diet Plan for {disease}")
        st.write(f"- Breakfast: {choices[0]}")
        if len(choices) > 1:
            st.write(f"- Lunch: {choices[1]}")
        if len(choices) > 2:
            st.write(f"- Dinner: {choices[2]}")
    else:
        st.warning("No recommended foods available for diet plan.")
