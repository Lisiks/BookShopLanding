import enum

class OrderStatuses(enum.Enum):
    InAssembly = "В сборке"
    Assembled = "Собран"
    Received = "Получен"
    Canceled = "Отменен"