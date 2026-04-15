import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import time

# --- 1. CONFIGURATION & STATE ---
st.set_page_config(page_title="Niramaya AI", layout="wide")

# --- CUSTOM CSS FOR BORDERS & BOXES ---
st.markdown("""
    <style>
    .main-box {
        border: 1px solid #e6e9ef;
        border-radius: 15px;
        padding: 25px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #2E7D32;
        padding: 15px;
        border-radius: 8px;
    }
    .stButton>button {
        border-radius: 20px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

FILE_NAME = 'sugar_data.csv'
PANTRY_FILE = 'pantry.csv'

if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

@st.cache_data
def load_pantry():
    if os.path.exists(PANTRY_FILE):
        return pd.read_csv(PANTRY_FILE)
    return pd.DataFrame()

def load_history():
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        if 'Status' not in df.columns:
            df['Status'] = "N/A"
        return df
    return pd.DataFrame(columns=['Date', 'Sugar_Level', 'Status'])

pantry_df = load_pantry()

# --- 2. MASTER TRANSLATIONS ---
food_trans = {
    # GRAINS & RICE
    "brown rice": {"Telugu": "బ్రౌన్ రైస్", "Hindi": "ब्राउन राइस"},
    "black rice": {"Telugu": "నలుపు బియ్యం (Kavuni)", "Hindi": "काला चावल"},
    "red rice": {"Telugu": "ఎర్ర బియ్యం", "Hindi": "लाल चावल"},
    "hand-pounded rice": {"Telugu": "దంచిన బియ్యం", "Hindi": "हाथ से कुटा चावल"},
    "basmati rice": {"Telugu": "బాస్మతి బియ్యం", "Hindi": "बासमती चावल"},
    "bamboo rice": {"Telugu": "వెదురు బియ్యం (Moongil Arisi)", "Hindi": "बंबू राइस"},
    "little millet": {"Telugu": "సామలు", "Hindi": "कुटकी"},
    "foxtail millet": {"Telugu": "కొర్రలు", "Hindi": "कंगनी"},
    "barnyard millet": {"Telugu": "ఊదలు", "Hindi": "सांवा"},
    "kodo millet": {"Telugu": "అరికెలు", "Hindi": "कोदो"},
    "browntop millet": {"Telugu": "అందు కొర్రలు", "Hindi": "ब्राउनटॉप मिलेट"},
    "proso millet": {"Telugu": "వరిగెలు", "Hindi": "चेना"},
    "pearl millet": {"Telugu": "సజ్జలు (Bajra)", "Hindi": "बाजरा"},
    "finger millet": {"Telugu": "రాగులు (Ragi)", "Hindi": "रागी"},
    "sorghum": {"Telugu": "జొన్నలు (Jowar)", "Hindi": "ज्वार"},
    "amaranth": {"Telugu": "రాజగిర", "Hindi": "राजगिरा"},
    "buckwheat": {"Telugu": "కుట్టు", "Hindi": "कुट्टू"},
    "flattened rice": {"Telugu": "అటుకులు (Poha)", "Hindi": "पोहा"},
    "steel cut oats": {"Telugu": "ఓట్స్", "Hindi": "ओट्स"},
    "missi roti": {"Telugu": "మిస్సి రోటి", "Hindi": "मिस्सी रोटी"},
    "bajra roti": {"Telugu": "సజ్జ రోట్టె", "Hindi": "बाजरा रोटी"},
    "jowar bhakri": {"Telugu": "జొన్న రొట్టె", "Hindi": "ज्वार भाకరి"},
    "multi-grain chapati": {"Telugu": "మల్టీ గ్రెయిన్ చపాతీ", "Hindi": "मल्टीग्रेन चपाती"},
    "methi thepla": {"Telugu": "మెంతి థెప్లా", "Hindi": "मेथी थेपला"},
    "moong dal idli": {"Telugu": "పెసరపప్పు ఇడ్లీ", "Hindi": "मूंग दाल इडली"},
    "vegetable upma": {"Telugu": "వెజిటబుల్ ఉప్మా", "Hindi": "वेजिटेबल उपमा"},

    # PROTEINS & DALS
    "toor dal": {"Telugu": "కందిపప్పు", "Hindi": "अरहर दाल"},
    "chana dal": {"Telugu": "శనగ పప్పు", "Hindi": "चना दाल"},
    "urad dal": {"Telugu": "మినపప్పు", "Hindi": "उड़द दाल"},
    "moong dal": {"Telugu": "పెసరపప్పు", "Hindi": "मूंग दाल"},
    "masoor dal": {"Telugu": "ఎర్ర కందిపప్పు", "Hindi": "मसூர் दाल"},
    "kala chana": {"Telugu": "నల్ల శనగలు", "Hindi": "काला चना"},
    "rajma": {"Telugu": "రాజ్మా", "Hindi": "राजमा"},
    "horse gram": {"Telugu": "ఉలవలు (Kollu)", "Hindi": "कुलथी"},
    "paneer": {"Telugu": "పనీర్", "Hindi": "पनीर"},
    "tofu": {"Telugu": "టోఫు (Soya Paneer)", "Hindi": "टोफू"},
    "peanut chutney": {"Telugu": "పల్లి పచ్చడి", "Hindi": "मूंगफली चटनी"},
    "flaxseed podi": {"Telugu": "అవిసె గింజల పొడి", "Hindi": "अलसी पाउडर"},
    "soya chunks": {"Telugu": "సోయా మీల్ మేకర్", "Hindi": "सोया चंक्स"},

    # VEGETABLES
    "bitter gourd": {"Telugu": "కాకరకాయ", "Hindi": "करेला"},
    "drumstick leaves": {"Telugu": "మునగాకు", "Hindi": "सहजन के पत्ते"},
    "gongura": {"Telugu": "గోంగూర", "Hindi": "गोंगुरा"},
    "ivy gourd": {"Telugu": "దొండకాయ", "Hindi": "कुंदरू"},
    "ladies finger": {"Telugu": "బెండకాయ", "Hindi": "भिंडी"},
    "ash gourd": {"Telugu": "బూడిద గుమ్మడి", "Hindi": "पेठा"},
    "sambar": {"Telugu": "సాంబార్", "Hindi": "सांभर"},
    "coconut chutney": {"Telugu": "కొబ్బరి పచ్చడి", "Hindi": "नारियल चटनी"},
    "pudina chutney": {"Telugu": "పుదీనా పచ్చడి", "Hindi": "पुदीना चटनी"},
    "ginger chutney": {"Telugu": "అల్లం పచ్చడి", "Hindi": "अदरक चटनी"},
    "tomato": {"Telugu": "టమాటా", "Hindi": "टमाटर"},
    "onion": {"Telugu": "ఉల్లిపాయ", "Hindi": "प्याज़"},
    "green peas": {"Telugu": "బఠానీలు", "Hindi": "मटर"},
    "french beans": {"Telugu": "బీన్స్", "Hindi": "फ्रेन्च बीन्स"},
    "cauliflower": {"Telugu": "క్యాలీఫ్లవర్", "Hindi": "गोभी"},
    "cabbage": {"Telugu": "క్యాబేజీ", "Hindi": "पत्ता गोभी"},
    "capsicum": {"Telugu": "క్యాప్సికమ్", "Hindi": "शिमला मिर्च"},
    "carrot": {"Telugu": "క్యారెట్", "Hindi": "गाजर"},
    "radish": {"Telugu": "ముల్లంగి", "Hindi": "मूली"},
    "beetroot": {"Telugu": "బీట్‌రూట్", "Hindi": "चुकंदर"},

    # SPICES
    "fenugreek seeds": {"Telugu": "మెంతులు", "Hindi": "मेथी दाना"},
    "cinnamon": {"Telugu": "దాల్చిన చెక్క", "Hindi": "दालचीनी"},
    "curry leaf podi": {"Telugu": "కరివేపాకు పొడి", "Hindi": "करी पत्ता पाउडर"},
    "garlic podi": {"Telugu": "వెల్లుల్లి పొడి", "Hindi": "लहसुन पाउडर"},
    "turmeric": {"Telugu": "పసుపు", "Hindi": "हल्दी"},
    "cumin": {"Telugu": "జీలకర్ర", "Hindi": "जीरा"},
    "mustard seeds": {"Telugu": "ఆవాలు", "Hindi": "सरसों"},
    "black pepper": {"Telugu": "మిరియాలు", "Hindi": "काली मिर्च"},

    # JUICES & DRINKS
    "karela-amla juice": {"Telugu": "కాకరకాయ-ఉసిరి రసం", "Hindi": "करेला-आंवला रस"},
    "buttermilk": {"Telugu": "మజ్జిగ", "Hindi": "छाछ"},
    "ragi malt": {"Telugu": "రాగి మాల్ట్", "Hindi": "రాగి మామ్ట్"},
    "coconut water": {"Telugu": "కొబ్బరి నీళ్లు", "Hindi": "नारियल पानी"},
    "barley water": {"Telugu": "బార్లీ నీళ్లు", "Hindi": "जौ का पानी"},
    "lemon water": {"Telugu": "నిమ్మ నీళ్లు", "Hindi": "नींबू पानी"},
    "tomato soup": {"Telugu": "టమాటా సూప్", "Hindi": "टमाटर सूप"},
    "bottle gourd juice": {"Telugu": "ఆనపకాయ రసం", "Hindi": "लौकी का रस"},
    "tomato-celery juice": {"Telugu": "టమాటా-సెలరీ రసం", "Hindi": "टमाटर-सेलरी रस"},
    "aloe vera juice": {"Telugu": "కలబంద రసం", "Hindi": "एलोवेरा जूस"},
    "smoothie": {"Telugu": "స్మూతీ", "Hindi": "स्मूदी"},

    # SNACKS & FRUITS
    "makhana": {"Telugu": "తామర గింజలు", "Hindi": "मखाना"},
    "walnuts": {"Telugu": "అక్రోట్", "Hindi": "अखरोट"},
    "almonds": {"Telugu": "బాదం", "Hindi": "बादाम"},
    "pumpkin seeds": {"Telugu": "గుమ్మడి గింజలు", "Hindi": "कद्दू के बीज"},
    "sunflower seeds": {"Telugu": "సూర్యకాంత గింజలు", "Hindi": "सूरजमुखी के बीज"},
    "flaxseeds": {"Telugu": "అవిసె గింజలు", "Hindi": "अलसी"},
    "sprouted moong": {"Telugu": "మొలకెత్తిన పెసలు", "Hindi": "अंकुरित मूंग"},
    "roasted chana": {"Telugu": "పుట్నాల పప్పు", "Hindi": "भुना चना"},
    "guava": {"Telugu": "జామకాయ", "Hindi": "अमरूद"},
    "papaya": {"Telugu": "బొప్పాయి", "Hindi": "पपीता"},
    "amla": {"Telugu": "ఉసిరి", "Hindi": "आंवला"},
    "jamun": {"Telugu": "నేరేడు పండు", "Hindi": "जामुन"},
    "pomegranate": {"Telugu": "దానిమ్మ", "Hindi": "अनार"},
    "apple": {"Telugu": "ఆపిల్", "Hindi": "सेब"},
    "pear": {"Telugu": "బేరి పండు", "Hindi": "नाशपाती"},
    "muskmelon": {"Telugu": "ఖర్బూజ", "Hindi": "खरबूजा"},
    "custard apple": {"Telugu": "సీతాఫలం", "Hindi": "शरीफा"},
    "wood apple": {"Telugu": "వెలగపండు", "Hindi": "बेल"},
    "ber": {"Telugu": "రేగు పండు", "Hindi": "बेर"},
    "coconut": {"Telugu": "కొబ్బరి", "Hindi": "नारियल"},
    "phalsa": {"Telugu": "ఫల్సా", "Hindi": "फालसा"},
    "star fruit": {"Telugu": "నక్షత్ర ఫలం", "Hindi": "कमरख"}
}

def translate_any(name, lang):
    if lang == "English": return name
    name_lower = str(name).lower()
    for key, trans in food_trans.items():
        if key in name_lower: return trans.get(lang, name)
    return name

translations = {
    "English": {
        "title": "🌿 Niramaya AI",
        "input": "Enter Glucose (mg/dL)",
        "btn": "Generate Roadmap",
        "pay_title": "💳 Subscription Hub",
        "pay_btn": "Unlock Pro - ₹499",
        "locked": "🔒 Pro Feature: Unlock history and trend analysis.",
        "history": "📊 Personal Health Log",
        "road": "Nutrition Roadmap",
        "hunger": "💡 Optional: Eat only if you feel hungry",
        "disclaimer": "⚠️ Disclaimer: This is a diet plan tool only. Neither the creator nor the AI is responsible for your eating habits or health incidents.",
        "units": {"Cup": "Cup", "Glass": "Glass", "Handful": "Handful", "Small": "Small", "Medium": "Medium", "Large": "Large", "None": "None"},
        "alerts": {"high": "🚨 HIGH ALERT", "elevated": "⚠️ ELEVATED", "low": "📉 LOW ALERT", "normal": "✅ NORMAL"}
    },
    "Telugu": {
        "title": "🌿 నిరామయ AI",
        "input": "గ్లూకోజ్ స్థాయి (mg/dL)",
        "btn": "డైట్ ప్లాన్",
        "pay_title": "💳 సబ్‌స్క్రిప్షన్ హబ్",
        "pay_btn": "ప్రో అన్‌లాక్ చేయండి - ₹499",
        "locked": "🔒 ప్రో ఫీచర్: చరిత్రను చూడటానికి సబ్‌స్క్రిప్షన్ అవసరం.",
        "history": "📊 ఆరోగ్య చరిత్ర",
        "road": "ఆహార ప్రణాళిక",
        "hunger": "💡 గమనిక: ఆకలిగా అనిపిస్తేనే తీసుకోండి",
        "disclaimer": "⚠️ గమనిక: ఇది ఆహార ప్రణాళిక సాధనం మాత్రమే. మీ ఆహారపు అలవాట్లు లేదా ఆరోగ్య సమస్యలకు సృష్టికర్త లేదా AI బాధ్యత వహించదు.",
        "units": {"Cup": "కప్పు", "Glass": "గ్లాసు", "Handful": "పిడికెడు", "Small": "చిన్న", "Medium": "మధ్యస్థ", "Large": "పెద్ద", "None": "ఏమీ లేదు"},
        "alerts": {"high": "🚨 హై అలర్ట్ (ఎక్కువ)", "elevated": "⚠️ పెరిగిన స్థాయి", "low": "📉 లో అలర్ట్ (తక్కువ)", "normal": "✅ సాధారణం"}
    },
    "Hindi": {
        "title": "🌿 निरामय AI",
        "input": "ग्लूकोज स्तर (mg/dL)",
        "btn": "आहार योजना",
        "pay_title": "💳 सदस्यता केंद्र",
        "pay_btn": "प्रो अनलॉक करें - ₹499",
        "locked": "🔒 प्रो फीचर: इतिहास और रुझान विश्लेषण अनलॉक करें।",
        "history": "📊 स्वास्थ्य इतिहास",
        "road": "पोषण रोडमैप",
        "hunger": "💡 नोट: भूख लगे तभी खाएं",
        "disclaimer": "⚠️ डिस्क्लेमर: यह केवल एक आहार योजना उपकरण है। आपके खान-पान या स्वास्थ्य घटनाओं के लिए निर्माता या AI जिम्मेदार नहीं है।",
        "units": {"Cup": "कप", "Glass": "ग्लास", "Handful": "मुट्ठी भर", "Small": "छोटा", "Medium": "मध्यम", "Large": "बड़ा", "None": "कोई नहीं"},
        "alerts": {"high": "🚨 हाई अलर्ट", "elevated": "⚠️ बढ़ा हुआ स्तर", "low": "📉 लो अलर्ट", "normal": "✅ सामान्य"}
    }
}

# --- 3. SIDEBAR & PAYMENT GATEWAY ---
lang = st.sidebar.selectbox("Language / భాష", ["English", "Telugu", "Hindi"])
t = translations[lang]

st.sidebar.divider()
st.sidebar.subheader(t["pay_title"])
if not st.session_state.is_pro:
    if st.sidebar.button(t["pay_btn"]):
        with st.sidebar.status("Opening Razorpay Gateway..."): time.sleep(1.5)
        st.session_state.is_pro = True
        st.balloons()
        st.rerun()
else:
    st.sidebar.success("Pro Member ✅")
    if st.sidebar.button("Logout"):
        st.session_state.is_pro = False
        st.rerun()

# --- 4. CORE LOGIC ---
def get_config(val):
    u = t["units"]
    a = t["alerts"]
    if val > 180:
        return a["high"], {"Grain": f"1/2 {u['Cup']}", "Veg": f"3 {u['Cup']}", "Juice": f"1 {u['Glass']}", "Snack": u["None"], "Fruit": u["None"]}
    elif val > 140:
        return a["elevated"], {"Grain": f"1 {u['Cup']}", "Veg": f"2 {u['Cup']}", "Juice": f"1 {u['Glass']}", "Snack": f"1 {u['Handful']}", "Fruit": f"1 {u['Small']}"}
    elif val < 70:
        return a["low"], {"Grain": f"1.5 {u['Cup']}", "Veg": f"1 {u['Cup']}", "Juice": f"1 {u['Glass']}", "Snack": f"1 {u['Handful']}", "Fruit": f"1 {u['Large']}"}
    else:
        return a["normal"], {"Grain": f"1 {u['Cup']}", "Veg": f"2 {u['Cup']}", "Juice": f"1 {u['Glass']}", "Snack": f"1 {u['Handful']}", "Fruit": f"1 {u['Medium']}"}

# --- 5. MAIN DASHBOARD ---
st.title(t["title"])

# Wrapper for Input Section
st.markdown('<div class="main-box">', unsafe_allow_html=True)
c1, c2 = st.columns([2, 1])
with c1:
    sugar_input = st.number_input(t['input'], 10, 500, 110)
with c2:
    st.write("##") # Spacer
    if st.button(t['btn']):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        status_txt, _ = get_config(sugar_input)
        pd.DataFrame([[now, sugar_input, status_txt]], columns=['Date', 'Sugar_Level', 'Status']).to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False)
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PRO HISTORY ---
if st.session_state.is_pro:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader(t["history"])
    h_df = load_history()
    if not h_df.empty:
        st.plotly_chart(px.area(h_df, x='Date', y='Sugar_Level', color_discrete_sequence=['#2E7D32'], height=250), use_container_width=True)
        def color_rows(val):
            v_low = str(val).lower()
            if "high" in v_low or "ఎక్కువ" in v_low: return 'background-color: #ffcccc'
            if "low" in v_low or "తక్కువ" in v_low: return 'background-color: #cce5ff'
            if "normal" in v_low or "సాధారణం" in v_low: return 'background-color: #d4edda'
            return ''
        st.dataframe(h_df.style.map(color_rows, subset=['Status']), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning(t["locked"])

# --- 7. DIET ROADMAP & HUNGER ---
status_txt, p_text = get_config(sugar_input)

st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.subheader(f"{t['road']} — ({status_txt})")

if not pantry_df.empty:
    m_cols = st.columns(3)
    meals = [("Breakfast", [("Grain", "🥣"), ("Juice", "🥤")]),
             ("Lunch", [("Grain", "🍚"), ("Veg", "🥗")]),
             ("Dinner", [("Grain", "🫓"), ("Veg", "🥗")])]

    for i, (m_name, items) in enumerate(meals):
        with m_cols[i]:
            st.markdown(f'<div class="metric-card"><h4>{translate_any(m_name, lang)}</h4>', unsafe_allow_html=True)
            for cat, icon in items:
                subset = pantry_df[pantry_df['type'] == cat]
                if not subset.empty:
                    row = subset.sample(1).iloc[0]
                    st.markdown(f"{icon} **{translate_any(row['name'], lang)}** <br><span style='color:green;'>[{p_text.get(cat, '')}]</span>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Hunger Section Logic
    st.divider()
    st.markdown(f"### {t['hunger']}")
    hc1, hc2 = st.columns(2)
    for col, cat, icon in zip([hc1, hc2], ["Snack", "Fruit"], ["🥜", "🍎"]):
        qty = p_text.get(cat, "")
        if qty != t["units"]["None"]:
            subset = pantry_df[pantry_df['type'] == cat]
            if not subset.empty:
                row = subset.sample(1).iloc[0]
                col.success(f"{icon} **{translate_any(row['name'], lang)}** ({qty})")
st.markdown('</div>', unsafe_allow_html=True)

# --- 8. FOOTER ---
st.divider()
st.caption(t["disclaimer"])