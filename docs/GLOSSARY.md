# Emulation & Computer Architecture Glossary

A comprehensive reference for technical terms used in emulation and computer architecture.

## A

**Address Bus**
- The set of wires/connections that carry memory addresses from the CPU to memory
- Width determines addressable memory (8-bit = 256 bytes, 16-bit = 64KB, etc.)
- Example: CHIP-8 has a 12-bit address bus (4096 bytes addressable)

**ALU (Arithmetic Logic Unit)**
- The part of the CPU that performs arithmetic (ADD, SUB) and logic (AND, OR, XOR) operations
- Takes inputs from registers, performs operation, outputs result
- Example: When you execute `ADD V0, V1`, the ALU adds the values

**Addressing Mode**
- The method by which an instruction specifies where its operands are located
- Types: Immediate, Direct, Indirect, Indexed, Register
- Example: `LD V0, 5` uses immediate addressing (value in instruction)

**Assembler**
- A program that converts assembly language to machine code
- Translates mnemonics (like `ADD`) to opcodes (like `0x8014`)
- Example: [Octo](https://johnearnest.github.io/Octo/) is a CHIP-8 assembler

## B

**Big-Endian**
- Byte order where most significant byte is stored first
- Example: 0x1234 stored as [0x12, 0x34]
- CHIP-8, 6502, and network protocols use big-endian
- Opposite: Little-endian

**Binary**
- Base-2 number system using only 0 and 1
- Fundamental to all computer systems
- Example: Decimal 5 = Binary 0101

**Bit**
- Smallest unit of data (0 or 1)
- 8 bits = 1 byte
- Example: Register VF has 8 bits (can hold values 0-255)

**Bitwise Operation**
- Operations that work on individual bits
- Types: AND (&), OR (|), XOR (^), NOT (~), shift (<<, >>)
- Example: `0b1010 & 0b1100 = 0b1000`

**Branch**
- An instruction that can change the program counter conditionally
- Tests a condition and jumps if true
- Example: `SE V0, 5` skips next instruction if V0 == 5

**Byte**
- 8 bits, can represent 0-255 (unsigned) or -128 to 127 (signed)
- Fundamental unit of memory addressing
- Example: Each CHIP-8 register holds one byte

**Bytecode**
- Binary instructions for a virtual machine
- More portable than native machine code
- Example: Java bytecode, Python bytecode, CHIP-8 ROM

## C

**Cache**
- Fast memory between CPU and RAM
- Stores frequently accessed data
- Levels: L1 (fastest), L2, L3
- Not present in simple systems like CHIP-8

**Call Stack**
- Stack used to store return addresses for function calls
- Allows nested function calls
- Example: CHIP-8 has 16-level call stack

**Clock Cycle**
- One tick of the CPU clock
- Modern CPUs: billions per second (GHz)
- CHIP-8: typically 500-700 per second

**Clock Speed**
- Rate at which CPU executes instructions
- Measured in Hz (cycles per second)
- Example: CHIP-8 runs at ~500Hz, modern CPUs at ~3GHz

**Control Unit**
- Part of CPU that directs operations
- Fetches instructions, decodes them, controls execution
- The "brain" that coordinates everything

**CPU (Central Processing Unit)**
- The main processor that executes instructions
- Contains: Control Unit, ALU, Registers
- Example: CHIP-8 CPU, Intel 8080, ARM Cortex

**Cycle-Accurate**
- Emulation that matches the timing of original hardware exactly
- Every instruction takes the correct number of clock cycles
- Required for some timing-sensitive programs

## D

**Decoder**
- Circuit or code that interprets opcodes
- Determines what operation to perform
- Example: Switch statement that handles different CHIP-8 opcodes

**Direct Addressing**
- Addressing mode where instruction contains the exact memory address
- Example: `LD I, 0x300` directly specifies address 0x300

**Disassembler**
- Tool that converts machine code back to assembly
- Reverse of an assembler
- Example: `0x6105` → `LD V1, 5`

**Display Buffer**
- Area of memory that holds what should be shown on screen
- Often directly mapped to pixels
- Example: CHIP-8 has 64×32 pixel display buffer

## E

**Emulation**
- Software that mimics hardware behavior
- Translates guest instructions to host instructions
- Slower than native but enables cross-platform compatibility

**Emulator**
- A program that performs emulation
- Example: Our CHIP-8 emulator, Dolphin (GameCube), MAME (arcade)

**Endianness**
- Byte order in multi-byte values
- Big-endian: Most significant byte first
- Little-endian: Least significant byte first

## F

**Fetch-Decode-Execute Cycle**
- The fundamental loop of all CPUs
1. Fetch: Read instruction from memory
2. Decode: Figure out what it means
3. Execute: Perform the operation
- Repeats billions of times per second

**Flag Register**
- Register that stores condition flags
- Flags: Carry, Zero, Overflow, Negative, etc.
- Example: CHIP-8 uses VF as flag register

**Framebuffer**
- Memory area holding pixel data for display
- Direct mapping: memory → screen
- Example: CHIP-8's 64×32 pixel array

## H

**Hexadecimal (Hex)**
- Base-16 number system (0-9, A-F)
- Compact representation of binary
- Example: 0xFF = 255 decimal = 11111111 binary

**HLE (High-Level Emulation)**
- Emulating functionality rather than hardware
- Faster but less accurate
- Example: Emulating BIOS calls directly instead of running BIOS code

## I

**I/O (Input/Output)**
- Communication between CPU and external devices
- Input: Keyboard, mouse, sensors
- Output: Display, sound, motors
- Example: CHIP-8 keyboard (16 keys) and display (64×32 pixels)

**Immediate Addressing**
- Value is part of the instruction itself
- No memory access needed (fast!)
- Example: `LD V0, 5` - the 5 is immediate

**Indirect Addressing**
- Instruction contains address of address (pointer)
- Example: `LD V0, [I]` - loads from address stored in I

**Instruction**
- A single command the CPU can execute
- Encoded as opcode + operands
- Example: `0x6105` is the CHIP-8 instruction "LD V1, 5"

**Instruction Set Architecture (ISA)**
- The complete set of instructions a CPU can execute
- Defines opcodes, registers, addressing modes
- Examples: CHIP-8 (35 instructions), x86, ARM, RISC-V

**Interpreter**
- Program that executes code without compiling
- Reads and executes instructions one at a time
- Example: Our CHIP-8 emulator is an interpreter

**Interrupt**
- Signal that causes CPU to pause and handle an event
- Types: Hardware (timer, input) and Software (system calls)
- Example: NES generates interrupt 60 times per second for display

## J

**JIT (Just-In-Time Compilation)**
- Translating code to native machine code at runtime
- Much faster than interpretation
- Example: JavaScript JIT, Java JIT, some emulators

**Jump**
- Instruction that changes the program counter
- Unconditional: Always jumps
- Conditional: Jumps if condition is true
- Example: `JP 0x300` sets PC to 0x300

## L

**LIFO (Last In, First Out)**
- Stack behavior: Last pushed is first popped
- Like a stack of plates
- Example: Call stack, operand stack

**Little-Endian**
- Byte order where least significant byte is stored first
- Example: 0x1234 stored as [0x34, 0x12]
- x86/x64 CPUs use little-endian

**Load**
- Read data from memory into a register
- Example: `LD V0, [I]` loads byte from address I into V0

## M

**Machine Code**
- Binary instructions directly executed by CPU
- What assembly assembles to
- Example: CHIP-8 ROM file contains machine code

**Memory-Mapped I/O**
- Using memory addresses to access I/O devices
- Reading/writing memory actually controls hardware
- Example: Many systems map display to specific memory region

**Mnemonic**
- Human-readable instruction name
- Example: `ADD` instead of `0x8004`

## N

**Nibble**
- 4 bits (half a byte)
- Can represent 0-15 (0x0-0xF)
- Example: CHIP-8 opcodes are decoded nibble by nibble

**NOP (No Operation)**
- Instruction that does nothing
- Used for timing, padding, or placeholders
- Example: `0x0000` in some CPUs

## O

**Opcode (Operation Code)**
- Numeric code representing an instruction
- What the CPU actually executes
- Example: `0x6105` is opcode for "LD V1, 5"

**Operand**
- Data that an instruction operates on
- Can be register, memory address, or immediate value
- Example: In `ADD V0, V1`, V0 and V1 are operands

## P

**PC (Program Counter)**
- Register that holds address of next instruction
- Automatically incremented after each instruction
- Jumps/calls modify it directly
- Example: CHIP-8 PC starts at 0x200

**Pipeline**
- Technique where multiple instructions are processed simultaneously
- Like assembly line
- Increases throughput
- Not used in simple CPUs like CHIP-8

**Pointer**
- Variable that stores a memory address
- Used for indirect addressing
- Example: CHIP-8's I register is a pointer

**Pop**
- Remove and return top value from stack
- Opposite of push
- Example: `RET` pops return address from stack

**Push**
- Add value to top of stack
- Opposite of pop
- Example: `CALL` pushes return address onto stack

## R

**RAM (Random Access Memory)**
- Volatile memory for storing programs and data
- Fast but lost when power off
- Example: CHIP-8 has 4KB of RAM

**Register**
- Fast storage location inside CPU
- Much faster than RAM
- Example: CHIP-8 has 16 8-bit registers (V0-VF)

**RISC (Reduced Instruction Set Computer)**
- CPU design with simple, regular instructions
- Easier to implement and optimize
- Examples: ARM, RISC-V, MIPS

**ROM (Read-Only Memory)**
- Non-volatile memory, can't be written
- Stores firmware, games, etc.
- Example: CHIP-8 game stored in ROM file

## S

**Signed**
- Number representation that includes negative values
- 8-bit signed: -128 to 127
- Uses two's complement
- Example: -1 = 0xFF in 8-bit signed

**Simulation**
- Modeling behavior without exact implementation
- Focuses on results, not internal mechanics
- Different from emulation (which models hardware)

**SP (Stack Pointer)**
- Register pointing to top of stack
- Incremented on push, decremented on pop
- Example: CHIP-8 SP ranges from 0-15

**Stack**
- LIFO data structure
- Used for function calls, temporary storage
- Example: CHIP-8 call stack stores return addresses

**Store**
- Write data from register to memory
- Opposite of load
- Example: `LD [I], V0` stores V0 at address I

**Subroutine**
- Reusable section of code (function)
- Called with CALL, returns with RET
- Example: CHIP-8 supports nested subroutines

## T

**Timer**
- Hardware that counts at fixed rate
- Used for delays, timing, periodic events
- Example: CHIP-8 has delay timer and sound timer (both 60Hz)

**Two's Complement**
- Method for representing signed integers
- Negative numbers: Invert bits and add 1
- Example: -5 = ~5 + 1 = ~0000_0101 + 1 = 1111_1011

## U

**Unsigned**
- Number representation with no negative values
- 8-bit unsigned: 0 to 255
- Example: CHIP-8 registers hold unsigned bytes

## V

**Virtual Machine (VM)**
- Software that emulates a computer
- Provides abstraction layer between code and hardware
- Examples: JVM, .NET CLR, CHIP-8 emulator

**Virtualization**
- Running same architecture with isolation
- Guest and host use same instruction set
- Much faster than emulation
- Example: VirtualBox, VMware

**Von Neumann Architecture**
- Computer design with shared memory for code and data
- Most computers use this
- Named after John von Neumann

## W

**Word**
- Natural data size of CPU
- 8-bit CPU: 1 byte word
- 16-bit CPU: 2 byte word
- 64-bit CPU: 8 byte word

## X

**XOR (Exclusive OR)**
- Bitwise operation: 1 if bits differ, 0 if same
- Useful for toggling bits, comparing values
- Example: `a ^ a = 0` (anything XOR itself is zero)

## Numbers & Symbols

**0x Prefix**
- Indicates hexadecimal number
- Example: 0xFF = 255 decimal

**0b Prefix**
- Indicates binary number
- Example: 0b1010 = 10 decimal

**& (AND operator)**
- Bitwise AND operation
- Used for masking bits
- Example: `0xFF & 0x0F = 0x0F` (isolate low nibble)

**| (OR operator)**
- Bitwise OR operation
- Used for combining bits
- Example: `0xF0 | 0x0F = 0xFF`

**^ (XOR operator)**
- Bitwise XOR operation
- Used for toggling bits
- Example: `0xAA ^ 0xFF = 0x55`

**~ (NOT operator)**
- Bitwise NOT operation (invert all bits)
- Example: `~0x00 = 0xFF`

**<< (Left Shift)**
- Shift bits left (multiply by 2 per shift)
- Example: `5 << 1 = 10` (0101 → 1010)

**>> (Right Shift)**
- Shift bits right (divide by 2 per shift)
- Example: `10 >> 1 = 5` (1010 → 0101)

---

## Quick Reference by Category

### Number Systems
- Binary, Hexadecimal, Decimal
- Signed vs Unsigned
- Bit, Nibble, Byte, Word
- Endianness

### CPU Components
- ALU, Control Unit, Registers
- Program Counter, Stack Pointer
- Instruction Decoder

### Memory
- RAM, ROM
- Address Bus, Data Bus
- Memory-Mapped I/O
- Cache

### Instructions
- Opcode, Operand
- Mnemonic
- Addressing Modes
- Fetch-Decode-Execute

### Emulation Techniques
- Interpreter vs JIT
- Cycle-Accurate vs HLE
- Simulation vs Emulation

### Data Structures
- Stack (LIFO)
- Buffer
- Framebuffer

### Operations
- Arithmetic: ADD, SUB, MUL, DIV
- Logic: AND, OR, XOR, NOT
- Bitwise: Shift, Mask
- Control: Jump, Call, Return

---

**Additional Resources:**
- [Wikipedia - Computer Architecture](https://en.wikipedia.org/wiki/Computer_architecture)
- [OSDev Wiki](https://wiki.osdev.org/)
- [Computer Science Glossary](https://www.cs.cmu.edu/~adamchik/15-121/glossary.html)
