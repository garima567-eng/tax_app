import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

# Set page configuration with premium dark/light branding
st.set_page_config(page_title="TaxRefund-Guard | Compliance Engine", layout="wide", page_icon="🛡️")

# --- CUSTOM CSS INJECTION FOR PREMIUM BRANDING & SLIDERS ---
st.markdown(
    """
    <style>
    /* Styling Streamlit metric containers */
    [data-testid="stMetricContainer"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    /* Brand-specific customization for active slider tracks */
    div[data-baseweb="slider"] [role="slider"] {
        background-color: #1e3a8a !important; /* Premium Navy Blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- MOCK MODEL TRAINING DATA FOREGROUND ---
# In a real environment, this loads from a database or serialized pickle file (.pkl)
@st.cache_resource
def train_baseline_compliance_model():
    np.random.seed(42)
    n_records = 1000
    
    # Simulating real-world variables
    itc_output_ratio = np.random.uniform(0.05, 0.95, n_records)
    supplier_reconcile_rate = np.random.uniform(40, 100, n_records)
    filing_latency_days = np.random.poisson(lam=3, size=n_records)
    
    # Target label: 0 = Compliant, 1 = High-Risk Anomaly (Shell/Carousel indicator)
    # Risk factor naturally spikes if ITC exceeds output tax and supplier data doesn't match
    risk_score = (itc_output_ratio * 0.6) - (supplier_reconcile_rate / 100 * 0.5) + (filing_latency_days * 0.05)
    risk_labels = (risk_score > 0.25).astype(int)
    
<<<<<<< Updated upstream
    fraud_indices = np.random.choice(df.index, size=60, replace=False)
    df.loc[fraud_indices, 'Refund_Requested'] = df.loc[fraud_indices, 'Turnover'] * np.random.uniform(0.25, 0.60)
    df.loc[fraud_indices, 'Supplier_Risk_Score'] = np.random.uniform(75, 99, size=60)
    df.loc[fraud_indices, 'Filing_Delay_Days'] = np.random.poisson(lam=12, size=60)
    df.loc[fraud_indices, 'Is_Fraud'] = 1
    
    df['Claim_to_Turnover_Ratio'] = df['Refund_Requested'].astype(float) / df['Turnover'].astype(float)
    
    features = ['Claim_to_Turnover_Ratio', 'Supplier_Risk_Score', 'Filing_Delay_Days']
    X = df[features]
    y = df['Is_Fraud']
=======
    X = pd.DataFrame({
        'ITC_to_Output_Ratio': itc_output_ratio,
        'Supplier_Reconcile_Rate': supplier_reconcile_rate,
        'Filing_Latency_Days': filing_latency_days
    })
>>>>>>> Stashed changes
    
    # Using balanced class weights to neutralize real-world sparse anomaly footprint (~3-5%)
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X, risk_labels)
    return model

model = train_baseline_compliance_model()

# --- APP LAYOUT HEADER ---
st.title("🛡️ TaxRefund-Guard: Machine Learning Compliance & Triage Engine")
st.markdown(
    "An AI-driven operational gateway translating statutory compliance anomalies into "
    "automated administrative directives."
)
st.write("---")

# --- SIDEBAR INTERACTIVE ENTRY CHANNEL (LIVE FEATURE INGESTION) ---
st.sidebar.header("📥 Live Application Parameters")
st.sidebar.markdown("Input data directly from the active filing registry to compute real-time risk triage.")

input_itc_ratio = st.sidebar.slider(
    "1. ITC-to-Output Tax Ratio",
    min_value=0.0, max_value=2.0, value=0.4, step=0.05,
    help="Measures Input Tax Credit claimed against output tax liability. Ratios exceeding 1.0 mean the company is claiming more tax back than it paid out, signaling a structural risk baseline."
)

input_reconcile_rate = st.sidebar.slider(
    "2. GSTR-2B / Supplier Match Rate (%)",
    min_value=0.0, max_value=100.0, value=94.5, step=0.5,
    help="The percentage of input credit that successfully reconciles against tax invoices uploaded independently by your suppliers. Low scores drop hints about phantom shell invoices."
)

input_latency = st.sidebar.number_input(
    "3. Statutory Filing Latency (Days)",
    min_value=0, max_value=90, value=2, step=1,
    help="The window of days between the mandatory government filing deadline and the actual operational upload timestamp."
)

# --- MAIN DASHBOARD CONTROL MATRIX ---
tabs = st.tabs(["⚡ Live Triage Diagnostics", "📊 Explainable AI (XAI) Architecture", "📂 Batch Matrix Processing"])

# --- TAB 1: LIVE DIAGNOSTICS ---
with tabs[0]:
    st.subheader("📋 Dynamic Risk Assessment & Enforcement Gateway")
    
<<<<<<< Updated upstream
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Behavioral Metrics")
    input_supplier_score = st.sidebar.slider("Supplier Risk Index", 0, 100, 25, help="Vendor non-compliance tier.")
    input_delay = st.sidebar.slider("Filing Delay Window (Days)", 0, 30, 2, help="Days past deadline baseline.")
    
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
=======
    # Compile the live entry vector
    live_record = pd.DataFrame([{
        'ITC_to_Output_Ratio': float(input_itc_ratio),
        'Supplier_Reconcile_Rate': float(input_reconcile_rate),
        'Filing_Latency_Days': float(input_latency)
>>>>>>> Stashed changes
    }])
    
    # Calculate inference probability
    probability = model.predict_proba(live_record)[0][1]
    
    # Dashboard Grid metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="📊 Target Risk Probability", value=f"{probability * 100:.1f}%")
    with c2:
        st.metric(label="📈 Operational ITC Scale Factor", value=f"{input_itc_ratio:.2f}x")
    with c3:
        st.metric(label="🛡️ Supply Chain Reconciliation Integrity", value=f"{input_reconcile_rate:.1f}%")
        
    st.write("### 🚨 System Directive Verdict")
    
    # Deterministic Triage Boundary Engine
    if probability < 0.30:
        st.success("🟢 **DIRECTIVE: AUTO-APPROVE (Low Risk Baseline)**")
        st.info("Application falls within standard compliance thresholds. Clear ledger outlays immediately to maintain economic cash-flow velocity.")
    elif 0.30 <= probability <= 0.75:
        st.warning("🟠 **DIRECTIVE: DESK REVIEW INTERCEPT (Moderate Variance)**")
        st.info("System intercepted variance anomalies. Claims held pending desktop verification of invoice records against ledger attachments.")
    else:
        st.error("🔴 **DIRECTIVE: AUDIT SYSTEM FREEZE (High-Risk Counterpart Alert)**")
        st.info("Immediate transaction freeze ordered. Disbursal accounts locked out automatically. Priority field-enforcement inspection ticket has been generated.")

# --- TAB 2: EXPLAINABLE AI ---
with tabs[1]:
    st.subheader("🔮 Algorithmic Model Transparency & Feature Influences")
    st.markdown("Exposing underlying ensemble metrics to ensure audit trails remain fully transparent and legally defensible.")
    
    # Extract Feature Importances directly from the Random Forest weights
    importances = model.feature_importances_
    features = ['ITC to Output Ratio', 'Supplier Reconcile Rate', 'Filing Latency Window']
    
    fig, ax = plt.subplots(figsize=(6, 2.5))
    sns.barplot(x=importances, y=features, palette="viridis", ax=ax)
    ax.set_title("Global Feature Weight Allocation Matrix")
    ax.set_xlabel("Relative Informational Gain Weight")
    st.pyplot(fig)
    
    st.caption("ℹ️ **Data Science Footnote:** The chart maps feature weighting. High parameters signify that variance in that metric contributes heavily toward model decisions, effectively eliminating black-box opacity.")

# --- TAB 3: BATCH PROCESSING ---
with tabs[2]:
    st.subheader("📥 Mass Registry Drag-and-Drop Uploader")
    st.markdown("Run asynchronous vector evaluation over complete daily department spreadsheets.")
    
    uploaded_file = st.file_uploader("Upload Daily Registry CSV File", type="csv")
    
    if uploaded_file is not None:
        try:
            batch_df = pd.read_csv(uploaded_file)
            
            # Real-world structural validation check
            required_cols = ['ITC_to_Output_Ratio', 'Supplier_Reconcile_Rate', 'Filing_Latency_Days']
            if all(col in batch_df.columns for col in required_cols):
                # Predict over complete matrix
                predictions = model.predict(batch_df[required_cols])
                probabilities = model.predict_proba(batch_df[required_cols])[:, 1]
                
                batch_df['Risk_Probability'] = probabilities
                batch_df['System_Verdict'] = np.where(probabilities < 0.30, 'Auto-Approve', 
                                                     np.where(probabilities <= 0.75, 'Desk Review', 'Audit Freeze'))
                
                st.write("### 📊 Processed Registry Matrix Overview")
                st.dataframe(batch_df.head(10), use_container_width=True)
                
                # Summary Aggregations
                st.markdown("#### 📈 Registry Distribution Summary")
                counts = batch_df['System_Verdict'].value_counts()
                st.bar_chart(counts)
            else:
                st.error(f"❌ Schema Validation Error: Verify that your columns exactly match: {required_cols}")
        except Exception as e:
<<<<<<< Updated upstream
            st.error(f"Schema Validation Error: Verify that your columns exactly match: 'Turnover', 'Refund_Requested', 'Supplier_Risk_Score', 'Filing_Delay_Days'. Error details: {e}")
=======
            st.error(f"Error parsing structural registry file: {e}")
>>>>>>> Stashed changes
