# Memory Systems in Emulation

Understanding memory is crucial for emulation. This guide explains how memory works in computers and how to emulate it.

## What is Memory?

**Memory** is an array of bytes that stores both instructions (code) and data. Think of it as a giant series of numbered boxes:

```
Address    Value     Description
┌─────┐   ┌────┐
│ 0x0 │ → │ 61 │    Instruction byte 1
├─────┤   ├────┤
│ 0x1 │ → │ 23 │    Instruction byte 2
├─────┤   ├────┤
│ 0x2 │ → │ A3 │    Next instruction...
├─────┤   ├────┤
│ 0x3 │ → │ 00 │
├─────┤   ├────┤
│ ... │   │... │
└─────┘   └────┘
```

## Memory in CHIP-8

CHIP-8 has a simple memory layout:

```
╔═════════════════════════════════════╗
║  CHIP-8 Memory Map (4KB total)     ║
╠═════════════════════════════════════╣
║                                     ║
║  0xFFF ┌──────────────────┐         ║
║        │                  │         ║
║        │   Program ROM    │         ║
║        │   & Work RAM     │         ║
║        │                  │         ║
║  0x200 ├──────────────────┤ ← PC    ║
║        │ Reserved for     │ starts  ║
║        │ Interpreter      │ here    ║
║  0x050 ├──────────────────┤         ║
║        │   Font Data      │         ║
║        │  (0-F sprites)   │         ║
║  0x000 └──────────────────┘         ║
║                                     ║
╚═════════════════════════════════════╝
```

### Memory Regions

**0x000-0x1FF: Reserved (512 bytes)**
- CHIP-8 interpreter space
- Font sprites (0x050-0x09F)
- Not used by most programs

**0x200-0xFFF: Program Space (3584 bytes)**
- ROM loaded here
- Programs can use this as RAM too
- Maximum program size: ~3.5 KB

### Implementing Memory

In Python, memory is simply a list:

```python
class CHIP8:
    def __init__(self):
        # Memory: 4096 bytes (0x000 to 0xFFF)
        self.memory = [0] * 4096

    def read_byte(self, address):
        """Read a byte from memory"""
        return self.memory[address & 0xFFF]  # Mask to 12 bits

    def write_byte(self, address, value):
        """Write a byte to memory"""
        self.memory[address & 0xFFF] = value & 0xFF  # Ensure 8-bit
```

**Why mask addresses?** To ensure addresses wrap around if they go out of bounds.

## Memory Addressing

### Address Bus Width

The **address bus** determines how much memory can be accessed:

- **12-bit address bus**: Can address 2^12 = 4096 bytes (4KB) ← CHIP-8
- **16-bit address bus**: Can address 2^16 = 65536 bytes (64KB) ← 6502
- **32-bit address bus**: Can address 2^32 = 4GB
- **64-bit address bus**: Can address 2^64 = 16 EB (exabytes!)

CHIP-8 uses 12-bit addresses (0x000 to 0xFFF).

### Endianness

**Endianness** is the order in which multi-byte values are stored:

#### Big-Endian (CHIP-8, 6502, Network order)
Most significant byte first:
```
Value: 0x1234

Address  Value
  0x200   12   ← High byte first
  0x201   34   ← Low byte second
```

#### Little-Endian (x86, ARM)
Least significant byte first:
```
Value: 0x1234

Address  Value
  0x200   34   ← Low byte first
  0x201   12   ← High byte second
```

**Reading big-endian in CHIP-8**:
```python
def read_word(self, address):
    """Read 16-bit big-endian word"""
    high = self.memory[address]
    low = self.memory[address + 1]
    return (high << 8) | low
```

**Mnemonic**: Big-endian = Big end first (most significant byte)

**Reference**: "Computer Organization and Design" by Patterson & Hennessy covers endianness in detail.

## Addressing Modes

How instructions specify which memory to access:

### 1. Immediate Addressing
Value is in the instruction itself:
```
CHIP-8: 6A0F  (LD VA, 0x0F)
                    ↑
              Value is here
```

No memory access needed!

### 2. Direct Addressing
Instruction contains the address:
```
6502: LDA $0200  (Load from address 0x200)
           ↑
      Address is here
```

```python
def op_load_direct(self, address):
    self.A = self.memory[address]
```

### 3. Indirect Addressing
Instruction points to address that contains the address (pointer!):
```
CHIP-8: FX65  (Load V0-VX from memory[I])
                                       ↑
                        I contains the address
```

```python
def op_FX65(self, x):
    for i in range(x + 1):
        self.V[i] = self.memory[self.I + i]
                                 ↑
                    I is the address
```

### 4. Indexed Addressing
Base address + offset:
```
CHIP-8: FX65 with I = 0x300
  Read from: 0x300, 0x301, 0x302, ...
             (base)  (base+1) (base+2)
```

```python
for i in range(x + 1):
    address = self.I + i  # Base + offset
    self.V[i] = self.memory[address]
```

## Memory Access Patterns

### Sequential Access (Loading ROM)
```python
def load_rom(self, filepath):
    with open(filepath, 'rb') as f:
        rom_data = f.read()

    # Sequential write to memory
    for i, byte in enumerate(rom_data):
        self.memory[0x200 + i] = byte
```

### Random Access (Instruction Fetch)
```python
def fetch_instruction(self):
    # Can jump anywhere in memory
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
    return opcode
```

### Block Transfer (FX55/FX65)
```python
def op_FX55(self, x):
    """Store V0-VX in memory starting at I"""
    # Block write
    for i in range(x + 1):
        self.memory[self.I + i] = self.V[i]
```

## Memory-Mapped I/O

In real systems, memory addresses can map to hardware devices!

```
Example: NES Memory Map
┌────────────────────────────┐
│ 0xFFFF                     │
│   ┌────────────────┐       │
│   │  Cartridge ROM │       │
│   └────────────────┘       │
│ 0x8000                     │
│   ┌────────────────┐       │
│   │   Save RAM     │       │
│   └────────────────┘       │
│ 0x6000                     │
│   ┌────────────────┐       │
│   │ I/O Registers  │ ← Controller, PPU, etc.
│   └────────────────┘       │
│ 0x2000                     │
│   ┌────────────────┐       │
│   │   Work RAM     │       │
│   └────────────────┘       │
│ 0x0000                     │
└────────────────────────────┘
```

Writing to certain addresses triggers hardware actions!

```python
# Example: Writing to PPU control register
def write_byte(self, address, value):
    if address == 0x2000:  # PPU control
        self.ppu.set_control(value)
    elif address == 0x2001:  # PPU mask
        self.ppu.set_mask(value)
    else:
        self.memory[address] = value
```

CHIP-8 doesn't have memory-mapped I/O (display is separate), but more advanced systems do.

## Memory Banking

When you need more memory than can be addressed:

**Problem**: 16-bit address bus only addresses 64KB, but cartridge has 256KB!

**Solution**: Bank switching!

```
┌─────────────────────────────────┐
│    Addressable Memory (64KB)    │
├─────────────────────────────────┤
│  0xFFFF                          │
│    ┌──────────────┐              │
│    │  Bank 2      │ ← Currently  │
│    │  (16KB)      │   mapped     │
│    └──────────────┘              │
│  0xC000                          │
│    ┌──────────────┐              │
│    │  Bank 1      │              │
│    │  (16KB)      │              │
│    └──────────────┘              │
│  ...                             │
└─────────────────────────────────┘

Cartridge has 16 banks!
Write to control register to switch which bank is visible.
```

**Implementation**:
```python
class Cartridge:
    def __init__(self, rom_data):
        # Divide ROM into 16KB banks
        self.banks = []
        for i in range(0, len(rom_data), 16384):
            self.banks.append(rom_data[i:i+16384])

        self.current_bank = 0

    def read(self, address):
        bank_offset = address - 0xC000
        return self.banks[self.current_bank][bank_offset]

    def switch_bank(self, bank_number):
        self.current_bank = bank_number
```

Game Boy and NES use extensive bank switching!

## Cache (Advanced)

Real CPUs have cache to speed up memory access:

```
CPU ← L1 Cache (32KB, 1 cycle)
      ↓ miss
    L2 Cache (256KB, 10 cycles)
      ↓ miss
    L3 Cache (8MB, 40 cycles)
      ↓ miss
    RAM (16GB, 100+ cycles)
```

**For emulation**: Usually not necessary to emulate cache. Most systems are too old to have it, or we can ignore it for functional emulation.

## Virtual Memory (Way Advanced)

Modern systems use virtual memory:

```
Program sees:        Actually uses:
┌──────────┐        ┌──────────┐
│ 0xFFFF   │  map   │ Phys     │
│  ...     │  ───→  │ addr     │
│ 0x0000   │        │ varies   │
└──────────┘        └──────────┘
     ↑
  Virtual              Physical
```

**For emulation**: Usually don't emulate this either. Guest system has its own virtual memory, host handles ours.

## Memory Access Optimization

### Bounds Checking

Always check memory access:

```python
def read_byte(self, address):
    if address < 0 or address >= len(self.memory):
        raise MemoryError(f"Invalid read at 0x{address:X}")
    return self.memory[address]
```

In production, mask instead (faster):
```python
def read_byte(self, address):
    return self.memory[address & 0xFFF]  # Wrap around
```

### Direct Access vs. Methods

**Slower** (function call overhead):
```python
value = self.read_byte(0x200)
```

**Faster** (direct access):
```python
value = self.memory[0x200]
```

Use direct access in tight loops (fetch-decode-execute).

## Memory in Other Systems

### 6502 (NES, Apple II)
- **64KB total** (0x0000-0xFFFF)
- Memory-mapped I/O
- No built-in ROM (loads from cartridge)

### Game Boy
- **64KB addressable**
- Bank switching for larger ROMs
- Separate VRAM, OAM, HRAM
- Complex memory map

### x86 (original)
- **1MB addressable** (20-bit address bus)
- Segmented memory
- Real mode vs. protected mode

## Practical Exercise

Implement a memory inspector:

```python
def inspect_memory(self):
    """Interactive memory browser"""
    address = 0x200

    while True:
        # Show 16 bytes
        print(f"\nAddress 0x{address:03X}:")
        for i in range(16):
            byte = self.memory[address + i]
            print(f"  {address+i:03X}: {byte:02X} ({byte:3d}) {chr(byte) if 32 <= byte < 127 else '.'}")

        cmd = input("\nCommand (n=next, p=prev, g=goto, q=quit): ")

        if cmd == 'n':
            address = (address + 16) & 0xFFF
        elif cmd == 'p':
            address = (address - 16) & 0xFFF
        elif cmd.startswith('g'):
            address = int(cmd[1:].strip(), 16) & 0xFFF
        elif cmd == 'q':
            break
```

Try it! Load a ROM and browse through memory.

## Summary

Key concepts:
- Memory is an array of bytes
- Addresses are indices into this array
- Different regions have different purposes
- Endianness matters for multi-byte values
- Addressing modes determine how to access memory
- More complex systems use banking, memory-mapped I/O, etc.

**Next**: [04-building-chip8.md](04-building-chip8.md) - Put it all together!

## Resources

- **"Code" by Charles Petzold**: Chapter 16 (Memory)
- **"Computer Organization and Design"**: Chapter 2 (Memory Hierarchy)
- **[Memory Addressing Tutorial](http://www.emulator101.com/memory-addressing.html)**: Practical examples
- **[6502 Memory Map](https://www.pagetable.com/c64ref/c64mem/)**: Real-world example

---

**Practice**: Try implementing bank switching for a hypothetical 8KB CHIP-8 variant with two 4KB banks!
