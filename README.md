# OBEYY

**Intelligent AI Assistant**

---

# 🇹🇷 Türkçe

OBEYY; **Groq API, kalıcı hafıza, araç kullanımı ve ReAct tabanlı ajan mimarisi** ile çalışan, Python ile geliştirilmiş modüler bir kişisel yapay zekâ asistanıdır.

## 🌐 Canlı Demo

**OBEYY'yi çevrimiçi deneyin:**

https://obeyyai.streamlit.app

## ✨ Özellikler

* 🤖 Yapay zekâ destekli sohbet
* 🧠 Kalıcı konuşma hafızası
* 💾 SQLite tabanlı veri yönetimi
* 🛠️ ReAct tabanlı araç kullanımı
* 🧮 Güvenli matematik hesaplama
* 🎨 Farklı arayüz temaları
* 💬 Kompakt sohbet modu
* 📜 Sohbet geçmişi
* 🧠 Hafıza görüntüleme ve yönetme
* 🌐 Streamlit web arayüzü
* 💻 Terminal arayüzü
* 📝 Loglama ve hata takibi
* 🧩 Modüler ajan mimarisi

## 🛠️ Kullanılan Teknolojiler

* Python
* Groq API
* Streamlit
* SQLite
* Rich
* ReAct Agent Architecture

## 📁 Proje Yapısı

```text
AetherAgent/
├── config/
│   ├── prompts.py
│   └── settings.py
├── core/
│   ├── agent.py
│   └── context.py
├── memory/
├── tools/
├── llm/
│   └── client.py
├── ui/
│   └── web_app.py
├── tests/
├── logs/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Kurulum

### 1. Repoyu klonlayın

```bash
git clone https://github.com/YOUR_USERNAME/AetherAgent.git
cd AetherAgent
```

### 2. Gerekli paketleri yükleyin

```bash
pip install -r requirements.txt
```

### 3. API anahtarını ayarlayın

Projenin ana dizininde `.env` dosyası oluşturun:

```env
GROQ_API_KEY=your_api_key
```

### 4. Uygulamayı başlatın

```bash
streamlit run ui/web_app.py
```

## ☁️ Streamlit Cloud

OBEYY, Streamlit Cloud üzerinde çalışacak şekilde yapılandırılmıştır.

1. Projeyi GitHub'a yükleyin.
2. Streamlit Cloud'da yeni bir uygulama oluşturun.
3. Repository'yi seçin.
4. Ana dosya olarak `ui/web_app.py` seçin.
5. Streamlit Secrets bölümüne API anahtarınızı ekleyin:

```toml
GROQ_API_KEY = "your_api_key"
```

6. Uygulamayı deploy edin.

## 🧠 Mimari

OBEYY modüler bir ajan mimarisi kullanır.

Temel çalışma akışı:

```text
Kullanıcı
   ↓
Streamlit / Terminal Arayüzü
   ↓
AetherAgent
   ↓
Context & Memory
   ↓
ReAct Kararı
   ↓
Tool / LLM
   ↓
Yanıt
   ↓
Kalıcı Hafıza
```

Ajan, kullanıcının isteğine göre bir araç gerekip gerekmediğine karar verebilir. Araç kullanıldığında araç sonucu tekrar LLM'ye gönderilir ve kullanıcıya doğal bir yanıt oluşturulur.

## 🧮 Araç Sistemi

OBEYY modüler bir araç sistemi kullanır.

Yeni araçlar ajan sistemine dinamik olarak eklenebilir.

Örneğin:

```python
agent.register_tool(
    "calculator",
    calculator_function
)
```

Bu yapı sayesinde yeni özellikler, çekirdek ajan mimarisi değiştirilmeden sisteme eklenebilir.

## 💾 Hafıza Sistemi

OBEYY, kalıcı konuşma verilerini SQLite kullanarak saklar.

Hafıza sistemi:

* Kullanıcı mesajlarını kaydeder
* Asistan yanıtlarını kaydeder
* Önceki konuşmaları getirir
* LLM için bağlam oluşturur
* Konuşma geçmişinin yönetilmesini sağlar

## 🔐 Güvenlik

API anahtarları ve diğer hassas bilgiler kesinlikle GitHub'a yüklenmemelidir.

`.gitignore` içerisinde aşağıdaki dosyaların hariç tutulması önerilir:

```text
.env
*.db
*.sqlite
*.sqlite3
logs/
__pycache__/
```

API anahtarları yalnızca environment variables veya Streamlit Secrets üzerinden saklanmalıdır.

## 📋 Gereksinimler

Python bağımlılıkları `requirements.txt` içerisinde bulunmaktadır.

Kurulum:

```bash
pip install -r requirements.txt
```

## 📄 Lisans

Bu proje **MIT License** altında yayınlanmıştır.

---

# 🇬🇧 English

OBEYY is a **modular personal AI assistant** built with Python, powered by the **Groq API**, persistent memory, tool usage, and a ReAct-based agent architecture.

## 🌐 Live Demo

**Try OBEYY online:**

https://obeyyai.streamlit.app

## ✨ Features

* 🤖 AI-powered conversations
* 🧠 Persistent conversation memory
* 💾 SQLite-based data management
* 🛠️ ReAct-based tool usage
* 🧮 Secure mathematical calculations
* 🎨 Multiple interface themes
* 💬 Compact chat mode
* 📜 Conversation history
* 🧠 Memory management
* 🌐 Streamlit web interface
* 💻 Terminal interface
* 📝 Logging and error tracking
* 🧩 Modular agent architecture

## 🛠️ Technologies

* Python
* Groq API
* Streamlit
* SQLite
* Rich
* ReAct Agent Architecture

## 📁 Project Structure

```text
AetherAgent/
├── config/
│   ├── prompts.py
│   └── settings.py
├── core/
│   ├── agent.py
│   └── context.py
├── memory/
├── tools/
├── llm/
│   └── client.py
├── ui/
│   └── web_app.py
├── tests/
├── logs/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AetherAgent.git
cd AetherAgent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key
```

### 4. Run the application

```bash
streamlit run ui/web_app.py
```

## ☁️ Streamlit Cloud Deployment

OBEYY is configured to run on Streamlit Cloud.

1. Push the project to GitHub.
2. Create a new Streamlit application.
3. Select the repository.
4. Set `ui/web_app.py` as the main file.
5. Add your API key to Streamlit Secrets:

```toml
GROQ_API_KEY = "your_api_key"
```

6. Deploy the application.

## 🧠 Architecture

OBEYY uses a modular agent architecture.

The general workflow is:

```text
User
  ↓
Streamlit / Terminal UI
  ↓
AetherAgent
  ↓
Context & Memory
  ↓
ReAct Decision
  ↓
Tool / LLM
  ↓
Response
  ↓
Persistent Memory
```

The agent can decide whether a tool is required for a request. When a tool is used, its result is passed back to the LLM to generate a natural response.

## 🧮 Tool System

OBEYY supports a modular tool architecture.

New tools can be dynamically registered with the agent.

Example:

```python
agent.register_tool(
    "calculator",
    calculator_function
)
```

This allows new capabilities to be added without changing the core agent architecture.

## 💾 Memory System

OBEYY uses SQLite for persistent conversation storage.

The memory system can:

* Store user messages
* Store assistant responses
* Retrieve previous conversations
* Build context for the LLM
* Manage conversation history

## 🔐 Security

API keys and other sensitive information should never be committed to GitHub.

The following should be excluded through `.gitignore`:

```text
.env
*.db
*.sqlite
*.sqlite3
logs/
__pycache__/
```

API keys should only be stored using environment variables or Streamlit Secrets.

## 📋 Requirements

Python dependencies are listed in:

```text
requirements.txt
```

Install them with:

```bash
pip install -r requirements.txt
```

## 📄 License

This project is released under the **MIT License**.

---

**OBEYY — A modular AI assistant built for experimentation, learning, and extensibility.**
