import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(
    page_title="TaxRefund-Guard | Enterprise Compliance Platform", 
    page_icon="🛡️",
    layout="wide"
)

@st.cache_resource
def load_and_train_backend_model():
    """Builds synthetic historical dataset and trains the Random Forest asset."""
    np.random.seed(101)
    n_claims = 2000
    
    turnover = np.random.exponential(scale=4000000, size=n_claims) + 200000
    df = pd.DataFrame({'Turnover': turnover})
    
    df['Refund_Requested'] = df['Turnover'] * np.random.uniform(0.02, 0.08, size=n_claims)
    df['Supplier_Risk_Score'] = np.random.uniform(10, 40, size=n_claims)
    df['Filing_Delay_Days'] = np.random.poisson(lam=3, size=n_claims)
    df['Is_Fraud'] = 0
    
    # Inject 60 fraud outliers
    fraud_indices = np.random.choice(df.index, size=60, replace=False)
    df.loc[fraud_indices, 'Refund_Requested'] = df.loc[fraud_indices, 'Turnover'] * np.random.uniform(0.25, 0.60)
    df.loc[fraud_indices, 'Supplier_Risk_Score'] = np.random.uniform(75, 99, size=60)
    df.loc[fraud_indices, 'Filing_Delay_Days'] = np.random.poisson(lam=12, size=60)
    df.loc[fraud_indices, 'Is_Fraud'] = 1
    
    df['Claim_to_Turnover_Ratio'] = df['Refund_Requested'].astype(float) / df['Turnover'].astype(float)
    
    features = ['Claim_to_Turnover_Ratio', 'Supplier_Risk_Score', 'Filing_Delay_Days']
    X = df[features]
    y = df['Is_Fraud']
    
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X, y)
    return model, df

risk_model, historical_df = load_and_train_backend_model()

st.sidebar.title("🛠️ Platform Ingestion")
st.sidebar.markdown("Choose your audit processing mode below:")

app_mode = st.sidebar.radio("Navigation", ["Single Claim Entry", "Bulk Spreadsheet Upload"])

if app_mode == "Single Claim Entry":
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Manual Input Fields")
    input_tin = st.sidebar.text_input("Dealer Identification Number", value="TIN-883492",
                                      help="A unique 14-digit code issued by banks for foreign exchange, or a region-specific alpha-numeric code used by transport departments to authorize motor vehicle dealers.")
    input_turnover = st.sidebar.number_input("Annual Gross Turnover (INR)", min_value=100000, value=2500000, step=50000,
                                             help="The total revenue a business generates from its core sales over a 12-month period, before any expenses, taxes, or deductions")
    input_refund = st.sidebar.number_input("Refund Requested Amount (INR)", min_value=1000, value=150000, step=10000
                                           ,help="Measures the refund scale against gross turnover. Normal baselines range between 2% and 8%; spikes above 25% indicate aggressive structural tax risk.")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Behavioral Metrics")
    input_supplier_score = st.sidebar.slider("Supplier Risk Index", 0, 100, 25, help="Vendor non-compliance tier.")
    input_delay = st.sidebar.slider("Filing Delay Window (Days)", 0, 30, 2, help="Days past deadline baseline.")
    
    # Mathematical computation fallback
    computed_ratio = float(input_refund) / float(input_turnover)

else:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📂 Bulk CSV Ingestion")
    uploaded_file = st.sidebar.file_uploader("Upload Daily Claims Registry (CSV)", type=["csv"])

st.title("🛡️ TaxRefund-Guard: Risk Management Dashboard")
st.caption("An AI-driven compliance engine running real-time predictive analytics to intercept tax leakage while fast-tracking low-risk business disbursals.")
st.markdown("---")

if app_mode == "Single Claim Entry":
    
    live_features = pd.DataFrame([{
        'Claim_to_Turnover_Ratio': float(computed_ratio),
        'Supplier_Risk_Score': float(input_supplier_score),
        'Filing_Delay_Days': float(input_delay)
    }])
    fraud_probability = float(risk_model.predict_proba(live_features)[0][1])

    tab1, tab2, tab3 = st.tabs(["⚡ Live Triage Decision", "📊 Macro Visual Analytics", "🎯 Model Interpretability (XAI)"])

    with tab1:
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(label="📊 Fraud Risk Probability", value=f"{fraud_probability * 100:.2f}%",
                      help="ℹ️ **Description:** A dynamic metric used to measure the statistical probability that an activity, transaction, or application is fraudulent.")
        with m2:
            st.metric(label="📈 Claim-to-Turnover Ratio", value=f"{computed_ratio * 100:.2f}%",
                      help="ℹ️ **Description:** Tracking financial compliance scale to catch tax evaders by checking what percentage of turnover is claimed back.")
        with m3:
            st.metric(label="⚠️ Supplier Network Risk", value=f"{input_supplier_score}/100",
                      help="ℹ️ **Description:** Vulnerabilities in a multi-tier supply ecosystem—including operational, financial, cyber, and geopolitical threats.")
        with m4:
            st.metric(label="⏳ Filing Latency Period", value=f"{input_delay} Days",
                       help="ℹ️ **Description:** It refers to the delay between an exposure or procedure and a subsequent event or effect.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if fraud_probability > 0.75:
            st.markdown(
                f'<div style="border-left: 6px solid #d9383a; background-color: #fdf2f2; padding: 20px; border-radius: 6px;">'
                f'<h3 style="color: #d9383a; margin: 0; font-family: sans-serif;">🚨 CRITICAL AUDIT STATUS: DISBURSEMENT HELD</h3>'
                f'<p style="color: #2c3e50; margin-top: 10px; font-size: 15px;">'
                f'The application submitted by <strong>{input_tin}</strong> shows high structural correlation with known invoice fraud networks. '
                f'Financial transfer halted pending a physical field examination.</p>'
                f'</div>', unsafe_allow_html=True
            )
        elif fraud_probability > 0.30:
            st.markdown(
                f'<div style="border-left: 6px solid #f39c12; background-color: #fef9e7; padding: 20px; border-radius: 6px;">'
                f'<h3 style="color: #e67e22; margin: 0; font-family: sans-serif;">⚠️ WARNING: DESK VERIFICATION ESCALATION</h3>'
                f'<p style="color: #2c3e50; margin-top: 10px; font-size: 15px;">'
                f'Moderate behavioral variance detected. Clear this claim only after an internal officer reviews the uploaded invoice attachments manually.</p>'
                f'</div>', unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div style="border-left: 6px solid #2ecc71; background-color: #eafaf1; padding: 20px; border-radius: 6px;">'
                f'<h3 style="color: #27ae60; margin: 0; font-family: sans-serif;">✅ STATUS: GREEN CHANNELS AUTO-APPROVAL</h3>'
                f'<p style="color: #2c3e50; margin-top: 10px; font-size: 15px;">'
                f'Application profiles cleanly inside normal benchmarks. Automatically queued for instant automated bank clearance.</p>'
                f'</div>', unsafe_allow_html=True
            )

    with tab2:
        st.subheader("📊 Macro Distribution Plot Matrix")
        fig, ax = plt.subplots(figsize=(11, 4))
        sns.scatterplot(
            data=historical_df, x='Claim_to_Turnover_Ratio', y='Supplier_Risk_Score', 
            hue='Is_Fraud', palette={0: '#45062a', 1: '#14dbf5'}, alpha=0.35, ax=ax
        )
        ax.scatter(computed_ratio, input_supplier_score, color='#f51493', edgecolor='black', s=250, marker='*', zorder=5)
        ax.set_xlabel("Claim-to-Turnover Ratio")
        ax.set_ylabel("Supplier Risk Score")
        sns.despine(left=True, bottom=True)
        st.pyplot(fig)

    with tab3:
        st.subheader("🎯 Algorithmic Feature Importance (SHAP Approximation)")
        st.caption("Extracted mathematical feature weights informing the underlying Random Forest decision forest trees.")
        
        importances = risk_model.feature_importances_
        importance_df = pd.DataFrame({
            'Financial Attribute': ['Claim/Turnover Ratio', 'Supplier Risk Index', 'Filing Delay Window'],
            'Relative Influence Weight': importances
        }).sort_values(by='Relative Influence Weight', ascending=True)
        
        st.bar_chart(data=importance_df, x='Financial Attribute', y='Relative Influence Weight', color='#e897d6', use_container_width=True)

else:
    st.subheader("📂 Batch File Triage Suite")
    
    if uploaded_file is None:
        st.info("💡 Pro Tip: Drop a `.csv` data table inside the sidebar uploader workspace to calculate multi-row triage matrices instantly.")
    else:
        batch_df = pd.read_csv(uploaded_file)
        
        try:
            batch_df['Claim_to_Turnover_Ratio'] = batch_df['Refund_Requested'].astype(float) / batch_df['Turnover'].astype(float)
            
            features_list = ['Claim_to_Turnover_Ratio', 'Supplier_Risk_Score', 'Filing_Delay_Days']
            batch_df['Fraud_Probability'] = risk_model.predict_proba(batch_df[features_list])[:, 1]
            
            batch_df['Triage_Action'] = np.where(batch_df['Fraud_Probability'] > 0.75, 'HOLD & AUDIT', 'AUTO-APPROVE')
            
            st.success("✅ Complete Batch Records Scored Successfully!")
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Total Bulk Applications Evaluated", value=len(batch_df))
            with c2:
                total_holds = len(batch_df[batch_df['Triage_Action'] == 'HOLD & AUDIT'])
                st.metric(label="High-Risk Transactions Frozen", value=total_holds, delta=f"{total_holds} Holds Triggered", delta_color="inverse",
                          help="ℹ️ **Description:** An immediate Audit Hold to freeze money before fraud happens.")
            
            st.markdown("### Previewing Scored Registry Output Grid:")
            st.dataframe(batch_df[['Turnover', 'Refund_Requested', 'Fraud_Probability', 'Triage_Action']].head(10), use_container_width=True)
            
            hold_records = batch_df[batch_df['Triage_Action'] == 'HOLD & AUDIT']
            st.download_button(
                label="📥 Download Priority Field Audit Target List",
                data=hold_records.to_csv(index=False),
                file_name="priority_hold_audit_registry.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Schema Validation Error: Verify that your columns exactly match: 'Turnover', 'Refund_Requested', 'Supplier_Risk_Score', 'Filing_Delay_Days'. Error details: {e}")