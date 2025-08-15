"""
Vietnamese Text Processing for Legal AI Chatbot
Xử lý Văn bản Tiếng Việt cho Chatbot AI Pháp lý

Specialized text processing for Vietnamese legal documents and queries.
Xử lý văn bản chuyên biệt cho tài liệu và truy vấn pháp lý tiếng Việt.
"""

import re
import unicodedata
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
import logging

# TODO: Import khi implement
# import underthesea
# from pyvi import ViTokenizer
# from app.utils.config import settings

@dataclass
class VietnameseTextAnalysis:
    """Analysis result for Vietnamese text"""
    original_text: str
    normalized_text: str
    tokens: List[str]
    legal_terms: List[str]
    entities: List[Dict[str, str]]
    language_confidence: float

class VietnameseTextProcessor:
    """Main processor for Vietnamese text in legal context"""
    
    def __init__(self):
        """Initialize Vietnamese text processor"""
        self.legal_terms = self._load_legal_terms()
        self.stopwords = self._load_vietnamese_stopwords()
        self.legal_abbreviations = self._load_legal_abbreviations()
        
    def process_legal_text(self, text: str) -> VietnameseTextAnalysis:
        """Process Vietnamese legal text comprehensively"""
        try:
            # 1. Normalize text
            normalized = self.normalize_vietnamese_text(text)
            
            # 2. Tokenize
            tokens = self.tokenize_vietnamese(normalized)
            
            # 3. Extract legal terms
            legal_terms = self.extract_legal_terms(normalized)
            
            # 4. Extract entities
            entities = self.extract_legal_entities(normalized)
            
            # 5. Calculate confidence
            confidence = self._calculate_language_confidence(text)
            
            return VietnameseTextAnalysis(
                original_text=text,
                normalized_text=normalized,
                tokens=tokens,
                legal_terms=legal_terms,
                entities=entities,
                language_confidence=confidence
            )
            
        except Exception as e:
            logging.error(f"Vietnamese text processing failed: {e}")
            # Return basic analysis
            return VietnameseTextAnalysis(
                original_text=text,
                normalized_text=text,
                tokens=text.split(),
                legal_terms=[],
                entities=[],
                language_confidence=0.5
            )
    
    def normalize_vietnamese_text(self, text: str) -> str:
        """Normalize Vietnamese text for better processing"""
        try:
            # 1. Unicode normalization
            text = unicodedata.normalize('NFC', text)
            
            # 2. Clean whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            # 3. Standardize punctuation
            text = re.sub(r'([.!?])\s*([.!?]+)', r'\1', text)
            
            # 4. Normalize Vietnamese legal terms
            text = self._normalize_legal_terms(text)
            
            # 5. Handle abbreviations
            text = self._expand_abbreviations(text)
            
            # 6. Standardize quotes
            text = re.sub(r'["""]', '"', text)
            text = re.sub(r'[''']', "'", text)
            
            return text
            
        except Exception as e:
            logging.error(f"Text normalization failed: {e}")
            return text
    
    def tokenize_vietnamese(self, text: str) -> List[str]:
        """Tokenize Vietnamese text using appropriate methods"""
        # TODO: Implement Vietnamese tokenization
        try:
            # Using underthesea or pyvi for better Vietnamese tokenization
            # tokens = underthesea.word_tokenize(text)
            
            # Fallback: simple tokenization
            tokens = text.split()
            
            # Filter out stopwords and clean tokens
            filtered_tokens = []
            for token in tokens:
                cleaned_token = self._clean_token(token)
                if cleaned_token and cleaned_token.lower() not in self.stopwords:
                    filtered_tokens.append(cleaned_token)
            
            return filtered_tokens
            
        except Exception as e:
            logging.error(f"Tokenization failed: {e}")
            return text.split()
    
    def extract_legal_terms(self, text: str) -> List[str]:
        """Extract Vietnamese legal terms from text"""
        try:
            found_terms = []
            text_lower = text.lower()
            
            # Search for legal terms in text
            for term in self.legal_terms:
                if term.lower() in text_lower:
                    found_terms.append(term)
            
            # Extract legal document references
            legal_refs = self._extract_legal_references(text)
            found_terms.extend(legal_refs)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_terms = []
            for term in found_terms:
                if term not in seen:
                    seen.add(term)
                    unique_terms.append(term)
            
            return unique_terms
            
        except Exception as e:
            logging.error(f"Legal term extraction failed: {e}")
            return []
    
    def extract_legal_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract legal entities from Vietnamese text"""
        entities = []
        
        try:
            # 1. Extract legal document references
            doc_refs = self._extract_document_references(text)
            entities.extend(doc_refs)
            
            # 2. Extract monetary amounts
            amounts = self._extract_monetary_amounts(text)
            entities.extend(amounts)
            
            # 3. Extract dates
            dates = self._extract_dates(text)
            entities.extend(dates)
            
            # 4. Extract person/organization names
            names = self._extract_names(text)
            entities.extend(names)
            
            # 5. Extract legal procedures
            procedures = self._extract_procedures(text)
            entities.extend(procedures)
            
            return entities
            
        except Exception as e:
            logging.error(f"Entity extraction failed: {e}")
            return []
    
    def _normalize_legal_terms(self, text: str) -> str:
        """Normalize Vietnamese legal terms"""
        # Standardize common legal term variations
        replacements = {
            'Bộ luật dân sự': 'Bộ luật Dân sự',
            'bộ luật dân sự': 'Bộ luật Dân sự',
            'Bộ luật hình sự': 'Bộ luật Hình sự',
            'bộ luật hình sự': 'Bộ luật Hình sự',
            'Bộ luật lao động': 'Bộ luật Lao động',
            'bộ luật lao động': 'Bộ luật Lao động',
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand Vietnamese legal abbreviations"""
        for abbrev, full_form in self.legal_abbreviations.items():
            text = re.sub(r'\b' + re.escape(abbrev) + r'\b', full_form, text)
        
        return text
    
    def _clean_token(self, token: str) -> str:
        """Clean individual token"""
        # Remove punctuation from ends
        token = re.sub(r'^[^\w]+|[^\w]+$', '', token)
        
        # Keep only meaningful tokens
        if len(token) < 2:
            return ""
        
        return token
    
    def _extract_legal_references(self, text: str) -> List[str]:
        """Extract legal document references"""
        references = []
        
        # Pattern for Vietnamese legal references
        patterns = [
            r'(Điều\s+\d+)',                          # Article references
            r'(Khoản\s+\d+)',                         # Clause references  
            r'(Chương\s+[IVX]+)',                     # Chapter references
            r'(Mục\s+\d+)',                           # Section references
            r'(Nghị định\s+\d+/\d+/NĐ-CP)',          # Decree references
            r'(Thông tư\s+\d+/\d+/TT-[A-Z]+)',       # Circular references
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                references.append(match.group(1))
        
        return references
    
    def _extract_document_references(self, text: str) -> List[Dict[str, str]]:
        """Extract legal document references as entities"""
        entities = []
        
        # Law references
        law_pattern = r'(Luật|Bộ luật)\s+([^,.\n]+)'
        matches = re.finditer(law_pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({
                'type': 'legal_document',
                'subtype': 'law',
                'value': match.group(0),
                'law_type': match.group(1),
                'law_name': match.group(2)
            })
        
        return entities
    
    def _extract_monetary_amounts(self, text: str) -> List[Dict[str, str]]:
        """Extract monetary amounts"""
        entities = []
        
        # Vietnamese monetary patterns
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(đồng|VND)',
            r'(\d+(?:\.\d+)?)\s*(triệu|tỷ)\s*(đồng|VND)?',
            r'(\d+(?:,\d+)*)\s*(đồng|VND)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': 'monetary_amount',
                    'value': match.group(0),
                    'amount': match.group(1),
                    'currency': match.group(2)
                })
        
        return entities
    
    def _extract_dates(self, text: str) -> List[Dict[str, str]]:
        """Extract dates in Vietnamese format"""
        entities = []
        
        date_patterns = [
            r'(\d{1,2}\/\d{1,2}\/\d{4})',                    # DD/MM/YYYY
            r'(\d{1,2}-\d{1,2}-\d{4})',                      # DD-MM-YYYY
            r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})', # Vietnamese date format
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': 'date',
                    'value': match.group(0),
                    'normalized_date': self._normalize_date(match.group(0))
                })
        
        return entities
    
    def _extract_names(self, text: str) -> List[Dict[str, str]]:
        """Extract person and organization names"""
        # TODO: Implement Vietnamese name extraction
        # This would require more sophisticated NER
        return []
    
    def _extract_procedures(self, text: str) -> List[Dict[str, str]]:
        """Extract legal procedures"""
        entities = []
        
        procedure_keywords = [
            'thủ tục', 'quy trình', 'trình tự', 'hồ sơ',
            'đăng ký', 'cấp phép', 'xin phép', 'khai báo'
        ]
        
        for keyword in procedure_keywords:
            if keyword in text.lower():
                entities.append({
                    'type': 'legal_procedure',
                    'keyword': keyword,
                    'context': self._get_context_around_keyword(text, keyword)
                })
        
        return entities
    
    def _get_context_around_keyword(self, text: str, keyword: str, window: int = 50) -> str:
        """Get context around a keyword"""
        # TODO: Implement context extraction
        return ""
    
    def _normalize_date(self, date_str: str) -> str:
        """Normalize Vietnamese date to standard format"""
        # TODO: Implement date normalization
        return date_str
    
    def _calculate_language_confidence(self, text: str) -> float:
        """Calculate confidence that text is Vietnamese"""
        # Simple heuristic based on Vietnamese characters
        vietnamese_chars = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ'
        
        vietnamese_count = sum(1 for char in text.lower() if char in vietnamese_chars)
        total_chars = len([char for char in text if char.isalpha()])
        
        if total_chars == 0:
            return 0.0
        
        return min(vietnamese_count / total_chars * 2, 1.0)  # Scale up for better sensitivity
    
    def _load_legal_terms(self) -> List[str]:
        """Load Vietnamese legal terms dictionary"""
        # TODO: Load from external file or database
        return [
            'Bộ luật Dân sự', 'Bộ luật Hình sự', 'Bộ luật Lao động',
            'Hiến pháp', 'Luật Thương mại', 'Luật Hành chính',
            'hợp đồng', 'tài sản', 'quyền sở hữu', 'nghĩa vụ',
            'vi phạm', 'trách nhiệm', 'bồi thường', 'tội phạm',
            'hình phạt', 'an toàn lao động', 'bảo hiểm xã hội',
            'thủ tục hành chính', 'cấp phép', 'đăng ký kinh doanh'
        ]
    
    def _load_vietnamese_stopwords(self) -> Set[str]:
        """Load Vietnamese stopwords"""
        # TODO: Load comprehensive stopwords list
        return {
            'là', 'của', 'và', 'có', 'được', 'trong', 'với', 'cho',
            'về', 'từ', 'theo', 'như', 'để', 'khi', 'nếu', 'mà',
            'các', 'những', 'này', 'đó', 'thì', 'sẽ', 'đã', 'đang'
        }
    
    def _load_legal_abbreviations(self) -> Dict[str, str]:
        """Load Vietnamese legal abbreviations"""
        return {
            'NĐ-CP': 'Nghị định của Chính phủ',
            'TT': 'Thông tư',
            'QĐ': 'Quyết định',
            'CV': 'Công văn',
            'TB': 'Thông báo',
            'BLHS': 'Bộ luật Hình sự',
            'BLDS': 'Bộ luật Dân sự',
            'BLLD': 'Bộ luật Lao động'
        }

class VietnameseQueryPreprocessor:
    """Preprocessor specifically for Vietnamese legal queries"""
    
    def __init__(self):
        self.text_processor = VietnameseTextProcessor()
    
    def preprocess_query(self, query: str) -> Dict[str, Any]:
        """Preprocess Vietnamese legal query for better search"""
        try:
            # Process text
            analysis = self.text_processor.process_legal_text(query)
            
            # Extract intent
            intent = self._extract_query_intent(query)
            
            # Generate search keywords
            search_keywords = self._generate_search_keywords(analysis)
            
            # Extract constraints
            constraints = self._extract_query_constraints(analysis)
            
            return {
                'original_query': query,
                'normalized_query': analysis.normalized_text,
                'intent': intent,
                'search_keywords': search_keywords,
                'legal_terms': analysis.legal_terms,
                'entities': analysis.entities,
                'constraints': constraints,
                'language_confidence': analysis.language_confidence
            }
            
        except Exception as e:
            logging.error(f"Query preprocessing failed: {e}")
            return {
                'original_query': query,
                'normalized_query': query,
                'intent': 'unknown',
                'search_keywords': query.split(),
                'legal_terms': [],
                'entities': [],
                'constraints': {},
                'language_confidence': 0.5
            }
    
    def _extract_query_intent(self, query: str) -> str:
        """Extract intent from Vietnamese legal query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['cách', 'làm thế nào', 'thủ tục']):
            return 'procedure_inquiry'
        elif any(word in query_lower for word in ['có được', 'có thể', 'quyền']):
            return 'rights_inquiry'
        elif any(word in query_lower for word in ['phải', 'bắt buộc', 'nghĩa vụ']):
            return 'obligation_inquiry'
        elif any(word in query_lower for word in ['vi phạm', 'sai', 'lỗi']):
            return 'violation_inquiry'
        else:
            return 'information_inquiry'
    
    def _generate_search_keywords(self, analysis: VietnameseTextAnalysis) -> List[str]:
        """Generate optimized search keywords"""
        keywords = []
        
        # Add legal terms (highest priority)
        keywords.extend(analysis.legal_terms)
        
        # Add important tokens
        important_tokens = [token for token in analysis.tokens if len(token) > 3]
        keywords.extend(important_tokens[:10])  # Limit to avoid noise
        
        # Add entity values
        for entity in analysis.entities:
            if entity.get('type') in ['legal_document', 'legal_procedure']:
                keywords.append(entity['value'])
        
        return list(set(keywords))  # Remove duplicates
    
    def _extract_query_constraints(self, analysis: VietnameseTextAnalysis) -> Dict[str, Any]:
        """Extract constraints from query"""
        constraints = {}
        
        # Date constraints
        date_entities = [e for e in analysis.entities if e['type'] == 'date']
        if date_entities:
            constraints['date_range'] = date_entities
        
        # Amount constraints
        amount_entities = [e for e in analysis.entities if e['type'] == 'monetary_amount']
        if amount_entities:
            constraints['amount_range'] = amount_entities
        
        # Legal domain constraints
        domain_keywords = {
            'dân sự': 'dan_su',
            'hình sự': 'hinh_su', 
            'lao động': 'lao_dong',
            'thương mại': 'thuong_mai'
        }
        
        for keyword, domain in domain_keywords.items():
            if keyword in analysis.normalized_text.lower():
                constraints['legal_domain'] = domain
                break
        
        return constraints
