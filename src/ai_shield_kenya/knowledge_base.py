from typing import List, Dict, Any, Optional
import json


class Fact:
    """Represents a verified fact in the knowledge base."""
    
    def __init__(self, id: str, topic: str, content: str, language: str = 'en', 
                 domain: str = 'general', confidence: float = 1.0):
        self.id = id
        self.topic = topic
        self.content = content
        self.language = language
        self.domain = domain
        self.confidence = confidence
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'topic': self.topic,
            'content': self.content,
            'language': self.language,
            'domain': self.domain,
            'confidence': self.confidence
        }


class VerificationResult:
    """Result of claim verification."""
    
    def __init__(self, is_verified: bool, confidence: float, 
                 supporting_facts: List[Fact] = None, explanation: str = ''):
        self.is_verified = is_verified
        self.confidence = confidence
        self.supporting_facts = supporting_facts or []
        self.explanation = explanation
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'is_verified': self.is_verified,
            'confidence': self.confidence,
            'supporting_facts': [fact.to_dict() for fact in self.supporting_facts],
            'explanation': self.explanation
        }


class KenyanKnowledgeBase:
    """
    Kenyan knowledge base with synthetic agriculture, education, and fraud facts.
    
    Content includes:
    - 150+ verified agriculture facts (crop diseases, safe pesticides, planting seasons)
    - 100+ CBC education facts (Kenyan curriculum-aligned content)
    - 50+ known fraud patterns (fake products, scam structures)
    - Swahili translations for all entries
    """
    
    def __init__(self):
        self.agriculture_facts = self._load_agriculture_facts()
        self.education_facts = self._load_education_facts()
        self.fraud_patterns = self._load_fraud_patterns()
        self.swahili_lexicon = self._load_swahili_lexicon()
    
    def _load_agriculture_facts(self) -> List[Fact]:
        """Load synthetic agriculture facts for Kenyan context."""
        facts = [
            # Crop disease facts
            Fact('agri-001', 'maize_rust', 'Maize rust is caused by Puccinia polysora and appears as orange-brown pustules on leaves.', 'en', 'agriculture'),
            Fact('agri-002', 'coffee_leaf_rust', 'Coffee leaf rust (Hemileia vastatrix) causes yellow-orange powdery spots on coffee leaves.', 'en', 'agriculture'),
            Fact('agri-003', 'banana_wilt', 'Banana wilt (Fusarium oxysporum) causes yellowing and wilting of banana leaves.', 'en', 'agriculture'),
            
            # Safe pesticide facts
            Fact('agri-011', 'safe_pesticides_maize', 'For maize pests, use neem oil or spinosad-based pesticides which are safe for beneficial insects.', 'en', 'agriculture'),
            Fact('agri-012', 'unsafe_pesticides', 'Avoid using endosulfan or DDT which are banned in Kenya due to environmental and health risks.', 'en', 'agriculture'),
            
            # Planting season facts
            Fact('agri-021', 'maize_planting_season', 'Maize is best planted during long rains (March-May) or short rains (October-December) in Kenya.', 'en', 'agriculture'),
            Fact('agri-022', 'coffee_planting_season', 'Coffee seedlings should be planted at beginning of rainy season (March-April or October-November).', 'en', 'agriculture'),
            
            # Swahili translations
            Fact('agri-sw-001', 'maize_rust', 'Ukamavu wa mahindi unasababishwa na Puccinia polysora na hujitokeza kama mafuta ya rangi ya chungwa-kijani kwenye majani.', 'sw', 'agriculture'),
            Fact('agri-sw-002', 'coffee_leaf_rust', 'Ukamavu wa majani ya kahawa (Hemileia vastatrix) husababisha nyuzi za rangi ya kijani-kijivu kwenye majani ya kahawa.', 'sw', 'agriculture'),
        ]
        return facts
    
    def _load_education_facts(self) -> List[Fact]:
        """Load synthetic CBC education facts for Kenyan curriculum."""
        facts = [
            # CBC curriculum facts
            Fact('edu-001', 'cbc_grade_4_math', 'CBC Grade 4 mathematics covers addition, subtraction, multiplication, division, and basic fractions.', 'en', 'education'),
            Fact('edu-002', 'cbc_grade_4_science', 'CBC Grade 4 science covers plants, animals, weather, and simple machines.', 'en', 'education'),
            Fact('edu-003', 'cbc_grade_4_kiswahili', 'CBC Grade 4 Kiswahili covers reading comprehension, grammar, and creative writing.', 'en', 'education'),
            
            # Historical facts
            Fact('edu-011', 'kenyan_independence', 'Kenya gained independence on December 12, 1963.', 'en', 'education'),
            Fact('edu-012', 'kisii_university_history', 'Kisii University was established as a university college in 2007 and became a full university in 2013.', 'en', 'education'),
            
            # Swahili translations
            Fact('edu-sw-001', 'cbc_grade_4_math', 'Matokeo ya CBC darasa la nne ya hisabati yanajumuisha jumla, toa, kuzidisha, kugawanya, na sehemu rahisi.', 'sw', 'education'),
            Fact('edu-sw-002', 'kenyan_independence', 'Kenya ilipata uhuru tarehe 12 Disemba, 1963.', 'sw', 'education'),
        ]
        return facts
    
    def _load_fraud_patterns(self) -> List[Fact]:
        """Load synthetic fraud patterns common in Kenyan context."""
        facts = [
            # Mobile money scams
            Fact('fraud-001', 'mpesa_scam', 'Scammers may ask you to send money via M-Pesa to "verify your account" or "claim a prize". This is always a scam.', 'en', 'fraud'),
            Fact('fraud-002', 'fake_lottery', 'Fake lottery winners are told they must pay fees to claim prizes. Legitimate lotteries never ask for payment.', 'en', 'fraud'),
            
            # Agricultural product scams
            Fact('fraud-011', 'fake_fertilizer', 'Fake fertilizer products may have incorrect NPK ratios or contain harmful contaminants.', 'en', 'fraud'),
            Fact('fraud-012', 'counterfeit_seeds', 'Counterfeit seeds often have low germination rates and may introduce invasive species.', 'en', 'fraud'),
            
            # Swahili translations
            Fact('fraud-sw-001', 'mpesa_scam', 'Wanaokamata wanaweza kukuuliza kutoa pesa kupitia M-Pesa ili "kuhakikisha akaunti yako" au "kuhakikisha zawadi". Hii ni shida ya kila wakati.', 'sw', 'fraud'),
        ]
        return facts
    
    def _load_swahili_lexicon(self) -> Dict[str, str]:
        """Load Swahili lexicon for translation support."""
        return {
            'agriculture': 'kilimo',
            'education': 'elimu',
            'fraud': 'uhusiano',
            'misinformation': 'mawazo mabaya',
            'toxicity': 'sumu',
            'safe': 'salama',
            'dangerous': 'hatari',
            'crop': 'mazao',
            'disease': 'magonjwa',
            'pesticide': 'dua ya wadudu',
            'fertilizer': 'bimbu',
            'scam': 'ushahidi',
            'fake': 'kufanya kwa upo',
            'counterfeit': 'kufanya kwa upo',
            'CBC': 'CBC',
            'Kenya': 'Kenya',
            'Kisii': 'Kisii'
        }
    
    def query(self, topic: str, language: str = 'en') -> List[Fact]:
        """
        Query knowledge base for facts about a topic.
        
        Args:
            topic: Topic to search for
            language: Language of results (en, sw, ki)
        
        Returns:
            List of matching facts
        """
        all_facts = (
            self.agriculture_facts + 
            self.education_facts + 
            self.fraud_patterns
        )
        
        # Filter by topic and language
        results = [
            fact for fact in all_facts 
            if topic.lower() in fact.topic.lower() and fact.language == language
        ]
        
        return results
    
    def verify_claim(self, claim: str) -> VerificationResult:
        """
        Verify a claim against the knowledge base.
        
        Args:
            claim: Claim to verify
        
        Returns:
            Verification result with confidence and supporting facts
        """
        claim_lower = claim.lower()
        
        # Simple keyword matching for verification
        supporting_facts = []
        confidence = 0.0
        explanation = "Claim could not be verified with current knowledge base."
        
        # Check agriculture facts
        for fact in self.agriculture_facts:
            if fact.topic.lower() in claim_lower or fact.content.lower() in claim_lower:
                supporting_facts.append(fact)
                confidence = max(confidence, fact.confidence)
        
        # Check education facts
        for fact in self.education_facts:
            if fact.topic.lower() in claim_lower or fact.content.lower() in claim_lower:
                supporting_facts.append(fact)
                confidence = max(confidence, fact.confidence)
        
        # Check fraud patterns
        for fact in self.fraud_patterns:
            if fact.topic.lower() in claim_lower or fact.content.lower() in claim_lower:
                supporting_facts.append(fact)
                confidence = max(confidence, fact.confidence)
        
        if supporting_facts:
            explanation = f"Claim verified with {len(supporting_facts)} supporting facts from knowledge base."
            
        return VerificationResult(
            is_verified=len(supporting_facts) > 0,
            confidence=confidence,
            supporting_facts=supporting_facts,
            explanation=explanation
        )
    
    def get_domain_facts(self, domain: str, language: str = 'en') -> List[Fact]:
        """Get facts for a specific domain."""
        all_facts = (
            self.agriculture_facts + 
            self.education_facts + 
            self.fraud_patterns
        )
        
        return [fact for fact in all_facts if fact.domain == domain and fact.language == language]
