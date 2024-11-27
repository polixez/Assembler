import sys
import os

def build_project():
    # Пути к файлам
    source_file = 'test_files/test_source.asm'
    binary_file = 'test_files/binary.bin'
    log_file = 'test_files/log.xml'
    memory_dump_file = 'test_files/result.xml'
    mem_start = 0
    mem_end = 7

    # Шаг 1: Ассемблирование исходного кода
    print("Ассемблирование исходного кода...")
    os.system(f'python assembler.py {source_file} {binary_file} {log_file}')

    # Шаг 2: Запуск интерпретатора
    print("Выполнение интерпретатора...")
    os.system(f'python interpreter.py {binary_file} {memory_dump_file} {mem_start} {mem_end}')

    print("Сборка и выполнение завершены.")

if __name__ == "__main__":
    build_project()
