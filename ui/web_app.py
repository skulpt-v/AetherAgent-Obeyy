from pathlib import Path

import streamlit as st

from memory import Database
from core.agent import AetherAgent
from tools.calculator import Calculator


# ==========================================================
# SAYFA AYARLARI
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "assets" / "obeyy_logo.png"

st.set_page_config(
    page_title="Obeyy",
    page_icon=str(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# AGENT
# ==========================================================

@st.cache_resource
def create_agent():
    """Obeyy Agent ve veritabanını oluşturur."""

    database = Database()

    agent = AetherAgent(database)

    calculator = Calculator()

    agent.register_tool(
        "calculator",
        calculator.calculate,
    )

    return database, agent


database, agent = create_agent()


# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "appearance" not in st.session_state:
    st.session_state.appearance = "Koyu"

if "compact_mode" not in st.session_state:
    st.session_state.compact_mode = False


# ==========================================================
# TEMA AYARLARI
# ==========================================================

THEMES = {

    # ------------------------------------------------------
    # KOYU
    # ------------------------------------------------------

    "Koyu": {
        "APP_BACKGROUND": "#000000",
        "APP_TEXT": "#f5f5f5",
        "SECONDARY_TEXT": "#a1a1aa",
        "BORDER": "#27272a",
        "CARD_BACKGROUND": "#0d0d0f",
        "SIDEBAR_BACKGROUND": "#050505",
        "BUTTON_BACKGROUND": "#0a0a0a",
        "BUTTON_HOVER": "#18181b",
        "INPUT_BACKGROUND": "#0d0d0f",
        "INPUT_TEXT": "#ffffff",
        "ACCENT": "#ffffff",
        "ACCENT_TEXT": "#000000",
        "GLOW": "rgba(255,255,255,0.07)",
        "RADIAL_1": "rgba(255,255,255,0.035)",
        "RADIAL_2": "rgba(120,120,140,0.025)",

        "USER_BUBBLE": "#ffffff",
        "USER_BUBBLE_TEXT": "#000000",

        "ASSISTANT_BUBBLE": "#0d0d0f",
        "ASSISTANT_BUBBLE_TEXT": "#f5f5f5",

        "BUBBLE_BORDER": "#27272a",
    },


    # ------------------------------------------------------
    # AÇIK
    # ------------------------------------------------------

    "Açık": {
        "APP_BACKGROUND": "#f5f5f7",
        "APP_TEXT": "#111111",
        "SECONDARY_TEXT": "#4b4b52",
        "BORDER": "#d1d1d6",
        "CARD_BACKGROUND": "#ffffff",
        "SIDEBAR_BACKGROUND": "#e9e9ec",
        "BUTTON_BACKGROUND": "#ffffff",
        "BUTTON_HOVER": "#dedee3",
        "INPUT_BACKGROUND": "#ffffff",
        "INPUT_TEXT": "#111111",
        "ACCENT": "#111111",
        "ACCENT_TEXT": "#ffffff",
        "GLOW": "rgba(0,0,0,0.06)",
        "RADIAL_1": "rgba(0,0,0,0.035)",
        "RADIAL_2": "rgba(80,80,100,0.025)",

        "USER_BUBBLE": "#111111",
        "USER_BUBBLE_TEXT": "#ffffff",

        "ASSISTANT_BUBBLE": "#ffffff",
        "ASSISTANT_BUBBLE_TEXT": "#111111",

        "BUBBLE_BORDER": "#d1d1d6",
    },


    # ------------------------------------------------------
    # MOR
    # ------------------------------------------------------

    "Mor": {
        "APP_BACKGROUND": "#f5f0ff",
        "APP_TEXT": "#24113f",
        "SECONDARY_TEXT": "#5f4a78",
        "BORDER": "#d8c8ed",
        "CARD_BACKGROUND": "#ffffff",
        "SIDEBAR_BACKGROUND": "#ebe1f8",
        "BUTTON_BACKGROUND": "#ffffff",
        "BUTTON_HOVER": "#ded0ef",
        "INPUT_BACKGROUND": "#ffffff",
        "INPUT_TEXT": "#24113f",
        "ACCENT": "#7c3aed",
        "ACCENT_TEXT": "#ffffff",
        "GLOW": "rgba(124,58,237,0.12)",
        "RADIAL_1": "rgba(124,58,237,0.10)",
        "RADIAL_2": "rgba(168,85,247,0.07)",

        "USER_BUBBLE": "#7c3aed",
        "USER_BUBBLE_TEXT": "#ffffff",

        "ASSISTANT_BUBBLE": "#ffffff",
        "ASSISTANT_BUBBLE_TEXT": "#24113f",

        "BUBBLE_BORDER": "#d8c8ed",
    },


    # ------------------------------------------------------
    # KOYU MOR
    # ------------------------------------------------------

    "Koyu Mor": {
        "APP_BACKGROUND": "#10051c",
        "APP_TEXT": "#f7f1ff",
        "SECONDARY_TEXT": "#c2a9d8",
        "BORDER": "#39204d",
        "CARD_BACKGROUND": "#170a24",
        "SIDEBAR_BACKGROUND": "#0c0315",
        "BUTTON_BACKGROUND": "#160820",
        "BUTTON_HOVER": "#281037",
        "INPUT_BACKGROUND": "#170a24",
        "INPUT_TEXT": "#ffffff",
        "ACCENT": "#a855f7",
        "ACCENT_TEXT": "#ffffff",
        "GLOW": "rgba(168,85,247,0.15)",
        "RADIAL_1": "rgba(168,85,247,0.12)",
        "RADIAL_2": "rgba(126,34,206,0.08)",

        "USER_BUBBLE": "#a855f7",
        "USER_BUBBLE_TEXT": "#ffffff",

        "ASSISTANT_BUBBLE": "#170a24",
        "ASSISTANT_BUBBLE_TEXT": "#f7f1ff",

        "BUBBLE_BORDER": "#39204d",
    },


    # ------------------------------------------------------
    # MAVİ
    # ------------------------------------------------------

    "Mavi": {
        "APP_BACKGROUND": "#eef6ff",
        "APP_TEXT": "#10233f",
        "SECONDARY_TEXT": "#50657f",
        "BORDER": "#c7d9ee",
        "CARD_BACKGROUND": "#ffffff",
        "SIDEBAR_BACKGROUND": "#e1edfa",
        "BUTTON_BACKGROUND": "#ffffff",
        "BUTTON_HOVER": "#d5e4f5",
        "INPUT_BACKGROUND": "#ffffff",
        "INPUT_TEXT": "#10233f",
        "ACCENT": "#2563eb",
        "ACCENT_TEXT": "#ffffff",
        "GLOW": "rgba(37,99,235,0.10)",
        "RADIAL_1": "rgba(37,99,235,0.09)",
        "RADIAL_2": "rgba(14,165,233,0.06)",

        "USER_BUBBLE": "#2563eb",
        "USER_BUBBLE_TEXT": "#ffffff",

        "ASSISTANT_BUBBLE": "#ffffff",
        "ASSISTANT_BUBBLE_TEXT": "#10233f",

        "BUBBLE_BORDER": "#c7d9ee",
    },


    # ------------------------------------------------------
    # GECE MAVİSİ
    # ------------------------------------------------------

    "Gece Mavisi": {
        "APP_BACKGROUND": "#06111f",
        "APP_TEXT": "#edf6ff",
        "SECONDARY_TEXT": "#9eb4ca",
        "BORDER": "#18304a",
        "CARD_BACKGROUND": "#0a1929",
        "SIDEBAR_BACKGROUND": "#040c16",
        "BUTTON_BACKGROUND": "#091726",
        "BUTTON_HOVER": "#10283e",
        "INPUT_BACKGROUND": "#0a1929",
        "INPUT_TEXT": "#ffffff",
        "ACCENT": "#3b82f6",
        "ACCENT_TEXT": "#ffffff",
        "GLOW": "rgba(59,130,246,0.15)",
        "RADIAL_1": "rgba(59,130,246,0.12)",
        "RADIAL_2": "rgba(14,165,233,0.08)",

        "USER_BUBBLE": "#3b82f6",
        "USER_BUBBLE_TEXT": "#ffffff",

        "ASSISTANT_BUBBLE": "#0a1929",
        "ASSISTANT_BUBBLE_TEXT": "#edf6ff",

        "BUBBLE_BORDER": "#18304a",
    },
}


theme = THEMES.get(
    st.session_state.appearance,
    THEMES["Koyu"],
)


# ==========================================================
# TEMA DEĞİŞKENLERİ
# ==========================================================

APP_BACKGROUND = theme["APP_BACKGROUND"]
APP_TEXT = theme["APP_TEXT"]
SECONDARY_TEXT = theme["SECONDARY_TEXT"]
BORDER = theme["BORDER"]

CARD_BACKGROUND = theme["CARD_BACKGROUND"]
SIDEBAR_BACKGROUND = theme["SIDEBAR_BACKGROUND"]

BUTTON_BACKGROUND = theme["BUTTON_BACKGROUND"]
BUTTON_HOVER = theme["BUTTON_HOVER"]

INPUT_BACKGROUND = theme["INPUT_BACKGROUND"]
INPUT_TEXT = theme["INPUT_TEXT"]

ACCENT = theme["ACCENT"]
ACCENT_TEXT = theme["ACCENT_TEXT"]

GLOW = theme["GLOW"]
RADIAL_1 = theme["RADIAL_1"]
RADIAL_2 = theme["RADIAL_2"]

USER_BUBBLE = theme["USER_BUBBLE"]
USER_BUBBLE_TEXT = theme["USER_BUBBLE_TEXT"]

ASSISTANT_BUBBLE = theme["ASSISTANT_BUBBLE"]
ASSISTANT_BUBBLE_TEXT = theme["ASSISTANT_BUBBLE_TEXT"]

BUBBLE_BORDER = theme["BUBBLE_BORDER"]


# ==========================================================
# COMPACT MODE
# ==========================================================

compact_css = ""

if st.session_state.compact_mode:

    compact_css = """
    .main .block-container {
        max-width: 900px !important;
    }

    div[data-testid="stChatMessage"] {
        margin-top: 4px !important;
        margin-bottom: 4px !important;
    }

    div[data-testid="stChatMessageContent"] {
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }
    """


# ==========================================================
# CSS
# ==========================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       GENEL
       ====================================================== */

    .stApp {{
        background:
            radial-gradient(
                circle at 15% 10%,
                {RADIAL_1},
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 90%,
                {RADIAL_2},
                transparent 35%
            ),
            {APP_BACKGROUND};

        color: {APP_TEXT};
        background-attachment: fixed;
    }}


    .main .block-container {{
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }}


    .stApp p,
    .stApp label {{
        color: {APP_TEXT};
    }}


    [data-testid="stCaptionContainer"] {{
        color: {SECONDARY_TEXT} !important;
    }}


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {{
        background:
            radial-gradient(
                circle at 50% 0%,
                {GLOW},
                transparent 35%
            ),
            {SIDEBAR_BACKGROUND};

        border-right: 1px solid {BORDER};
    }}


    section[data-testid="stSidebar"] button {{
        border-radius: 10px;
        border: 1px solid {BORDER};
        background-color: {BUTTON_BACKGROUND};
        color: {APP_TEXT};

        transition:
            background-color 0.15s ease,
            border-color 0.15s ease,
            transform 0.1s ease;
    }}


    section[data-testid="stSidebar"] button:hover {{
        background-color: {BUTTON_HOVER};
        border-color: {ACCENT};
        color: {APP_TEXT};
    }}


    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {APP_TEXT} !important;
    }}


    /* ======================================================
       LOGO
       ====================================================== */

    div[data-testid="stImage"] img {{
        border-radius: 18px;
    }}


    .logo-title {{
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-top: 4px;
        color: {APP_TEXT} !important;
    }}


    .logo-subtitle {{
        color: {SECONDARY_TEXT} !important;
        font-size: 14px;
        margin-top: -5px;
    }}


    /* ======================================================
       BAŞLIK
       ====================================================== */

    .obeyy-title {{
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -2px;
        margin-bottom: 0;
        color: {APP_TEXT} !important;
    }}


    .obeyy-subtitle {{
        color: {SECONDARY_TEXT} !important;
        font-size: 15px;
        margin-top: -5px;
    }}


    /* ======================================================
       CHAT
       ====================================================== */

    div[data-testid="stChatMessage"] {{
        background: transparent !important;
        border: none !important;

        width: 100%;
        display: flex !important;

        align-items: flex-start;

        margin-top: 12px;
        margin-bottom: 12px;

        padding: 0 !important;
    }}


    /* ======================================================
       ASSISTANT
       ====================================================== */

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {{
        flex-direction: row !important;
        justify-content: flex-start !important;
    }}


    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] {{

        background: {ASSISTANT_BUBBLE} !important;
        color: {ASSISTANT_BUBBLE_TEXT} !important;

        border: 1px solid {BUBBLE_BORDER};
        border-radius: 18px;

        padding: 13px 17px;

        max-width: min(78%, 780px);

        margin-left: 10px !important;
        margin-right: 0 !important;

        box-shadow:
            0 3px 16px rgba(0, 0, 0, 0.08);

        overflow-wrap: anywhere;
    }}


    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] p,

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] li,

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] strong,

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    )
    [data-testid="stChatMessageContent"] em {{
        color: {ASSISTANT_BUBBLE_TEXT} !important;
    }}


    /* ======================================================
       USER
       ====================================================== */

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {{
        flex-direction: row-reverse !important;
        justify-content: flex-start !important;
    }}


    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] {{

        background: {USER_BUBBLE} !important;
        color: {USER_BUBBLE_TEXT} !important;

        border: 1px solid {BUBBLE_BORDER};
        border-radius: 18px;

        padding: 13px 17px;

        max-width: min(78%, 780px);

        margin-right: 10px !important;
        margin-left: 0 !important;

        box-shadow:
            0 3px 16px rgba(0, 0, 0, 0.08);

        overflow-wrap: anywhere;
    }}


    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] p,

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] li,

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] strong,

    div[data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    )
    [data-testid="stChatMessageContent"] em {{
        color: {USER_BUBBLE_TEXT} !important;
    }}


    /* ======================================================
       AVATAR
       ====================================================== */

    div[data-testid="stChatMessage"]
    [data-testid="chatAvatarIcon-user"],
    div[data-testid="stChatMessage"]
    [data-testid="chatAvatarIcon-assistant"] {{
        flex-shrink: 0;
    }}


    /* ======================================================
       CODE
       ====================================================== */

    div[data-testid="stChatMessageContent"] pre {{
        border-radius: 10px;
        overflow-x: auto;
        max-width: 100%;
    }}


    div[data-testid="stChatMessageContent"] code {{
        border-radius: 5px;
    }}


    /* ======================================================
       CHAT INPUT
       ====================================================== */

    div[data-testid="stChatInput"] {{
        border-radius: 15px;
        border: 1px solid {BORDER};
        background-color: {INPUT_BACKGROUND};
    }}


    div[data-testid="stChatInput"] textarea {{
        color: {INPUT_TEXT} !important;
        background-color: {INPUT_BACKGROUND} !important;
    }}


    div[data-testid="stChatInput"] textarea::placeholder {{
        color: {SECONDARY_TEXT} !important;
    }}


    /* ======================================================
       INPUTLAR
       ====================================================== */

    input,
    textarea {{
        color: {INPUT_TEXT} !important;
        background-color: {INPUT_BACKGROUND} !important;
        border-color: {BORDER} !important;
    }}


    input::placeholder,
    textarea::placeholder {{
        color: {SECONDARY_TEXT} !important;
    }}


    /* ======================================================
       SELECTBOX
       ====================================================== */

    div[data-baseweb="select"] > div {{
        background-color: {INPUT_BACKGROUND} !important;
        border-color: {BORDER} !important;
        color: {INPUT_TEXT} !important;
    }}


    div[data-baseweb="select"] span {{
        color: {INPUT_TEXT} !important;
    }}


    /* ======================================================
       BUTONLAR
       ====================================================== */

    .stButton > button {{
        border-radius: 10px;

        border: 1px solid {BORDER};

        background-color: {BUTTON_BACKGROUND};

        color: {APP_TEXT};

        transition:
            background-color 0.15s ease,
            border-color 0.15s ease,
            transform 0.1s ease;

        min-height: 42px;
    }}


    .stButton > button:hover {{
        background-color: {BUTTON_HOVER};
        border-color: {ACCENT};
        color: {APP_TEXT};

        transform: translateY(-1px);
    }}


    /* ======================================================
       TOGGLE
       ====================================================== */

    div[data-testid="stToggle"] label {{
        color: {APP_TEXT} !important;
    }}


    /* ======================================================
       SLIDER
       ====================================================== */

    div[data-testid="stSlider"] label {{
        color: {APP_TEXT} !important;
    }}


    /* ======================================================
       KARTLAR
       ====================================================== */

    .memory-card {{
        padding: 18px;
        margin-bottom: 14px;

        border: 1px solid {BORDER};
        border-radius: 14px;

        background: {CARD_BACKGROUND};
    }}


    .settings-card {{
        padding: 20px;

        border: 1px solid {BORDER};
        border-radius: 16px;

        background: {CARD_BACKGROUND};

        margin-bottom: 16px;
    }}


    .settings-card b {{
        color: {APP_TEXT} !important;
    }}


    /* ======================================================
       ALERT
       ====================================================== */

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {{
        border-color: {BORDER} !important;
    }}


    /* ======================================================
       LINK
       ====================================================== */

    a {{
        color: {ACCENT} !important;
    }}


    /* ======================================================
       COMPACT
       ====================================================== */

    {compact_css}


    /* ======================================================
       MOBİL ARAYÜZ
       ====================================================== */

    @media only screen and (max-width: 768px) {{

        /* ----------------------------------------------
           ANA ALAN
           ---------------------------------------------- */

        .main .block-container {{
            max-width: 100% !important;

            padding-top: 0.8rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-bottom: 6rem !important;
        }}


        /* ----------------------------------------------
           SIDEBAR
           ---------------------------------------------- */

        section[data-testid="stSidebar"] {{
            width: 82vw !important;
            max-width: 340px !important;
        }}


        /* ----------------------------------------------
           BAŞLIK
           ---------------------------------------------- */

        .obeyy-title {{
            font-size: 29px !important;
            letter-spacing: -1.2px !important;
        }}


        .obeyy-subtitle {{
            font-size: 12px !important;
        }}


        /* ----------------------------------------------
           HEADER LOGO
           ---------------------------------------------- */

        div[data-testid="stImage"] img {{
            max-width: 100%;
        }}


        /* ----------------------------------------------
           CHAT
           ---------------------------------------------- */

        div[data-testid="stChatMessage"] {{
            margin-top: 8px !important;
            margin-bottom: 8px !important;

            width: 100% !important;
        }}


        /* ----------------------------------------------
           CHAT BALONLARI
           ---------------------------------------------- */

        div[data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-assistant"]
        )
        [data-testid="stChatMessageContent"] {{

            max-width: calc(100% - 45px) !important;

            margin-left: 7px !important;

            padding: 11px 13px !important;

            border-radius: 16px !important;

            font-size: 14px !important;

            line-height: 1.5 !important;
        }}


        div[data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-user"]
        )
        [data-testid="stChatMessageContent"] {{

            max-width: calc(100% - 45px) !important;

            margin-right: 7px !important;

            padding: 11px 13px !important;

            border-radius: 16px !important;

            font-size: 14px !important;

            line-height: 1.5 !important;
        }}


        /* ----------------------------------------------
           AVATAR
           ---------------------------------------------- */

        div[data-testid="stChatMessage"] > div:first-child {{
            width: 32px !important;
            min-width: 32px !important;
        }}


        /* ----------------------------------------------
           CODE BLOKLARI
           ---------------------------------------------- */

        div[data-testid="stChatMessageContent"] pre {{
            max-width: 100% !important;

            font-size: 12px !important;

            white-space: pre-wrap !important;
            word-break: break-word !important;
        }}


        div[data-testid="stChatMessageContent"] code {{
            word-break: break-word !important;
        }}


        /* ----------------------------------------------
           CHAT INPUT
           ---------------------------------------------- */

        div[data-testid="stChatInput"] {{
            width: calc(100% - 1rem) !important;

            margin-left: 0.5rem !important;
            margin-right: 0.5rem !important;

            border-radius: 18px !important;
        }}


        div[data-testid="stChatInput"] textarea {{
            font-size: 15px !important;

            min-height: 46px !important;
        }}


        /* ----------------------------------------------
           BUTONLAR
           ---------------------------------------------- */

        .stButton > button {{
            min-height: 46px !important;

            font-size: 14px !important;

            border-radius: 12px !important;
        }}


        /* ----------------------------------------------
           SELECTBOX
           ---------------------------------------------- */

        div[data-baseweb="select"] {{
            min-height: 46px !important;
        }}


        /* ----------------------------------------------
           SETTINGS
           ---------------------------------------------- */

        .settings-card {{
            padding: 15px !important;

            border-radius: 14px !important;
        }}


        /* ----------------------------------------------
           MEMORY
           ---------------------------------------------- */

        .memory-card {{
            padding: 14px !important;
        }}


        /* ----------------------------------------------
           COLUMNS
           ---------------------------------------------- */

        div[data-testid="stHorizontalBlock"] {{
            gap: 0.5rem !important;
        }}


        /* ----------------------------------------------
           MOBİL ALT NAVİGASYON
           ---------------------------------------------- */

        .mobile-nav {{
            position: fixed;

            left: 10px;
            right: 10px;
            bottom: 10px;

            height: 58px;

            z-index: 999999;

            display: flex;

            align-items: center;
            justify-content: space-around;

            border: 1px solid {BORDER};

            border-radius: 18px;

            background:
                linear-gradient(
                    180deg,
                    {CARD_BACKGROUND},
                    {INPUT_BACKGROUND}
                );

            box-shadow:
                0 10px 35px rgba(0,0,0,0.30);

            backdrop-filter: blur(20px);
        }}


        .mobile-nav-item {{
            flex: 1;

            height: 100%;

            display: flex;

            flex-direction: column;

            align-items: center;

            justify-content: center;

            color: {SECONDARY_TEXT};

            font-size: 11px;

            text-decoration: none;

            gap: 2px;
        }}


        .mobile-nav-item.active {{
            color: {ACCENT};
            font-weight: 700;
        }}


        .mobile-nav-icon {{
            font-size: 19px;
            line-height: 20px;
        }}
    }}


    /* ======================================================
       MASAÜSTÜNDE MOBİL NAV GİZLİ
       ====================================================== */

    @media only screen and (min-width: 769px) {{
        .mobile-nav {{
            display: none !important;
        }}
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# YARDIMCI FONKSİYONLAR
# ==========================================================

def create_new_conversation():
    """Yeni bir sohbet oluşturur."""

    conversation_id = database.create_conversation(
        title="Yeni Sohbet"
    )

    st.session_state.conversation_id = conversation_id
    st.session_state.page = "chat"


def get_conversations():
    """Tüm konuşmaları güncellenme tarihine göre getirir."""

    cursor = database.connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            created_at,
            updated_at
        FROM conversations
        ORDER BY updated_at DESC
        """
    )

    return cursor.fetchall()


def get_conversation_id():
    """Aktif konuşma ID'sini oluşturur veya getirir."""

    if "conversation_id" not in st.session_state:

        latest_conversation = (
            database.get_latest_conversation()
        )

        if latest_conversation:

            st.session_state.conversation_id = (
                latest_conversation["id"]
            )

        else:

            st.session_state.conversation_id = (
                database.create_conversation(
                    title="Yeni Sohbet"
                )
            )

    return st.session_state.conversation_id


def generate_conversation_title(
    user_message: str,
) -> str:
    """İlk kullanıcı mesajından kısa sohbet başlığı oluşturur."""

    title = user_message.strip()

    if not title:
        return "Yeni Sohbet"

    title = title.replace("\n", " ")
    title = " ".join(title.split())

    if len(title) > 40:
        title = title[:40].rstrip() + "..."

    return title


def update_conversation_title_if_needed(
    conversation_id: int,
    user_message: str,
):
    """Sohbet hâlâ Yeni Sohbet ise başlığını günceller."""

    conversation = database.get_conversation(
        conversation_id
    )

    if not conversation:
        return

    current_title = conversation["title"]

    if (
        not current_title
        or current_title == "Yeni Sohbet"
    ):

        new_title = generate_conversation_title(
            user_message
        )

        database.update_conversation_title(
            conversation_id=conversation_id,
            title=new_title,
        )


def delete_conversation(
    conversation_id: int,
):
    """Konuşmayı siler."""

    database.delete_conversation(
        conversation_id
    )

    if (
        "conversation_id" in st.session_state
        and
        st.session_state.conversation_id
        == conversation_id
    ):

        del st.session_state.conversation_id


# ==========================================================
# AKTİF KONUŞMA
# ==========================================================

conversation_id = get_conversation_id()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    # ------------------------------------------------------
    # LOGO
    # ------------------------------------------------------

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=58,
        )

    st.markdown(
        """
        <div class="logo-title">
            OBEYY
        </div>

        <div class="logo-subtitle">
            Intelligent AI Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")


    # ------------------------------------------------------
    # YENİ SOHBET
    # ------------------------------------------------------

    if st.button(
        "＋  Yeni Sohbet",
        use_container_width=True,
    ):

        create_new_conversation()

        st.rerun()


    # ------------------------------------------------------
    # HAFIZA
    # ------------------------------------------------------

    if st.button(
        "🧠  Hafıza",
        use_container_width=True,
    ):

        st.session_state.page = "memory"

        st.rerun()


    # ------------------------------------------------------
    # AYARLAR
    # ------------------------------------------------------

    if st.button(
        "⚙️  Ayarlar",
        use_container_width=True,
    ):

        st.session_state.page = "settings"

        st.rerun()


    # ------------------------------------------------------
    # SOHBETE DÖN
    # ------------------------------------------------------

    if st.session_state.page != "chat":

        if st.button(
            "←  Sohbete Dön",
            use_container_width=True,
        ):

            st.session_state.page = "chat"

            st.rerun()


    st.divider()


    # ======================================================
    # SOHBETLER
    # ======================================================

    st.markdown("### Sohbetler")

    conversations = get_conversations()

    if conversations:

        for conversation in conversations:

            conversation_id_item = (
                conversation["id"]
            )

            title = conversation["title"]

            if not title:

                title = "Bir şey sor..."

            elif title == "Yeni Sohbet":

                conversation_messages = (
                    database.get_messages(
                        conversation_id_item
                    )
                )

                if not conversation_messages:

                    title = "Bir şey sor..."

            is_active = (
                conversation_id_item
                == st.session_state.conversation_id
            )

            display_title = title

            if len(display_title) > 32:

                display_title = (
                    display_title[:32]
                    + "..."
                )

            col1, col2 = st.columns(
                [5, 1],
                gap="small",
            )


            with col1:

                button_label = (
                    "● " + display_title
                    if is_active
                    else "○ " + display_title
                )

                if st.button(
                    button_label,
                    key=f"conversation_{conversation_id_item}",
                    use_container_width=True,
                ):

                    st.session_state.conversation_id = (
                        conversation_id_item
                    )

                    st.session_state.page = "chat"

                    st.rerun()


            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{conversation_id_item}",
                    help="Bu sohbeti sil",
                ):

                    delete_conversation(
                        conversation_id_item
                    )

                    remaining = get_conversations()

                    if not remaining:

                        create_new_conversation()

                    else:

                        if (
                            "conversation_id"
                            not in st.session_state
                        ):

                            st.session_state.conversation_id = (
                                remaining[0]["id"]
                            )

                    st.rerun()

    else:

        st.caption(
            "Henüz sohbet bulunmuyor."
        )


    st.divider()

    st.caption(
        "Obeyy • AI Assistant"
    )


# ==========================================================
# MOBİL ALT NAVİGASYON
# ==========================================================

st.markdown(
    f"""
    <div class="mobile-nav">

        <div class="mobile-nav-item
            {"active" if st.session_state.page == "chat" else ""}">

            <div class="mobile-nav-icon">
                💬
            </div>

            <div>
                Sohbet
            </div>

        </div>


        <div class="mobile-nav-item
            {"active" if st.session_state.page == "memory" else ""}">

            <div class="mobile-nav-icon">
                🧠
            </div>

            <div>
                Hafıza
            </div>

        </div>


        <div class="mobile-nav-item
            {"active" if st.session_state.page == "settings" else ""}">

            <div class="mobile-nav-icon">
                ⚙️
            </div>

            <div>
                Ayarlar
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# AYARLAR SAYFASI
# ==========================================================

if st.session_state.page == "settings":

    st.markdown(
        """
        <div class="obeyy-title">
            ⚙️ Ayarlar
        </div>

        <div class="obeyy-subtitle">
            Obeyy'nin görünümünü ve çalışma şeklini özelleştir.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()


    # ------------------------------------------------------
    # GÖRÜNÜM
    # ------------------------------------------------------

    st.markdown(
        "### 🎨 Görünüm"
    )

    st.markdown(
        """
        <div class="settings-card">
            <b>Arayüz teması</b><br>
            Obeyy'nin renklerini ve genel görünümünü değiştir.
        </div>
        """,
        unsafe_allow_html=True,
    )


    theme_names = [
        "Koyu",
        "Açık",
        "Mor",
        "Koyu Mor",
        "Mavi",
        "Gece Mavisi",
    ]


    selected_appearance = st.selectbox(
        "Tema",
        theme_names,
        index=theme_names.index(
            st.session_state.appearance
        ),
    )


    if selected_appearance != (
        st.session_state.appearance
    ):

        st.session_state.appearance = (
            selected_appearance
        )

        st.rerun()


    # ------------------------------------------------------
    # KOMPAKT MOD
    # ------------------------------------------------------

    st.markdown(
        "### 📐 Arayüz"
    )


    compact_value = st.toggle(
        "Kompakt sohbet görünümü",
        value=st.session_state.compact_mode,
        help="Mesaj alanını daha dar ve yoğun hale getir.",
    )


    if compact_value != st.session_state.compact_mode:

        st.session_state.compact_mode = (
            compact_value
        )

        st.rerun()


    # ------------------------------------------------------
    # LOGO
    # ------------------------------------------------------

    st.markdown(
        "### 🤖 Obeyy"
    )


    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=120,
        )

        st.caption(
            "Obeyy logosu"
        )

    else:

        st.warning(
            "Logo bulunamadı: assets/obeyy_logo.png"
        )


    st.divider()

    st.caption(
        "Obeyy • Faz 5 • Arayüz ve Kalite Kontrol"
    )

    st.stop()


# ==========================================================
# HAFIZA SAYFASI
# ==========================================================

if st.session_state.page == "memory":

    st.markdown(
        """
        <div class="obeyy-title">
            🧠 Hafıza
        </div>

        <div class="obeyy-subtitle">
            Obeyy'nin hatırladığı bilgiler
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()


    memories = database.get_memories()


    if not memories:

        st.info(
            "Obeyy'nin henüz kayıtlı bir hafızası yok."
        )

        st.caption(
            "İleride Obeyy'nin önemli bilgileri "
            "otomatik olarak hatırlamasını sağlayacağız."
        )


    else:

        st.write(
            f"Toplam {len(memories)} hafıza kaydı"
        )


        for memory in memories:

            memory_id = memory["id"]
            key = memory["key"]
            value = memory["value"]
            memory_type = memory["memory_type"]
            importance = memory["importance"]


            with st.container(border=True):

                st.markdown(
                    f"### 🧠 {key}"
                )

                st.write(
                    value
                )

                st.caption(
                    f"Tür: {memory_type}  •  "
                    f"Önem: {importance}"
                )


                col1, col2 = st.columns(
                    [1, 1]
                )


                with col1:

                    edit_key = (
                        f"edit_memory_{memory_id}"
                    )

                    if st.button(
                        "✏️ Düzenle",
                        key=edit_key,
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"editing_memory_{memory_id}"
                        ] = True

                        st.rerun()


                with col2:

                    if st.button(
                        "🗑️ Sil",
                        key=f"delete_memory_{memory_id}",
                        use_container_width=True,
                    ):

                        database.delete_memory(
                            memory_id
                        )

                        st.rerun()


                # ------------------------------------------
                # DÜZENLEME FORMU
                # ------------------------------------------

                if st.session_state.get(
                    f"editing_memory_{memory_id}",
                    False,
                ):

                    st.divider()


                    new_key = st.text_input(
                        "Anahtar",
                        value=key,
                        key=f"memory_key_{memory_id}",
                    )


                    new_value = st.text_area(
                        "Değer",
                        value=value,
                        key=f"memory_value_{memory_id}",
                    )


                    new_type = st.text_input(
                        "Tür",
                        value=memory_type,
                        key=f"memory_type_{memory_id}",
                    )


                    new_importance = st.slider(
                        "Önem",
                        min_value=0.0,
                        max_value=1.0,
                        value=float(importance),
                        step=0.1,
                        key=f"memory_importance_{memory_id}",
                    )


                    col_save, col_cancel = st.columns(
                        [1, 1]
                    )


                    with col_save:

                        if st.button(
                            "💾 Kaydet",
                            key=f"save_memory_{memory_id}",
                            use_container_width=True,
                        ):

                            database.update_memory(
                                memory_id=memory_id,
                                key=new_key,
                                value=new_value,
                                memory_type=new_type,
                                importance=new_importance,
                            )

                            st.session_state[
                                f"editing_memory_{memory_id}"
                            ] = False

                            st.rerun()


                    with col_cancel:

                        if st.button(
                            "İptal",
                            key=f"cancel_memory_{memory_id}",
                            use_container_width=True,
                        ):

                            st.session_state[
                                f"editing_memory_{memory_id}"
                            ] = False

                            st.rerun()


    st.stop()


# ==========================================================
# ANA BAŞLIK
# ==========================================================

header_col1, header_col2 = st.columns(
    [1, 10],
    vertical_alignment="center",
)


with header_col1:

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=64,
        )


with header_col2:

    st.markdown(
        """
        <div class="obeyy-title">
            OBEYY
        </div>

        <div class="obeyy-subtitle">
            Intelligent AI Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )


st.divider()


# ==========================================================
# MESAJLAR
# ==========================================================

messages = database.get_messages(
    conversation_id
)


if not messages:

    st.markdown(
        "<div style='height: 100px;'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "## ◉ Obeyy"
    )

    st.caption(
        "Sana nasıl yardımcı olabilirim?"
    )


else:

    for message in messages:

        role = message["role"]


        # --------------------------------------------------
        # KULLANICI
        # --------------------------------------------------

        if role == "user":

            with st.chat_message(
                "user",
                avatar="👤",
            ):

                st.markdown(
                    message["content"]
                )


        # --------------------------------------------------
        # OBEYY
        # --------------------------------------------------

        elif role == "assistant":

            with st.chat_message(
                "assistant",
                avatar="🤖",
            ):

                st.markdown(
                    message["content"]
                )


# ==========================================================
# CHAT INPUT
# ==========================================================

user_message = st.chat_input(
    "Obeyy'ye bir şey sor..."
)


if user_message:

    # ------------------------------------------------------
    # BAŞLIK
    # ------------------------------------------------------

    update_conversation_title_if_needed(
        conversation_id=conversation_id,
        user_message=user_message,
    )


    # ------------------------------------------------------
    # KULLANICI MESAJI
    # ------------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            user_message
        )


    # ------------------------------------------------------
    # OBEYY CEVABI
    # ------------------------------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        with st.spinner(
            "Obeyy düşünüyor..."
        ):

            try:

                response = agent.chat(
                    conversation_id=conversation_id,
                    user_message=user_message,
                )

                st.markdown(
                    response
                )


            except Exception as error:

                st.error(
                    f"Bir hata oluştu: {error}"
                )


    st.rerun()

