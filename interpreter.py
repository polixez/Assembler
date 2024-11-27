import sys
import xml.etree.ElementTree as ET

def interpret(binary_file, memory_dump_file, mem_start, mem_end):
    memory_size = 1024
    memory = [0] * memory_size
    accumulator = 0

    # Инициализация векторов A и B
    # Вектор A (адреса 0-3)
    memory[0] = 10
    memory[1] = 20
    memory[2] = 30
    memory[3] = 40

    # Вектор B (адреса 4-7)
    memory[4] = 10
    memory[5] = 25
    memory[6] = 35
    memory[7] = 40

    # Загрузка бинарного файла
    with open(binary_file, 'rb') as f:
        binary_code = f.read()

    # Парсинг инструкций
    instructions = []
    for i in range(0, len(binary_code), 4):
        instr = int.from_bytes(binary_code[i:i+4], byteorder='little')
        instructions.append(instr)

    pc = 0  # Счетчик команд

    while pc < len(instructions):
        instr = instructions[pc]
        opcode = instr & 0x7F
        operand = instr >> 7

        if opcode == 12:  # LDC
            accumulator = operand
        elif opcode == 58:  # LD
            addr = (accumulator + operand) % memory_size
            accumulator = memory[addr]
        elif opcode == 24:  # ST
            addr = operand % memory_size
            memory[addr] = accumulator
        elif opcode == 90:  # EQ
            addr = operand % memory_size
            accumulator = int(accumulator == memory[addr])
        else:
            raise ValueError(f"Неизвестный opcode {opcode}")

        pc += 1

    # Создание дампа памяти
    root = ET.Element('MemoryDump')
    for addr in range(mem_start, mem_end + 1):
        mem_elem = ET.SubElement(root, 'Memory')
        ET.SubElement(mem_elem, 'Address').text = str(addr)
        ET.SubElement(mem_elem, 'Value').text = str(memory[addr])

    tree = ET.ElementTree(root)
    tree.write(memory_dump_file)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Использование: python interpreter.py <binary_file> <memory_dump_file> <mem_start> <mem_end>")
        sys.exit(1)
    binary_file = sys.argv[1]
    memory_dump_file = sys.argv[2]
    mem_start = int(sys.argv[3])
    mem_end = int(sys.argv[4])
    interpret(binary_file, memory_dump_file, mem_start, mem_end)
