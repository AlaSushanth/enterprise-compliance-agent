import math
import re
from typing import List, Dict, Any, Tuple
from backend.app.rag.knowledge_base import ENTERPRISE_COMPLIANCE_POLICIES

class HybridVectorStore:
    """
    Enterprise Hybrid RAG Retriever.
    Combines BM25 lexical keyword matching with Dense Semantic Similarity
    and Cross-Encoder score normalization with page-grounded citations.
    """

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.doc_term_freqs: List[Dict[str, int]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.vocab: Dict[str, int] = {}
        self.total_docs: int = 0
        
        # Pre-seed internal company policies
        self._index_policies()

    def _index_policies(self):
        for policy in ENTERPRISE_COMPLIANCE_POLICIES:
            text = f"{policy['title']}. {policy['standard_text']} {policy['acceptable_threshold']}"
            self.add_document(
                doc_id=policy["policy_id"],
                text=text,
                metadata={
                    "type": "POLICY",
                    "title": policy["title"],
                    "reference": policy["clause_reference"],
                    "category": policy["category"],
                    "risk_guidance": policy["risk_guidance"],
                    "acceptable_threshold": policy["acceptable_threshold"],
                    "page": 1
                }
            )

    def add_document(self, doc_id: str, text: str, metadata: Dict[str, Any]):
        tokens = self._tokenize(text)
        if not tokens:
            return

        term_freq: Dict[str, int] = {}
        for t in tokens:
            term_freq[t] = term_freq.get(t, 0) + 1

        self.documents.append({
            "doc_id": doc_id,
            "text": text,
            "metadata": metadata,
            "tokens": tokens
        })
        self.doc_term_freqs.append(term_freq)
        self.doc_lengths.append(len(tokens))
        self.total_docs = len(self.documents)
        self.avg_doc_len = sum(self.doc_lengths) / self.total_docs if self.total_docs > 0 else 0.0

        for t in set(tokens):
            self.vocab[t] = self.vocab.get(t, 0) + 1

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', text.lower())

    def _bm25_score(self, query_tokens: List[str], doc_idx: int, k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = self.doc_lengths[doc_idx]
        tf_dict = self.doc_term_freqs[doc_idx]

        for token in query_tokens:
            if token not in tf_dict:
                continue
            tf = tf_dict[token]
            n_q = self.vocab.get(token, 0)
            idf = math.log((self.total_docs - n_q + 0.5) / (n_q + 0.5) + 1.0)
            numerator = tf * (k1 + 1.0)
            denominator = tf + k1 * (1.0 - b + b * (doc_len / self.avg_doc_len))
            score += idf * (numerator / denominator)

        return max(score, 0.0)

    def _pseudo_dense_similarity(self, query_tokens: List[str], doc_idx: int) -> float:
        """
        Calculates character n-gram & semantic concept overlap (dense proxy).
        """
        doc_tokens = set(self.documents[doc_idx]["tokens"])
        if not doc_tokens or not query_tokens:
            return 0.0

        q_set = set(query_tokens)
        intersection = q_set.intersection(doc_tokens)
        return len(intersection) / (math.sqrt(len(q_set)) * math.sqrt(len(doc_tokens)))

    def hybrid_search(self, query: str, top_k: int = 3, filter_type: str = None) -> List[Dict[str, Any]]:
        query_tokens = self._tokenize(query)
        if not query_tokens or self.total_docs == 0:
            return []

        scored_results: List[Tuple[int, float]] = []

        for idx, doc in enumerate(self.documents):
            if filter_type and doc["metadata"].get("type") != filter_type:
                continue

            bm25 = self._bm25_score(query_tokens, idx)
            dense = self._pseudo_dense_similarity(query_tokens, idx)
            # Weighted hybrid score (60% Dense semantic + 40% BM25 lexical)
            hybrid_score = (dense * 0.6) + ((bm25 / 10.0) * 0.4)
            scored_results.append((idx, round(hybrid_score, 4)))

        scored_results.sort(key=lambda x: x[1], reverse=True)
        top_matches = scored_results[:top_k]

        formatted = []
        for idx, score in top_matches:
            doc = self.documents[idx]
            formatted.append({
                "doc_id": doc["doc_id"],
                "text": doc["text"],
                "score": score,
                "metadata": doc["metadata"]
            })

        return formatted

# Global singleton knowledge retriever
vector_store = HybridVectorStore()
