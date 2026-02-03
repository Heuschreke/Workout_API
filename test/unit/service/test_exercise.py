from model.muscle_group import Exercise
from service import exercise as code


sample = Exercise(name="Йети", description="Ходьба с высокоподнятыми коленями", muscle_group="Ноги")
sample2 = Exercise(name="Выпады со штангой",
             description="Положите штангу на плечи, сделайте широкий шаг вперед. Опустите корпус до образования в коленях углов 90°, затем оттолкнитесь передней ногой, чтобы вернуться в стойку.",
             muscle_group="Ноги")

def test_create():
    resp = code.create(sample)
    assert resp == sample

def test_get_exists():
    resp = code.get_one("Выпады со штангой")
    assert resp == sample2

def test_get_missing():
    resp = code.get_one("boxturtle")
    assert resp is None

# test/unit/service/test_exercise.py
# from model.muscle_group import Exercise
# from service import exercise as code

# print("=== НАЧАЛО ТЕСТОВ ===")

# # 1. Создаем упражнение
# print("\n1. Создаем упражнение 'Приседания'")
# sample = Exercise(
#     name="Приседания",
#     description="Для ног",
#     muscle_group="Ноги"
# )

# # 2. Сохраняем его
# print(f"   Сохраняем: {sample.name}")
# saved = code.create(sample)
# print(f"   Сохранено: {saved.name}")

# # 3. Пытаемся получить ТО ЖЕ САМОЕ упражнение
# print("\n2. Получаем упражнение 'Приседания'")
# found = code.get_one("Приседания")
# if found:
#     print(f"   Найдено: {found.name}")
#     print(f"   Совпадает с сохраненным? {found == sample}")
# else:
#     print("   ❌ НЕ НАЙДЕНО!")

# # 4. Пытаемся получить НЕСУЩЕСТВУЮЩЕЕ
# print("\n3. Получаем упражнение 'Несуществующее'")
# not_found = code.get_one("Несуществующее")
# print(f"   Результат: {not_found}")
# print(f"   Это None? {not_found is None}")

# print("\n=== КОНЕЦ ТЕСТОВ ===")

# # Теперь тесты
# def test_create():
#     """Проверяем создание"""
#     assert saved == sample
#     print("✅ test_create пройден")

# def test_get_exists():
#     """Проверяем получение существующего"""
#     assert found == sample
#     print("✅ test_get_exists пройден")

# def test_get_missing():
#     """Проверяем получение отсутствующего"""
#     assert not_found is None
#     print("✅ test_get_missing пройден")