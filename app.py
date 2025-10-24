# app.py
import streamlit as st
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# -----------------------------
# Streamlit page config
# -----------------------------
st.set_page_config(
    page_title="🎧 AI Music Recommender",
    page_icon="🎶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
body { background-color: #0d0d0d; color: #f5f5f5; }
h1, h2, h3 { color: #9b59b6; }
.stButton>button { background-color: #001f3f; color: #ffb380; border-radius: 12px; padding: 0.5em 1em; }
.stTextInput>div>input { background-color: #1a1a1a; color: #f5f5f5; border: 1px solid #9b59b6; border-radius: 8px; padding: 0.4em; }
.card { background-color: #1a1a1a; border-radius: 12px; padding: 10px; margin: 5px; text-align:center; }
.card img { border-radius: 8px; width:150px; height:150px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Spotify setup
# -----------------------------
CLIENT_ID = "f80e45b95a4a41d38c90efa626eda9cc"
CLIENT_SECRET = "fd91b9a0c57e47158b86b3f51e11a14d"
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
))

# -----------------------------
# Load precomputed objects
# -----------------------------
@st.cache_resource
def load_model():
    df = pickle.load(open("fast_df.pkl", "rb"))
    tfidf = pickle.load(open("tfidf.pkl", "rb"))
    tfidf_matrix = tfidf.transform(df['processed_text'])
    return df, tfidf, tfidf_matrix

df, tfidf, tfidf_matrix = load_model()

# -----------------------------
# Initialize favorites
# -----------------------------
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

def add_to_favorites(song, artist):
    entry = f"{song} | {artist}"
    if entry not in st.session_state["favorites"]:
        st.session_state["favorites"].append(entry)
        st.success(f"Added {song} to favorites!")

# -----------------------------
# Helper functions
# -----------------------------
@st.cache_data
def get_cover_cached(song, artist):
    fallback = "https://i.postimg.cc/0QNxYz4V/social.png"
    try:
        res = sp.search(q=f"track:{song} artist:{artist}", type="track")
        if res['tracks']['items']:
            imgs = res['tracks']['items'][0]['album']['images']
            if imgs and imgs[0].get('url'):
                return imgs[0]['url']
    except:
        pass
    return fallback

def recommend(song_name, top=5):
    if not song_name.strip():
        st.warning("❗ Enter a song name!")
        return [], []
    all_songs = df['song'].tolist()
    match_tuple = process.extractOne(song_name, all_songs, scorer=fuzz.token_sort_ratio)
    if not match_tuple or match_tuple[1] < 70:
        st.warning(f"No close match found for '{song_name}'.")
        return [], []
    match = match_tuple[0]
    idx = df[df['song'] == match].index[0]
    song_vec = tfidf_matrix[idx]
    similarities = cosine_similarity(song_vec, tfidf_matrix).flatten()
    top_idx = similarities.argsort()[::-1][1:top+1]
    names, covers = [], []
    for i in top_idx:
        row = df.iloc[i]
        names.append(row.song)
        covers.append(get_cover_cached(row.song, row.artist))
    return names, covers

def ai_suggest_local(query, top=5):
    if not query.strip():
        st.warning("❗ Type mood, keyword, or style!")
        return [], []
    query_vec = tfidf.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_idx = similarities.argsort()[::-1][:top]
    names, covers = [], []
    for i in top_idx:
        row = df.iloc[i]
        names.append(row.song)
        covers.append(get_cover_cached(row.song, row.artist))
    return names, covers

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎧 AI Music Recommender System")
st.markdown("Type a song name or mood/keyword to get instant song recommendations!")

tab1, tab2 = st.tabs(["🎵 Song-based", "🤖 AI Recommendation"])

# -----------------------------
# Tab 1: Song-based
# -----------------------------
with tab1:
    top_n = st.slider("Number of recommendations:", 3, 10, 5)
    song_input = st.text_input("Enter a song name:", key="song_tab")
    if st.button("Recommend", key="song"):
        with st.spinner("Finding similar songs..."):
            rec_songs, rec_covers = recommend(song_input, top=top_n)
        if rec_songs:
            cols = st.columns(len(rec_songs))
            for i, col in enumerate(cols):
                with col:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.text(rec_songs[i])
                    artist_name = df[df['song']==rec_songs[i]]['artist'].values[0]
                    st.caption(f"{artist_name}")
                    st.image(rec_covers[i])
                    if st.button("⭐ Add to Favorites", key=f"fav_song_{i}"):
                        add_to_favorites(rec_songs[i], artist_name)
                    # Spotify link
                    try:
                        query = f"track:{rec_songs[i]} artist:{artist_name}"
                        result = sp.search(q=query, type="track", limit=1)
                        if result["tracks"]["items"]:
                            spotify_url = result["tracks"]["items"][0]["external_urls"]["spotify"]
                            st.markdown(f"""
                                <a href="{spotify_url}" target="_blank" style="
                                    text-decoration:none;
                                    background-color:#1DB954;
                                    color:white;
                                    padding:8px 16px;
                                    border-radius:20px;
                                    font-weight:bold;
                                    display:inline-block;
                                ">
                                🎧 Play on Spotify
                                </a>
                            """, unsafe_allow_html=True)
                        else:
                            st.caption("🔗 Spotify link not available")
                    except:
                        st.caption("⚠️ Error retrieving Spotify link")
                    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Tab 2: AI-powered (local)
# -----------------------------
with tab2:
    top_n_ai = st.slider("Number of AI recommendations:", 3, 10, 5)
    ai_input = st.text_input("Enter mood, keyword, or style:", key="ai_tab")
    if st.button("AI Recommend", key="ai"):
        with st.spinner("Computing AI-based recommendations..."):
            ai_songs, ai_covers = ai_suggest_local(ai_input, top=top_n_ai)
        if ai_songs:
            cols = st.columns(len(ai_songs))
            for i, col in enumerate(cols):
                with col:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.text(ai_songs[i])
                    artist_name = df[df['song']==ai_songs[i]]['artist'].values[0]
                    st.caption(f"{artist_name}")
                    st.image(ai_covers[i])
                    if st.button("⭐ Add to Favorites", key=f"fav_ai_{i}"):
                        add_to_favorites(ai_songs[i], artist_name)
                    # Spotify link
                    try:
                        query = f"track:{ai_songs[i]} artist:{artist_name}"
                        result = sp.search(q=query, type="track", limit=1)
                        if result["tracks"]["items"]:
                            spotify_url = result["tracks"]["items"][0]["external_urls"]["spotify"]
                            st.markdown(f"""
                                <a href="{spotify_url}" target="_blank" style="
                                    text-decoration:none;
                                    background-color:#1DB954;
                                    color:white;
                                    padding:8px 16px;
                                    border-radius:20px;
                                    font-weight:bold;
                                    display:inline-block;
                                ">
                                🎧 Play on Spotify
                                </a>
                            """, unsafe_allow_html=True)
                        else:
                            st.caption("🔗 Spotify link not available")
                    except:
                        st.caption("⚠️ Error retrieving Spotify link")
                    st.markdown("</div>", unsafe_allow_html=True)
