from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(summary):
    doc = SimpleDocTemplate("contract_report.pdf")
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(
        f"<b>Contract Risk Level:</b> {summary['contract_score']}",
        styles["Normal"]
    ))

    for r in summary["details"]:
        story.append(Paragraph(
            f"<b>Clause {r['id']} — Risk: {r['score']}</b><br/>{r['explanation']}",
            styles["Normal"]
        ))

    doc.build(story)
