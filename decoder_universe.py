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

# App URLs for premium access
PREMIUM_APP_URLS = {
    "financial_advisor": "https://advisor-decoder-g33giprnbapgqxybkgxk5h.streamlit.app/",
    "car_salesman": "https://car-salesman-decoder-tiye3psbwpspizha8kta8o.streamlit.app/",
    "real_estate": "https://real-estate-agent-decoder-cqunc4r2zarq4rtqkej7bh.streamlit.app/",
    "funeral_director": "https://funeral-home-decoder-p6bfaya2wqy4wgzoxrsa48.streamlit.app/"
}

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

def show_premium_app_access(decoder_key):
    """Show premium app access for founding members"""
    decoder = DECODERS[decoder_key]
    app_url = PREMIUM_APP_URLS.get(decoder_key)
    
    if app_url:
        st.markdown("---")
        st.markdown("### 🌟 Founding Member Exclusive Access")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            **🚀 Launch Your Complete {decoder['name']} App**
            
            Access the full-featured app with advanced tools:
            • Interactive calculators and analysis tools
            • Comprehensive databases and reference materials  
            • Meeting preparation and strategy guides
            • Psychology and manipulation tactics training
            • Real industry data and case studies
            """)
        
        with col2:
            st.markdown("&nbsp;")  # Spacing
            if st.button(f"🚀 Launch Full {decoder['icon']} App", use_container_width=True, type="primary"):
                st.markdown(f"""
                <script>
                window.open('{app_url}', '_blank');
                </script>
                """, unsafe_allow_html=True)
                st.success(f"Opening your complete {decoder['name']} app in a new tab!")
                st.markdown(f"**If it didn't open automatically, [click here]({app_url})**")

def show_legal_disclaimers():
    """Show comprehensive legal disclaimers and terms"""
    st.markdown("---")
    st.markdown("### ⚖️ Legal Disclaimers & Terms of Use")
    
    disclaimer_tabs = st.tabs(["📋 General Disclaimer", "🏦 Financial", "🏠 Real Estate", "🚗 Automotive", "⚱️ Funeral", "🔒 Privacy & Data"])
    
    with disclaimer_tabs[0]:
        st.markdown("""
        **EDUCATIONAL PURPOSES ONLY**
        
        Decoder Universe provides educational information designed to help consumers understand sales tactics and protect themselves from manipulation. This platform:
        
        • **Is NOT professional advice** - We do not provide financial, legal, real estate, or other professional advice
        • **Educational content only** - All information is for informational and educational purposes
        • **No professional relationship** - Use of this platform does not create any advisor-client relationship
        • **User responsibility** - You assume full responsibility for any decisions based on this information
        • **No guarantees** - We make no warranties about outcomes from using this information
        • **Consult professionals** - Always consult qualified professionals for specific advice
        
        **LIMITATION OF LIABILITY**
        
        To the maximum extent permitted by law, Decoder Universe and its operators shall not be liable for any direct, indirect, incidental, consequential, or punitive damages arising from your use of this platform, including but not limited to financial losses, business interruption, or personal injury.
        
        **USER RESPONSIBILITIES**
        
        By using this platform, you agree to:
        • Use information for educational purposes only
        • Make independent decisions about professional services
        • Verify all information independently before taking action
        • Not rely solely on this platform for important decisions
        • Consult appropriate professionals for advice
        """)
    
    with disclaimer_tabs[1]:
        st.markdown("""
        **FINANCIAL SERVICES DISCLAIMER**
        
        **NOT INVESTMENT OR FINANCIAL ADVICE**
        • Content related to financial advisors, fees, and investments is educational only
        • We are not registered investment advisors, broker-dealers, or financial planners
        • No content constitutes investment advice, financial planning, or recommendations
        • Past performance information does not predict future results
        
        **REGULATORY COMPLIANCE**
        • Fee and compensation data is based on publicly available disclosure documents
        • We encourage users to verify all information with official regulatory sources
        • Check FINRA BrokerCheck and SEC records for advisor information
        • Understand that regulations and compensation structures change over time
        
        **PROFESSIONAL CONSULTATION REQUIRED**
        • Always consult licensed financial professionals for personalized advice
        • Consider fee-only financial advisors for unbiased guidance
        • Verify all advisor credentials and regulatory standing independently
        • Make investment decisions based on your individual circumstances
        """)
    
    with disclaimer_tabs[2]:
        st.markdown("""
        **REAL ESTATE SERVICES DISCLAIMER**
        
        **NOT REAL ESTATE ADVICE**
        • Content about real estate agents and transactions is educational only
        • We are not licensed real estate professionals or attorneys
        • Real estate laws and practices vary by state and locality
        • No content constitutes real estate or legal advice
        
        **MARKET INFORMATION**
        • Market data and pricing information may not be current or accurate
        • Real estate values and market conditions change frequently
        • Always verify market information with local real estate professionals
        • Obtain current market analyses for specific properties or areas
        
        **PROFESSIONAL CONSULTATION REQUIRED**
        • Consult licensed real estate agents for market guidance
        • Use qualified real estate attorneys for contract and legal matters
        • Obtain professional inspections and appraisals
        • Verify all legal requirements with local authorities
        """)
    
    with disclaimer_tabs[3]:
        st.markdown("""
        **AUTOMOTIVE SERVICES DISCLAIMER**
        
        **NOT AUTOMOTIVE ADVICE**
        • Content about car buying and dealership practices is educational only
        • We are not automotive professionals or consumer finance experts
        • Vehicle values, financing terms, and regulations vary by location
        • No content constitutes specific purchasing or financing advice
        
        **VEHICLE INFORMATION**
        • Vehicle values and market data may not be current
        • Financing terms and incentives change frequently
        • Always verify vehicle history, condition, and value independently
        • Obtain professional inspections for used vehicles
        
        **PROFESSIONAL CONSULTATION REQUIRED**
        • Consult automotive professionals for technical advice
        • Use qualified mechanics for vehicle inspections
        • Verify financing terms with multiple lenders
        • Understand your consumer rights under applicable laws
        """)
    
    with disclaimer_tabs[4]:
        st.markdown("""
        **FUNERAL SERVICES DISCLAIMER**
        
        **NOT LEGAL OR FUNERAL INDUSTRY ADVICE**
        • Content about funeral homes and services is educational only
        • We are not funeral industry professionals or attorneys
        • Funeral regulations and requirements vary by state and locality
        • No content constitutes legal or professional funeral advice
        
        **REGULATORY INFORMATION**
        • References to FTC Funeral Rule and state laws are for general information
        • Regulations and requirements may have changed since content creation
        • Always verify current legal requirements with appropriate authorities
        • Funeral home practices and pricing vary significantly
        
        **PROFESSIONAL CONSULTATION REQUIRED**
        • Consult funeral industry professionals for specific guidance
        • Use qualified attorneys for legal matters related to death and estates
        • Verify all legal requirements with local authorities
        • Consider emotional support resources during difficult times
        """)
    
    with disclaimer_tabs[5]:
        st.markdown("""
        **PRIVACY & DATA PROTECTION**
        
        **DATA COLLECTION**
        • We collect minimal data necessary for platform operation
        • Document analysis is processed securely and not stored permanently
        • Usage analytics may be collected to improve the platform
        • No personal financial information is stored on our servers
        
        **THIRD-PARTY SERVICES**
        • Document analysis uses OpenAI services subject to their privacy policy
        • Platform hosted on Streamlit Cloud subject to their terms
        • We do not control third-party data handling practices
        • Review third-party privacy policies for complete information
        
        **DATA SECURITY**
        • We implement reasonable security measures to protect user data
        • No system is completely secure - use caution with sensitive information
        • We are not responsible for unauthorized access beyond our reasonable control
        • Report security concerns immediately to our support team
        
        **USER RIGHTS**
        • You may request deletion of any data we have collected
        • You can discontinue use of the platform at any time
        • Contact us for questions about data handling or privacy concerns
        • We will respond to privacy requests in accordance with applicable law
        """)

def show_terms_of_service():
    """Show terms of service"""
    st.markdown("### 📜 Terms of Service")
    
    terms_tabs = st.tabs(["🎯 User Agreement", "💳 Payment Terms", "🚫 Prohibited Uses", "⚖️ Legal Terms"])
    
    with terms_tabs[0]:
        st.markdown("""
        **ACCEPTANCE OF TERMS**
        
        By accessing and using Decoder Universe, you accept and agree to be bound by these Terms of Service. If you do not agree to these terms, you may not use this platform.
        
        **PERMITTED USES**
        • Educational research and personal knowledge enhancement
        • Preparation for interactions with sales professionals
        • Understanding industry practices and consumer protection
        • Personal reference and decision-making support
        
        **ACCOUNT RESPONSIBILITIES**
        • Provide accurate information if creating an account
        • Maintain confidentiality of any account credentials
        • Notify us immediately of unauthorized account access
        • Use the platform in accordance with these terms
        
        **CONTENT ACCURACY**
        • We strive for accuracy but make no guarantees about content correctness
        • Information may become outdated or change without notice
        • Users should verify all information independently
        • Report inaccuracies to help us improve the platform
        """)
    
    with terms_tabs[1]:
        st.markdown("""
        **FOUNDING MEMBER TERMS**
        
        **LIFETIME ACCESS**
        • Founding membership grants lifetime access to current and future decoder applications
        • Access includes all premium features and content available at time of payment
        • New features and decoders will be added to your lifetime access at no additional cost
        
        **PAYMENT PROCESSING**
        • Payments processed securely through Stripe payment systems
        • All sales are final - no refunds after access is granted
        • Payment confirmation required before premium access is activated
        • Contact support within 24 hours for payment processing issues
        
        **SERVICE AVAILABILITY**
        • We strive for 99% uptime but cannot guarantee continuous availability
        • Scheduled maintenance will be announced in advance when possible
        • Premium access may be temporarily unavailable during system updates
        • No refunds for temporary service interruptions
        """)
    
    with terms_tabs[2]:
        st.markdown("""
        **PROHIBITED ACTIVITIES**
        
        You may NOT use this platform to:
        • Provide professional advice to others without proper licensing
        • Reproduce, distribute, or sell platform content without permission
        • Attempt to reverse engineer or copy platform functionality
        • Upload malicious files or attempt to compromise platform security
        • Use automated systems to access or scrape platform content
        • Violate any applicable laws or regulations
        • Harass other users or platform operators
        • Misrepresent your identity or credentials
        
        **CONTENT GUIDELINES**
        • Document uploads should be legitimate personal documents only
        • Do not upload documents containing others' personal information
        • Do not upload copyrighted materials you don't have rights to analyze
        • We reserve the right to refuse analysis of inappropriate content
        
        **ENFORCEMENT**
        • Violations may result in immediate termination of access
        • We reserve the right to refuse service to anyone
        • Legal action may be pursued for serious violations
        • No refunds for termination due to terms violations
        """)
    
    with terms_tabs[3]:
        st.markdown("""
        **LEGAL PROVISIONS**
        
        **INTELLECTUAL PROPERTY**
        • All platform content, design, and functionality is proprietary
        • Users retain rights to documents they upload for analysis
        • Analysis results are provided for user's personal use only
        • No license granted for commercial use of platform content
        
        **DISPUTE RESOLUTION**
        • Good faith effort to resolve disputes directly before legal action
        • Disputes subject to jurisdiction where platform operators are located
        • Arbitration may be required for certain types of disputes
        • Class action lawsuits are waived to the extent permitted by law
        
        **CHANGES TO TERMS**
        • Terms may be updated periodically with reasonable notice
        • Continued use after changes constitutes acceptance of new terms
        • Material changes will be highlighted and require explicit acceptance
        • Users may discontinue use if they disagree with term changes
        
        **CONTACT INFORMATION**
        • Questions about terms should be directed to platform support
        • Legal notices should be sent to designated contact address
        • We will respond to legitimate inquiries within reasonable time
        • Emergency security issues should be reported immediately
        """)

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
            "The 5-Stage Psychological Manipulation Process: PREPARE (planning influence), CONNECT (false intimacy), EXPLORE (extracting vulnerabilities), PRESENT (using your words against you), DEVELOP (securing the close)",
            "Variable compensation 55-80% creates bias - advisors at major firms earn more from complex products vs simple investments",
            "Revenue sharing agreements with fund companies - advisors get paid by investment companies to sell their products",
            "The 'FIND' questioning technique: Facts (your situation), Issues (pain points), Needs (what you want), Drivers (emotional triggers)",
            "State of mind manipulation - trained to manage your emotional state during meetings to increase receptivity",
            "Real compensation data: Company A pays 0.001 rate for Wealth Services vs 0.0001 for Money Market (10x difference)",
            "Company B relationship pay: 32-42 basis points for managed accounts vs 9-12 for self-directed (3-4x difference)",
            "Solutions pay bonuses: $200 per $100k enrolled in advisory programs creates enrollment bias",
            "Asset consolidation incentives: $80 per $100k transferred creates pressure to move your accounts",
            "Annual engagement fees on your balances - ongoing payments based on what you invest in"
        ],
        "preview_tips": [
            "Always ask for fee disclosures in writing",
            "Take time to research any recommendation",
            "Get a second opinion from a fee-only advisor"
        ],
        "premium_tips": [
            "Essential first meeting questions: 'How exactly are you compensated? Are you a fiduciary at all times? Do you receive money from fund companies?'",
            "Fee negotiation: Fees are often negotiable, especially for larger accounts - ask for written breakdown and compare to industry averages",
            "Decode advisor-speak: 'Let's diversify your portfolio' = I want fees from multiple sources. 'Professional management' = I earn more from managed accounts",
            "Use the meeting prep tool: Bring specific questions about their compensation structure and document their answers",
            "Conflict identification: Look for commission-based compensation, proprietary products, revenue sharing, sales contests, referral bonuses",
            "Check FINRA BrokerCheck for complaints and disciplinary actions before meeting",
            "Understand fiduciary vs suitability standards - fiduciaries must act in your best interest at ALL times",
            "Calculate total cost of ownership: Include management fees, platform fees, fund expenses, and trading costs",
            "Company-specific protections: Company C charges $175 annual fees unless you have $500k+ - know these pressure tactics",
            "Use their psychology against them: Ask 'What would you recommend if you weren't paid differently for various products?'"
        ],
        "preview_flags": [
            "Refuses to explain fees clearly",
            "Pushes immediate decisions",
            "Only recommends high-fee products"
        ],
        "premium_flags": [
            "Psychological red flag phrases: 'This is what I use for my own family', 'You need to act quickly', 'Don't worry about the fees'",
            "State manipulation tactics: Meeting designed to impress/intimidate, using your fears to create urgency, making you feel special",
            "The 5-stage process in action: Overly structured meetings, questions designed to find vulnerabilities, using your own words against you",
            "Compensation-driven recommendations: Only suggesting products from companies with revenue sharing agreements",
            "False scarcity tactics: 'This opportunity won't be available next week', 'I can only offer this rate if you decide today'",
            "EXPLORE stage red flags: Questions like 'What keeps you up at night about money?' designed to find emotional pressure points",
            "PRESENT stage manipulation: 'Remember when you said your biggest fear was...' using your vulnerabilities against you",
            "Revenue sharing concealment: Mentions fund performance but won't disclose they receive payments from fund companies",
            "Annual fee pressure: Company C-style tactics pressuring you toward advisory accounts to 'waive' fees",
            "Referral payment conflicts: Introducing you to 'specialists' because they earn $450-$3,500 referral bonuses"
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
        <p><strong>One payment = Lifetime access to ALL complete decoder apps + AI analysis!</strong><br>
        Join our founding members for just <strong>$12.95 - Forever!</strong></p>
        <ul style="text-align: left; max-width: 500px; margin: 1rem auto;">
            <li>🚀 <strong>Complete Access to 4 Full Decoder Apps:</strong> Advanced tools, calculators & databases</li>
            <li>🧠 <strong>Psychology & Manipulation Training:</strong> 5-stage process, meeting prep, negotiation</li>
            <li>💰 <strong>Real Industry Compensation Data:</strong> Actual disclosure documents from major firms</li>
            <li>📄 <strong>AI Document Analysis:</strong> Upload contracts for intelligent analysis - unlimited</li>
            <li>⚡ <strong>Lifetime access to ALL future decoders</strong> (Timeshare, Crypto, Insurance & more)</li>
            <li>🛡️ <strong>Founding member priority support</strong> and consultation</li>
        </ul>
        <p style="margin-top: 1rem;"><em>💡 4 complete professional apps + AI analysis + future releases - all for life!</em></p>
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
    
    # Footer with legal links
    st.markdown("---")
    st.markdown("### ⚖️ Legal & Compliance")
    
    footer_col1, footer_col2, footer_col3, footer_col4 = st.columns(4)
    
    with footer_col1:
        if st.button("📋 Disclaimers", use_container_width=True, key="footer_disclaimers"):
            st.session_state.show_legal = True
            st.rerun()
    
    with footer_col2:
        if st.button("📜 Terms of Service", use_container_width=True, key="footer_terms"):
            st.session_state.show_terms = True
            st.rerun()
    
    with footer_col3:
        if st.button("🔒 Privacy Policy", use_container_width=True, key="footer_privacy"):
            st.session_state.show_privacy = True
            st.rerun()
    
    with footer_col4:
        if st.button("📞 Compliance Info", use_container_width=True, key="footer_compliance"):
            st.info("""
            **For Compliance Inquiries:**
            
            This platform provides educational content only and does not constitute professional advice. 
            
            All content is designed to help consumers understand sales tactics and make informed decisions.
            
            Questions about compliance or regulatory matters should be directed to appropriate legal counsel.
            """)
    
    # Copyright and version info
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem; padding: 1rem; border-top: 1px solid #eee;'>
        <p><strong>Decoder Universe</strong> | Educational Consumer Protection Platform</p>
        <p><small>© 2025 Decoder Universe. All rights reserved. | Version 1.0 | For educational purposes only.</small></p>
        <p><small>This platform does not provide professional advice. Consult qualified professionals for specific guidance.</small></p>
    </div>
    """, unsafe_allow_html=True)

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
    
    # Founding Member App Access
    if st.session_state.is_premium:
        show_premium_app_access(decoder_key)
    
    # Founding Member Document Analysis
    if st.session_state.is_premium:
        st.markdown("---")
        show_document_analysis(decoder_key)
    
    # Premium features section for free users
    if not st.session_state.is_premium:
        st.markdown("---")
        st.markdown("### 🔒 Founding Member Exclusive Features")
        
        prem_col1, prem_col2 = st.columns(2)
        with prem_col1:
            st.markdown("""
            **🚀 Complete Decoder App Access**
            - Launch full-featured individual decoder apps with advanced tools
            - Interactive calculators, databases, and comprehensive analysis
            - Meeting preparation guides and negotiation strategies
            - Psychology training and real industry compensation data
            """)
        
        with prem_col2:
            st.markdown("""
            **📄 AI-Powered Document Analysis**
            - Upload ANY contracts across all decoder categories - forever
            - Advanced AI analysis for financial, real estate, auto & funeral documents
            - Get plain-English explanations and red flag detection - no limits
            - Download detailed analysis reports for your records
            """)
        
        show_premium_upgrade()
    
    # Legal and compliance section
    st.markdown("---")
    
    legal_col1, legal_col2, legal_col3 = st.columns(3)
    
    with legal_col1:
        if st.button("📋 Legal Disclaimers", use_container_width=True):
            st.session_state.show_legal = True
            st.rerun()
    
    with legal_col2:
        if st.button("📜 Terms of Service", use_container_width=True):
            st.session_state.show_terms = True
            st.rerun()
    
    with legal_col3:
        if st.button("🔒 Privacy Policy", use_container_width=True):
            st.session_state.show_privacy = True
            st.rerun()
    
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
    # Initialize session state for legal pages
    if 'show_legal' not in st.session_state:
        st.session_state.show_legal = False
    if 'show_terms' not in st.session_state:
        st.session_state.show_terms = False
    if 'show_privacy' not in st.session_state:
        st.session_state.show_privacy = False
    
    # Show legal pages if requested
    if st.session_state.show_legal:
        if st.button("← Back to Decoder Universe", key="back_from_legal"):
            st.session_state.show_legal = False
            st.rerun()
        show_legal_disclaimers()
        return
    
    if st.session_state.show_terms:
        if st.button("← Back to Decoder Universe", key="back_from_terms"):
            st.session_state.show_terms = False
            st.rerun()
        show_terms_of_service()
        return
    
    if st.session_state.show_privacy:
        if st.button("← Back to Decoder Universe", key="back_from_privacy"):
            st.session_state.show_privacy = False
            st.rerun()
        st.markdown("### 🔒 Privacy Policy")
        st.markdown("""
        **DATA COLLECTION & USE**
        
        Decoder Universe collects minimal data to provide educational services:
        
        **Information We Collect:**
        • Usage analytics (pages visited, features used) to improve the platform
        • Document content temporarily for AI analysis (not stored permanently)
        • Payment information (processed securely through Stripe, not stored by us)
        • Account status (free vs founding member) to control access
        
        **How We Use Information:**
        • Provide document analysis services through OpenAI API
        • Improve platform functionality and user experience
        • Verify founding member status for premium access
        • Communicate important service updates
        
        **Information Sharing:**
        • Document content shared with OpenAI for analysis (subject to their privacy policy)
        • Payment processing through Stripe (subject to their privacy policy)
        • We do not sell or share personal information with other third parties
        • Anonymous usage statistics may be shared for research purposes
        
        **Data Security:**
        • All data transmission encrypted using industry-standard protocols
        • Document analysis performed securely and content not permanently stored
        • Access controls protect against unauthorized data access
        • Regular security assessments and updates to protect user information
        
        **Your Rights:**
        • Request deletion of any data we have collected about you
        • Ask questions about our data handling practices
        • Discontinue use of the platform at any time
        • Contact us to exercise your privacy rights
        
        **Contact for Privacy Matters:**
        • Email privacy questions to: [insert contact email]
        • We will respond to privacy requests within 30 days
        • Report security concerns immediately for prompt investigation
        
        **Updates to Privacy Policy:**
        • We may update this policy to reflect changes in our practices
        • Material changes will be announced prominently on the platform
        • Continued use after changes constitutes acceptance of updated policy
        """)
        return
    
    # Show appropriate page based on navigation
    if st.session_state.current_decoder:
        show_decoder_detail(st.session_state.current_decoder)
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
