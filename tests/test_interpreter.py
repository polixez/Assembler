import unittest
import os
import subprocess
import shutil
import sys
import xml.etree.ElementTree as ET


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        # Путь к интерпретатору
        self.interpreter = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'interpreter.py'))

        # Папки тестов и ожидаемых результатов
        self.test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_files'))
        self.expected_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'expected'))

        # Инициализация памяти (можно расширить при необходимости)
        self.initial_memory = {
            0: 10,
            1: 20,
            2: 30,
            3: 40,
            4: 10,
            5: 25,
            6: 35,
            7: 40
        }

        # Создаем начальную инициализацию памяти
        # Здесь предполагается, что интерпретатор инициализирует память внутри себя
        # Если нужно, можно модифицировать интерпретатор для загрузки начальной памяти из файла

    def run_interpreter(self, test_case):
        binary_file = os.path.join(self.test_dir, f'{test_case}_binary.bin')
        memory_dump_file = os.path.join(self.test_dir, f'{test_case}_result.xml')
        mem_start = '0'
        mem_end = '7'

        # Удаляем предыдущие результаты, если они есть
        if os.path.exists(memory_dump_file):
            os.remove(memory_dump_file)

        # Запуск интерпретатора
        result = subprocess.run([sys.executable, self.interpreter, binary_file, memory_dump_file, mem_start, mem_end],
                                capture_output=True, text=True)

        # Проверка успешного выполнения
        self.assertEqual(result.returncode, 0, msg=f'Интерпретатор завершился с ошибкой: {result.stderr}')

        # Проверка существования файла дампа памяти
        self.assertTrue(os.path.exists(memory_dump_file), msg='Файл дампа памяти не создан.')

        # Сравнение дампов памяти
        expected_result = os.path.join(self.expected_dir, f'{test_case}_result.xml')
        tree_actual = ET.parse(memory_dump_file)
        tree_expected = ET.parse(expected_result)
        self.assertEqual(ET.tostring(tree_actual.getroot()), ET.tostring(tree_expected.getroot()),
                         msg=f'Файл дампа памяти для {test_case} не совпадает.')

    def test_interpreter_case_1(self):
        self.run_interpreter('test_case_1')

    def test_interpreter_case_2(self):
        self.run_interpreter('test_case_2')

    def test_interpreter_case_3(self):
        self.run_interpreter('test_case_3')

    # Добавьте дополнительные тесты по мере необходимости


if __name__ == '__main__':
    unittest.main()
