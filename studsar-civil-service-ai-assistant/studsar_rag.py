import json
import re
import os
from typing import Dict, List, Tuple, Any

class StudSAREngine:
    """Enhanced StudSAR RAG implementation with improved features."""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base.json"):
        self.knowledge_base_path = knowledge_base_path
        self.knowledge_base = self.load_knowledge_base()
        self.query_history = []
        
    def load_knowledge_base(self) -> Dict[str, str]:
        """Load knowledge base from JSON file or use default if file doesn't exist."""
        try:
            if os.path.exists(self.knowledge_base_path):
                with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                    kb = json.load(f)
                    if not isinstance(kb, dict):
                        raise ValueError("Knowledge base JSON is not a dictionary.")
                    return kb
            else:
                print(f"Knowledge base file not found at {self.knowledge_base_path}. Using default.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {self.knowledge_base_path}: {e}. Using default.")
        except Exception as e:
            print(f"An unexpected error occurred loading knowledge base: {e}. Using default.")
        
        # Fallback to default knowledge base if file not found or error occurs
        return {
            "civil_service_overview": "The UK Civil Service is the permanent executive arm of His Majesty's Government. It supports the government of the day in developing and implementing policies, delivering public services, and supporting British interests abroad. Civil servants are politically impartial and serve the government of the day, whatever its political persuasion. Key values include integrity, honesty, objectivity, and impartiality.",
            "civil_service_code": "The Civil Service Code sets out the core values and standards of behaviour expected of all civil servants. These values are: Integrity (putting public service before personal interests), Honesty (being truthful and open), Objectivity (basing advice and decisions on evidence), and Impartiality (acting solely according to the merits of the case). The Code requires civil servants to serve the government of the day, act in a way that deserves public trust, comply with the law, and not misuse official position or information.",
            "green_book": "The Green Book is HM Treasury guidance on how to appraise policies, programmes, and projects. Its purpose is to ensure that public money delivers the best value. It outlines the ROAMEF cycle: Rationale, Objectives, Appraisal, Monitoring, Evaluation, and Feedback. Key principles include considering all realistic options, calculating costs and benefits, accounting for risks, and considering who gains and loses from a proposal.",
            "ministerial_briefings": "Ministerial briefings are concise documents prepared by civil servants to inform ministers and enable them to make decisions. A standard format often includes a summary page (issue, recommendation, timing, background) and a detail page (key considerations, options analysis, financial/legal implications, communications handling). Golden rules for briefings include being concise (typically 2 pages max), leading with the recommendation, using plain English, including only essential information, and dating/classifying appropriately.",
            "policy_development": "Policy development in the Civil Service involves identifying issues, gathering evidence, defining problems, developing and assessing alternative options, presenting recommendations to ministers for decision, implementing the chosen policy, and finally reviewing and evaluating its effectiveness. Key tools used include the Green Book for economic appraisal, the Magenta Book for evaluation methods, and the Aqua Book for quality analysis. Civil servants advise, while ministers decide.",
            "data_protection_act_2018": "The Data Protection Act 2018 (DPA 2018) is the UK's implementation of the General Data Protection Regulation (GDPR). It controls how personal information is used by organisations, businesses, or the government. It sets out rights for individuals regarding their data and obligations for those who process data. Key principles include lawfulness, fairness and transparency, purpose limitation, data minimisation, accuracy, storage limitation, integrity and confidentiality, and accountability.",
            "parliamentary_process": "The parliamentary process in the UK involves the legislative journey of a bill from its introduction to becoming an Act of Parliament. This typically includes first reading, second reading (debate on general principles), committee stage (detailed scrutiny), report stage (further amendments), and third reading (final debate). After passing both the House of Commons and the House of Lords, a bill receives Royal Assent and becomes law.",
            "public_sector_equality_duty": "The Public Sector Equality Duty (PSED) is part of the Equality Act 2010. It requires public bodies, in the exercise of their functions, to have due regard to the need to: eliminate discrimination, advance equality of opportunity, and foster good relations between persons who share a relevant protected characteristic and persons who do not share it. Protected characteristics include age, disability, gender reassignment, marriage and civil partnership, pregnancy and maternity, race, religion or belief, sex, and sexual orientation.",
            "freedom_of_information_act": "The Freedom of Information Act 2000 (FOIA) gives members of the public a right of access to information held by public authorities. It promotes transparency and accountability by allowing individuals to request information, which must be provided unless an exemption applies. Public authorities are also required to proactively publish certain information.",
            "devolution_uk": "Devolution in the UK refers to the statutory granting of powers from the Parliament of the United Kingdom to the Scottish Parliament, the Senedd (Welsh Parliament), and the Northern Ireland Assembly. This means these bodies have the power to make laws on certain matters specific to their regions, while Westminster retains control over reserved matters like defence and foreign policy."
        }

    def query(self, query_text: str, k: int = 5) -> Dict[str, Any]:
        """Process query with enhanced features."""
        if not query_text or not isinstance(query_text, str):
            return {
                'answer': "Please provide a valid query.",
                'sources': [],
                'confidence': 0.0,
                'query_type': 'invalid'
            }

        query_lower = query_text.lower()
        
        # Store query in history
        self.query_history.append(query_text)
        
        # Fix common typos
        query_lower = self._fix_typos(query_lower)
        
        # Tokenize query for better matching
        query_words = set(re.findall(r'\w+', query_lower))
        
        # Find relevant entries with enhanced scoring
        scored_entries = self._score_entries(query_lower, query_words)
        
        # Sort by score in descending order
        scored_entries.sort(key=lambda x: x[0], reverse=True)
        
        # Generate enhanced response
        answer, confidence = self._generate_enhanced_response(query_text, scored_entries)
        
        # Prepare sources
        sources = self._prepare_sources(scored_entries)
        
        return {
            'answer': answer,
            'sources': sources,
            'confidence': confidence,
            'query_type': self._classify_query(query_text)
        }
    
    def _fix_typos(self, query: str) -> str:
        """Fix common typos in queries."""
        typo_fixes = {
            "ivil service": "civil service",
            "cvil service": "civil service",
            "minsterial": "ministerial",
            "breifing": "briefing",
            "goverment": "government",
            "parliment": "parliament",
            "equalty": "equality",
            "devlution": "devolution"
        }
        
        for typo, correction in typo_fixes.items():
            query = query.replace(typo, correction)
        
        return query
    
    def _score_entries(self, query_lower: str, query_words: set) -> List[Tuple[float, str, str]]:
        """Score knowledge base entries with enhanced algorithm."""
        scored_entries = []
        
        for key, content in self.knowledge_base.items():
            score = 0.0
            content_lower = content.lower()
            
            # Exact phrase match (highest weight)
            if query_lower in content_lower:
                score += 20  # Increased weight for exact match
            
            # Word overlap scoring
            content_words = set(re.findall(r'\w+', content_lower))
            overlap = len(query_words.intersection(content_words))
            score += overlap * 3  # Increased weight for word overlap
            
            # Key matching (medium weight)
            key_words = set(key.lower().split('_'))
            if any(word in key_words for word in query_words):
                score += 10  # Increased weight for key match
            
            # Semantic relevance (basic implementation)
            score += self._calculate_semantic_relevance(query_words, content_words)
            
            if score > 0:
                scored_entries.append((score, content, key))
        
        return scored_entries
    
    def _calculate_semantic_relevance(self, query_words: set, content_words: set) -> float:
        """Calculate basic semantic relevance score based on predefined semantic groups."""
        semantic_groups = {
            'policy': {'policy', 'policies', 'development', 'implementation', 'strategy', 'guidance', 'framework'},
            'ethics': {'ethics', 'code', 'conduct', 'values', 'integrity', 'honesty', 'impartiality', 'objectivity'},
            'process': {'process', 'procedure', 'steps', 'stages', 'workflow', 'cycle', 'methodology'},
            'government': {'government', 'minister', 'ministerial', 'parliament', 'parliamentary', 'public', 'authority'},
            'legal': {'law', 'legal', 'act', 'legislation', 'regulation', 'compliance', 'duty', 'rights'},
            'finance': {'finance', 'treasury', 'money', 'value', 'appraisal', 'cost', 'benefit'}
        }
        
        score = 0.0
        for group_name, group_words in semantic_groups.items():
            query_in_group = len(query_words.intersection(group_words))
            content_in_group = len(content_words.intersection(group_words))
            if query_in_group > 0 and content_in_group > 0:
                score += min(query_in_group, content_in_group) * 2.0 # Increased semantic weight
        
        return score
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of query for better response formatting."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['what is', 'define', 'definition', 'meaning of']):
            return 'definition'
        elif any(word in query_lower for word in ['how to', 'how do', 'steps', 'process', 'procedure', 'guide']):
            return 'process'
        elif any(word in query_lower for word in ['list', 'principles', 'values', 'requirements', 'key points', 'features']):
            return 'list'
        elif any(word in query_lower for word in ['example', 'template', 'format', 'sample', 'structure']):
            return 'example'
        elif any(word in query_lower for word in ['tell me about', 'explain', 'describe']):
            return 'general'
        else:
            return 'general'
    
    def _generate_enhanced_response(self, query: str, scored_entries: List[Tuple[float, str, str]]) -> Tuple[str, float]:
        """Generate enhanced response based on query type and retrieved content."""
        min_threshold = 10 # Increased threshold for higher relevance
        selected_entries = [entry for entry in scored_entries if entry[0] >= min_threshold]
        
        if not selected_entries:
            return self._generate_fallback_response(query), 0.0
        
        query_type = self._classify_query(query)
        top_score = selected_entries[0][0]
        # Adjust confidence calculation to be more sensitive to higher scores
        confidence = min(1.0, top_score / 30.0) # Adjusted divisor for new scoring weights
        
        # Generate response based on query type
        if query_type == 'definition':
            answer = self._generate_definition_response(query, selected_entries)
        elif query_type == 'process':
            answer = self._generate_process_response(query, selected_entries)
        elif query_type == 'list':
            answer = self._generate_list_response(query, selected_entries)
        elif query_type == 'example':
            answer = self._generate_example_response(query, selected_entries)
        else:
            answer = self._generate_general_response(query, selected_entries)
        
        return answer, confidence
    
    def _generate_definition_response(self, query: str, entries: List[Tuple[float, str, str]]) -> str:
        """Generate a definition-style response with more context."""
        top_content = entries[0][1]
        title = entries[0][2].replace('_', ' ').title()
        
        # Attempt to extract a concise definition
        definition_match = re.search(r'^(.*?\.)', top_content)
        concise_definition = definition_match.group(1) if definition_match else top_content.split('.')[0] + '.'
        
        answer = f"### {title}\n\n"
        answer += f"**Definition:** {concise_definition}\n\n"
        answer += f"**Detailed Information:**\n{top_content}\n\n"
        
        if len(entries) > 1:
            answer += "**Related Information:**\n"
            for _, content, key in entries[1:3]:  # Include up to 2 more entries
                related_title = key.replace('_', ' ').title()
                related_summary = content.split('.')[0] + '.' if content.split('.') else content
                answer += f"• **{related_title}:** {related_summary}\n"
        
        answer += "\n*This information is retrieved from the StudSAR knowledge base.*"
        return answer
    
    def _generate_process_response(self, query: str, entries: List[Tuple[float, str, str]]) -> str:
        """Generate a process-oriented response with clear steps."""
        answer = f"### Understanding the Process for: {query}\n\n"
        
        for i, (score, content, key) in enumerate(entries[:2]):
            answer += f"#### {i+1}. {key.replace('_', ' ').title()}\n"
            # Attempt to break down content into steps/points
            points = [p.strip() for p in re.split(r'\d+\.', content) if p.strip()]
            if not points:
                points = [p.strip() for p in content.split('.') if p.strip() and len(p.strip()) > 20]
            
            if points:
                for j, point in enumerate(points[:5]): # Limit to 5 key points
                    answer += f"- {point}\n"
            else:
                answer += f"{content}\n"
            answer += "\n"
        
        answer += "*This information is retrieved from the StudSAR knowledge base.*"
        return answer
    
    def _generate_list_response(self, query: str, entries: List[Tuple[float, str, str]]) -> str:
        """Generate a list-style response with clear enumeration."""
        answer = f"### Key Points and Principles for: {query}\n\n"
        
        top_content = entries[0][1]
        title = entries[0][2].replace('_', ' ').title()
        
        answer += f"#### From {title}:\n"
        sentences = [s.strip() for s in top_content.split('.') if s.strip()]
        key_points = [s for s in sentences if len(s) > 20][:5] # Get up to 5 meaningful sentences
        
        if key_points:
            for i, point in enumerate(key_points, 1):
                answer += f"{i}. {point}.\n"
        else:
            answer += f"{top_content}\n"
        
        if len(entries) > 1:
            answer += "\n**Additional Relevant Information:**\n"
            for _, content, key in entries[1:3]:
                related_title = key.replace('_', ' ').title()
                related_summary = content.split('.')[0] + '.' if content.split('.') else content
                answer += f"• **{related_title}:** {related_summary}\n"
        
        answer += "\n*This information is retrieved from the StudSAR knowledge base.*"
        return answer
    
    def _generate_example_response(self, query: str, entries: List[Tuple[float, str, str]]) -> str:
        """Generate an example-oriented response with practical insights."""
        answer = f"### Examples and Practical Guidance for: {query}\n\n"
        
        for i, (score, content, key) in enumerate(entries[:2]):
            answer += f"#### {i+1}. {key.replace('_', ' ').title()}\n"
            answer += f"{content}\n\n"
        
        answer += "*This information is retrieved from the StudSAR knowledge base.*"
        return answer
    
    def _generate_general_response(self, query: str, entries: List[Tuple[float, str, str]]) -> str:
        """Generate a general response with a clear summary and detailed section."""
        top_content = entries[0][1]
        title = entries[0][2].replace('_', ' ').title()
        
        # Attempt to create a more sophisticated summary
        summary_sentences = [s.strip() for s in top_content.split('.') if s.strip()][:3] # First 3 sentences
        summary = ' '.join(summary_sentences) + ('.' if summary_sentences and not summary_sentences[-1].endswith('.') else '')
        
        answer = f"Based on your query about \'{query}\', here is the most relevant information from **{title}**:\n\n"
        answer += f"**Summary:** {summary}\n\n"
        answer += f"**Detailed Information:**\n{top_content}\n\n"
        
        if len(entries) > 1:
            answer += "**Additional Related Information:**\n"
            for _, content, key in entries[1:3]:
                related_title = key.replace('_', ' ').title()
                related_summary = content.split('.')[0] + '.' if content.split('.') else content
                answer += f"• **{related_title}:** {related_summary}\n"
        
        answer += "\n*This information is retrieved from the StudSAR knowledge base.*"
        return answer
    
    def _generate_fallback_response(self, query: str) -> str:
        """Generate fallback response when no relevant content is found."""
        return f"""I apologize, but I couldn't find specific content related to '{query}' in my current knowledge base. My purpose is to provide accurate information based on the UK Civil Service context.

To get the best results, please try rephrasing your question or ask about one of the following topics:

•   **The Civil Service:** roles, structure, values, and impartiality.
•   **Civil Service Code:** standards of conduct, integrity, honesty, objectivity, and impartiality.
•   **Ministerial Briefings:** guidance on drafting, format, and key considerations.
•   **Green Book:** HM Treasury guidance on policy appraisal, value for money, and the ROAMEF cycle.
•   **Policy Development:** the stages of policy creation, from identification to evaluation.
•   **Data Protection Act 2018:** UK's implementation of GDPR, individual rights, and organizational obligations.
•   **Parliamentary Process:** how bills become law, stages in the House of Commons and Lords.
•   **Public Sector Equality Duty:** requirements under the Equality Act 2010, protected characteristics.
•   **Freedom of Information Act 2000:** public right of access to information, transparency, and accountability.
•   **UK Devolution:** powers granted to Scottish Parliament, Senedd, and Northern Ireland Assembly.

**Example questions you can ask:**
- "What is the Civil Service?"
- "How do I write a ministerial briefing?"
- "What are the Green Book principles?"
- "Explain the Civil Service Code"

I'm here to help you navigate the complexities of the UK Civil Service. Please ask a specific question and I'll do my best to provide detailed guidance."""
    
    def _prepare_sources(self, scored_entries: List[Tuple[float, str, str]]) -> List[Dict[str, Any]]:
        """Prepare sources with enhanced metadata."""
        sources = []
        if not scored_entries:
            return sources

        max_score = max(score for score, _, _ in scored_entries)
        
        for score, content, key in scored_entries:
            sources.append({
                'content': content,
                'similarity': score / max(1, max_score), # Normalize similarity between 0 and 1
                'title': key.replace('_', ' ').title(),
                'key': key,
                'relevance_score': score
            })
        
        return sources
    
    def get_query_history(self) -> List[str]:
        """Get the query history."""
        return self.query_history.copy()
    
    def clear_history(self):
        """Clear the query history."""
        self.query_history.clear()
