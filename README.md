# Movie-Recommender

## ✅ What you need to do to build this project

1. Clone repository and set up environment
   - `git clone <repo-url>`
   - `python -m venv venv`
   - Activate virtualenv (`venv\Scripts\activate` on Windows, `source venv/bin/activate` on macOS/Linux)
2. Install required packages
   - `pip install streamlit pandas numpy requests sentence-transformers faiss-cpu`
   - Optional: `pip install -r requirements.txt` (if provided)
3. Prepare input data files
   - Get `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` in project root
4. Run preprocessing step
   - `python main.py` (builds pickles: `movies_dict.pkl`, `similarity.pkl`)
5. Run the Streamlit UI
   - `streamlit run app.py`
6. Debug flow (if needed)
   - Clear browser cache / hard refresh
   - Stop and restart the Streamlit server on each code update

## 🛠️ What I implemented in project

- Data preprocessing in `main.py`:
  - import and merge raw TMDB datasets
  - clean/norm data and build combined tags
  - embed tags with `SentenceTransformer`
  - compute cosine similarity and save pickles
- UI implementation in `app.py`:
  - dark gradient theme and responsive layout
  - movie chooser with suggestions
  - recommend button with spinner
  - card-based output with posters + titles
  - error handling for missing files and invalid selection

## 📁 Project files

- `main.py`: preprocess and build similarity
- `app.py`: model UI and recommendation logic
- `movies_dict.pkl`: preprocessed movie dictionary
- `similarity.pkl`: cosine similarity matrix
- `README.md`: this guide

## 🔁 Development steps while changing the project

1. edit code in `app.py` / `main.py`
2. run `streamlit run app.py`
3. check logs in terminal for errors
4. reload browser, use `Ctrl + F5` (hard refresh)
5. commit and push to git

## 🧩 Notes

- requires `movies_dict.pkl` and `similarity.pkl` to run `app.py`.
- if these files are missing, run `python main.py` first.
- in production, store API key securely and not in source.

## 👤 Author

Made by Ishan Kundra
