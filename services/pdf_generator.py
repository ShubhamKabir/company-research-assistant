from io import BytesIO
import re

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import inch


def clean_text(text):

    text = text.replace("**", "")
    text = text.replace("---", "")

    text = text.replace("■", "-")
    text = text.replace("•", "-")
    text = text.replace("–", "-")   # en dash
    text = text.replace("—", "-")   # em dash
    text = text.replace("-", "-")   # non-breaking hyphen

    text = re.sub(r"\n{3,}", "\n\n", text)

    headings = [
        "Company Summary",
        "Products & Services",
        "AI-Generated Pain Points",
        "Suggested Competitors",
        "Competitor Analysis",
    ]

    for heading in headings:
        text = text.replace(heading, f"\n\n{heading}\n")

    return text.strip()


def add_report(story, text, styles):

    headings = [
        "Company Summary",
        "Products & Services",
        "AI-Generated Pain Points",
        "Suggested Competitors",
        "Competitor Analysis",
    ]

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Remove markdown heading symbols
        if line.startswith("#"):
            line = line.lstrip("#").strip()

        # Main section headings
        if line in headings:

            story.append(Spacer(1, 10))

            story.append(
                Paragraph(
                    f"<b>{line}</b>",
                    styles["Heading2"],
                )
            )

            story.append(Spacer(1, 10))

            continue

        # Bullet points
        if line.startswith("- "):

            story.append(
                Paragraph(line, styles["BodyText"])
            )

            continue

        # Normal paragraph
        story.append(
            Paragraph(line, styles["BodyText"])
        )

    story.append(Spacer(1, 18))


def generate_pdf(company, report, competitors):

    report = clean_text(report)
    competitors = clean_text(competitors)

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(
            "<b>AI Company Research Report</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 18))

    # Company Name
    story.append(
        Paragraph(
            f"<b>Company:</b> {company.title()}",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 20))

    # Research Section
    story.append(
        Paragraph(
            "<b>Company Research</b>",
            styles["Heading1"],
        )
    )

    story.append(Spacer(1, 12))

    add_report(
        story,
        report,
        styles,
    )

    story.append(Spacer(1, 20))

    # Competitor Section
    story.append(
        Paragraph(
            "<b>Competitor Analysis</b>",
            styles["Heading1"],
        )
    )

    story.append(Spacer(1, 12))

    add_report(
        story,
        competitors,
        styles,
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf