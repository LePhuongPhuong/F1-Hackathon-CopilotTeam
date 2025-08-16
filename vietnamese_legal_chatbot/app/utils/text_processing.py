"""
Vietnamese Text Processing for Legal AI Chatbot
Xử lý Văn bản Tiếng Việt cho Chatbot AI Pháp lý

Specialized text processing for Vietnamese legal documents and queries.
Xử lý văn bản chuyên biệt cho tài liệu và truy vấn pháp lý tiếng Việt.
"""

import re
import unicodedata
from typing import List, Dict, Optional, Tuple, Set, Any
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
        
    def _load_legal_terms(self) -> List[str]:
        """Load Vietnamese legal terms dictionary"""
        return [
            # Quyền và nghĩa vụ
            "quyền dân sự", "quyền con người", "quyền cơ bản", "nghĩa vụ công dân",
            "quyền sở hữu", "quyền sử dụng", "quyền thừa kế", "quyền tác giả",
            
            # Cơ quan nhà nước
            "quốc hội", "chính phủ", "thủ tướng", "bộ trưởng", "tòa án",
            "viện kiểm sát", "công an", "bộ tư pháp", "cục pháp chế",
            
            # Văn bản pháp luật
            "hiến pháp", "luật", "bộ luật", "nghị quyết", "nghị định",
            "thông tư", "quyết định", "chỉ thị", "pháp lệnh",
            
            # Lĩnh vực pháp lý
            "dân sự", "hình sự", "lao động", "thương mại", "hành chính",
            "hôn nhân gia đình", "bất động sản", "môi trường", "thuế",
            
            # Thủ tục pháp lý
            "khởi kiện", "tố tụng", "phúc thẩm", "giám đốc thẩm", "thi hành án",
            "hòa giải", "trọng tài", "bồi thường", "xử phạt", "án phí",
            
            # Chủ thể pháp lý
            "công dân", "pháp nhân", "doanh nghiệp", "tổ chức", "cá nhân",
            "người lao động", "người sử dụng lao động", "đại diện pháp luật"
        ]
    
    def _load_vietnamese_stopwords(self) -> Set[str]:
        """Load Vietnamese stopwords for legal text"""
        return {
            # Common Vietnamese stopwords
            "và", "của", "trong", "với", "về", "để", "cho", "từ", "theo",
            "như", "khi", "nếu", "mà", "này", "đó", "các", "những", "một",
            "có", "là", "được", "bị", "phải", "cần", "sẽ", "đã", "đang",
            "tại", "trên", "dưới", "giữa", "ngoài", "bên", "sau", "trước",
            
            # Legal-specific stopwords
            "quy định", "theo như", "căn cứ", "trên cơ sở", "phù hợp",
            "tuân thủ", "thực hiện", "áp dụng", "ban hành", "có hiệu lực"
        }
    
    def _load_legal_abbreviations(self) -> Dict[str, str]:
        """Load Vietnamese legal abbreviations"""
        return {
            # Government agencies
            "BTP": "Bộ Tư pháp",
            "BCA": "Bộ Công an", 
            "TANDTC": "Tòa án nhân dân tối cao",
            "VKSTC": "Viện kiểm sát nhân dân tối cao",
            
            # Legal documents
            "NĐ-CP": "Nghị định của Chính phủ",
            "QĐ-TTg": "Quyết định của Thủ tướng",
            "TT-BTP": "Thông tư của Bộ Tư pháp",
            "CV": "Công văn",
            
            # Legal codes
            "BLDS": "Bộ luật Dân sự",
            "BLHS": "Bộ luật Hình sự", 
            "BLLD": "Bộ luật Lao động",
            "BLTM": "Bộ luật Thương mại",
            
            # Others
            "TP.HCM": "Thành phố Hồ Chí Minh",
            "UBND": "Ủy ban nhân dân",
            "HĐND": "Hội đồng nhân dân"
        }
        
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
            text = re.sub(r"[''']", "'", text)
            
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
        
        # Vietnamese date patterns
        patterns = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',                    # dd/mm/yyyy
            r'(\d{1,2})-(\d{1,2})-(\d{4})',                    # dd-mm-yyyy
            r'ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})',  # Vietnamese format
            r'(\d{4})-(\d{1,2})-(\d{1,2})',                    # yyyy-mm-dd
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': 'date',
                    'value': match.group(0),
                    'raw_match': match.groups()
                })
        
        return entities
    
    def _extract_names(self, text: str) -> List[Dict[str, str]]:
        """Extract person and organization names"""
        entities = []
        
        # Vietnamese name patterns (basic)
        # This is a simplified version - real implementation would use NER
        patterns = [
            r'(ông|bà|anh|chị)\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]*)*)',
            r'(Công ty|Doanh nghiệp|Tập đoàn|Ngân hàng)\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][^,.\n]*)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                if 'ông|bà|anh|chị' in pattern:
                    entities.append({
                        'type': 'person',
                        'value': match.group(0),
                        'title': match.group(1),
                        'name': match.group(2)
                    })
                else:
                    entities.append({
                        'type': 'organization',
                        'value': match.group(0),
                        'org_type': match.group(1),
                        'org_name': match.group(2)
                    })
        
        return entities
    
    def _extract_procedures(self, text: str) -> List[Dict[str, str]]:
        """Extract legal procedures and processes"""
        entities = []
        
        # Legal procedure patterns
        procedures = [
            'khởi kiện', 'tố tụng', 'phúc thẩm', 'giám đốc thẩm',
            'hòa giải', 'trọng tài', 'thi hành án', 'cưỡng chế',
            'kháng cáo', 'kháng nghị', 'tạm giam', 'tạm giữ',
            'điều tra', 'truy tố', 'xét xử', 'tuyên án'
        ]
        
        for procedure in procedures:
            pattern = r'\b' + re.escape(procedure) + r'\b'
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': 'legal_procedure',
                    'value': match.group(0),
                    'procedure_type': procedure
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
        
        total_chars = len([c for c in text.lower() if c.isalpha()])
        if total_chars == 0:
            return 0.0
        
        vietnamese_char_count = len([c for c in text.lower() if c in vietnamese_chars])
        confidence = vietnamese_char_count / total_chars
        
        # Boost confidence if common Vietnamese words are found
        common_vn_words = ['và', 'của', 'trong', 'với', 'về', 'cho', 'từ', 'theo', 'như']
        word_boost = sum(1 for word in common_vn_words if word in text.lower()) * 0.05
        
        return min(1.0, confidence + word_boost)
    
    def get_legal_domain(self, text: str) -> str:
        """Determine legal domain from Vietnamese text"""
        text_lower = text.lower()
        
        # Legal domain keywords
        domain_keywords = {
            'dan_su': ['dân sự', 'hợp đồng', 'tài sản', 'quyền sở hữu', 'bồi thường', 'thừa kế'],
            'hinh_su': ['hình sự', 'tội phạm', 'hình phạt', 'án tù', 'vi phạm pháp luật'],
            'lao_dong': ['lao động', 'người lao động', 'hợp đồng lao động', 'bảo hiểm xã hội', 'thời gian làm việc'],
            'thuong_mai': ['thương mại', 'kinh doanh', 'công ty', 'doanh nghiệp', 'đăng ký kinh doanh'],
            'hanh_chinh': ['hành chính', 'thủ tục', 'cấp phép', 'đăng ký', 'giấy phép']
        }
        
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        
        return 'general'
    
    def extract_legal_citations(self, text: str) -> List[Dict[str, str]]:
        """Extract Vietnamese legal citations"""
        citations = []
        
        # Legal citation patterns
        patterns = [
            # Law citations
            r'(Luật|Bộ luật)\s+([^,.\n\d]+)\s+(\d{4})',
            # Article citations  
            r'Điều\s+(\d+)\s+(Luật|Bộ luật)\s+([^,.\n\d]+)\s+(\d{4})',
            # Decree citations
            r'Nghị định\s+(\d+)/(\d{4})/NĐ-CP',
            # Circular citations
            r'Thông tư\s+(\d+)/(\d{4})/TT-([A-Z]+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                citation = {
                    'type': 'legal_citation',
                    'full_text': match.group(0),
                    'groups': match.groups()
                }
                
                # Parse specific citation types
                if 'Luật' in match.group(0) or 'Bộ luật' in match.group(0):
                    citation['citation_type'] = 'law'
                elif 'Nghị định' in match.group(0):
                    citation['citation_type'] = 'decree'
                elif 'Thông tư' in match.group(0):
                    citation['citation_type'] = 'circular'
                elif 'Điều' in match.group(0):
                    citation['citation_type'] = 'article'
                
                citations.append(citation)
        
        return citations
        
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


# Utility functions for external use
def process_vietnamese_legal_text(text: str) -> VietnameseTextAnalysis:
    """Quick function to process Vietnamese legal text"""
    processor = VietnameseTextProcessor()
    return processor.process_legal_text(text)

def preprocess_vietnamese_query(query: str) -> Dict[str, Any]:
    """Quick function to preprocess Vietnamese legal query"""
    preprocessor = VietnameseQueryPreprocessor()
    return preprocessor.preprocess_query(query)

def extract_legal_terms(text: str) -> List[str]:
    """Quick function to extract legal terms from text"""
    processor = VietnameseTextProcessor()
    return processor.extract_legal_terms(text)

def get_legal_domain(text: str) -> str:
    """Quick function to get legal domain from text"""
    processor = VietnameseTextProcessor()
    return processor.get_legal_domain(text)

def extract_legal_citations(text: str) -> List[Dict[str, str]]:
    """Quick function to extract legal citations"""
    processor = VietnameseTextProcessor()
    return processor.extract_legal_citations(text)

def normalize_vietnamese_text(text: str) -> str:
    """Quick function to normalize Vietnamese text"""
    processor = VietnameseTextProcessor()
    return processor.normalize_vietnamese_text(text)

# Test function
def test_vietnamese_text_processing():
    """Test Vietnamese text processing functions"""
    
    # Test texts
    test_texts = [
        "Quyền dân sự của công dân được bảo vệ như thế nào?",
        "Điều 15 Bộ luật Dân sự 2015 quy định gì về quyền sở hữu?",
        "Thời gian làm việc theo Bộ luật Lao động 2019 là bao lâu?",
        "Công ty tôi yêu cầu làm việc 10 giờ/ngày có vi phạm không?"
    ]
    
    print("🇻🇳 VIETNAMESE TEXT PROCESSING TEST")
    print("=" * 60)
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n📋 TEST {i}: {text}")
        print("-" * 40)
        
        # Process text
        analysis = process_vietnamese_legal_text(text)
        print(f"✅ Normalized: {analysis.normalized_text}")
        print(f"🔍 Legal terms: {analysis.legal_terms}")
        print(f"🏷️ Entities: {len(analysis.entities)} found")
        print(f"🌏 Language confidence: {analysis.language_confidence:.2f}")
        
        # Preprocess query
        query_info = preprocess_vietnamese_query(text)
        print(f"🎯 Intent: {query_info['intent']}")
        print(f"🔑 Keywords: {query_info['search_keywords'][:5]}")  # Show first 5
        print(f"📚 Domain: {get_legal_domain(text)}")
        
        # Extract citations
        citations = extract_legal_citations(text)
        if citations:
            print(f"📖 Citations: {len(citations)} found")
            for citation in citations:
                print(f"   - {citation['full_text']} ({citation['citation_type']})")
    
    print(f"\n{'='*60}")
    print("🎉 Vietnamese text processing test completed!")

if __name__ == "__main__":
    test_vietnamese_text_processing()
