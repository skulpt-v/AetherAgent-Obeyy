import logging
import re

from memory import Database
from core.context import ContextManager
from config.prompts import build_prompt, build_react_prompt
from llm.client import LLMClient


# ==========================================================
# LOGGING
# ==========================================================

logger = logging.getLogger("AetherAgent")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(
        "logs/agent.log",
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


# ==========================================================
# AETHER AGENT
# ==========================================================

class AetherAgent:
    """AetherAgent'ın ana karar ve çalışma mekanizması."""

    def __init__(self, database: Database):
        self.database = database
        self.context_manager = ContextManager(database)
        self.llm = LLMClient()

        # Agent'ın kullanabileceği araçlar.
        self.tools = {}

        logger.info("AetherAgent başlatıldı.")

    # ======================================================
    # REQUEST
    # ======================================================

    def build_request(
        self,
        conversation_id: int,
        user_message: str,
        context_limit: int = 20
    ) -> str:
        """
        Kullanıcı mesajı ve konuşma geçmişinden
        modele gönderilecek isteği oluşturur.
        """

        context = self.context_manager.build_context(
            conversation_id,
            limit=context_limit
        )

        return build_prompt(
            user_message=user_message,
            context=context
        )

    # ======================================================
    # MEMORY
    # ======================================================

    def save_user_message(
        self,
        conversation_id: int,
        content: str
    ) -> int:
        """Kullanıcı mesajını veritabanına kaydeder."""

        return self.database.add_message(
            conversation_id=conversation_id,
            role="user",
            content=content
        )

    def save_assistant_message(
        self,
        conversation_id: int,
        content: str
    ) -> int:
        """Agent cevabını veritabanına kaydeder."""

        return self.database.add_message(
            conversation_id=conversation_id,
            role="assistant",
            content=content
        )

    # ======================================================
    # TOOL SYSTEM
    # ======================================================

    def register_tool(
        self,
        name: str,
        tool
    ) -> None:
        """Agent'a yeni bir araç kaydeder."""

        if not name:
            raise ValueError(
                "Araç adı boş olamaz."
            )

        if not callable(tool):
            raise TypeError(
                f"'{name}' aracı çağrılabilir "
                "bir fonksiyon olmalıdır."
            )

        self.tools[name] = tool

        logger.info(
            "Tool kaydedildi: %s",
            name
        )

    def execute_tool(
        self,
        name: str,
        **kwargs
    ):
        """Kayıtlı bir aracı çalıştırır."""

        if name not in self.tools:
            raise ValueError(
                f"'{name}' isimli araç kayıtlı değil."
            )

        tool = self.tools[name]

        logger.info(
            "Tool çalıştırılıyor: %s | args=%s",
            name,
            kwargs
        )

        result = tool(**kwargs)

        logger.info(
            "Tool tamamlandı: %s",
            name
        )

        return result

    def get_tool_descriptions(self) -> str:
        """
        Kayıtlı araçların isimlerini ve açıklamalarını
        modele gönderilecek metne dönüştürür.
        """

        if not self.tools:
            return "Kullanılabilir araç yok."

        descriptions = []

        for name, tool in self.tools.items():

            description = getattr(
                tool,
                "__doc__",
                None
            )

            if description:
                description = description.strip()
            else:
                description = (
                    "Açıklama belirtilmemiş."
                )

            descriptions.append(
                f"- {name}: {description}"
            )

        return "\n".join(descriptions)

    # ======================================================
    # CALCULATOR NORMALIZATION
    # ======================================================

    def _normalize_calculator_expression(
        self,
        expression: str
    ) -> str:
        """
        Gemini'nin doğal dilde verdiği matematik ifadesini
        Calculator'ın anlayabileceği ifadeye dönüştürür.
        """

        if not expression:
            return expression

        text = expression.lower().strip()

        text = text.replace("×", "*")
        text = text.replace("÷", "/")
        text = text.replace("−", "-")

        # Türkçe ondalık ayracı.
        text = re.sub(
            r"(\d),(\d)",
            r"\1.\2",
            text
        )

        # Zaten doğrudan matematikse bozma.
        if re.fullmatch(
            r"[0-9+\-*/%.()\s]+",
            text
        ):
            return text.strip()

        operator_symbol = None

        if re.search(
            r"\b(toplam|toplamı|topla|artı|ekle)\b",
            text
        ):
            operator_symbol = "+"

        elif re.search(
            r"\b(çarpım|çarpımı|çarpı|kere)\b",
            text
        ):
            operator_symbol = "*"

        elif re.search(
            r"\b(bölüm|bölümü|bölü)\b",
            text
        ):
            operator_symbol = "/"

        elif re.search(
            r"\b(fark|farkı|çıkar|çıkarma|eksilt)\b",
            text
        ):
            operator_symbol = "-"

        numbers = re.findall(
            r"\d+(?:\.\d+)?",
            text
        )

        if len(numbers) >= 2 and operator_symbol:

            first = numbers[0]
            second = numbers[1]

            return (
                f"{first} "
                f"{operator_symbol} "
                f"{second}"
            )

        # Doğal dili temizle.
        text = re.sub(
            r"\b(kaç|nedir|hesapla|sonuç|sonucu)\b",
            " ",
            text
        )

        text = re.sub(
            r"[^0-9+\-*/%.() ]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return text

    def _prepare_tool_args(
        self,
        tool_name: str,
        args: dict
    ) -> dict:
        """Tool'a gönderilecek argümanları hazırlar."""

        prepared_args = dict(args)

        if tool_name == "calculator":

            if "expression" in prepared_args:

                prepared_args["expression"] = (
                    self._normalize_calculator_expression(
                        prepared_args["expression"]
                    )
                )

        return prepared_args

    # ======================================================
    # REACT PARSER
    # ======================================================

    def parse_react_response(
        self,
        response: str
    ) -> dict:
        """
        Gemini'nin ReAct cevabını Python sözlüğüne dönüştürür.
        """

        result = {
            "action": "none",
            "tool": None,
            "args": {}
        }

        if not response:
            return result

        action_match = re.search(
            r"ACTION:\s*(\w+)",
            response,
            re.IGNORECASE
        )

        if not action_match:
            logger.info(
                "ReAct cevabında ACTION bulunamadı."
            )
            return result

        action = action_match.group(1).lower()

        result["action"] = action

        if action != "tool":
            return result

        tool_match = re.search(
            r"TOOL:\s*([^\s]+)",
            response,
            re.IGNORECASE
        )

        if tool_match:

            result["tool"] = (
                tool_match.group(1).strip()
            )

        args_match = re.search(
            r"ARGS:\s*(.*)",
            response,
            re.IGNORECASE
        )

        if args_match:

            args_text = (
                args_match.group(1).strip()
            )

            if args_text:

                result["args"] = {
                    "expression": args_text
                }

        if result["tool"]:

            result["args"] = (
                self._prepare_tool_args(
                    result["tool"],
                    result["args"]
                )
            )

        logger.info(
            "ReAct kararı: action=%s | tool=%s | args=%s",
            result["action"],
            result["tool"],
            result["args"]
        )

        return result

    # ======================================================
    # ACTION DECISION
    # ======================================================

    def decide_action(
        self,
        conversation_id: int,
        user_message: str,
        context_limit: int = 20
    ) -> dict:
        """Gemini'den ReAct formatında eylem kararı alır."""

        context = (
            self.context_manager.build_context(
                conversation_id,
                limit=context_limit
            )
        )

        tool_descriptions = (
            self.get_tool_descriptions()
        )

        prompt = build_react_prompt(
            user_message=user_message,
            context=context,
            tool_descriptions=tool_descriptions
        )

        logger.info(
            "ReAct karar isteği gönderiliyor."
        )

        response = self.llm.ask(
            prompt=prompt
        )

        return self.parse_react_response(
            response
        )

    # ======================================================
    # NORMAL RESPONSE
    # ======================================================

    def generate_response(
        self,
        conversation_id: int,
        user_message: str,
        context_limit: int = 20
    ) -> str:
        """Kullanıcı mesajından normal LLM cevabı üretir."""

        prompt = self.build_request(
            conversation_id=conversation_id,
            user_message=user_message,
            context_limit=context_limit
        )

        logger.info(
            "Normal LLM cevabı oluşturuluyor."
        )

        return self.llm.ask(
            prompt=prompt
        )

    # ======================================================
    # ERROR RESPONSE
    # ======================================================

    def generate_error_response(
        self,
        user_message: str,
        tool_name: str,
        error
    ) -> str:
        """Tool hatası durumunda kullanıcıya doğal cevap üretir."""

        logger.error(
            "Tool hatası: %s | %s",
            tool_name,
            error
        )

        error_prompt = f"""
Kullanıcı şu soruyu sordu:

{user_message}

Kullanılmak istenen araç:

{tool_name}

Araç şu hatayı verdi:

{error}

Kullanıcıya doğal ve kısa bir cevap ver.

Teknik hata ayrıntılarını gereksiz yere anlatma.
Hesaplama yapılamadıysa bunu dürüstçe belirt.
"""

        return self.llm.ask(
            prompt=error_prompt
        )

    # ======================================================
    # TOOL RESULT SYNTHESIS
    # ======================================================

    def synthesize_tool_result(
        self,
        user_message: str,
        tool_name: str,
        tool_args: dict,
        tool_result
    ) -> str:
        """Tool sonucunu kullanıcıya doğal cevap hâline getirir."""

        final_prompt = f"""
Kullanıcının mesajı:

{user_message}

Kullanılan araç:

{tool_name}

Aracın girdisi:

{tool_args}

Aracın sonucu:

{tool_result}

Yukarıdaki araç sonucunu kullanarak
kullanıcıya doğrudan ve doğal bir cevap ver.

Araç sonucunu değiştirme.
Yeni bir sonuç uydurma.
Gereksiz teknik detay verme.

Kullanıcı sadece sonucu istiyorsa
kısa ve net cevap ver.
"""

        return self.llm.ask(
            prompt=final_prompt
        )

    # ======================================================
    # CHAT
    # ======================================================

    def chat(
        self,
        conversation_id: int,
        user_message: str,
        context_limit: int = 20
    ) -> str:
        """
        Kullanıcı mesajını işler.

        Akış:

        1. Kullanıcı mesajını kaydet.
        2. ReAct ile araç gerekip gerekmediğine karar ver.
        3. Gerekirse aracı çalıştır.
        4. Sonucu LLM'ye gönder.
        5. Nihai cevabı kaydet.
        """

        logger.info(
            "Yeni mesaj alındı | conversation=%s",
            conversation_id
        )

        # --------------------------------------------------
        # 1. USER MESSAGE
        # --------------------------------------------------

        self.save_user_message(
            conversation_id=conversation_id,
            content=user_message
        )

        # --------------------------------------------------
        # 2. REACT DECISION
        # --------------------------------------------------

        try:

            action = self.decide_action(
                conversation_id=conversation_id,
                user_message=user_message,
                context_limit=context_limit
            )

        except Exception as error:

            logger.exception(
                "ReAct karar aşamasında hata oluştu."
            )

            response = self.generate_response(
                conversation_id=conversation_id,
                user_message=user_message,
                context_limit=context_limit
            )

            self.save_assistant_message(
                conversation_id=conversation_id,
                content=response
            )

            return response

        # --------------------------------------------------
        # 3. NORMAL RESPONSE
        # --------------------------------------------------

        if action["action"] != "tool":

            logger.info(
                "Tool kullanılmadan cevap üretilecek."
            )

            response = self.generate_response(
                conversation_id=conversation_id,
                user_message=user_message,
                context_limit=context_limit
            )

            self.save_assistant_message(
                conversation_id=conversation_id,
                content=response
            )

            return response

        # --------------------------------------------------
        # 4. TOOL VALIDATION
        # --------------------------------------------------

        if not action["tool"]:

            logger.warning(
                "ReAct tool istedi ancak tool adı bulunamadı."
            )

            response = self.generate_response(
                conversation_id=conversation_id,
                user_message=user_message,
                context_limit=context_limit
            )

            self.save_assistant_message(
                conversation_id=conversation_id,
                content=response
            )

            return response

        tool_name = action["tool"]
        tool_args = action["args"]

        # --------------------------------------------------
        # 5. TOOL EXECUTION
        # --------------------------------------------------

        try:

            tool_result = self.execute_tool(
                tool_name,
                **tool_args
            )

        except Exception as error:

            response = self.generate_error_response(
                user_message=user_message,
                tool_name=tool_name,
                error=error
            )

            self.save_assistant_message(
                conversation_id=conversation_id,
                content=response
            )

            return response

        # --------------------------------------------------
        # 6. TOOL RESULT
        # --------------------------------------------------

        try:

            response = self.synthesize_tool_result(
                user_message=user_message,
                tool_name=tool_name,
                tool_args=tool_args,
                tool_result=tool_result
            )

        except Exception as error:

            logger.exception(
                "Tool sonucu sentezlenirken hata oluştu."
            )

            response = (
                f"İşlem tamamlandı fakat sonucu "
                f"hazırlarken bir hata oluştu: {error}"
            )

        # --------------------------------------------------
        # 7. SAVE RESPONSE
        # --------------------------------------------------

        self.save_assistant_message(
            conversation_id=conversation_id,
            content=response
        )

        logger.info(
            "Mesaj işlemi tamamlandı | conversation=%s",
            conversation_id
        )

        return response

