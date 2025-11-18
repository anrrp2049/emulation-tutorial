#!/usr/bin/env python3
"""
CHIP-8 Tutorial - Step 1: Basic CPU Structure

This is the first step in building a CHIP-8 emulator.
We'll create the basic CPU structure with minimal functionality:
- Memory
- Registers
- Program counter
- Basic fetch-decode-execute cycle
- A few simple opcodes

This step demonstrates the fundamental structure without the complexity
of graphics, input, or all 35 opcodes.
"""


class BasicCHIP8:
    """
    Minimal CHIP-8 CPU - Step 1

    This version implements only the core CPU components:
    - 4KB memory
    - 16 registers
    - Program counter
    - Basic opcodes: 6XNN, 7XNN, ANNN, 1NNN
    """

    def __init__(self):
        print("Initializing basic CHIP-8 CPU...")

        # Memory: 4096 bytes (4KB)
        # Address space: 0x000 to 0xFFF
        self.memory = [0] * 4096
        print("  ✓ Allocated 4KB memory")

        # Registers: 16 general-purpose 8-bit registers (V0-VF)
        # V0-VE: General use
        # VF: Flag register (used by some instructions for carry, borrow, etc.)
        self.V = [0] * 16
        print("  ✓ Created 16 registers (V0-VF)")

        # Index register: 16-bit register for memory addressing
        self.I = 0
        print("  ✓ Initialized index register (I)")

        # Program counter: Points to current instruction
        # Programs are loaded at 0x200, so we start there
        self.pc = 0x200
        print("  ✓ Set program counter to 0x200")

        # Control flag
        self.running = True

        print("Initialization complete!\n")

    def load_program(self, program_bytes):
        """
        Load a program into memory.

        Args:
            program_bytes: List of bytes to load at 0x200
        """
        print(f"Loading program ({len(program_bytes)} bytes)...")

        for i, byte in enumerate(program_bytes):
            self.memory[0x200 + i] = byte

        print("Program loaded into memory at 0x200")
        print()

    def cycle(self):
        """
        Execute one CPU cycle: Fetch, Decode, Execute

        This is the heart of the emulator!
        """
        # FETCH: Get the next instruction from memory
        # CHIP-8 instructions are 2 bytes (16 bits), stored big-endian
        #
        # Big-endian means: most significant byte first
        # Example: instruction 0x6123 is stored as [0x61, 0x23]

        high_byte = self.memory[self.pc]      # First byte (bits 15-8)
        low_byte = self.memory[self.pc + 1]   # Second byte (bits 7-0)

        # Combine bytes into 16-bit opcode
        opcode = (high_byte << 8) | low_byte

        print(f"[PC: 0x{self.pc:03X}] Fetched opcode: 0x{opcode:04X}")

        # Move program counter to next instruction
        # (Jump instructions will override this)
        self.pc += 2

        # DECODE & EXECUTE: Figure out what the instruction means and do it
        self.execute(opcode)

    def execute(self, opcode):
        """
        Decode and execute an opcode.

        For this basic version, we only implement 4 opcodes:
        - 6XNN: Set VX = NN
        - 7XNN: Add NN to VX
        - ANNN: Set I = NNN
        - 1NNN: Jump to NNN
        - 0000: Halt (custom, for this tutorial)
        """

        # Extract parts of the opcode
        # Different opcodes use different parts

        first_nibble = (opcode & 0xF000) >> 12  # First hex digit
        x = (opcode & 0x0F00) >> 8               # Second hex digit (register number)
        nn = opcode & 0x00FF                     # Last two hex digits (byte value)
        nnn = opcode & 0x0FFF                    # Last three hex digits (address)

        # Decode by pattern matching
        if opcode == 0x0000:
            # Special: Halt instruction (not in real CHIP-8)
            print("  → HALT (end of program)")
            self.running = False

        elif first_nibble == 0x6:
            # 6XNN: LD VX, NN - Set register VX to value NN
            print(f"  → LD V{x:X}, 0x{nn:02X}  (Set V{x:X} = {nn})")
            self.V[x] = nn

        elif first_nibble == 0x7:
            # 7XNN: ADD VX, NN - Add NN to register VX
            old_value = self.V[x]
            self.V[x] = (self.V[x] + nn) & 0xFF  # Wrap to 8 bits
            print(f"  → ADD V{x:X}, 0x{nn:02X}  (V{x:X}: {old_value} + {nn} = {self.V[x]})")

        elif first_nibble == 0xA:
            # ANNN: LD I, NNN - Set index register I to address NNN
            print(f"  → LD I, 0x{nnn:03X}  (Set I = 0x{nnn:03X})")
            self.I = nnn

        elif first_nibble == 0x1:
            # 1NNN: JP NNN - Jump to address NNN
            print(f"  → JP 0x{nnn:03X}  (Jump to 0x{nnn:03X})")
            self.pc = nnn

        else:
            print(f"  → UNKNOWN opcode: 0x{opcode:04X}")
            self.running = False

        print()

    def run(self):
        """
        Main execution loop.

        Keep executing cycles until the program halts.
        """
        print("Starting execution...\n")
        print("=" * 60)
        print()

        cycle_count = 0

        while self.running:
            self.cycle()
            cycle_count += 1

            # Safety: stop after 100 cycles to prevent infinite loops
            if cycle_count > 100:
                print("⚠ Safety stop: 100 cycles executed")
                break

        print("=" * 60)
        print("\nExecution finished!")
        self.print_state()

    def print_state(self):
        """Print the current CPU state"""
        print("\nFinal CPU State:")
        print("-" * 60)
        print(f"Program Counter (PC): 0x{self.pc:03X}")
        print(f"Index Register (I):   0x{self.I:03X}")
        print("\nRegisters:")
        for i in range(16):
            print(f"  V{i:X}: 0x{self.V[i]:02X} ({self.V[i]:3d})", end="")
            if i % 4 == 3:
                print()  # Newline every 4 registers
        print("-" * 60)


def main():
    """
    Run a simple test program.

    This program demonstrates basic functionality:
    1. Set V0 = 5
    2. Set V1 = 10
    3. Add 3 to V0 (V0 becomes 8)
    4. Set I = 0x300
    5. Halt
    """

    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "CHIP-8 Tutorial - Step 1" + " " * 19 + "║")
    print("║" + " " * 18 + "Basic CPU Structure" + " " * 21 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    # Create CPU
    cpu = BasicCHIP8()

    # Create a simple test program
    # Programs are stored as a list of 16-bit instructions
    # We'll convert them to bytes for loading into memory

    program = [
        0x6005,  # V0 = 5       : Set register V0 to 5
        0x610A,  # V1 = 10      : Set register V1 to 10
        0x7003,  # V0 = V0 + 3  : Add 3 to V0 (now V0 = 8)
        0xA300,  # I = 0x300    : Set I to 0x300
        0x7105,  # V1 = V1 + 5  : Add 5 to V1 (now V1 = 15)
        0x0000,  # HALT         : Stop execution
    ]

    # Convert instructions to bytes (big-endian)
    program_bytes = []
    for instruction in program:
        program_bytes.append((instruction >> 8) & 0xFF)  # High byte
        program_bytes.append(instruction & 0xFF)          # Low byte

    # Load and run
    cpu.load_program(program_bytes)
    cpu.run()

    # Show what we expected
    print("\n📝 Expected results:")
    print("  V0 should be 8  (started at 5, added 3)")
    print("  V1 should be 15 (started at 10, added 5)")
    print("  I should be 0x300")
    print()

    # Verify
    success = True
    if cpu.V[0] != 8:
        print("❌ V0 is incorrect!")
        success = False
    if cpu.V[1] != 15:
        print("❌ V1 is incorrect!")
        success = False
    if cpu.I != 0x300:
        print("❌ I is incorrect!")
        success = False

    if success:
        print("✅ All tests passed! Your basic CPU works!")
    else:
        print("⚠ Some tests failed. Check your implementation.")

    print()
    print("=" * 60)
    print("Next step: Add more opcodes, graphics, and input!")
    print("See: src/chip8.py for the complete implementation")
    print("=" * 60)


if __name__ == '__main__':
    main()
