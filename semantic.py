import uuid
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class SemanticEntity:
    """Извлеченная сущность из текста"""
    entity_type: str
    value: str
    confidence: float

@dataclass
class SemanticResult:
    """Общий результат семантического анализа"""
    intent: str                  # Основной текст
    entities: List[SemanticEntity] # Найденные сущности
    summary: str                 # Краткая выжимка
    domain: str                  # Предметная область

class OSSemanticSubsystem:
    """Прототип системной службы семантического анализа ОС"""
    
    def __init__(self):
        self._active_sessions: Dict[str, str] = {} # session_id -> domain
        self._is_initialized = False
        
        # Моковые базы знаний для разных предметных областей
        self._knowledge_bases = {
            "medicine": ["симптом", "диагноз", "лекарство"],
            "finance": ["валюта", "транзакция", "счет"],
            "it_support": ["ошибка", "приложение", "сервер"]
        }

    def init_subsystem(self) -> bool:
        """Инициализация подсистемы (загрузка базовых библиотек ОС)"""
        print("[OS LOG] Инициализация семантической подсистемы...")
        self._is_initialized = True
        return True

    def shutdown_subsystem(self) -> None:
        """Завершение работы подсистемы"""
        self._active_sessions.clear()
        self._is_initialized = False
        print("[OS LOG] Семантическая подсистема остановлена.")

    def create_session(self, domain: str) -> Optional[str]:
        """Открытие сессии для конкретной предметной области"""
        if not self._is_initialized:
            raise RuntimeError("Подсистема не инициализирована")
            
        if domain not in self._knowledge_bases:
            print(f"[OS ERROR] Предметная область '{domain}' не найдена в системе.")
            return None
            
        session_id = str(uuid.uuid4())
        self._active_sessions[session_id] = domain
        print(f"[OS LOG] Создана сессия {session_id} для домена '{domain}'")
        return session_id

    def close_session(self, session_id: str) -> bool:
        """Закрытие сессии и освобождение памяти"""
        if session_id in self._active_sessions:
            del self._active_sessions[session_id]
            print(f"[OS LOG] Сессия {session_id} закрыта")
            return True
        return False

    def analyze_text(self, session_id: str, text: str) -> Optional[SemanticResult]:
        """Семантический анализ текста в рамках предметной области сессии"""
        if session_id not in self._active_sessions:
            print("[OS ERROR] Неверный дескриптор сессии")
            return None
            
        domain = self._active_sessions[session_id]
        print(f"[OS LOG] Анализ текста в домене '{domain}'...")
        
        # Семантический анализатор (mock)
        text_lower = text.lower()
        entities = []
        intent = "unknown"
        
        if domain == "medicine":
            if "болит" in text_lower or "температура" in text_lower:
                intent = "жалоба_пациента"
            if "голова" in text_lower:
                entities.append(SemanticEntity("локация_боли", "голова", 0.95))
            if "аспирин" in text_lower:
                entities.append(SemanticEntity("лекарство", "аспирин", 0.99))
                
        elif domain == "finance":
            if "переведи" in text_lower:
                intent = "создание_транзакции"
            if "руб" in text_lower:
                entities.append(SemanticEntity("валюта", "RUB", 1.0))
                
        return SemanticResult(
            intent=intent,
            entities=entities,
            summary=text[:20] + "..." if len(text) > 20 else text,
            domain=domain
        )

# Пример использования
if __name__ == "__main__":
    # Приложение запрашивает доступ к API
    nlp_api = OSSemanticSubsystem()
    nlp_api.init_subsystem()
    
    # Приложение создает контекст для программы
    h_session = nlp_api.create_session("medicine")
    
    if h_session:
        # Анализ текста
        user_input = "У пациента со вчерашнего дня сильно болит голова, он принял аспирин."
        result = nlp_api.analyze_text(h_session, user_input)
        
        # Обработка результата
        print("\n--- Результат для приложения ---")
        print(f"Смысл (Intent): {result.intent}")
        print(f"Сущности:")
        for ent in result.entities:
            print(f"  - {ent.entity_type}: {ent.value} (уверенность: {ent.confidence})")
        print("--------------------------------\n")
        
        # Освобождение ресурсов
        nlp_api.close_session(h_session)
        
    nlp_api.shutdown_subsystem()