import os
import pandas as pd
from src.preprocess import load_and_build_profiles
from src.ranker import rank_candidates

def main():
    print("🚀 Running Production Candidate Ranker Pipeline...\n")
    
    try:
        candidates = load_and_build_profiles()
        
        # Define objective requirements
        job_requirements = "Looking for a Machine Learning Engineer experienced in Python, data analysis libraries like Pandas, and building predictive models using Scikit-Learn."
        
        results = rank_candidates(candidates, job_requirements)
        
        output_df = pd.DataFrame(results)
        output_df = output_df[['candidate_id', 'rank', 'score', 'reasoning']]
        
        # Point right to data/sample_submission.csv
        output_path = os.path.join("data", "sample_submission.csv")
        output_df.to_csv(output_path, index=False)
        
        print("\n🏆 --- FINAL RECRUITER LEADERBOARD --- 🏆")
        print(output_df.to_string(index=False))
        print(f"\n💾 Submission file written successfully at: {output_path}")
        
    except Exception as e:
        print(f"❌ Error during runtime: {e}")

if __name__ == "__main__":
    main()