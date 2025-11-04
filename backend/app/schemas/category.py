# from pydantic import BaseModel, Field
# from typing import List, Dict

# # --- Pydantic Схема Категории ---
# class CategoryBase(BaseModel):
#     name: str = Field(..., max_length=50)

# class Category(CategoryBase):
#     id: int

#     class Config:
#         from_attributes = True

# # -----------------------------------------------------------------
# # --- ЖЕСТКО ЗАДАННЫЙ СПИСОК КАТЕГОРИЙ (ЗАМЕНА БАЗЫ ДАННЫХ) ---
# # -----------------------------------------------------------------

# FIXED_CATEGORIES: List[Category] = [
#     Category(id=1, name="iPhone"),
#     Category(id=2, name="iPad"),
#     Category(id=3, name="Apple Watch"),
#     Category(id=4, name="AirPods"),
#     Category(id=5, name="Macbook"),
#     Category(id=6, name="Красота и уход"),
#     Category(id=7, name="Аксессуары"),
#     Category(id=8, name="Б/У товары"),
# ]

# # Удобный словарь для быстрого поиска категории по ID
# CATEGORY_MAP: Dict[int, Category] = {cat.id: cat for cat in FIXED_CATEGORIES}

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

# --- Pydantic Схема Категории (с поддержкой вложенности) ---

class Category(BaseModel):
    id: int
    name: str = Field(..., max_length=50)
    # 🌟 НОВОЕ ПОЛЕ: Список дочерних категорий
    subcategories: List['Category'] = []

    class Config:
        from_attributes = True

# 🌟 ВАЖНО: Обновляем ссылки для Pydantic, чтобы он понял 'Category' внутри 'Category'
Category.model_rebuild()

# -----------------------------------------------------------------
# --- 🌟 НОВЫЙ ЖЕСТКО ЗАДАННЫЙ СПИСОК КАТЕГОРИЙ (с вложенностью) ---
# -----------------------------------------------------------------

FIXED_CATEGORIES: List[Category] = [
    Category(id=1, name="iPhone"),
    Category(id=2, name="iPad"),
    Category(id=3, name="Apple Watch"),
    Category(id=4, name="AirPods"),
    Category(id=5, name="Macbook"),
    Category(
        id=7, 
        name="Аксессуары", # Старая категория (ID 7)
        subcategories=[
            Category(id=701, name="Зарядные устройства"),
            Category(id=702, name="Накопители"),
            Category(id=703, name="Apple Pencil"),
        ]
    ),
    Category(id=8, name="Б/У товары"), # Старая категория (ID 8)
    Category(
        id=9, # Новая категория (ID 9)
        name="Прочее", # Вместо "Красота и уход"
        subcategories=[
            Category(id=901, name="Dyson"),
            Category(id=902, name="Sony"),
            Category(id=903, name="Samsung"),
        ]
    ),
]

# --- 🌟 НОВЫЙ КОД: "Расплющенный" словарь ID -> Category ---
# Это нужно, чтобы ваш код, который ищет имя категории по ID, 
# мог находить в том числе и вложенные категории.

def flatten_categories(categories: List[Category]) -> Dict[int, Category]:
    """
    Рекурсивно "расплющивает" дерево категорий в плоский словарь {id: Category}.
    """
    category_map = {}
    for cat in categories:
        # Копируем категорию без подкатегорий, чтобы не было путаницы
        category_map[cat.id] = Category(id=cat.id, name=cat.name) 
        
        # Рекурсивно добавляем детей
        if cat.subcategories:
            flat_children = flatten_categories(cat.subcategories)
            category_map.update(flat_children)
    return category_map

# Этот словарь может использоваться бэкендом для быстрой проверки ID
CATEGORY_MAP: Dict[int, Category] = flatten_categories(FIXED_CATEGORIES)