import unittest
import os
import subprocess
import shutil
import sys
import xml.etree.ElementTree as ET


class TestAssembler(unittest.TestCase):
    def setUp(self):
        # Путь к ассемблеру
        self.assembler = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assembler.py'))

        # Папки тестов и ожидаемых результатов
        self.test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_files'))
        self.expected_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'expected'))

    def run_assembler(self, test_case):
        source_file = os.path.join(self.test_dir, f'{test_case}.asm')
        binary_file = os.path.join(self.test_dir, f'{test_case}_binary.bin')
        log_file = os.path.join(self.test_dir, f'{test_case}_log.xml')

        # Удаляем предыдущие результаты, если они есть
        for file in [binary_file, log_file]:
            if os.path.exists(file):
                os.remove(file)

        # Запуск ассемблера
        result = subprocess.run([sys.executable, self.assembler, source_file, binary_file, log_file],
                                capture_output=True, text=True)

        # Проверка успешного выполнения
        self.assertEqual(result.returncode, 0, msg=f'Ассемблер завершился с ошибкой: {result.stderr}')

        # Проверка существования файлов
        self.assertTrue(os.path.exists(binary_file), msg='Бинарный файл не создан.')
        self.assertTrue(os.path.exists(log_file), msg='Лог-файл не создан.')

        # Сравнение бинарных файлов
        expected_binary = os.path.join(self.expected_dir, f'{test_case}_binary.bin')
        with open(binary_file, 'rb') as f_actual, open(expected_binary, 'rb') as f_expected:
            actual = f_actual.read()
            expected = f_expected.read()
            self.assertEqual(actual, expected, msg=f'Бинарные файлы для {test_case} не совпадают.')

        # Сравнение лог-файлов
        expected_log = os.path.join(self.expected_dir, f'{test_case}_log.xml')
        tree_actual = ET.parse(log_file)
        tree_expected = ET.parse(expected_log)
        self.assertEqual(ET.tostring(tree_actual.getroot()), ET.tostring(tree_expected.getroot()),
                         msg=f'Лог-файлы для {test_case} не совпадают.')

    def test_assembler_case_1(self):
        self.run_assembler('test_case_1')

    def test_assembler_case_2(self):
        self.run_assembler('test_case_2')

    def test_assembler_case_3(self):
        self.run_assembler('test_case_3')

    # Добавьте дополнительные тесты по мере необходимости


if __name__ == '__main__':
    unittest.main()
