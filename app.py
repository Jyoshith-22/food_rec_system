import streamlit as st

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Restaurant Recommender",
    page_icon="🍽️",
    layout="centered"
)

# ─── DEMO DATA ────────────────────────────────────────────────────────────────
USERS = {
    "rLtl8ZkDX5vH5nAx9C3q6g": {
        "name": "Alice M.", "reviews": 14, "isNew": False,
        "reviewed": ["biz001", "biz003", "biz007"],
        "cf_scores": {
            "biz002": 3.8, "biz004": 4.6, "biz005": 2.1,
            "biz006": 4.4, "biz008": 1.8, "biz009": 3.5, "biz010": 4.2
        }
    },
    "hG2kPzX9mNvR7sQw4tYuJb": {
        "name": "Bob K.", "reviews": 22, "isNew": False,
        "reviewed": ["biz002", "biz005", "biz009"],
        "cf_scores": {
            "biz001": 4.5, "biz003": 3.2, "biz004": 2.8,
            "biz006": 3.9, "biz007": 4.7, "biz008": 2.2, "biz010": 3.6
        }
    },
    "NEW_USER_001": {
        "name": "New User", "reviews": 0, "isNew": True,
        "reviewed": [],
        "cf_scores": {}
    }
}

RESTAURANTS = [
    {"id": "biz001", "name": "Bella Italia Ristorante", "cat": "Italian, Pizza, Pasta",          "city": "Phoenix",    "reviews": 342, "cluster": 0, "bert": 4.72, "cb": 4.38},
    {"id": "biz002", "name": "The Burger Republic",     "cat": "Burgers, American, Grill",        "city": "Phoenix",    "reviews": 289, "cluster": 1, "bert": 4.31, "cb": 4.10},
    {"id": "biz003", "name": "Sakura Sushi & Ramen",    "cat": "Japanese, Sushi, Ramen",          "city": "Tempe",      "reviews": 198, "cluster": 2, "bert": 4.58, "cb": 4.25},
    {"id": "biz004", "name": "Casa Mexicana",           "cat": "Mexican, Tacos, Burritos",        "city": "Phoenix",    "reviews": 411, "cluster": 3, "bert": 4.65, "cb": 4.42},
    {"id": "biz005", "name": "Dragon Palace",           "cat": "Chinese, Dim Sum, Noodles",       "city": "Mesa",       "reviews": 156, "cluster": 2, "bert": 3.92, "cb": 3.85},
    {"id": "biz006", "name": "The French Bistro",       "cat": "French, European, Fine Dining",   "city": "Scottsdale", "reviews": 203, "cluster": 4, "bert": 4.48, "cb": 4.30},
    {"id": "biz007", "name": "BBQ Nation",              "cat": "BBQ, American, Smokehouse",       "city": "Phoenix",    "reviews": 278, "cluster": 1, "bert": 4.20, "cb": 4.05},
    {"id": "biz008", "name": "Spice Garden",            "cat": "Indian, Curry, Vegetarian",       "city": "Tempe",      "reviews": 134, "cluster": 5, "bert": 3.78, "cb": 3.60},
    {"id": "biz009", "name": "Mediterranean Oasis",     "cat": "Mediterranean, Greek, Seafood",   "city": "Mesa",       "reviews": 167, "cluster": 6, "bert": 4.15, "cb": 3.95},
    {"id": "biz010", "name": "Seoul Kitchen",           "cat": "Korean, BBQ, Bibimbap",           "city": "Phoenix",    "reviews": 221, "cluster": 2, "bert": 4.44, "cb": 4.18},
]

GLOBAL_CF_MEAN   = 2.85
GLOBAL_BERT_MEAN = 4.19
CLUSTER_NAMES    = {0:"Italian",1:"American",2:"Asian",3:"Mexican",4:"European",5:"Indian",6:"Mediterranean"}

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def minmax(val, min_v, max_v, out_min=1, out_max=5):
    if max_v == min_v:
        return (out_min + out_max) / 2
    return out_min + (val - min_v) / (max_v - min_v) * (out_max - out_min)

def nmf_factors(cf, cb, bert):
    f1 = 0.42 * cf + 0.38 * cb + 0.20 * bert
    f2 = 0.30 * cf + 0.25 * cb + 0.45 * bert
    return round(f1, 3), round(f2, 3)

def dtr_predict(cf, cb, bert, f1, f2):
    if cf > 3.5:
        if bert > 4.3:
            return min(5, 0.35*cf + 0.25*cb + 0.25*bert + 0.1*f1 + 0.05*f2 + 0.3)
        return min(5, 0.35*cf + 0.28*cb + 0.22*bert + 0.1*f1 + 0.05*f2 + 0.1)
    elif cf > 2.5:
        return min(5, 0.28*cf + 0.32*cb + 0.28*bert + 0.07*f1 + 0.05*f2)
    else:
        return min(5, 0.20*cf + 0.35*cb + 0.30*bert + 0.1*f1 + 0.05*f2 - 0.2)

def star_bar(val, max_val=5):
    pct = (val - 1) / (max_val - 1)
    filled = int(pct * 20)
    return "█" * filled + "░" * (20 - filled)

# ─── UI ──────────────────────────────────────────────────────────────────────
st.markdown("## 🍽️ Restaurant Recommender")
st.caption("Hybrid Recommendation Engine — CF + CB + BERT + NMF + DTR")
st.divider()

# Input
uid = st.text_input("Enter User ID", placeholder="e.g. rLtl8ZkDX5vH5nAx9C3q6g")

st.markdown("**Try a sample user:**")
cols = st.columns(len(USERS))
for col, (sample_uid, u) in zip(cols, USERS.items()):
    label = f"★ New User" if u["isNew"] else f"{u['name']} ({u['reviews']} reviews)"
    if col.button(label, key=sample_uid):
        uid = sample_uid
        st.session_state["uid_override"] = sample_uid

# Use session override if button was clicked
if "uid_override" in st.session_state and not uid:
    uid = st.session_state["uid_override"]

run = st.button("Get Recommendations ↗", type="primary", use_container_width=True)

# ─── PIPELINE ────────────────────────────────────────────────────────────────
if run and uid:
    st.session_state.pop("uid_override", None)
    uid = uid.strip()

    user    = USERS.get(uid)
    is_new  = not user or user["isNew"]
    is_known = bool(user) and not user["isNew"]

    st.divider()

    # Status
    if is_new:
        st.warning(f"🟡 **{uid}** — New User (0 reviews) — Cold Start Mode Active")
        with st.expander("⚠️ Cold Start Problem — what happens for new users?", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.info("**CF Score → Global Mean**\nNo user history → every restaurant gets the dataset average CF score (≈ 2.85).")
            c2.info("**CB Score → Cluster Mean**\nContent-based clustering still works — it uses restaurant features, not user history.")
            c3.info("**BERT → Global BERT Mean**\nBERT sentiment scores on all reviews still available. Well-reviewed restaurants rise to the top.")
    else:
        st.success(f"🟢 **{uid}** — {user['reviews']} reviews found — Personalised Mode")

    st.markdown("### Step-by-Step Pipeline")

    # ── STEP 1 ────────────────────────────────────────────────────────────────
    with st.expander("**Step 1 — User Lookup & History Check**", expanded=False):
        if is_new:
            st.code(f"""
user_id = "{uid}"
result  = df[df['user_id'] == user_id]

WARNING: User not found in training data!
Reviews found : 0
Strategy      : COLD START — use global averages
CF available  : NO  → fallback = dataset mean ({GLOBAL_CF_MEAN})
CB available  : YES → cluster-based scoring still works
BERT available: YES → global BERT mean = {GLOBAL_BERT_MEAN}
CF similarity matrix available : NO
""", language="python")
        else:
            reviewed_names = []
            for rid in user["reviewed"]:
                r = next((b for b in RESTAURANTS if b["id"] == rid), None)
                reviewed_names.append(r["name"].split()[0] if r else rid)
            st.code(f"""
user_id              = "{uid}"
reviews_found        = {user['reviews']}
restaurants_reviewed = {len(user['reviewed'])}
already_reviewed     = {reviewed_names}

User found! Personalised recommendation mode active.
CF similarity matrix available : YES
""", language="python")
        st.success("✅ Done")

    # ── STEP 2 ────────────────────────────────────────────────────────────────
    reviewed_ids = user["reviewed"] if user else []
    candidates   = [r for r in RESTAURANTS if r["id"] not in reviewed_ids]

    with st.expander(f"**Step 2 — Filter Candidate Restaurants** ({len(candidates)} candidates)", expanded=False):
        lines = [f"All restaurants in dataset : {len(RESTAURANTS)}",
                 f"Already reviewed by user   : {len(reviewed_ids)}",
                 f"candidates = {len(candidates)} restaurants\n"]
        for r in candidates:
            lines.append(f"  ✓ {r['name']}  ({r['cat'].split(',')[0].strip()})")
        st.code("\n".join(lines), language="text")
        st.success("✅ Done")

    # ── STEP 3 ────────────────────────────────────────────────────────────────
    cf_scores = {}
    for r in candidates:
        cf_scores[r["id"]] = (
            user["cf_scores"].get(r["id"], GLOBAL_CF_MEAN)
            if is_known else GLOBAL_CF_MEAN
        )

    with st.expander(f"**Step 3 — {'Collaborative Filtering Scores' if is_known else 'CF Fallback (Global Mean)'}**", expanded=False):
        lines = []
        if is_new:
            lines += [f'COLD START: No similar users found for "{uid}"',
                      f"global_cf_mean = {GLOBAL_CF_MEAN}", ""]
        else:
            lines += [f'Finding top-40 users similar to "{uid}"',
                      "Using cosine similarity on bert_normalized matrix", ""]
        for r in candidates:
            lines.append(f"  {r['name']:<30} cf = {cf_scores[r['id']]:.2f}")
        st.code("\n".join(lines), language="text")
        st.success("✅ Done")

    # ── STEP 4 ────────────────────────────────────────────────────────────────
    with st.expander("**Step 4 — Content-Based Scores**", expanded=False):
        lines = ["CB score = cluster's average bert_normalized (MinMaxScaled to [1,5])",
                 "This works for ALL users including new ones!",
                 "Cluster map: 0=Italian 1=American 2=Asian 3=Mexican 4=European 5=Indian 6=Mediterranean\n"]
        for r in candidates:
            lines.append(f"  {r['name']:<30} cluster={r['cluster']} ({CLUSTER_NAMES[r['cluster']]:<13})  cb={r['cb']:.2f}")
        st.code("\n".join(lines), language="text")
        st.success("✅ Done")

    # ── STEP 5 ────────────────────────────────────────────────────────────────
    with st.expander("**Step 5 — BERT Sentiment Scores**", expanded=False):
        lines = ["BERT reads every review → P(positive sentiment) [0,1]",
                 "MinMaxScaled to [1,5] → bert_normalized\n"]
        for r in candidates:
            bert_prob = (r["bert"] - 1) / 4
            lines.append(f"  {r['name']:<30} bert_prob ≈ {bert_prob:.2f}  bert_norm = {r['bert']:.2f}")
        st.code("\n".join(lines), language="text")
        st.success("✅ Done")

    # ── STEP 6 ────────────────────────────────────────────────────────────────
    scored = []
    for r in candidates:
        cf   = cf_scores[r["id"]]
        cb   = r["cb"]
        bert = r["bert"]
        cf_s   = minmax(cf,   1, 5)
        cb_s   = minmax(cb,   1, 5)
        bert_s = minmax(bert, 1, 5)
        f1, f2 = nmf_factors(cf_s, cb_s, bert_s)
        pred   = round(dtr_predict(cf_s, cb_s, bert_s, f1, f2), 2)
        scored.append({**r, "cf": cf, "cf_s": cf_s, "cb_s": cb_s,
                       "bert_s": bert_s, "f1": f1, "f2": f2, "pred": pred})

    with st.expander("**Step 6 — MinMaxScale + NMF + Decision Tree Regressor**", expanded=False):
        lines = ["Step 6a: MinMaxScaler [1,5] on all three scores",
                 "Step 6b: NMF(n_components=2) → F1 (quality), F2 (taste/sentiment)",
                 "Step 6c: feature_vec = [cf_s, cb_s, bert_s, F1, F2]",
                 "Step 6d: dtr_model.predict(feature_vec) → star rating\n"]
        for r in scored:
            lines += [
                f"  {r['name']}",
                f"    cf_s={r['cf_s']:.2f}  cb_s={r['cb_s']:.2f}  bert_s={r['bert_s']:.2f}",
                f"    NMF → F1={r['f1']}  F2={r['f2']}",
                f"    DTR → predict = {r['pred']:.2f} ★",
                ""
            ]
        st.code("\n".join(lines), language="text")
        st.success("✅ Done")

    # ── STEP 7 ────────────────────────────────────────────────────────────────
    sorted_recs = sorted(scored, key=lambda x: x["pred"], reverse=True)

    with st.expander(f"**Step 7 — Rank by Predicted Rating** (Top {len(sorted_recs)})", expanded=False):
        lines = ["Sort by pred descending, return top-10\n",
                 "recommendations = sorted(candidates, key=lambda x: x['pred'], reverse=True)[:10]\n"]
        for i, r in enumerate(sorted_recs):
            lines.append(f"  #{i+1}  {r['name']:<30}  {r['pred']:.2f} ★")
        st.code("\n".join(lines), language="text")
        st.success("✅ Done")

    # ── RESULTS ───────────────────────────────────────────────────────────────
    st.divider()
    st.markdown(f"### 🏆 Top Recommendations — {len(sorted_recs)} results for `{uid[:20]}...`")

    rank_icons = ["🥇", "🥈", "🥉"]

    for i, r in enumerate(sorted_recs):
        icon = rank_icons[i] if i < 3 else f"#{i+1}"
        bar  = star_bar(r["pred"])
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{icon} {r['name']}**")
                st.caption(f"{r['cat']}  ·  📍 {r['city']}  ·  {r['reviews']} reviews")
                st.markdown(
                    f"`CF {r['cf']:.2f}` &nbsp; `CB {r['cb']:.2f}` &nbsp; `BERT {r['bert']:.2f}`",
                    unsafe_allow_html=True
                )
            with c2:
                st.metric("Pred. Stars", f"{r['pred']:.1f} ★")
            st.text(bar)

elif run and not uid:
    st.error("Please enter a User ID first.")
else:
    st.info("👆 Enter a User ID above — or click a sample user — then hit **Get Recommendations**.")
