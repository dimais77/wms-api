from enum import Enum


class OrderStatusEnum(str, Enum):
    draft = "черновик"
    pending = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"
