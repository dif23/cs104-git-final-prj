from cpu import CPU
import sys
import time

INSTRUCTION_INPUT_FILE = "/Users/michaelhaggerty/Documents/CS/Python Projects/CPU_Simulation/instruction_input.txt"
DATA_INPUT_FILE = "/Users/michaelhaggerty/Documents/CS/Python Projects/CPU_Simulation/data_input.txt"

# Generate list of instructions from input file, use lambda function to strip off '\n' character from each line
def fetch_instructions():
    instruction_file = open(INSTRUCTION_INPUT_FILE, 'r')
    instructions = instruction_file.readlines()
    instructions = list(map(lambda s: s.strip(), instructions))
    return instructions

# Generate list of data inputs to initialize the memory bus from.
# Use lambda function to strip off '\n' character from each line
def fetch_data():
    data_file = open(DATA_INPUT_FILE, 'r')
    data = data_file.readlines()
    data = list(map(lambda s: s.strip(), data))
    return data

# Method to write each value from data_input file to CPU's memory bus
def initialize_memory_bus(cpu):
    data_loaded = fetch_data()
    for data in data_loaded:
        data_parsed = data.split(",")
        cpu.write_memory_bus(data_parsed[0], data_parsed[1])

# Method to send instructions line-by-line to CPU object
def send_instructions_to_cpu(cpu):
    instructions_loaded = fetch_instructions()
    for instruction in instructions_loaded:
        if not cpu.parse_instruction(instruction):
            break


def print_memory_matrix(cpu):
    print("Here are the Memory Bus contents...")
    print("---------------------------------------------------")
    memory_contents = cpu.memory_bus.memory_bus
    max_address_length = len(str(len(memory_contents) - 1))  # Calculate the maximum length of the address
    max_value_length = max(len(str(value)) for value in memory_contents.values())  # Calculate the maximum length of the value
    for i in range(0, len(memory_contents), 8):  # Assuming 8 columns for simplicity
        for j in range(8):
            address = i + j
            binary_address = "{:08b}".format(address)
            if binary_address in memory_contents:
                value = memory_contents[binary_address]
                print(f"| {address:>{max_address_length}}: {value:>{max_value_length}} ", end="")
            else:
                print(f"| {address:>{max_address_length}}: {' ':>{max_value_length}} ", end="")
        print("|")
    print("---------------------------------------------------")


# Generate a single binary string representing all instructions
def fetch_instructions_binary(cpu):
    instructions_loaded = fetch_instructions()
    binary_string = ""
    for instruction in instructions_loaded:
        binary_instruction = cpu.instruction_to_binary(instruction)  # Using the method from CPU class
        if binary_instruction is not None:
            binary_string += binary_instruction
    for bit in binary_string:
        print(bit, end='', flush=True)
        time.sleep(0.01)  # Adjust the sleep time as needed
    print()  # Add a newline at the end
    
# Start of Python script to run the CPU simulator
my_cpu = CPU()
print("---------------------------------------------------")
print("Welcome to the Python CPU Simulator!")
print("---------------------------------------------------")
time.sleep(0.7)
print("Initializing Memory Bus from data input file...")
initialize_memory_bus(my_cpu)
print("Memory Bus successfully initialized")
print("---------------------------------------------------")
time.sleep(0.7)
print_memory_matrix(my_cpu)
time.sleep(0.7)
print("Reading instructions in Assembly...")
print("---------------------------------------------------")
time.sleep(0.7)
send_instructions_to_cpu(my_cpu)
print("---------------------------------------------------")
# Print instructions as a single binary string
print("Sending instructions in Machine Language:")
print("---------------------------------------------------")
time.sleep(0.7)

fetch_instructions_binary(my_cpu)

print("---------------------------------------------------")
time.sleep(0.7)
print("Terminating CPU Processing...")
print("---------------------------------------------------")
time.sleep(0.7)
print("Contents of CPU Registers:")
for i, reg in enumerate(my_cpu.registers):
    print(f"| R{i}: {reg} ", end="")
print("|")
print("---------------------------------------------------")
