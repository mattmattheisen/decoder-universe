import streamlit as st
from datetime import datetime
import PyPDF2
import docx
from openai import OpenAI

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
    
    .premium-badge {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: #333;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    .preview-badge {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    
    .coming-soon-badge {
        background: #6c757d;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: inline-block;
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
    
    .premium-overlay {
        background: rgba(255, 215, 0, 0.1);
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
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
    
    .upgrade-cta {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'current_decoder' not in st.session_state:
    st.session_state.current_decoder = None

def extract_text_from_file(uploaded_file):
    """Extract text from various file types"""
    text = ""
    
    if uploaded_file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return None
            
    elif uploaded_file.type == "text/plain":
        text = str(uploaded_file.read(), "utf-8")
        
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            doc = docx.Document(uploaded_file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            st.error(f"Error reading Word document: {str(e)}")
            return None
            
    else:
        st.error("Unsupported file type. Please upload PDF, TXT, or DOCX files.")
        return None
    
    return text

def analyze_document_with_ai(file_content, decoder_type):
    """Analyze document using OpenAI based on decoder type"""
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        # Create decoder-specific prompts
        prompts = {
            "financial_advisor": f"""
            Analyze this financial document for hidden fees, conflicts of interest, and predatory tactics.
            
            Document: {file_content}
            
            Provide analysis in this format:
            1. FEES IDENTIFIED: List specific fees with percentages/amounts
            2. CONFLICT INDICATORS: Note any compensation conflicts
            3. RED FLAGS: Identify manipulative language or high-pressure tactics
            4. RECOMMENDATIONS: Suggest protective actions
            
            Focus on: advisor compensation, hidden fees, revenue sharing, proprietary products.
            """,
            
            "real_estate": f"""
            Analyze this real estate document for predatory practices and hidden costs.
            
            Document: {file_content}
            
            Provide analysis in this format:
            1. COSTS IDENTIFIED: All fees, commissions, and charges
            2. AGENCY CONFLICTS: Dual agency or representation issues  
            3. RED FLAGS: Pressure tactics or misleading information
            4. RECOMMENDATIONS: Protective steps to take
            
            Focus on: agent commissions, dual agency, inflated prices, rushed decisions.
            """,
            
            "car_salesman": f"""
            Analyze this automotive document for dealership tricks and hidden costs.
            
            Document: {file_content}
            
            Provide analysis in this format:
            1. COSTS IDENTIFIED: All fees, financing terms, and add-ons
            2. FINANCING TRICKS: Interest rate markups or payment manipulation
            3. RED FLAGS: Bait-and-switch or pressure tactics
            4. RECOMMENDATIONS: Negotiation strategies
            
            Focus on: dealer markup, financing scams, unnecessary add-ons, pressure tactics.
            """,
            
            "funeral_director": f"""
            Analyze this funeral service document for unnecessary costs and emotional manipulation.
            
            Document: {file_content}
            
            Provide analysis in this format:
            1. COSTS IDENTIFIED: All service fees and merchandise charges
            2. UNNECESSARY SERVICES: Optional items presented as required
            3. RED FLAGS: Emotional manipulation or legal misrepresentations
            4. RECOMMENDATIONS: Ways to reduce costs legally
            
            Focus on: required vs optional services, emotional manipulation, overpricing, legal requirements.
            """
        }
        
        prompt = prompts.get(decoder_type, prompts["financial_advisor"])
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing document: {str(e)}. Please check your OpenAI API key configuration."

def show_document_analysis(decoder_key):
    """Show document analysis feature for founding members"""
    st.markdown("### 📄 AI-Powered Document Analysis")
    st.markdown("*Upload contracts, agreements, or proposals for intelligent analysis*")
    
    uploaded_file = st.file_uploader(
        "Choose a document to analyze",
        type=['pdf', 'docx', 'txt'],
        help="Upload financial documents, contracts, or proposals for AI analysis",
        key=f"doc_upload_{decoder_key}"
    )
    
    if uploaded_file is not None:
        st.success("✅ Document uploaded successfully!")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
        
        with col2:
            if st.button("🔍 Analyze Document", use_container_width=True):
                with st.spinner("🤖 AI is analyzing your document..."):
                    # Extract text
                    extracted_text = extract_text_from_file(uploaded_file)
                    
                    if extracted_text:
                        # Analyze with AI
                        analysis_result = analyze_document_with_ai(extracted_text, decoder_key)
                        
                        # Display results
                        st.markdown("### 📊 Analysis Results")
                        st.markdown(analysis_result)
                        
                        # Add download option
                        st.download_button(
                            label="📥 Download Analysis Report",
                            data=f"Document Analysis Report\n\nFile: {uploaded_file.name}\nAnalyzed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{analysis_result}",
                            file_name=f"decoder_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("Could not extract text from document. Please try a different file.")

# Session state initialization
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'current_decoder' not in st.session_state:
    st.session_state.current_decoder = None

# Decoder data structure with preview vs premium content
DECODERS = {
    "financial_advisor": {
        "name": "Financial Advisor Decoder",
        "icon": "💰",
        "description": "Protect yourself from high-pressure financial advisor sales tactics",
        "is_available": True,
        "preview_tactics": [
            "Creating artificial urgency: 'This offer expires today!'",
            "Fear-mongering about market crashes",
            "Using complex jargon to confuse clients"
        ],
        "premium_tactics": [
            "Churning - excessive trading to generate commissions",
            "Selling proprietary products with hidden fees",
            "Cold calling during vulnerable life events",
            "Bait-and-switch investment recommendations",
            "Using fake credentials or misleading titles"
        ],
        "preview_tips": [
            "Always ask for fee disclosures in writing",
            "Take time to research any recommendation",
            "Get a second opinion from a fee-only advisor"
        ],
        "premium_tips": [
            "Check advisor's FINRA BrokerCheck record",
            "Understand the difference between fiduciary and suitability standards",
            "Calculate total cost of ownership for all investments",
            "Review statements for unauthorized transactions",
            "Know your rights for dispute resolution through FINRA arbitration"
        ],
        "preview_flags": [
            "Refuses to explain fees clearly",
            "Pushes immediate decisions",
            "Only recommends high-fee products"
        ],
        "premium_flags": [
            "Claims to be a 'financial planner' without proper credentials",
            "Avoids putting recommendations in writing",
            "Discourages you from reading prospectuses",
            "Has complaints or disciplinary actions on their record",
            "Pressures you to liquidate existing investments immediately"
        ]
    },
    "real_estate": {
        "name": "Real Estate Agent Decoder",
        "icon": "🏠",
        "description": "Navigate high-pressure real estate tactics and understand what agents really mean",
        "is_available": True,
        "preview_tactics": [
            "'Other buyers are interested' - creating false competition",
            "Suggesting inflated listing prices to win business",
            "Rushing you through property viewings"
        ],
        "premium_tactics": [
            "Dual agency without proper disclosure",
            "Steering buyers away from certain neighborhoods",
            "Withholding negative property information",
            "Pocket listings to benefit preferred buyers",
            "Inflating comparable sales data"
        ],
        "preview_tips": [
            "Research comparable sales yourself",
            "Get pre-approved financing before hunting",
            "Take time between viewing and deciding"
        ],
        "premium_tips": [
            "Understand agency relationships and fiduciary duties",
            "Use independent home inspectors and appraisers",
            "Research neighborhood crime, schools, and development plans",
            "Know your rights under state real estate disclosure laws",
            "Negotiate commission rates and terms upfront"
        ],
        "preview_flags": [
            "Pressures you to make offers without inspection",
            "Won't provide market analysis",
            "Discourages negotiating"
        ],
        "premium_flags": [
            "Represents both parties without clear written disclosure",
            "Rushes you through contract signing",
            "Discourages attorney review of contracts",
            "Won't provide references from recent clients",
            "Shows properties only during optimal conditions"
        ]
    },
    "car_salesman": {
        "name": "Car Salesman Decoder",
        "icon": "🚗",
        "description": "Decode car dealership tricks and negotiate with confidence",
        "is_available": True,
        "preview_tactics": [
            "Four-square method to confuse pricing",
            "'What payment can you afford?' approach",
            "Bait and switch with advertised cars"
        ],
        "premium_tactics": [
            "Yo-yo financing - calling back after deal is signed",
            "Packing payments with unnecessary add-ons",
            "Spot delivery before financing is finalized",
            "Trade-in lowballing and equity manipulation",
            "Extended warranty fear tactics"
        ],
        "preview_tips": [
            "Research vehicle value using KBB and Edmunds",
            "Get financing pre-approved from bank",
            "Negotiate total price, not monthly payment"
        ],
        "premium_tips": [
            "Understand dealer holdback and manufacturer incentives",
            "Know the difference between invoice and MSRP",
            "Get all agreements in writing before signing",
            "Understand your right to cancel extended warranties",
            "Know lemon law protections in your state"
        ],
        "preview_flags": [
            "Won't let you take car to mechanic",
            "Refuses to negotiate or provide estimates",
            "Adds surprise fees at signing"
        ],
        "premium_flags": [
            "Changes terms after verbal agreement",
            "Pressures you to buy same day with 'manager specials'",
            "Won't explain financing terms line by line",
            "Insists on spot delivery before loan approval",
            "Makes verbal promises not included in written contract"
        ]
    },
    "funeral_director": {
        "name": "Funeral Home Director Decoder",
        "icon": "⚱️",
        "description": "Navigate funeral arrangements with confidence and avoid unnecessary upselling during difficult times",
        "is_available": True,
        "preview_tactics": [
            "Exploiting grief to upsell expensive packages",
            "Suggesting cheaper options show 'lack of love'",
            "Bundling unnecessary services together"
        ],
        "premium_tactics": [
            "Claiming embalming is required when it's not",
            "Refusing to show basic casket options first",
            "Adding unauthorized charges for 'standard' services",
            "Pressuring immediate payment in full",
            "Misrepresenting legal requirements"
        ],
        "preview_tips": [
            "Ask for itemized price lists (required by law)",
            "Know you can purchase caskets elsewhere",
            "Understand embalming is rarely required"
        ],
        "premium_tips": [
            "Know your rights under the FTC Funeral Rule",
            "Understand the difference between burial and cremation costs",
            "Get multiple quotes for comparison",
            "Know which services are actually required by law",
            "Understand pre-need contract protections and cancellation rights"
        ],
        "preview_flags": [
            "Won't provide written price lists",
            "Claims services are 'required' when optional",
            "Pressures immediate expensive decisions"
        ],
        "premium_flags": [
            "Refuses to accept caskets from other vendors",
            "Won't itemize charges or explain fees",
            "Discourages price shopping with other funeral homes",
            "Makes verbal promises not included in written contracts",
            "Charges for services without authorization"
        ]
    }
}

# Coming Soon decoders
COMING_SOON = [
    {"name": "Timeshare Decoder", "icon": "🏖️", "description": "Escape timeshare presentation traps and high-pressure vacation sales"},
    {"name": "Crypto Decoder", "icon": "₿", "description": "Identify cryptocurrency scams and predatory investment schemes"},
    {"name": "Insurance Decoder", "icon": "🛡️", "description": "Navigate insurance sales tactics and understand policy fine print"}
]

def show_premium_upgrade():
    """Display premium upgrade call-to-action"""
    st.markdown("""
    <div class="upgrade-cta">
        <h3>🌟 Become a Founding Member - Lifetime Access!</h3>
        <p><strong>One payment = Lifetime access to ALL current and future decoders!</strong><br>
        Join our founding members for just <strong>$12.95 - Forever!</strong></p>
        <ul style="text-align: left; max-width: 500px; margin: 1rem auto;">
            <li>🔓 <strong>ALL 4 Premium Decoders:</strong> Financial, Real Estate, Car Sales & Funeral</li>
            <li>📄 <strong>Unlimited document scanning & analysis</strong> - for life</li>
            <li>🎯 <strong>Complete tactics & red flags databases</strong> for every industry</li>
            <li>🧠 <strong>Advanced psychological manipulation guides</strong> for all sales types</li>
            <li>⚡ <strong>Lifetime access to ALL future decoders</strong> (Timeshare, Crypto, Insurance & more)</li>
            <li>🛡️ <strong>Founding member priority support</strong> and consultation</li>
        </ul>
        <p style="margin-top: 1rem;"><em>💡 Pay once, protected forever. No subscriptions, no recurring bills!</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌟 Become Founding Member - $12.95 Lifetime!", use_container_width=True, type="primary"):
            st.session_state.is_premium = True
            st.success("🎉 Welcome, Founding Member! You now have lifetime access to ALL decoders and future releases.")
            st.rerun()

def show_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Decoder Universe</h1>
        <p>Protect Yourself from High-Pressure Sales Tactics<br>Don't Get Sold - Get Decoded</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium status indicator
    if st.session_state.is_premium:
        st.success("🌟 **Founding Member Status Active** - Lifetime access to ALL decoders and future releases!")
    else:
        st.info("🔍 **Free Preview Mode** - Join our founding members for lifetime access to everything")
    
    st.markdown("### Available Decoders")
    
    # Main decoders in 2x2 grid
    cols = st.columns(2)
    
    for i, (key, decoder) in enumerate(DECODERS.items()):
        with cols[i % 2]:
            badge_html = '<div class="premium-badge">Founding Member Features Available</div>' if not st.session_state.is_premium else '<div class="preview-badge">Founding Member Active</div>'
            
            if st.button(
                f"{decoder['icon']}\n\n**{decoder['name']}**\n\n{decoder['description']}", 
                key=f"btn_{key}",
                use_container_width=True
            ):
                st.session_state.current_decoder = key
                st.rerun()
            
            # Show premium badge
            st.markdown(badge_html, unsafe_allow_html=True)
    
    # Coming Soon section
    st.markdown("---")
    
    # Why We're Different section
    st.markdown("### 🛡️ Why We're Different")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <strong>🎯 We Practice What We Preach</strong><br>
                <span style="color: #666;">No predatory recurring billing - just honest, one-time pricing</span>
            </div>
            <div>
                <strong>🛡️ True Consumer Protection</strong><br>
                <span style="color: #666;">Our protection extends to our own fair pricing model</span>
            </div>
            <div>
                <strong>💡 Anti-Manipulation Pricing</strong><br>
                <span style="color: #666;">No subscription traps in an industry full of them</span>
            </div>
            <div>
                <strong>🤝 Builds Genuine Trust</strong><br>
                <span style="color: #666;">We're not trying to extract ongoing revenue from you</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Coming Soon")
    st.markdown("*Expanding our protection universe with these upcoming decoders:*")
    
    coming_cols = st.columns(3)
    for i, decoder in enumerate(COMING_SOON):
        with coming_cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 2px dashed #ccc; border-radius: 10px; margin: 0.5rem 0;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{decoder['icon']}</div>
                <div class="coming-soon-badge">Coming Soon</div>
                <div style="font-weight: bold; margin: 0.5rem 0;">{decoder['name']}</div>
                <div style="font-size: 0.9rem; color: #666;">{decoder['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Premium upgrade CTA for free users
    if not st.session_state.is_premium:
        st.markdown("---")
        show_premium_upgrade()

def show_decoder_detail(decoder_key):
    decoder = DECODERS[decoder_key]
    
    # Back button
    if st.button("← Back to Dashboard", key="back_btn"):
        st.session_state.current_decoder = None
        st.rerun()
    
    # Header with premium status
    premium_indicator = "🌟 Founding Member" if st.session_state.is_premium else "🔍 Preview Mode"
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">{premium_indicator}</div>
        <h1>{decoder['icon']} {decoder['name']}</h1>
        <p style="font-size: 1.2rem; color: #666;">{decoder['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### ⚠️ Common Tactics")
        
        # Show preview tactics
        for tactic in decoder['preview_tactics']:
            st.markdown(f"""
            <div class="tactic-warning">
                <strong>Tactic:</strong> {tactic}
            </div>
            """, unsafe_allow_html=True)
        
        # Show premium tactics if user has premium
        if st.session_state.is_premium:
            st.markdown("**🌟 Founding Member Tactics:**")
            for tactic in decoder['premium_tactics']:
                st.markdown(f"""
                <div class="tactic-warning">
                    <strong>Advanced:</strong> {tactic}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="premium-overlay">
                <strong>🔒 Founding Member Feature</strong><br>
                Unlock 5+ additional advanced tactics used by industry professionals.<br>
                <em>Founding members get ALL current and future decoder content - forever!</em>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🛡️ Protection Tips")
        
        # Show preview tips
        for tip in decoder['preview_tips']:
            st.markdown(f"""
            <div class="protection-tip">
                <strong>Protect:</strong> {tip}
            </div>
            """, unsafe_allow_html=True)
        
        # Show premium tips if user has premium
        if st.session_state.is_premium:
            st.markdown("**🌟 Founding Member Protection:**")
            for tip in decoder['premium_tips']:
                st.markdown(f"""
                <div class="protection-tip">
                    <strong>Advanced:</strong> {tip}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="premium-overlay">
                <strong>🔒 Founding Member Feature</strong><br>
                Access 5+ expert-level protection strategies across ALL industries.<br>
                <em>Lifetime access = comprehensive defense for every sales situation.</em>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🚩 Red Flags")
        
        # Show preview flags
        for flag in decoder['preview_flags']:
            st.markdown(f"""
            <div class="red-flag">
                <strong>Warning:</strong> {flag}
            </div>
            """, unsafe_allow_html=True)
        
        # Show premium flags if user has premium
        if st.session_state.is_premium:
            st.markdown("**🌟 Founding Member Red Flags:**")
            for flag in decoder['premium_flags']:
                st.markdown(f"""
                <div class="red-flag">
                    <strong>Critical:</strong> {flag}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="premium-overlay">
                <strong>🔒 Founding Member Feature</strong><br>
                Discover 5+ critical warning signs across ALL decoder categories.<br>
                <em>Founding members get expert red flags for every sales scenario - forever!</em>
            </div>
            """, unsafe_allow_html=True)
    
    # Premium features section for free users
    if not st.session_state.is_premium:
        st.markdown("---")
        st.markdown("### 🔒 Founding Member Exclusive Features")
        
        prem_col1, prem_col2 = st.columns(2)
        with prem_col1:
            st.markdown("""
            **📄 Lifetime Document Analysis**
            - Upload ANY contracts across all decoder categories - forever
            - AI-powered analysis for financial, real estate, auto & funeral documents
            - Get plain-English explanations of complex language - no limits
            """)
        
        with prem_col2:
            st.markdown("""
            **🧠 Complete Psychology Tactics Library**
            - Deep-dive into manipulation psychology across ALL industries
            - Learn cognitive biases exploited by every type of salesperson
            - Master counter-techniques for any sales situation - lifetime access
            """)
        
        show_premium_upgrade()
    
    # Universal remember section
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
    # Show appropriate page
    if st.session_state.current_decoder:
        show_decoder_detail(st.session_state.current_decoder)
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
