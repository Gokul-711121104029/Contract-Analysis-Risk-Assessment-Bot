import streamlit as st
from src.ingestion.extract_text import extract_text
from src.ingestion.normalize import normalize_text
from src.nlp.clause_splitter import split_clauses
from src.nlp.ner import extract_entities
from src.nlp.deontic_tagger import tag_clause
from src.nlp.risk_rules import detect_risks
from src.nlp.ambiguity import detect_ambiguity
from src.llm.llm_client import explain_clause_llm  # now offline
from src.scoring.risk_scoring import score_clause, score_contract
from src.reporting.summary_builder import build_summary
from src.reporting.pdf_export import generate_pdf
from src.audit.logger import log_audit

st.set_page_config(page_title="Contract Risk Bot", layout="wide")
st.title("📜 Contract Analysis & Risk Assessment Bot")

uploaded = st.file_uploader("Upload Contract", type=["pdf","docx","txt"])

if uploaded:
    raw_text = extract_text(uploaded)
    clean_text, language = normalize_text(raw_text)

    clauses = split_clauses(clean_text)
    results = []

    for clause in clauses:
        entities = extract_entities(clause["text"])
        risks = detect_risks(clause["text"])
        ambiguity = detect_ambiguity(clause["text"])
        tag = tag_clause(clause["text"])
        explanation = explain_clause_llm(clause["text"])
        risk_score = score_clause(risks, ambiguity)

        results.append({
            "id": clause["id"],
            "text": clause["text"],
            "entities": entities,
            "tag": tag,
            "risks": risks,
            "ambiguity": ambiguity,
            "score": risk_score,
            "explanation": explanation
        })

        st.subheader(f"Clause {clause['id']} — Risk: {risk_score}")
        st.write(explanation)

    contract_score = score_contract(results)
    summary = build_summary(results, contract_score)

    st.markdown("## 📊 Contract Risk Score")
    st.success(contract_score)

    if st.button("📄 Download PDF Report"):
        generate_pdf(summary)
        st.success("PDF generated")

    log_audit(uploaded.name, language, contract_score)
