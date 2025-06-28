import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Decoder Universe",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 15px 15px;
    }
    
    .decoder-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
        margin-bottom: 1rem;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .decoder-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .card-icon {
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        font-size: 0.9rem;
        color: #666;
        text-align: center;
        line-height: 1.4;
    }
    
    .back-button {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .tactic-warning {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .protection-tip {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .red-flag {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Decoder data structure
DECODERS = {
    "financial_advisor": {
        "name": "Financial Advisor Decoder",
        "icon": "💰",
        "description": "Protect yourself from high-pressure financial advisor sales tactics",
        "tactics": [
            "Creating artificial urgency: 'This offer expires today!'",
            "Fear-mongering about market crashes or retirement security",
            "Pushing expensive products with high commissions",
            "Using complex jargon to confuse and intimidate",
            "Claiming exclusive access to 'special' investments",
        ],
        "protection_tips": [
            "Always ask for fee disclosures in writing",
            "Take time to research any investment recommendation",
            "Get a second opinion from a fee-only advisor",
            "Understand exactly how your advisor gets paid",
            "Never sign anything under pressure",
        ],
        "red_flags": [
            "Refuses to explain fees clearly",
            "Pushes immediate decisions without time to think",
            "Only recommends high-fee products",
            "Won't provide references or credentials",
            "Uses scare tactics about your financial future",
        ]
    },
    "real_estate": {
        "name": "Real Estate Agent Decoder",
        "icon": "🏠",
        "description": "Navigate high-pressure real estate tactics and understand what agents really mean",
        "tactics": [
            "'Other buyers are interested' - creating false competition",
            "Suggesting inflated listing prices to win your business",
            "Rushing you through property viewings",
            "Downplaying property issues or neighborhood problems",
            "Using emotional manipulation: 'Perfect for your family!'",
        ],
        "protection_tips": [
            "Research comparable sales yourself using online tools",
            "Get pre-approved for financing before house hunting",
            "Take time between viewing and deciding",
            "Hire your own home inspector, not agent's recommendation",
            "Understand dual agency conflicts of interest",
        ],
        "red_flags": [
            "Pressures you to make offers without inspection",
            "Won't provide market analysis or comparables",
            "Discourages you from negotiating",
            "Seems more interested in quick sale than your needs",
            "Represents both buyer and seller without disclosure",
        ]
    },
    "car_salesman": {
        "name": "Car Salesman Decoder",
        "icon": "🚗",
        "description": "Decode car dealership tricks and negotiate with confidence",
        "tactics": [
            "Four-square method to confuse pricing",
            "'What payment can you afford?' - focusing on monthly payment only",
            "Bait and switch - advertised car not available",
            "Extended warranty and add-on pressure after price agreement",
            "Good cop/bad cop with manager approval theater",
        ],
        "protection_tips": [
            "Research vehicle value using KBB, Edmunds, and AutoTrader",
            "Get financing pre-approved from your bank or credit union",
            "Negotiate total price, not monthly payment",
            "Be prepared to walk away if pressured",
            "Understand what warranties you actually need",
        ],
        "red_flags": [
            "Won't let you take car to independent mechanic",
            "Refuses to negotiate or provide written estimates",
            "Adds surprise fees at signing",
            "Pressures you to decide today",
            "Won't explain financing terms clearly",
        ]
    },
    "funeral_director": {
        "name": "Funeral Home Director Decoder",
        "icon": "⚱️",
        "description": "Navigate funeral arrangements with confidence and avoid unnecessary upselling during difficult times",
        "tactics": [
            "Exploiting grief and guilt to upsell expensive packages",
            "Suggesting cheaper options show 'lack of love' for deceased",
            "Bundling unnecessary services together",
            "Creating time pressure during emotional vulnerability",
            "Using religious or cultural guilt to justify higher costs",
        ],
        "protection_tips": [
            "Ask for itemized price lists (required by law)",
            "You can purchase caskets from third-party vendors",
            "Embalming is rarely required by law",
            "Consider bringing a trusted friend for support",
            "Know that you can shop around even after death",
        ],
        "red_flags": [
            "Won't provide written price lists",
            "Claims certain services are 'required' when they're not",
            "Pressures immediate decisions on expensive items",
            "Discourages price shopping or comparisons",
            "Uses emotional manipulation about 'honoring' the deceased",
        ]
    }
}

def show_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Decoder Universe</h1>
        <p>Protect Yourself from High-Pressure Sales Tactics</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Choose Your Decoder")
    st.markdown("Click on any decoder below to learn how to protect yourself from common sales manipulation tactics.")
    
    # Create columns for decoder cards
    cols = st.columns(2)
    
    for i, (key, decoder) in enumerate(DECODERS.items()):
        with cols[i % 2]:
            if st.button(
                f"{decoder['icon']}\n\n**{decoder['name']}**\n\n{decoder['description']}", 
                key=f"btn_{key}",
                use_container_width=True
            ):
                st.session_state.current_decoder = key
                st.rerun()

def show_decoder_detail(decoder_key):
    decoder = DECODERS[decoder_key]
    
    # Back button
    if st.button("← Back to Dashboard", key="back_btn"):
        st.session_state.current_decoder = None
        st.rerun()
    
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <h1>{decoder['icon']} {decoder['name']}</h1>
        <p style="font-size: 1.2rem; color: #666;">{decoder['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ⚠️ Common Tactics")
        for tactic in decoder['tactics']:
            st.markdown(f"""
            <div class="tactic-warning">
                <strong>Tactic:</strong> {tactic}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🛡️ Protection Tips")
        for tip in decoder['protection_tips']:
            st.markdown(f"""
            <div class="protection-tip">
                <strong>Protect:</strong> {tip}
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🚩 Red Flags")
        for flag in decoder['red_flags']:
            st.markdown(f"""
            <div class="red-flag">
                <strong>Warning:</strong> {flag}
            </div>
            """, unsafe_allow_html=True)
    
    # Additional resources section
    st.markdown("---")
    st.markdown("### 💡 Remember")
    st.info(
        "You always have the right to:\n"
        "• Take time to think about any decision\n"
        "• Ask questions and get clear answers\n"
        "• Shop around and compare options\n"
        "• Walk away if you feel pressured\n"
        "• Bring a trusted friend or advisor"
    )

def main():
    # Initialize session state
    if 'current_decoder' not in st.session_state:
        st.session_state.current_decoder = None
    
    # Show appropriate page
    if st.session_state.current_decoder:
        show_decoder_detail(st.session_state.current_decoder)
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
