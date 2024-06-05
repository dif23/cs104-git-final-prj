from cache import Cache
from memory import Memory


CPU_COUNTER_INIT_VALUE = 0
NUMBER_OF_REGISTERS = 9

ADD_INSTRUCTION_OPERATOR = "ADD"
ADD_I_INSTRUCTION_OPERATOR = "ADDI"
JUMP_INSTRUCTION_OPERATOR = "J"
CACHE_INSTRUCTION_OPERATOR = "CACHE"
HALT_INSTRUCTION_OPERATOR = "HALT"
MUL_INSTRUCTION_OPERATOR = "MUL"
SUB_I_INSTRUCTION_OPERATOR = "SUBI"
DIV_INSTRUCTION_OPERATOR = "DIV"

CACHE_OFF_VALUE = 0
CACHE_ON_VALUE = 1
CACHE_FLUSH_VALUE = 2

def convert_register_to_index(value):
    return int(value[1:])

class CPU:
    def __init__(self):
        self.cpu_counter = CPU_COUNTER_INIT_VALUE
        self.registers = [0] * NUMBER_OF_REGISTERS
        self.cache_flag = False
        self.cache = Cache()
        self.memory_bus = Memory()

    def increment_cpu_counter(self):
        self.cpu_counter += 1

    def reset_cpu_counter(self):
        self.cpu_counter = CPU_COUNTER_INIT_VALUE

    def set_cpu_counter(self, value):
        self.cpu_counter = value

    def get_cpu_counter(self):
        return self.cpu_counter

    def reset_registers(self):
        for i in range(len(self.registers)):
            self.registers[i] = 0

    def set_cache_flag(self, value):
        self.cache_flag = value

    def flush_cache(self):
        self.cache.flush_cache()

    def search_cache(self, address):
        return self.cache.search_cache(address)

    def write_cache(self, address, value):
        self.cache.write_cache(address, value)

    def search_memory_bus(self, address):
        return self.memory_bus.search_memory_bus(address)

    def write_memory_bus(self, address, value):
        self.memory_bus.write_memory_bus(address, value)

    def jump_instruction(self, target):
        self.cpu_counter = int(target)

    def add_instruction(self, destination, source, target):
        self.registers[convert_register_to_index(destination)] = self.registers[convert_register_to_index(source)] + \
                                                                 self.registers[convert_register_to_index(target)]

    def add_i_instruction(self, destination, source, immediate):
        self.registers[convert_register_to_index(destination)] = self.registers[convert_register_to_index(source)] + \
                                                                 int(immediate)

    def mul_instruction(self, destination, source, target):
        self.registers[convert_register_to_index(destination)] = self.registers[convert_register_to_index(source)] * \
                                                                 self.registers[convert_register_to_index(target)]

    def sub_i_instruction(self, destination, source, immediate):
        self.registers[convert_register_to_index(destination)] = self.registers[convert_register_to_index(source)] - \
                                                                 int(immediate)

    def div_instruction(self, destination, source, target):
        if self.registers[convert_register_to_index(target)] != 0:
            self.registers[convert_register_to_index(destination)] = self.registers[convert_register_to_index(source)] // \
                                                                     self.registers[convert_register_to_index(target)]
        else:
            print(f"Error: Division by zero in instruction {self.cpu_counter}")

    def cache_instruction(self, value):
        if value == CACHE_OFF_VALUE:
            self.set_cache_flag(False)
        elif value == CACHE_ON_VALUE:
            self.set_cache_flag(True)
        elif value == CACHE_FLUSH_VALUE:
            self.flush_cache()

    def halt_instruction(self):
        return False

    def parse_instruction(self, instruction):
        instruction_parsed = instruction.split(",")
        print(instruction)
        if instruction_parsed[0] == ADD_INSTRUCTION_OPERATOR:
            self.add_instruction(instruction_parsed[1], instruction_parsed[2], instruction_parsed[3])
        elif instruction_parsed[0] == ADD_I_INSTRUCTION_OPERATOR:
            self.add_i_instruction(instruction_parsed[1], instruction_parsed[2], instruction_parsed[3])
        elif instruction_parsed[0] == JUMP_INSTRUCTION_OPERATOR:
            self.jump_instruction(instruction_parsed[1])
            return True  # Skip incrementing cpu_counter as it's directly set by jump
        elif instruction_parsed[0] == CACHE_INSTRUCTION_OPERATOR:
            self.cache_instruction(int(instruction_parsed[1]))
        elif instruction_parsed[0] == MUL_INSTRUCTION_OPERATOR:
            self.mul_instruction(instruction_parsed[1], instruction_parsed[2], instruction_parsed[3])
        elif instruction_parsed[0] == SUB_I_INSTRUCTION_OPERATOR:
            self.sub_i_instruction(instruction_parsed[1], instruction_parsed[2], instruction_parsed[3])
        elif instruction_parsed[0] == DIV_INSTRUCTION_OPERATOR:
            self.div_instruction(instruction_parsed[1], instruction_parsed[2], instruction_parsed[3])
        elif instruction_parsed[0] == HALT_INSTRUCTION_OPERATOR:
            return False
        self.increment_cpu_counter()
        return True

        
    def instruction_to_binary(self, instruction):
        instruction_parsed = instruction.split(",")
        opcode_map = {
            "CACHE": "000000",
            "ADD": "000001",
            "ADDI": "000010",
            "J": "000011",
            "HALT": "000100",
            "SUBI": "000101",
            "MUL": "000110",
            "DIV": "000111"
        }
        
        opcode = opcode_map.get(instruction_parsed[0], "??????")
        if opcode == "??????":
            print(f"Unknown instruction: {instruction}")
            return None  # Return None for unknown instructions

        if instruction_parsed[0] in ["CACHE"]:
            # Format: opcode + value
            return f"{opcode}{int(instruction_parsed[1]):026b}"

        # Handle other instructions similarly
        
        if instruction_parsed[0] in ["ADD", "MUL", "DIV"]:
            # Format: opcode + destination + source + target
            return f"{opcode}{int(instruction_parsed[1][1:]):05b}{int(instruction_parsed[2][1:]):05b}{int(instruction_parsed[3][1:]):05b}"
        
        if instruction_parsed[0] in ["ADDI", "SUBI"]:
            # Format: opcode + destination + source + immediate
            return f"{opcode}{int(instruction_parsed[1][1:]):05b}{int(instruction_parsed[2][1:]):05b}{int(instruction_parsed[3]):016b}"
        
        if instruction_parsed[0] == "J":
            # Format: opcode + target
            return f"{opcode}{int(instruction_parsed[1]):026b}"

