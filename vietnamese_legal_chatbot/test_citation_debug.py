from app.models.legal_rag import LegalCitationExtractor

extractor = LegalCitationExtractor()
test_text = "Theo Điều 15 Khoản 1 Điểm a của Luật Dân sự số 91/2015/QH13"
citations = extractor.extract_citations_from_text(test_text)

print(f"Found {len(citations)} citations:")
for i, c in enumerate(citations):
    print(f"{i+1}. Type: {c.document_type}, Name: '{c.document_name}', Article: {c.article}, Number: {c.number}")

print("\nLaw citations with name:")
law_citations = [c for c in citations if "luật" in c.document_type.lower() and c.document_name]
for c in law_citations:
    print(f"- {c.document_type}: {c.document_name} (số {c.number})")
