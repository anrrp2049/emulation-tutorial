#!/usr/bin/env python3
"""
CHIP-8 Tutorial - Step 2: Understanding Fetch-Decode-Execute

This tutorial focuses on understanding how opcodes are fetched, decoded,
and executed. We'll implement more opcodes and understand bitwise operations
for instruction decoding.

New concepts:
- Detailed opcode decoding patterns
- Bitwise masking and shifting
- Different instruction formats
- More arithmetic operations
"""


class DetailedCHIP8:
    """
    CHIP-8 with detailed decode explanation.
    
    This step adds:
    - More opcodes (arithmetic, logic, display clear)
    - Detailed decoding explanations
    - Different opcode patterns
    """
    
    def __init__(self, debug=True):
        self.debug = debug
        
        # CPU State
        self.memory = [0] * 4096
        self.V = [0] * 16
        self.I = 0
        self.pc = 0x200
        
        # Display (simplified - just track if clear was called)
        self.display_cleared = False
        
        self.running = True
        
        print("CHIP-8 CPU initialized with detailed decode mode\n")
    
    def load_program(self, program_bytes):
        """Load program into memory at 0x200"""
        for i, byte in enumerate(program_bytes):
            self.memory[0x200 + i] = byte
        print(f"Loaded {len(program_bytes)} bytes\n")
    
    def decode_opcode(self, opcode):
        """
        Decode an opcode and explain the bit manipulation.
        
        This is educational - shows HOW we extract parts of the instruction.
        """
        print(f"\n{'='*70}")
        print(f"Decoding opcode: 0x{opcode:04X} = {opcode:016b}b")
        print(f"{'='*70}")
        
        # Show the opcode in binary with labels
        print("\nBinary breakdown:")
        print("  Bits 15-12  Bits 11-8   Bits 7-4    Bits 3-0")
        print("  (nibble 1)  (nibble 2)  (nibble 3)  (nibble 4)")
        
        # Extract nibbles
        nibble1 = (opcode & 0xF000) >> 12
        nibble2 = (opcode & 0x0F00) >> 8
        nibble3 = (opcode & 0x00F0) >> 4
        nibble4 = (opcode & 0x000F)
        
        print(f"    {nibble1:04b}        {nibble2:04b}        {nibble3:04b}        {nibble4:04b}")
        print(f"     {nibble1:X}           {nibble2:X}           {nibble3:X}           {nibble4:X}\n")
        
        # Common patterns
        print("Common instruction patterns:")
        print(f"  First nibble (opcode category): 0x{nibble1:X}")
        print(f"  X (register 1):                  0x{nibble2:X} (V{nibble2:X})")
        print(f"  Y (register 2):                  0x{nibble3:X} (V{nibble3:X})")
        print(f"  N (4-bit immediate):             0x{nibble4:X}")
        print(f"  NN (8-bit immediate):            0x{(opcode & 0x00FF):02X}")
        print(f"  NNN (12-bit address):            0x{(opcode & 0x0FFF):03X}")
        
        # Explain the masking
        print("\nHow we extract these values:")
        print(f"  First nibble: (0x{opcode:04X} & 0xF000) >> 12 = 0x{nibble1:X}")
        print(f"  X register:   (0x{opcode:04X} & 0x0F00) >> 8  = 0x{nibble2:X}")
        print(f"  Y register:   (0x{opcode:04X} & 0x00F0) >> 4  = 0x{nibble3:X}")
        print(f"  N value:      (0x{opcode:04X} & 0x000F)       = 0x{nibble4:X}")
        print(f"  NN value:     (0x{opcode:04X} & 0x00FF)       = 0x{(opcode & 0x00FF):02X}")
        print(f"  NNN value:    (0x{opcode:04X} & 0x0FFF)       = 0x{(opcode & 0x0FFF):03X}")
        
        return nibble1, nibble2, nibble3, nibble4
    
    def cycle(self):
        """Execute one CPU cycle with detailed explanation"""
        
        # FETCH
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        print(f"\n[PC=0x{self.pc:03X}] FETCH: Read bytes 0x{self.memory[self.pc]:02X} and 0x{self.memory[self.pc+1]:02X}")
        print(f"              Combined as: 0x{opcode:04X}")
        
        # Increment PC
        old_pc = self.pc
        self.pc += 2
        
        # DECODE
        n1, x, y, n = self.decode_opcode(opcode)
        nn = opcode & 0x00FF
        nnn = opcode & 0x0FFF
        
        # EXECUTE
        print(f"\n{'='*70}")
        print("EXECUTE:")
        print(f"{'='*70}")
        
        if opcode == 0x00E0:
            print("Instruction: CLS (Clear screen)")
            print("  Opcode pattern: 0x00E0")
            print("  Action: Clear the display")
            self.display_cleared = True
            print("  ✓ Display cleared")
            
        elif opcode == 0x00EE:
            print("Instruction: RET (Return from subroutine)")
            print("  Not implemented in this step")
            
        elif n1 == 0x1:
            print(f"Instruction: JP 0x{nnn:03X} (Jump to address)")
            print(f"  Opcode pattern: 1NNN where NNN={nnn:03X}")
            print(f"  Action: Set PC = 0x{nnn:03X}")
            print(f"  Before: PC = 0x{self.pc:03X}")
            self.pc = nnn
            print(f"  After:  PC = 0x{self.pc:03X}")
            
        elif n1 == 0x6:
            print(f"Instruction: LD V{x:X}, 0x{nn:02X} (Load immediate)")
            print(f"  Opcode pattern: 6XNN where X={x:X}, NN={nn:02X}")
            print(f"  Action: Set V{x:X} = {nn}")
            print(f"  Before: V{x:X} = {self.V[x]}")
            self.V[x] = nn
            print(f"  After:  V{x:X} = {self.V[x]}")
            
        elif n1 == 0x7:
            print(f"Instruction: ADD V{x:X}, 0x{nn:02X} (Add immediate)")
            print(f"  Opcode pattern: 7XNN where X={x:X}, NN={nn:02X}")
            print(f"  Action: V{x:X} = V{x:X} + {nn}")
            print(f"  Before: V{x:X} = {self.V[x]}")
            result = (self.V[x] + nn) & 0xFF
            print(f"  Calculation: {self.V[x]} + {nn} = {result}")
            print(f"  (Wrapped to 8 bits with & 0xFF)")
            self.V[x] = result
            print(f"  After:  V{x:X} = {self.V[x]}")
            
        elif n1 == 0x8:
            # Arithmetic/logic operations
            if n == 0:
                print(f"Instruction: LD V{x:X}, V{y:X} (Copy register)")
                print(f"  Opcode pattern: 8XY0 where X={x:X}, Y={y:X}")
                print(f"  Action: V{x:X} = V{y:X}")
                print(f"  Before: V{x:X}={self.V[x]}, V{y:X}={self.V[y]}")
                self.V[x] = self.V[y]
                print(f"  After:  V{x:X} = {self.V[x]}")
                
            elif n == 1:
                print(f"Instruction: OR V{x:X}, V{y:X} (Bitwise OR)")
                print(f"  Opcode pattern: 8XY1 where X={x:X}, Y={y:X}")
                print(f"  Action: V{x:X} = V{x:X} | V{y:X}")
                print(f"  Before: V{x:X}={self.V[x]:08b}b, V{y:X}={self.V[y]:08b}b")
                self.V[x] = self.V[x] | self.V[y]
                print(f"  After:  V{x:X}={self.V[x]:08b}b ({self.V[x]})")
                
            elif n == 2:
                print(f"Instruction: AND V{x:X}, V{y:X} (Bitwise AND)")
                print(f"  Opcode pattern: 8XY2 where X={x:X}, Y={y:X}")
                print(f"  Action: V{x:X} = V{x:X} & V{y:X}")
                print(f"  Before: V{x:X}={self.V[x]:08b}b, V{y:X}={self.V[y]:08b}b")
                self.V[x] = self.V[x] & self.V[y]
                print(f"  After:  V{x:X}={self.V[x]:08b}b ({self.V[x]})")
                
            elif n == 3:
                print(f"Instruction: XOR V{x:X}, V{y:X} (Bitwise XOR)")
                print(f"  Opcode pattern: 8XY3 where X={x:X}, Y={y:X}")
                print(f"  Action: V{x:X} = V{x:X} ^ V{y:X}")
                print(f"  Before: V{x:X}={self.V[x]:08b}b, V{y:X}={self.V[y]:08b}b")
                self.V[x] = self.V[x] ^ self.V[y]
                print(f"  After:  V{x:X}={self.V[x]:08b}b ({self.V[x]})")
                
            elif n == 4:
                print(f"Instruction: ADD V{x:X}, V{y:X} (Add with carry)")
                print(f"  Opcode pattern: 8XY4 where X={x:X}, Y={y:X}")
                print(f"  Action: V{x:X} = V{x:X} + V{y:X}, VF = carry")
                print(f"  Before: V{x:X}={self.V[x]}, V{y:X}={self.V[y]}")
                result = self.V[x] + self.V[y]
                carry = 1 if result > 255 else 0
                print(f"  Calculation: {self.V[x]} + {self.V[y]} = {result}")
                if carry:
                    print(f"  Result > 255, so carry flag (VF) = 1")
                else:
                    print(f"  Result <= 255, so carry flag (VF) = 0")
                self.V[x] = result & 0xFF
                self.V[0xF] = carry
                print(f"  After:  V{x:X}={self.V[x]}, VF={self.V[0xF]}")
            else:
                print(f"Opcode 0x8XY{n:X} not implemented in this step")
                
        elif n1 == 0xA:
            print(f"Instruction: LD I, 0x{nnn:03X} (Load index register)")
            print(f"  Opcode pattern: ANNN where NNN={nnn:03X}")
            print(f"  Action: Set I = 0x{nnn:03X}")
            print(f"  Before: I = 0x{self.I:03X}")
            self.I = nnn
            print(f"  After:  I = 0x{self.I:03X}")
            
        elif opcode == 0x0000:
            print("Instruction: HALT (end program)")
            self.running = False
            
        else:
            print(f"Unknown opcode: 0x{opcode:04X}")
            self.running = False
    
    def run(self):
        """Run until HALT"""
        print("\n" + "="*70)
        print("STARTING EXECUTION")
        print("="*70)
        
        cycle_count = 0
        while self.running and cycle_count < 50:
            self.cycle()
            cycle_count += 1
            
            # Print register state after each instruction
            self.print_registers()
            
            input("\nPress Enter for next instruction...")
        
        print("\n" + "="*70)
        print("EXECUTION FINISHED")
        print("="*70)
        self.print_registers()
    
    def print_registers(self):
        """Print all registers in a nice format"""
        print("\n" + "-"*70)
        print("REGISTER STATE:")
        print("-"*70)
        print(f"PC: 0x{self.pc:03X}    I: 0x{self.I:03X}")
        print("\nGeneral Purpose Registers:")
        for i in range(16):
            print(f"  V{i:X}: 0x{self.V[i]:02X} ({self.V[i]:3d}) = {self.V[i]:08b}b", end="")
            if i % 2 == 1:
                print()
        print("-"*70)


def main():
    """Run a demo program showing different instruction types"""
    
    print("╔" + "═"*68 + "╗")
    print("║" + " "*18 + "CHIP-8 Tutorial - Step 2" + " "*27 + "║")
    print("║" + " "*15 + "Fetch-Decode-Execute in Detail" + " "*22 + "║")
    print("╚" + "═"*68 + "╝\n")
    
    print("This tutorial will step through each instruction showing:")
    print("  1. How the opcode is fetched from memory")
    print("  2. How we decode it using bitwise operations")
    print("  3. How we execute the decoded instruction")
    print("  4. The resulting changes to CPU state\n")
    
    cpu = DetailedCHIP8()
    
    # Program demonstrating various instruction formats
    program = [
        0x6105,  # V1 = 5        : Load immediate (6XNN pattern)
        0x6203,  # V2 = 3        : Load immediate
        0x8124,  # V1 = V1 + V2  : Register add (8XY4 pattern)
        0x7107,  # V1 = V1 + 7   : Immediate add (7XNN pattern)
        0x6AFF,  # VA = 0xFF     : Load max value
        0x6B01,  # VB = 0x01     : Load 1
        0x8AB4,  # VA = VA + VB  : Test carry flag (255 + 1)
        0x00E0,  # CLS           : Clear screen (00E0 pattern)
        0xA500,  # I = 0x500     : Load address (ANNN pattern)
        0x0000,  # HALT          : Stop
    ]
    
    # Convert to bytes
    program_bytes = []
    for instruction in program:
        program_bytes.append((instruction >> 8) & 0xFF)
        program_bytes.append(instruction & 0xFF)
    
    cpu.load_program(program_bytes)
    
    print("Program loaded. Let's execute it step by step!")
    print("\nThis will be interactive - press Enter after each instruction.\n")
    
    cpu.run()
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS:")
    print("="*70)
    print("1. All instructions are 2 bytes (16 bits)")
    print("2. We use bitwise AND (&) and shift (>>) to extract parts")
    print("3. Different opcodes have different patterns:")
    print("   - 6XNN: First nibble identifies type, X is register, NN is value")
    print("   - 8XY4: First nibble and last nibble together identify type")
    print("   - 00E0: Exact match (all 16 bits)")
    print("4. The fetch-decode-execute cycle repeats for every instruction")
    print("="*70)


if __name__ == '__main__':
    main()
