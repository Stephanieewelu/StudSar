import streamlit as st
import re

class StudSAREngine:
    """Enhanced StudSAR RAG implementation with improved features."""
    
    def __init__(self):
        self.knowledge_base = {
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

    def query(self, query_text, k=5, return_sources=True):
        """
        Process query with intelligent responses based on content
        """
        query_lower = query_text.lower()

        # Fix common typos
        if "ivil service" in query_lower or "cvil service" in query_lower:
            query_lower = query_lower.replace("ivil service", "civil service").replace("cvil service", "civil service")

        # Build intelligent response
        answer = ""

        # Tokenize query for better matching
        query_words = set(re.findall(r'\w+', query_lower))

        # Find relevant entries in knowledge_base with scores
        scored_entries = []
        for key, content in self.knowledge_base.items():
            current_relevance_score = 0
            content_lower = content.lower()
            # Check for exact match of the query in the content
            if query_lower in content_lower:
                current_relevance_score += 10 # Higher score for direct phrase match

            # Count overlapping words
            content_words = set(re.findall(r'\w+', content_lower))
            current_relevance_score += len(query_words.intersection(content_words))

            # Prioritize entries whose key matches query words
            key_words = set(key.lower().split('_'))
            if any(word in key_words for word in query_words):
                current_relevance_score += 5

            if current_relevance_score > 0: # Only add if there's some relevance
                scored_entries.append((current_relevance_score, content, key))

        # Sort by score in descending order
        scored_entries.sort(key=lambda x: x[0], reverse=True)

        # Select entries above a certain threshold for the answer
        min_answer_relevance_threshold = 5 # This threshold can be tuned
        selected_entries = [entry for entry in scored_entries if entry[0] >= min_answer_relevance_threshold]

        if selected_entries:
            # Natural Language Generation (NLG) for a more conversational response
            top_entry_content = selected_entries[0][1]
            summary = ' '.join(top_entry_content.split('.')[:2]) + '.' # Simple summary of the first two sentences
            answer = f"""Based on your query about '{query_text}', here is a summary of the most relevant information I found:\n\n{summary}\n\nFor more details, I've compiled the following information from the StudSAR knowledge base:"""
            for score, content, key in selected_entries:
                answer += f"""\n\n---\n\n### {key.replace('_', ' ').title()}\n{content}"""
            answer += "\n\nThis information is derived from the StudSAR knowledge base."

        else:
            # Fallback to the more helpful generic response if no relevant content is found
            answer = f"""I can help you with UK Civil Service information. 

 **Your query:** '{query_text}' 

 **Try asking about:** 
 • The Civil Service - roles, structure, values 
 • Civil Service Code - standards and ethics 
 • Ministerial briefings - how to write them 
 • Green Book - policy appraisal guidance 
 • Policy development - the process 

 **Example questions:** 
 - "What is the Civil Service?" 
 - "How do I write a ministerial briefing?" 
 - "What are the Green Book principles?" 
 - "Explain the Civil Service Code" 

 Please ask a specific question and I'll provide detailed guidance."""

        # Populate sources with all scored entries (sorted by relevance)
        sources = []
        if scored_entries:
            max_overall_score = max(score for score, _, _ in scored_entries) # Get the highest score for normalization
            for score, content, key in scored_entries:
                sources.append({
                    'content': content,
                    'similarity': score / max(1, max_overall_score), # Normalize score for similarity
                    'title': key.replace('_', ' ').title()
                })
        
        confidence = 0.0
        if selected_entries:
            top_score = selected_entries[0][0]
            confidence = min(1.0, top_score / 15.0) # Simple confidence score based on relevance

        return { 
            'answer': answer,
            'sources': sources,
            'confidence': confidence
        }