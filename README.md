# OBEYY

**Intelligent AI Assistant**

Obeyy, hafıza sistemi, araç kullanımı ve Gemini tabanlı yapay zekâ ile çalışan kişisel bir AI assistant projesidir.

## Özellikler

* Yapay zekâ destekli sohbet
* Kalıcı konuşma hafızası
* SQLite tabanlı veri yönetimi
* ReAct tabanlı araç kullanımı
* Güvenli matematik hesaplama
* Farklı arayüz temaları
* Kompakt sohbet modu
* Sohbet geçmişi
* Hafıza görüntüleme ve düzenleme
* Streamlit tabanlı web arayüzü
* Terminal arayüzü
* Hata ve çalışma günlükleri

## Teknolojiler

* Python
* Google Gemini API
* Streamlit
* SQLite
* Rich
* ReAct Agent Architecture

## Proje Yapısı

```text
AetherAgent/
├── config/
├── core/
├── memory/
├── tools/
├── llm/
├── ui/
├── tests/
├── logs/
├── main.py
├── requirements.txt
└── README.md
```

## Kurulum

Projeyi klonlayın:

```bash
git clone https://github.com/KULLANICI_ADIN/AetherAgent.git
cd AetherAgent
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

`.env` dosyanızı oluşturun ve Gemini API anahtarınızı ekleyin.

```env
GEMINI_API_KEY=your_api_key
```

Uygulamayı başlatmak için:

```bash
streamlit run ui/web_app.py
```

## Güvenlik

API anahtarları ve diğer hassas bilgiler GitHub'a yüklenmemelidir.

`.gitignore` içerisinde `.env`, veritabanı dosyaları ve log dosyalarının hariç tutulması önerilir.

---

# OBEYY

**Intelligent AI Assistant**

Obeyy is a personal AI assistant project powered by Gemini, persistent memory, tool usage, and a modular agent architecture.

## Features

* AI-powered conversations
* Persistent conversation memory
* SQLite-based data management
* ReAct-based tool usage
* Secure mathematical calculations
* Multiple interface themes
* Compact chat mode
* Conversation history
* Memory management
* Streamlit web interface
* Terminal interface
* Logging and error tracking

## Technologies

* Python
* Google Gemini API
* Streamlit
* SQLite
* Rich
* ReAct Agent Architecture

## Project Structure

```text
AetherAgent/
├── config/
├── core/
├── memory/
├── tools/
├── llm/
├── ui/
├── tests/
├── logs/
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/AetherAgent.git
cd AetherAgent
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key
```

Run the application:

```bash
streamlit run ui/web_app.py
```

## Security

API keys and other sensitive information should never be committed to GitHub.

Make sure `.env`, database files, logs, and other private files are included in `.gitignore`.

## License

This project is released under the MIT License.
