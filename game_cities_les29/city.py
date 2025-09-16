# city.py
from dataclasses import dataclass, field


@dataclass(order=True)
class City:
    name: str = field(compare=False)
    population: int = field(compare=True)
    subject: str = field(compare=False)
    district: str = field(compare=False)
    latitude: float = field(compare=False)
    longitude: float = field(compare=False)
    is_used: bool = field(default=False, compare=False)

    def __post_init__(self):
        """
        Валидация данных после инициализации.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Поле 'name' должно быть непустой строкой.")
        if not isinstance(self.population, int) or self.population <= 0:
            raise ValueError(
                "Поле 'population' должно быть положительным целым числом."
            )
