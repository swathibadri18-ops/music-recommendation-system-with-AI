🧑‍💻 Author

**Swathi Badrinarayanan**
📬 Connect on [LinkedIn](https://www.linkedin.com/in/swathi-badrinarayanan/) | ✉️ [Email Me](swathi.badri18@gmail.com)

🎧 AI Music Recommender System

An intelligent **music recommendation app** built with **Streamlit** and **Spotify API**, designed to suggest songs based on **content similarity, AI-powered mood analysis**, and **user preferences**.
🚀 Features
* 🎵 **Song-Based Recommendations** – Find similar songs using TF-IDF and cosine similarity.
* 🤖 **AI-Powered Suggestions** – Generate mood or keyword-based song lists using NLP.
* ⭐ **Favorites Tab** – Save and revisit your favorite tracks.
* 🔗 **Spotify Integration** – Redirect to the full track in Spotify for instant listening.
* 📊 **Insights Dashboard** – Visualize top genres, durations, and dataset stats.
* ⚙️ **Customizable UI** – Built with Streamlit’s tabbed interface and modern design.
🏗️ Project Structure

📂 AI-Music-Recommender/
│
├── app.py                  # Main Streamlit app
├── prepare_model/          # Preprocessing scripts and helper functions
├── model_training/         # Scripts to train TF-IDF and similarity models
├── archive/                # Compressed dataset or backups
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
🧠 Tech Stack

| Category         | Tools / Libraries                        |
| ---------------- | ---------------------------------------- |
| Frontend         | Streamlit                                |
| Data Processing  | Pandas, NumPy                            |
| Machine Learning | scikit-learn (TF-IDF, Cosine Similarity) |
| NLP              | TF-IDF Vectorizer                        |
| API              | Spotipy (Spotify Web API)                |
| Visualization    | Streamlit Charts                         |

⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/ai-music-recommender.git
   cd ai-music-recommender
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

4. **(Optional)**
   Add your Spotify API credentials to `.streamlit/secrets.toml`:

   ```toml
   [spotify]
   client_id = "your_spotify_client_id"
   client_secret = "your_spotify_client_secret"
   redirect_uri = "http://localhost:8888/callback"
   ```
The model uses a subset of **Spotify’s Million Song Dataset**, containing metadata such as:

* Song title
* Artist
* Genre (if available)
* Duration
* TF-IDF-based features for lyrics or metadata similarity

> The dataset is stored locally and not included in the repo due to size constraints.

🧩 How It Works

1. The system loads precomputed **TF-IDF vectors** and **cosine similarity matrices**.

2. When a user enters a song name or mood, the model:

   * Extracts the song’s vector
   * Finds the top N most similar songs
   * Displays results with cover art and Spotify links

3. AI mode leverages **semantic keyword matching** for open-ended prompts like
   *"chill evening"* or *"energetic workout"*.

---

### 💾 Future Enhancements

* 🎧 Add real-time audio previews (Spotify 30-sec snippets)
* 🧠 Improve AI recommendation with fine-tuned embeddings
* 📱 Add user authentication & personalized profiles
* 🌈 Deploy on Streamlit Cloud or Hugging Face Spaces

---
🧑‍💻 Author

**Swathi Badrinarayanan**
📬 Connect on [LinkedIn](https://www.linkedin.com/in/swathi-badrinarayanan/) | ✉️ [Email Me](swathi.badri18@gmail.com)
