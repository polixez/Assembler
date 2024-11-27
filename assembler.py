import sys
import xml.etree.ElementTree as ET

def assemble_instruction(line):
    parts = line.strip().split()
    if not parts or parts[0].startswith(';'):
        return None, None
    opcode_str = parts[0].upper()
    operand = int(parts[1]) if len(parts) > 1 else 0

    if opcode_str == 'LDC':
        opcode = 12
        operand_bits = 15  # Биты 7–21
    elif opcode_str == 'LD':
        opcode = 58
        operand_bits = 15
    elif opcode_str == 'ST':
        opcode = 24
        operand_bits = 10  # Биты 7–16
    elif opcode_str == 'EQ':
        opcode = 90
        operand_bits = 10
    else:
        raise ValueError(f"Неизвестная инструкция {opcode_str}")

    instruction = (opcode & 0x7F) | ((operand & ((1 << operand_bits) - 1)) << 7)
    return instruction, {
        'opcode': opcode_str,
        'operand': operand
    }

def assemble(source_file, binary_file, log_file):
    # Изменение: указание кодировки 'utf-8' при открытии файла
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    binary_instructions = []
    log_entries = []

    for idx, line in enumerate(lines):
        try:
            instruction, log_entry = assemble_instruction(line)
            if instruction is not None:
                binary_instructions.append(instruction)
                log_entries.append(log_entry)
        except Exception as e:
            print(f"Ошибка в строке {idx + 1}: {line}")
            print(f"Исключение: {e}")
            continue

    # Запись бинарного файла
    with open(binary_file, 'wb') as f:
        for instr in binary_instructions:
            f.write(instr.to_bytes(4, byteorder='little'))

    # Создание XML лога
    root = ET.Element('Log')
    for i, entry in enumerate(log_entries):
        instr_elem = ET.SubElement(root, 'Instruction', {'index': str(i)})
        for k, v in entry.items():
            ET.SubElement(instr_elem, k).text = str(v)

    tree = ET.ElementTree(root)
    tree.write(log_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python assembler.py <source_file> <binary_file> <log_file>")
        sys.exit(1)
    source_file = sys.argv[1]
    binary_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(source_file, binary_file, log_file)