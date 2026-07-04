import streamlit as st

from services.serper import search_company
from services.crawler import crawl_website
from services.openrouter import generate_company_report
from services.competitors import get_competitors
from services.pdf_generator import generate_pdf

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="AI Company Research Assistant",
    page_icon="🔍",
    layout="wide",
)

# ---------------- Styling ---------------- #

st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
}

div[data-testid="stSidebar"]{
    background:#15161d;
}

.stButton button{
    width:100%;
    height:48px;
    border-radius:10px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ---------------- #

st.sidebar.title("⚙ Configuration")

st.sidebar.info(
    "API Keys are loaded automatically from the .env file."
)

model = st.sidebar.selectbox(
    "AI Model",
    [
        "openrouter/free",
        "poolside/laguna-xs-2.1:free"
    ]
)

st.sidebar.success("Configuration Ready")

# ---------------- Main ---------------- #

st.title("🔍 AI Company Research Assistant")

st.caption(
    "Research any company using its name or website URL."
)

company = st.text_input(
    "Company Name or Website URL",
    placeholder="Microsoft or https://microsoft.com"
)

search = st.button("Research Company")

st.divider()

# ---------------- Pipeline ---------------- #

if search:

    if not company.strip():
        st.warning("Please enter a company name.")
        st.stop()

    # ---------------- Search ---------------- #

    with st.spinner("🔍 Searching company..."):

        try:

            search_results = search_company(company)

            organic = search_results.get("organic", [])

            if not organic:
                st.error("No search results found.")
                st.stop()

            website = organic[0]["link"]

            st.success("✅ Official Website Found")

            st.code(website)

        except Exception as e:

            st.error(f"Search Error:\n{e}")
            st.stop()

    # ---------------- Crawl ---------------- #

    with st.spinner("🌐 Crawling website..."):

        crawl_result = crawl_website(website)

    ai_text = crawl_result["ai_text"]
    total_chars = crawl_result["total_chars"]
    pages_crawled = crawl_result["pages_crawled"]

    st.success("✅ Website crawled successfully.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Pages Crawled", pages_crawled)

    with col2:
        st.metric("Characters Extracted", f"{total_chars:,}")

    with col3:
        st.metric("Sent to AI", f"{len(ai_text):,}")

    # ---------------- AI Report ---------------- #

    with st.spinner("🤖 Generating AI report..."):

        report = generate_company_report(
            ai_text,
            model
        )

    st.divider()

    st.header("📄 Company Research Report")

    st.markdown(report)

    # ---------------- Competitor Analysis ---------------- #

    with st.spinner("🏆 Finding competitors..."):

        competitors = get_competitors(
            company,
            model
        )

    st.divider()

    st.header("🏆 Competitor Analysis")

    st.markdown(competitors)

    # ---------------- PDF Download ---------------- #

    pdf_data = generate_pdf(
        company,
        report,
        competitors
    )

    st.divider()

    st.download_button(
        label="📄 Download Research Report (PDF)",
        data=pdf_data,
        file_name=f"{company.replace(' ', '_')}_Research_Report.pdf",
        mime="application/pdf",
        on_click="ignore",
    )