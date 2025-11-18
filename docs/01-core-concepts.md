# Core Emulation Concepts

## What Happens in an Emulator?

At its heart, an emulator is a **software simulation of hardware**. To understand emulation, we need to understand what we're simulating.

### The Von Neumann Architecture

Most computers follow the **Von Neumann architecture** (named after mathematician John von Neumann):

```
┌─────────────────────────────────────────┐
│              Computer System             │
├──────────────┬──────────────────────────┤
│     CPU      │         Memory           │
│  ┌────────┐  │  ┌──────────────────┐   │
│  │ Control│  │  │   Instructions   │   │
│  │  Unit  │  │  │      & Data      │   │
│  ├────────┤  │  └──────────────────┘   │
│  │  ALU   │  │                          │
│  ├────────┤  │                          │
│  │Registers│ │                          │
│  └────────┘  │                          │
└──────────────┴──────────────────────────┘
         │                    │
         └────────┬───────────┘
                  │
         ┌────────▼────────┐
         │   Input/Output  │
         │    Devices      │
         └─────────────────┘
```

**Key Components:**

1. **CPU (Central Processing Unit)**
   - **Control Unit**: Fetches and decodes instructions
   - **ALU (Arithmetic Logic Unit)**: Performs calculations
   - **Registers**: Ultra-fast storage inside CPU

2. **Memory**: Stores both instructions and data (RAM, ROM)

3. **I/O Devices**: Keyboard, display, sound, etc.

**Reference**: The [Nand to Tetris](https://www.nand2tetris.org/) course (free) builds this architecture from scratch. Chapters 4-5 are especially relevant.

## The Fetch-Decode-Execute Cycle

This is the **fundamental loop** that every CPU executes, billions of times per second:

```
     ┌──────────────┐
     │   FETCH      │  1. Read instruction from memory
     │              │     at address in PC (Program Counter)
     └──────┬───────┘
            │
     ┌──────▼───────┐
     │   DECODE     │  2. Figure out what the instruction means
     │              │     (e.g., "ADD two numbers")
     └──────┬───────┘
            │
     ┌──────▼───────┐
     │   EXECUTE    │  3. Perform the operation
     │              │     (actually do the ADD)
     └──────┬───────┘
            │
            │  4. Update PC (usually PC = PC + instruction_size)
            │
            └──────→ (repeat forever)
```

### Example: Adding Two Numbers

Let's trace through a simple ADD instruction:

```
Memory:
  0x200: 0x8014  <- ADD register V0 to register V1

Registers:
  V0 = 5
  V1 = 3
  PC = 0x200
```

**Step-by-step execution:**

1. **FETCH**: Read memory[0x200] → get `0x8014`
2. **DECODE**: Parse `0x8014` → "ADD V0 to V1, store in V1"
3. **EXECUTE**:
   - Read V0 (5)
   - Read V1 (3)
   - Calculate 5 + 3 = 8
   - Write 8 to V1
4. **UPDATE PC**: PC = 0x200 + 2 = 0x202

**Result**: V1 now contains 8, PC points to next instruction

**Book Reference**: "Code" by Charles Petzold (Chapters 16-17) brilliantly explains this without assuming prior knowledge.

## Opcodes and Instruction Sets

An **opcode** (operation code) is a binary number that tells the CPU what to do.

### Anatomy of an Instruction

```
Instruction:  0x8014
               │││└── Parameter: Register 4
               ││└─── Parameter: Register 1
               │└──── Parameter: Register 0
               └───── Opcode: 8 (arithmetic operation)
```

Different CPUs have different instruction formats:

**CHIP-8** (16-bit instructions):
```
0x6A0F
││││
││││
││└└── Value (0x0F = 15)
│└──── Register (A = 10)
└───── Opcode (6 = SET register)
Meaning: Set register V[A] to 15
```

**6502** (variable length, 1-3 bytes):
```
0xA9 0x0F
 │    │
 │    └── Immediate value (15)
 └────── Opcode (LDA = Load Accumulator)
Meaning: Load 15 into Accumulator
```

### Common Opcode Categories

Every CPU has similar categories of operations:

1. **Data Transfer**: Move data between registers/memory
   - LOAD, STORE, MOVE
   - Example: `LD A, 5` → Load 5 into register A

2. **Arithmetic**: Math operations
   - ADD, SUB, MUL, DIV
   - Example: `ADD A, B` → A = A + B

3. **Logical**: Boolean operations
   - AND, OR, XOR, NOT
   - Example: `AND A, B` → A = A & B (bitwise AND)

4. **Control Flow**: Change execution order
   - JUMP, CALL, RETURN
   - Example: `JMP 0x300` → Set PC to 0x300

5. **Bitwise**: Bit manipulation
   - SHIFT, ROTATE
   - Example: `SHL A` → Shift A left (multiply by 2)

**Reference**: [6502 Instruction Reference](http://www.6502.org/tutorials/6502opcodes.html) shows a real CPU's instruction set.

## Memory Organization

Memory is a giant array of bytes, but it's organized into regions:

```
CHIP-8 Memory Map (4KB total):
┌─────────────────┐ 0xFFF
│                 │
│   Program ROM   │ ← Your game code lives here
│                 │
├─────────────────┤ 0x200
│                 │
│  Interpreter    │ ← Reserved for CHIP-8 interpreter
│   & Font Data   │
│                 │
└─────────────────┘ 0x000

Each address holds 1 byte (8 bits)
Total: 4096 bytes (0x000 to 0xFFF)
```

### Addressing Modes

How do we specify which memory location to use?

1. **Immediate**: Value is in the instruction itself
   ```
   LD A, 5  ; Load literal value 5
   ```

2. **Direct**: Instruction contains memory address
   ```
   LD A, [0x300]  ; Load from address 0x300
   ```

3. **Indirect**: Instruction contains address of address (pointer!)
   ```
   LD A, [I]  ; Load from address stored in register I
   ```

4. **Indexed**: Base address + offset
   ```
   LD A, [I + 3]  ; Load from (I + 3)
   ```

**Book Reference**: "Computer Systems: A Programmer's Perspective" (CS:APP) Chapter 3 covers addressing in depth.

## Registers: The CPU's Workspace

**Registers** are tiny, ultra-fast memory locations inside the CPU.

### Why Registers?

- **Speed**: 100x+ faster than RAM
- **Size**: Usually 8-16 bits each
- **Count**: CPUs typically have 4-32 registers

### Common Register Types

1. **General Purpose**: Store temporary values
   ```
   CHIP-8: V0-VF (16 registers, 8-bit each)
   6502:   A, X, Y (3 registers)
   ```

2. **Program Counter (PC)**: Points to current instruction
   ```
   PC = 0x200  ; Next instruction is at address 0x200
   ```

3. **Stack Pointer (SP)**: Points to top of stack
   ```
   SP = 0x0F  ; Stack top is at level 15
   ```

4. **Index Register (I)**: Often used for memory addressing
   ```
   I = 0x500  ; Point to sprite data at 0x500
   ```

5. **Flags/Status Register**: Store condition bits
   ```
   VF = 1  ; Carry flag set (CHIP-8 uses V15 for this)
   ```

## The Stack: LIFO Memory

The **stack** is a Last-In-First-Out (LIFO) data structure used for:
- Function calls and returns
- Saving temporary values
- Nested execution

```
Stack Operation Example:

CALL 0x400  (call function at 0x400)
┌─────┐         ┌─────┐
│     │         │0x200│ ← PUSH return address
│     │         ├─────┤
│     │   →     │     │
│     │         │     │
└─────┘         └─────┘
SP = 0          SP = 1


RET  (return from function)
┌─────┐         ┌─────┐
│0x200│ ← POP   │     │
├─────┤         │     │
│     │   →     │     │
│     │         │     │
└─────┘         └─────┘
SP = 1          SP = 0
                PC = 0x200
```

**Reference**: [Stack explanation](http://www.emulator101.com/more-about-the-stack.html) from Emulator 101.

## Timers and Timing

Real hardware runs at a specific **clock speed** (e.g., 60 Hz, 4 MHz).

### Timing Concepts

1. **CPU Clock**: How fast the CPU executes instructions
   - CHIP-8: ~500-700 Hz (instructions per second)
   - 6502 (NES): 1.79 MHz
   - Modern CPU: 3+ GHz

2. **Refresh Rate**: How often the screen updates
   - CHIP-8: 60 Hz
   - Most displays: 60 Hz

3. **Timers**: Count down at fixed rate
   - CHIP-8 has two 60 Hz timers
   - Used for delays and sound

### Implementing Timing in an Emulator

```python
# Pseudo-code timing loop
target_hz = 500  # CHIP-8 CPU speed
cycle_time = 1.0 / target_hz  # Time per instruction

while emulator_running:
    start_time = current_time()

    # Execute one CPU cycle
    fetch_decode_execute()

    # Wait to maintain timing
    elapsed = current_time() - start_time
    if elapsed < cycle_time:
        sleep(cycle_time - elapsed)
```

## Emulation vs. Simulation vs. Virtualization

These terms are often confused:

### Emulation
**Imitates hardware at instruction level**
- Guest CPU ≠ Host CPU (different architectures)
- Example: Running CHIP-8 (custom CPU) on x86 PC
- Slower (must translate every instruction)

### Simulation
**Models behavior, not exact implementation**
- Focus on outcomes, not internal mechanics
- Example: Flight simulator (physics model, not actual plane circuits)
- Can be faster or slower

### Virtualization
**Runs same architecture with isolation**
- Guest CPU = Host CPU (same architecture)
- Example: VirtualBox running Linux on Linux
- Much faster (can execute directly)

## Levels of Emulation Accuracy

### Instruction-Level (Easiest)
- Execute instructions correctly
- Ignore timing, edge cases
- Good enough for many games

### Cycle-Accurate
- Replicate exact timing of original hardware
- Count CPU cycles precisely
- Required for some timing-sensitive software

### Gate-Level (Hardest)
- Simulate individual transistors/logic gates
- Research-level, extremely slow
- Used for hardware verification

**For beginners**: Instruction-level is perfect. Get it working first!

## Data Representation

Understanding how data is stored is crucial for emulation.

### Binary and Hexadecimal

```
Decimal: 255
Binary:  11111111 (8 bits)
Hex:     0xFF

Hex is compact representation of binary:
0xA5 = 1010 0101
       │││││││└─ 1
       ││││││└── 0
       │││││└─── 1
       ││││└──── 0
       │││└───── 0
       ││└────── 1
       │└─────── 0
       └──────── 1
```

### Bitwise Operations

Essential for decoding opcodes:

```python
opcode = 0x8014

# Extract nibbles (4-bit chunks)
first  = (opcode & 0xF000) >> 12  # 0x8
second = (opcode & 0x0F00) >> 8   # 0x0
third  = (opcode & 0x00F0) >> 4   # 0x1
fourth = (opcode & 0x000F)        # 0x4

# Common operations
a | b   # OR:  Combine bits
a & b   # AND: Mask bits
a ^ b   # XOR: Toggle bits
~a      # NOT: Invert bits
a << 1  # Shift left (multiply by 2)
a >> 1  # Shift right (divide by 2)
```

**Reference**: "But How Do It Know?" by J. Clark Scott explains binary arithmetic beautifully.

## Debugging Emulators

Emulators are complex and bugs are inevitable. Debugging strategies:

### 1. Logging
```python
def execute_opcode(opcode):
    print(f"PC: {PC:04X} | Opcode: {opcode:04X} | V0: {V[0]:02X}")
    # ... execute ...
```

### 2. Test ROMs
Use programs designed to test specific features:
- CHIP-8: BC_test.ch8, test_opcode.ch8
- Game Boy: Blargg's test ROMs
- NES: Various test suites

### 3. Compare with Reference
Run your emulator and a working emulator side-by-side:
```
Your emulator:     Reference:
PC: 0x200          PC: 0x200  ✓
V0: 0x05           V0: 0x05   ✓
V1: 0x03           V1: 0x03   ✓
After ADD:
V1: 0x07           V1: 0x08   ✗ BUG FOUND!
```

### 4. Step-Through Debugger
Execute one instruction at a time, inspect state.

## Common Emulator Bugs

### Off-by-One Errors
```python
# Wrong: misses last byte
for i in range(0, memory_size - 1):

# Correct
for i in range(0, memory_size):
```

### Endianness Confusion
```
Big-endian:    0x1234 stored as [0x12, 0x34]
Little-endian: 0x1234 stored as [0x34, 0x12]

CHIP-8 is big-endian!
```

### Sign Extension
```python
# If bit 7 is set, might be treated as negative
byte = 0xFF  # Could be 255 or -1!

# Ensure unsigned
byte = value & 0xFF
```

### Timer/Timing Issues
```python
# Wrong: timers never decrease!
if timer > 0:
    timer = timer - 1

# Correct: only decrease at 60 Hz
if timer > 0 and frame_counter % (CPU_HZ / 60) == 0:
    timer = timer - 1
```

## Next Steps

Now that you understand the fundamentals, let's dive into CPU emulation specifically.

**Continue to**: [02-cpu-emulation.md](02-cpu-emulation.md)

## Additional Resources

- **[Emulator 101](http://www.emulator101.com/)**: Build Space Invaders emulator (Intel 8080)
- **[CHIP-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM)**: Complete CHIP-8 specification
- **[Easy 6502](https://skilldrick.github.io/easy6502/)**: Interactive 6502 assembly tutorial
- **[/r/EmuDev Wiki](https://www.reddit.com/r/EmuDev/wiki/index)**: Community resources

## Practice Exercises

Before moving on, try these:

1. **Binary Practice**: Convert these by hand:
   - 0x6A0F to binary
   - 0b10110011 to hex
   - 255 to binary and hex

2. **Opcode Decoding**: Given `0x7305`, extract:
   - First nibble
   - Register number (second nibble)
   - Byte value (last two nibbles)

3. **Fetch-Execute**: Trace through these instructions:
   ```
   0x6100  ; Set V1 = 0
   0x6205  ; Set V2 = 5
   0x8124  ; V1 = V1 + V2
   ```
   What is V1 at the end?

**Answers**:
1. 0x6A0F = 0110 1010 0000 1111; 0b10110011 = 0xB3; 255 = 0b11111111 = 0xFF
2. 0x7 (opcode), 0x3 (register), 0x05 (value)
3. V1 = 5

---

**Ready to build a CPU?** Head to [02-cpu-emulation.md](02-cpu-emulation.md)!
