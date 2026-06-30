import streamlit as st
import pandas as pd
import sys
import os
from pathlib import Path

# Add src to Python path to find ai_shield_kenya package
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_shield_kenya.risk_scorer import RiskScorer

# Initialize the risk scorer
@st.cache_resource
def load_scorer():
    return RiskScorer()

scorer = load_scorer()

st.set_page_config(page_title="AI Shield Kenya", page_icon="🛡️")

st.title("🛡️ AI Shield Kenya")
st.markdown("""
**Safeguarding Agriculture and Education from Fraud, Misinformation, and Toxins**
This tool uses SIR epidemiological modeling to detect and score harmful content in Kenyan AI conversations.
""")

st.divider()

# Sidebar for options
st.sidebar.header("Settings")
mode = st.sidebar.selectbox("Mode", ["Single Prompt", "Batch Processing"])

if mode == "Single Prompt":
    st.subheader("Risk Scoring")
    user_input = st.text_area("Enter a prompt to analyze:", placeholder="e.g., Use bleach to cure crop disease")
    
    if st.button("Analyze"):
        if user_input:
            with st.spinner("Analyzing..."):
                result = scorer.score(user_input)
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Risk Score", f"{result['risk_score']}/100")
                
                with col2:
                    st.metric("Category", result['category'])
                
                st.info(f"**Suggestion:** {result['suggestion']}")
                
                # Risk color coding
                score = result['risk_score']
                if score >= 70:
                    st.error("🚨 High Risk")
                elif score >= 40:
                    st.warning("⚠️ Medium Risk")
                else:
                    st.success("✅ Low Risk")
        else:
            st.warning("Please enter a prompt first.")

else:
    st.subheader("Batch Processing")
    uploaded_file = st.file_uploader("Upload a CSV file with a 'prompt_text' column", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'prompt_text' in df.columns:
            if st.button("Process Batch"):
                with st.spinner("Processing..."):
                    results = []
                    for _, row in df.iterrows():
                        res = scorer.score(row['prompt_text'])
                        results.append({
                            'prompt_text': row['prompt_text'],
                            'risk_score': res['risk_score'],
                            'category': res['category'],
                            'suggestion': res['suggestion']
                        })
                    
                    res_df = pd.DataFrame(results)
                    st.write("### Analysis Results")
                    st.dataframe(res_df)
                    
                    # Download button
                    csv = res_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name="ai_shield_results.csv",
                        mime="text/csv",
                    )
        else:
            st.error("CSV must contain a 'prompt_text' column.")

st.divider()
st.caption("AI Shield Kenya - A Minimal, Multilingual Safety Toolkit for Kenyan AI Conversations")
