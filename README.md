# AI Recruiter Ranker Pipeline

A production-grade NLP pipeline that screens, scores, and ranks candidates against job descriptions using state-of-the-art semantic embeddings, experience relevance scoring, and behavioral tracking.

---

## 🚀 Key Features

- **Semantic Similarity Matching**: Uses Sentence Transformers (`all-MiniLM-L6-v2`) to encode and compute cosine similarity between candidates' resumes and job requirements.
- **Experience Relevance Optimization**: Adjusts candidates' scores dynamically using an experience multiplier (optimizing for the 5-9 YOE sweet spot).
- **Behavioral Index Computation**: Factors in platform activity metrics and profile views to prioritize highly responsive and active candidates.
- **Disqualification Safeguards**: Automates policy compliance and filters out candidates matching excluded parameters (e.g., target consulting firms).
- **Robust Schema Normalization**: Seamlessly standardizes nested and flat candidate schemas and auto-pads target sizes to ensure submission validity.

---

## 📂 Project Structure

- **[run.py](run.py)**: End-to-end pipeline entry point.
- **[src/preprocess.py](src/preprocess.py)**: Handles data loading, schema normalization, ID cleaning, text preprocessing, and candidate padding.
- **[src/ranker.py](src/ranker.py)**: Contains core logic for semantic similarity, exclusions, multipliers, behavioral indexes, and ranking.
- **[validate_submission.py](validate_submission.py)**: Verifies the output format against submission criteria (exact row counts, unique constraints, and sorting rules).
- **`data/`**: Directory containing candidates database (`candidates.json`), job requirements, and outputs.

---

## 🛠️ Scoring Model Details

A candidate's composite score is computed using the following criteria:

$$\text{Final Score} = \left( (0.60 \times \text{Semantic Score}) + (0.40 \times \text{Behavioral Index}) \right) \times \text{Experience Multiplier}$$

1. **Semantic Score**: Cosine similarity between candidate profile embedding and the job description embedding.
2. **Behavioral Index**: Computed from response rate, profile views, and platform activity:
   $$\text{Behavioral Index} = (0.40 \times \text{Response Rate}) + (0.30 \times \text{Normalized Views}) + (0.30 \times \text{Normalized Activity Days})$$
3. **Experience Multiplier**:
   - **1.3** for 5 to 9 Years of Experience (Sweet Spot)
   - **0.6** for < 3 or > 12 Years of Experience
   - **1.0** for all other durations
4. **Exclusions**: Automatically set to a baseline score ($0.0001$) if the candidate's history contains predefined consulting organizations.

---

## ⚙️ Quick Start (Windows Setup & Run)

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Create the Virtual Environment
Create a clean virtual environment and install the production dependencies:
```powershell
# Create the environment
python -m venv .venv --clear

# Install dependencies (runs on Windows / Python 3.13+)
.\.venv\Scripts\pip install numpy pandas sentence-transformers scikit-learn torch transformers
```

### 3. Run the Pipeline
Execute the ranking pipeline. This script will generate the leaderboard and save the submission file to `data/sample_submission.csv`.
```powershell
# Set UTF-8 encoding environment variable (prevents console emoji encoding errors)
$env:PYTHONUTF8=1

# Run the runner
.\.venv\Scripts\python run.py
```

### 4. Validate the Results
Validate the generated file to ensure it matches submission standards:
```powershell
.\.venv\Scripts\python validate_submission.py data/sample_submission.csv
```
Upon success, the output will display:
```text
Submission is valid.
```
