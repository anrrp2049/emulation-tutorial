#!/usr/bin/env python3
"""
Simple Stack-Based Virtual Machine
===================================

This is a minimal stack-based VM to demonstrate VM/emulator concepts
in a simpler context than CHIP-8. Great for understanding:
- Stack-based architectures (vs. register-based like CHIP-8)
- Bytecode interpretation
- VM design patterns

Stack machines are used in:
- Java Virtual Machine (JVM)
- .NET Common Language Runtime (CLR)
- Python bytecode interpreter
- Forth programming language
- PostScript
- WebAssembly (stack-based)

This VM has only 15 instructions but is Turing complete!
"""

import sys
from typing import List, Dict, Any


class StackVM:
    """
    A simple stack-based virtual machine.

    Architecture:
    - Stack: Main data structure for operands
    - Memory: 256 bytes of RAM
    - PC: Program counter
    - Call stack: For function calls

    Instructions are 1-2 bytes:
    - Opcode (1 byte)
    - Optional operand (1 byte)
    """

    # Instruction set (opcodes)
    PUSH    = 0x01  # PUSH <value>    - Push value onto stack
    POP     = 0x02  # POP             - Discard top of stack
    ADD     = 0x03  # ADD             - Pop two values, push sum
    SUB     = 0x04  # SUB             - Pop two values, push difference
    MUL     = 0x05  # MUL             - Pop two values, push product
    DIV     = 0x06  # DIV             - Pop two values, push quotient
    LOAD    = 0x07  # LOAD <addr>     - Push memory[addr] onto stack
    STORE   = 0x08  # STORE <addr>    - Pop stack, store in memory[addr]
    JMP     = 0x09  # JMP <addr>      - Jump to address
    JZ      = 0x0A  # JZ <addr>       - Jump if top of stack is zero
    JNZ     = 0x0B  # JNZ <addr>      - Jump if top of stack is not zero
    CALL    = 0x0C  # CALL <addr>     - Call subroutine
    RET     = 0x0D  # RET             - Return from subroutine
    PRINT   = 0x0E  # PRINT           - Pop and print top of stack
    HALT    = 0x0F  # HALT            - Stop execution

    def __init__(self, debug=False):
        """Initialize the VM"""
        self.debug = debug

        # Stack for operands (grows upward)
        self.stack: List[int] = []

        # Memory (256 bytes)
        self.memory: List[int] = [0] * 256

        # Program counter
        self.pc: int = 0

        # Call stack for subroutine returns
        self.call_stack: List[int] = []

        # Execution state
        self.running: bool = False

        # Statistics
        self.cycles: int = 0

    def load_program(self, bytecode: List[int]):
        """
        Load bytecode into memory starting at address 0.

        Args:
            bytecode: List of instruction bytes
        """
        if len(bytecode) > 256:
            raise ValueError("Program too large (max 256 bytes)")

        for i, byte in enumerate(bytecode):
            self.memory[i] = byte

        if self.debug:
            print(f"Loaded {len(bytecode)} bytes into memory")

    def push(self, value: int):
        """Push value onto stack"""
        self.stack.append(value & 0xFF)  # Keep 8-bit

    def pop(self) -> int:
        """Pop value from stack"""
        if not self.stack:
            raise RuntimeError(f"Stack underflow at PC={self.pc}")
        return self.stack.pop()

    def fetch(self) -> int:
        """Fetch next byte from memory and increment PC"""
        byte = self.memory[self.pc]
        self.pc = (self.pc + 1) & 0xFF  # Wrap at 256
        return byte

    def execute_cycle(self):
        """Execute one instruction (Fetch-Decode-Execute)"""

        # FETCH
        opcode = self.fetch()

        # Debug output
        if self.debug:
            stack_str = str(self.stack[-5:] if len(self.stack) > 5 else self.stack)
            print(f"[{self.cycles:04d}] PC:{self.pc-1:02X} OP:{opcode:02X} Stack:{stack_str}")

        # DECODE & EXECUTE
        if opcode == self.PUSH:
            # PUSH <value>
            value = self.fetch()
            self.push(value)
            if self.debug:
                print(f"  → PUSH {value}")

        elif opcode == self.POP:
            # POP
            value = self.pop()
            if self.debug:
                print(f"  → POP (discarded {value})")

        elif opcode == self.ADD:
            # ADD: pop b, pop a, push a+b
            b = self.pop()
            a = self.pop()
            result = (a + b) & 0xFF
            self.push(result)
            if self.debug:
                print(f"  → ADD: {a} + {b} = {result}")

        elif opcode == self.SUB:
            # SUB: pop b, pop a, push a-b
            b = self.pop()
            a = self.pop()
            result = (a - b) & 0xFF
            self.push(result)
            if self.debug:
                print(f"  → SUB: {a} - {b} = {result}")

        elif opcode == self.MUL:
            # MUL: pop b, pop a, push a*b
            b = self.pop()
            a = self.pop()
            result = (a * b) & 0xFF
            self.push(result)
            if self.debug:
                print(f"  → MUL: {a} * {b} = {result}")

        elif opcode == self.DIV:
            # DIV: pop b, pop a, push a/b
            b = self.pop()
            a = self.pop()
            if b == 0:
                raise RuntimeError("Division by zero")
            result = a // b
            self.push(result)
            if self.debug:
                print(f"  → DIV: {a} / {b} = {result}")

        elif opcode == self.LOAD:
            # LOAD <addr>: push memory[addr]
            addr = self.fetch()
            value = self.memory[addr]
            self.push(value)
            if self.debug:
                print(f"  → LOAD from addr {addr:02X} = {value}")

        elif opcode == self.STORE:
            # STORE <addr>: pop value, store in memory[addr]
            addr = self.fetch()
            value = self.pop()
            self.memory[addr] = value
            if self.debug:
                print(f"  → STORE {value} to addr {addr:02X}")

        elif opcode == self.JMP:
            # JMP <addr>: unconditional jump
            addr = self.fetch()
            self.pc = addr
            if self.debug:
                print(f"  → JMP to {addr:02X}")

        elif opcode == self.JZ:
            # JZ <addr>: jump if top of stack is zero
            addr = self.fetch()
            value = self.pop()
            if value == 0:
                self.pc = addr
                if self.debug:
                    print(f"  → JZ: {value} == 0, jumping to {addr:02X}")
            else:
                if self.debug:
                    print(f"  → JZ: {value} != 0, not jumping")

        elif opcode == self.JNZ:
            # JNZ <addr>: jump if top of stack is not zero
            addr = self.fetch()
            value = self.pop()
            if value != 0:
                self.pc = addr
                if self.debug:
                    print(f"  → JNZ: {value} != 0, jumping to {addr:02X}")
            else:
                if self.debug:
                    print(f"  → JNZ: {value} == 0, not jumping")

        elif opcode == self.CALL:
            # CALL <addr>: call subroutine
            addr = self.fetch()
            self.call_stack.append(self.pc)
            self.pc = addr
            if self.debug:
                print(f"  → CALL {addr:02X} (return addr: {self.call_stack[-1]:02X})")

        elif opcode == self.RET:
            # RET: return from subroutine
            if not self.call_stack:
                raise RuntimeError("Return with empty call stack")
            self.pc = self.call_stack.pop()
            if self.debug:
                print(f"  → RET to {self.pc:02X}")

        elif opcode == self.PRINT:
            # PRINT: pop and print value
            value = self.pop()
            print(f"OUTPUT: {value}")
            if self.debug:
                print(f"  → PRINT {value}")

        elif opcode == self.HALT:
            # HALT: stop execution
            self.running = False
            if self.debug:
                print("  → HALT")

        else:
            raise RuntimeError(f"Unknown opcode: {opcode:02X} at PC={self.pc-1:02X}")

        self.cycles += 1

    def run(self, max_cycles=10000):
        """
        Run the program until HALT or max cycles.

        Args:
            max_cycles: Safety limit to prevent infinite loops
        """
        self.running = True
        self.pc = 0
        self.cycles = 0

        if self.debug:
            print("\n" + "="*60)
            print("Starting VM execution")
            print("="*60 + "\n")

        try:
            while self.running and self.cycles < max_cycles:
                self.execute_cycle()

            if self.cycles >= max_cycles:
                print(f"\n⚠ Hit max cycle limit ({max_cycles})")

        except Exception as e:
            print(f"\n❌ Runtime error: {e}")
            self.dump_state()
            raise

        if self.debug:
            print("\n" + "="*60)
            print(f"Execution finished after {self.cycles} cycles")
            print("="*60)

        self.dump_state()

    def dump_state(self):
        """Print current VM state"""
        print("\n--- VM State ---")
        print(f"PC: {self.pc:02X}")
        print(f"Stack: {self.stack}")
        print(f"Call stack: {self.call_stack}")
        print(f"Cycles: {self.cycles}")

        # Show non-zero memory
        non_zero = [(i, v) for i, v in enumerate(self.memory) if v != 0]
        if non_zero and len(non_zero) < 20:
            print("Non-zero memory:")
            for addr, value in non_zero:
                print(f"  [{addr:02X}] = {value}")


def example_add():
    """Example 1: Simple addition"""
    print("╔" + "═"*58 + "╗")
    print("║" + " "*15 + "Example 1: Simple Addition" + " "*16 + "║")
    print("╚" + "═"*58 + "╝\n")

    # Program: 5 + 3 = ?
    program = [
        StackVM.PUSH, 5,      # Push 5
        StackVM.PUSH, 3,      # Push 3
        StackVM.ADD,          # Add them
        StackVM.PRINT,        # Print result
        StackVM.HALT          # Stop
    ]

    vm = StackVM(debug=True)
    vm.load_program(program)
    vm.run()


def example_factorial():
    """Example 2: Calculate factorial using a loop"""
    print("\n\n╔" + "═"*58 + "╗")
    print("║" + " "*12 + "Example 2: Factorial (Iterative)" + " "*12 + "║")
    print("╚" + "═"*58 + "╝\n")

    # Calculate 5! = 5 * 4 * 3 * 2 * 1 = 120
    # Algorithm:
    #   result = 1
    #   counter = 5
    #   while counter > 0:
    #       result = result * counter
    #       counter = counter - 1

    # Memory layout:
    # Address 0xF0: result
    # Address 0xF1: counter

    program = [
        # Initialize: result = 1, counter = 5
        StackVM.PUSH, 1,        # 00: Push 1
        StackVM.STORE, 0xF0,    # 02: Store in result (0xF0)
        StackVM.PUSH, 5,        # 04: Push 5
        StackVM.STORE, 0xF1,    # 06: Store in counter (0xF1)

        # Loop start (address 08)
        StackVM.LOAD, 0xF1,     # 08: Load counter
        StackVM.JZ, 0x1E,       # 0A: If counter == 0, jump to end (0x1E)

        # Loop body: result *= counter
        StackVM.LOAD, 0xF0,     # 0C: Load result
        StackVM.LOAD, 0xF1,     # 0E: Load counter
        StackVM.MUL,            # 10: Multiply
        StackVM.STORE, 0xF0,    # 11: Store back to result

        # counter--
        StackVM.LOAD, 0xF1,     # 13: Load counter
        StackVM.PUSH, 1,        # 15: Push 1
        StackVM.SUB,            # 17: Subtract
        StackVM.STORE, 0xF1,    # 18: Store back to counter

        # Loop back
        StackVM.JMP, 0x08,      # 1A: Jump to loop start

        # End (address 1E)
        StackVM.LOAD, 0xF0,     # 1E: Load result
        StackVM.PRINT,          # 20: Print it
        StackVM.HALT            # 21: Stop
    ]

    vm = StackVM(debug=False)  # Too verbose for loops
    vm.load_program(program)
    vm.run()

    print("\n✓ Expected: 120 (5! = 5*4*3*2*1)")


def example_subroutine():
    """Example 3: Subroutine call"""
    print("\n\n╔" + "═"*58 + "╗")
    print("║" + " "*13 + "Example 3: Subroutine (Square)" + " "*14 + "║")
    print("╚" + "═"*58 + "╝\n")

    # Calculate 7^2 using a subroutine
    # Subroutine: square(n) = n * n

    program = [
        # Main program
        StackVM.PUSH, 7,        # 00: Push argument (7)
        StackVM.CALL, 0x08,     # 02: Call square function at 0x08
        StackVM.PRINT,          # 04: Print result
        StackVM.HALT,           # 05: Stop

        # Padding
        0x00, 0x00,             # 06-07: Padding to align function

        # Square subroutine (address 0x08)
        # Expects: value on stack
        # Returns: value^2 on stack
        StackVM.LOAD, 0xF0,     # 08: Load arg from temp storage
        # (Ideally we'd pass on stack, but this is simpler)

        # Actually, let's use stack properly:
        # The value is already on stack from PUSH
        # We need to duplicate it
        # Since we don't have DUP, store and load twice
        StackVM.STORE, 0xF0,    # 08: Store arg
        StackVM.LOAD, 0xF0,     # 0A: Load arg
        StackVM.LOAD, 0xF0,     # 0C: Load arg again
        StackVM.MUL,            # 0E: Multiply
        StackVM.RET             # 0F: Return
    ]

    vm = StackVM(debug=True)
    vm.load_program(program)
    vm.run()

    print("\n✓ Expected: 49 (7^2 = 49)")


def main():
    """Run all examples"""
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        example_add()
        example_factorial()
        example_subroutine()
    elif len(sys.argv) > 1:
        example_num = int(sys.argv[1])
        if example_num == 1:
            example_add()
        elif example_num == 2:
            example_factorial()
        elif example_num == 3:
            example_subroutine()
    else:
        print("Simple Stack VM Examples")
        print("========================\n")
        print("Usage:")
        print("  python simple_vm.py 1        # Run example 1 (addition)")
        print("  python simple_vm.py 2        # Run example 2 (factorial)")
        print("  python simple_vm.py 3        # Run example 3 (subroutine)")
        print("  python simple_vm.py --all    # Run all examples")
        print("\nRunning all examples:")
        print()
        example_add()
        example_factorial()
        example_subroutine()

    print("\n" + "="*60)
    print("Key Differences: Stack VM vs. Register VM (CHIP-8)")
    print("="*60)
    print("\nStack VM (this example):")
    print("  - Operations use implicit stack")
    print("  - ADD pops two values, pushes result")
    print("  - Compact bytecode")
    print("  - Examples: JVM, Python VM, WebAssembly")
    print("\nRegister VM (CHIP-8):")
    print("  - Operations specify registers explicitly")
    print("  - ADD V0, V1 reads from V0 and V1")
    print("  - Larger instructions but faster")
    print("  - Examples: Lua VM, most CPUs")
    print("\nBoth are valid designs with tradeoffs!")
    print("="*60)


if __name__ == '__main__':
    main()
