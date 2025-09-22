import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ----------------------------------------
# Sample Dataset (extend with full roles)
# ----------------------------------------
data = {
    "Banking & Finance": {
        "Retail Banking": {
            "Retail Banking Analyst": {
                "description": "Supports branch banking operations, analyzing customer accounts, credit products, and consumer lending. Focuses on personal finance products like savings, credit cards, and loans.",
                "majors": {
                    "Finance": ["Consumer Finance", "Banking Systems", "Intro to Corporate Finance", "Risk Management"],
                    "Business Administration": ["Principles of Management", "Business Law", "Organizational Behavior", "Operations Management"],
                    "Marketing": ["Consumer Behavior", "Marketing Analytics", "Digital Marketing", "Sales Management"],
                },
            }
        },
        "Investment Banking": {
            "Investment Banking Analyst": {
                "description": "Evaluates potential investment opportunities and assists in executing M&A and capital market transactions.",
                "majors": {
                    "Finance": ["Valuation", "Mergers & Acquisitions", "Financial Modeling"],
                    "Accounting": ["Intermediate Accounting", "Financial Statement Analysis"],
                    "Economics": ["Game Theory", "International Economics"],
                    "Engineering / Math / CS": ["Optimization", "Programming for Finance"],
                },
            }
        },
        "Commercial Banking": {
            "Commercial Banking Analyst": {
                "description": "Works with businesses to evaluate creditworthiness, structure loans, and analyze financial statements. Focuses on small to mid-sized companies’ financing needs.",
                "majors": {
                    "Finance": ["Corporate Finance", "Credit Analysis", "Financial Institutions", "Risk Management"],
                    "Accounting": ["Financial Accounting", "Managerial Accounting", "Auditing", "Taxation"],
                    "Economics": ["Microeconomics", "Macroeconomics", "Money & Banking", "Applied Econometrics"],
                },
            }
        },
        "Wholesale / Corporate Banking": {
            "Wholesale / Corporate Banking Analyst": {
                "description": "Serves large corporations and institutions by providing financing, cash management, and risk solutions. Involves complex financial modeling and credit analysis.",
                "majors": {
                    "Finance": ["Advanced Corporate Finance", "International Finance", "Fixed Income", "Derivatives"],
                    "Economics": ["Industrial Organization", "Monetary Economics", "International Trade", "Econometrics"],
                    "Math / Statistics": ["Probability", "Statistical Inference", "Quantitative Methods for Finance", "Applied Linear Algebra"],
                },
            }
        },
        "Markets": {
            "Junior Salesperson": {
                "description": "Supports senior sales teams by pitching financial products to clients, monitoring markets, and providing trade ideas. Requires strong communication and product knowledge.",
                "majors": {
                    "Finance": ["Securities Markets", "Fixed Income", "Options & Derivatives", "Investment Analysis"],
                    "Economics": ["Behavioral Economics", "Market Microstructure", "International Trade", "Applied Econometrics"],
                    "Business / Marketing": ["Negotiation", "Communication for Business", "Consumer Psychology", "Marketing Analytics"],
                },
            },
            "Junior Trader": {
                "description": "Executes and monitors trades across asset classes, manages risk exposure, and supports trading desks. Requires strong quantitative and analytical skills.",
                "majors": {
                    "Mathematics": ["Probability Theory", "Stochastic Processes", "Linear Algebra", "Calculus III"],
                    "Statistics": ["Regression Analysis", "Time Series Analysis", "Bayesian Statistics", "Experimental Design"],
                    "Computer Science": ["Data Structures", "Algorithms", "Machine Learning", "Python for Finance"],
                    "Physics": ["Computational Physics", "Statistical Mechanics", "Numerical Methods", "Differential Equations"],
                    "Finance": ["Derivatives Pricing", "Financial Engineering", "Risk Management", "Algorithmic Trading"],
                },
            },
        },
        "Wealth / Private Banking": {
            "Junior Private Banking Analyst": {
                "description": "Assists relationship managers in wealth management, prepares investment proposals, and analyzes client portfolios. Focuses on high-net-worth individuals.",
                "majors": {
                    "Finance": ["Wealth Management", "Portfolio Theory", "Financial Planning", "Risk Management"],
                    "Economics": ["Behavioral Economics", "Monetary Policy", "Applied Econometrics", "International Finance"],
                    "Accounting": ["Taxation", "Estate Planning", "Auditing", "Personal Financial Accounting"],
                    "Psychology": ["Behavioral Finance", "Consumer Psychology", "Social Psychology", "Decision Making"],
                },
            }
        },
        "Corporate Treasury": {
            "Junior Corporate Treasury Analyst": {
                "description": "Supports corporate treasury teams in managing liquidity, cash flow, and foreign exchange exposure. Involves risk management and funding strategies for large firms.",
                "majors": {
                    "Finance": ["Treasury & Liquidity Management", "Derivatives", "Risk Management", "Corporate Finance"],
                    "Accounting": ["Financial Accounting", "Managerial Accounting", "Taxation", "Auditing"],
                    "Economics": ["Monetary Economics", "International Economics", "Money & Banking", "Econometrics"],
                    "Math / Statistics": ["Probability", "Applied Statistics", "Quantitative Risk Analysis", "Optimization"],
                },
            }
        },
    }
}

# ----------------------------------------
# Helper: Generate full role PDF
# ----------------------------------------
def generate_role_pdf(role_name, role_info):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph(f"<b>{role_name}</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Description
    elements.append(Paragraph("<b>Description:</b>", styles["Heading2"]))
    elements.append(Paragraph(role_info["description"], styles["BodyText"]))
    elements.append(Spacer(1, 12))

    # Majors & Courses
    elements.append(Paragraph("<b>Recommended Majors & Courses:</b>", styles["Heading2"]))
    for major, courses in role_info["majors"].items():
        elements.append(Paragraph(f"<b>{major}</b>", styles["Heading3"]))
        for course in courses:
            elements.append(Paragraph(f"- {course}", styles["Normal"]))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ----------------------------------------
# Streamlit UI
# ----------------------------------------
st.set_page_config(page_title="Career Pathway Navigator", layout="wide")
st.title("Career Pathway Navigator")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Select Options")
    industry = st.selectbox("Select Industry", ["-- Select --"] + list(data.keys()))
    sub_industry = role = None
    if industry != "-- Select --":
        sub_industry = st.selectbox("Select Sub-Industry", ["-- Select --"] + list(data[industry].keys()))
        if sub_industry != "-- Select --":
            role = st.selectbox("Select Role", ["-- Select --"] + list(data[industry][sub_industry].keys()))

with col2:
    st.header("Role Details")
    if role and role != "-- Select --":
        role_info = data[industry][sub_industry][role]

        # Display role info
        st.subheader(role)
        st.write(role_info["description"])

        # Majors & Courses heading + button in same row
        col_left, col_right = st.columns([3, 1])
        with col_left:
            st.markdown("### Recommended Majors & Courses")
        with col_right:
            pdf_file = generate_role_pdf(role, role_info)
            st.download_button(
                label="📄 Download PDF",
                data=pdf_file,
                file_name=f"{role.replace(' ', '_')}.pdf",
                mime="application/pdf",
            )

        # Display majors & courses
        for major, courses in role_info["majors"].items():
            st.markdown(f"**{major}**")
            for course in courses:
                st.markdown(f"- {course}")
    else:
        st.info("Please select an industry, sub-industry, and role from the left panel.")