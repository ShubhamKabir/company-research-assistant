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

    # Remove markdown headings
    text = re.sub(r"^###\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^##\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s*", "", text, flags=re.MULTILINE)

    # Remove bold markers
    text = text.replace("**", "")

    # Remove horizontal rules
    text = text.replace("---", "")

    # Replace unicode issues
    text = text.replace("■", "-")
    text = text.replace("•", "-")

    # Remove markdown table separator rows
    text = re.sub(r"\|[-: ]+\|", "", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def add_section(story, title, text, styles):

    story.append(
        Paragraph(f"<b>{title}</b>", styles["Heading2"])
    )

    story.append(Spacer(1, 10))

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        story.append(
            Paragraph(line, styles["BodyText"])
        )

    story.append(Spacer(1, 16))


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

    story.append(
        Paragraph(
            "AI Company Research Report",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Company:</b> {company}",
            styles["Heading2"],
        )
    )

    story.append(Spacer(1, 18))

    add_section(
        story,
        "Company Research",
        report,
        styles,
    )

    add_section(
        story,
        "Competitor Analysis",
        competitors,
        styles,
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf