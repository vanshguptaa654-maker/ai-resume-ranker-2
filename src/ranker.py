import numpy as np
from sentence_transformers import SentenceTransformer

def calculate_cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    return float(dot_product / (norm_a * norm_b)) if norm_a and norm_b else 0.0

def rank_candidates(candidates, job_description):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    jd_embedding = model.encode(job_description)
    
    consulting_giants = ["tcs", "infosys", "wipro", "accenture", "cognizant", "capgemini", "mindtree"]
    scored_list = []
    
    for c in candidates:
        cid = c.get("candidate_id", "CAND_0000000")
        
        # Pull directly from the standardized schema built in preprocess.py
        title = c.get("current_title", "AI Engineer Partner")
        exp = float(c.get("years_of_experience", 2.0))
        profile_text = c.get("clean_profile_text", "").lower()
        
        # 1. Base Semantic Match
        cand_embedding = model.encode(profile_text) if profile_text else jd_embedding * 0
        semantic_score = calculate_cosine_similarity(jd_embedding, cand_embedding)
        
        # 2. Hard Exclusion Verification
        is_disqualified = any(firm in profile_text for firm in consulting_giants)
        
        # 3. Target Experience Assessment (5-9 Years Sweet-spot)
        if 5.0 <= exp <= 9.0:
            exp_multiplier = 1.3
        elif exp < 3.0 or exp > 12.0:
            exp_multiplier = 0.6
        else:
            exp_multiplier = 1.0
            
        # 4. Correctly map behavioral tracking metrics based on preprocess.py outputs
        views = float(c.get("profile_views", 10.0))
        activity = float(c.get("platform_activity_days", 5.0))
        
        # Safely normalize using the preprocessor's default scales
        norm_views = min(1.0, views / 250.0)
        norm_activity = min(1.0, activity / 30.0) # Assuming active days are out of a month
        
        # Let's use a 0.75 default response rate fallback since it's not present in preprocess.py
        response_rate = 0.75 
        
        behavioral_index = (response_rate * 0.4) + (norm_views * 0.3) + (norm_activity * 0.3)
        
        # 5. Composite Score Calculation
        if is_disqualified:
            final_score = 0.0001
        else:
            final_score = ((0.60 * semantic_score) + (0.40 * behavioral_index)) * exp_multiplier
            
        final_score = round(max(0.0, min(1.0, final_score)), 4)
        reasoning_msg = f"{title} | {exp} YOE | Behavioral: {round(behavioral_index, 2)}"
        
        scored_list.append({
            "candidate_id": cid,
            "score": final_score,
            "reasoning": reasoning_msg
        })
        
    # Strictly sort by Score (Descending) then Candidate ID (Ascending)
    scored_list.sort(key=lambda x: (-x['score'], x['candidate_id']))
    
    for rank_idx, item in enumerate(scored_list, 1):
        item['rank'] = rank_idx
        
    return scored_list