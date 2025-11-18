# Testing and Debugging Your Emulator

Building an emulator is complex, and bugs are inevitable. This guide teaches you how to find and fix them.

## Testing Strategy

### 1. Start Small
Don't load a complex game first! Build up gradually:

```
✓ Step 1: Test basic opcodes (6XNN, 7XNN, ANNN)
✓ Step 2: Test control flow (1NNN, 2NNN, 00EE)
✓ Step 3: Test arithmetic (8XY4, 8XY5)
✓ Step 4: Test graphics (DXYN)
✓ Step 5: Test input (EX9E, FX0A)
✓ Step 6: Test full games
```

### 2. Use Test ROMs
Don't rely on games alone. Use purpose-built test programs:

**Essential Test ROMs**:
1. **[Timendus CHIP-8 Test Suite](https://github.com/Timendus/chip8-test-suite)** ⭐
   - Tests all opcodes systematically
   - Visual pass/fail indicators
   - Tests quirks and edge cases
   - **Start here!**

2. **BC_test.ch8**
   - Tests all 35 opcodes
   - Shows which ones fail

3. **test_opcode.ch8**
   - Visual tests for each instruction
   - Helps verify graphics and timing

### 3. Compare with Reference
Run the same ROM on:
- Your emulator (with debug logging)
- A known-good emulator (e.g., [Octo](https://johnearnest.github.io/Octo/))

Compare execution step-by-step.

## Debug Logging

### Basic Logging

Add logging to your `cycle()` method:

```python
def cycle(self):
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

    # Log every instruction
    self.log_state(opcode)

    self.pc += 2
    self.execute_opcode(opcode)

def log_state(self, opcode):
    """Print CPU state before executing instruction"""
    regs = ' '.join(f'{v:02X}' for v in self.V)
    print(f"PC:{self.pc:03X} OP:{opcode:04X} I:{self.I:03X} V:[{regs}]")
```

**Output**:
```
PC:200 OP:6005 I:000 V:[00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00]
PC:202 OP:610A I:000 V:[05 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00]
PC:204 OP:7003 I:000 V:[05 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00]
```

### Detailed Logging

Add opcode mnemonics:

```python
def log_instruction(self, opcode, description):
    """Log with human-readable instruction name"""
    regs = ' '.join(f'{v:02X}' for v in self.V)
    print(f"PC:{self.pc:03X} {description:20} | I:{self.I:03X} | V:[{regs}]")

# In execute_opcode:
def op_6XNN(self, x, nn):
    """6XNN: Set VX = NN"""
    if self.debug:
        self.log_instruction(opcode, f"LD V{x:X}, 0x{nn:02X}")
    self.V[x] = nn
```

**Output**:
```
PC:200 LD V0, 0x05         | I:000 | V:[00 00 00 00 ...]
PC:202 LD V1, 0x0A         | I:000 | V:[05 00 00 00 ...]
PC:204 ADD V0, 0x03        | I:000 | V:[05 0A 00 00 ...]
```

### Conditional Logging

Don't log everything always (too slow). Use flags:

```python
class CHIP8:
    def __init__(self, debug=False, log_opcodes=False):
        self.debug = debug
        self.log_opcodes = log_opcodes

# Usage
emulator = CHIP8(debug=True, log_opcodes=True)
```

## Debugging Techniques

### 1. Step-Through Execution

Execute one instruction at a time:

```python
def run_debug(self):
    """Debug mode: press Enter to execute each instruction"""
    print("Debug mode: Press Enter to step, 'q' to quit")

    while self.running:
        # Show state before execution
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.log_state(opcode)

        # Wait for user input
        user_input = input("→ ")
        if user_input.lower() == 'q':
            break

        # Execute one cycle
        self.cycle()
```

### 2. Breakpoints

Stop execution at specific addresses:

```python
def cycle(self):
    # Check breakpoints
    if self.pc in self.breakpoints:
        print(f"\n🔴 Breakpoint hit at 0x{self.pc:03X}")
        self.debug_shell()

    # Normal execution
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
    self.pc += 2
    self.execute_opcode(opcode)

def debug_shell(self):
    """Interactive debug shell"""
    while True:
        cmd = input("debug> ").strip().split()

        if not cmd:
            continue

        if cmd[0] == 'c':  # Continue
            break
        elif cmd[0] == 's':  # Step
            self.cycle()
        elif cmd[0] == 'r':  # Show registers
            self.print_registers()
        elif cmd[0] == 'm':  # Show memory
            addr = int(cmd[1], 16)
            self.print_memory(addr, 16)
        elif cmd[0] == 'h':  # Help
            print("Commands: c (continue), s (step), r (registers), m <addr> (memory), h (help)")
```

### 3. Memory Dumps

Inspect memory at any address:

```python
def print_memory(self, start, length):
    """Print memory in hex dump format"""
    print(f"\nMemory at 0x{start:03X}:")

    for i in range(0, length, 16):
        addr = start + i
        # Get 16 bytes
        bytes_row = self.memory[addr:addr+16]

        # Format as hex
        hex_str = ' '.join(f'{b:02X}' for b in bytes_row)

        # Format as ASCII (printable chars only)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in bytes_row)

        print(f"  {addr:03X}: {hex_str:47} | {ascii_str}")
```

**Output**:
```
Memory at 0x200:
  200: 60 05 61 0A 70 03 A3 00 71 05 00 00 00 00 00 00 | `.a.p....q......
  210: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | ................
```

### 4. Display State

Show what's on screen (for debugging graphics):

```python
def print_display(self):
    """Print display buffer as ASCII art"""
    print("\n╔" + "═" * 64 + "╗")

    for row in self.display:
        line = ''.join('█' if pixel else ' ' for pixel in row)
        print(f"║{line}║")

    print("╚" + "═" * 64 + "╝\n")
```

### 5. Watch Variables

Track when specific registers change:

```python
class CHIP8:
    def __init__(self):
        # ... normal init ...
        self.watches = {'V0': None, 'I': None}  # Watch V0 and I

    def set_register(self, index, value):
        """Wrapper for register writes with watch support"""
        old_value = self.V[index]

        if old_value != value and f'V{index:X}' in self.watches:
            print(f"⚠ V{index:X} changed: {old_value:02X} → {value:02X}")

        self.V[index] = value
```

## Common Bugs and Fixes

### Bug 1: Opcode Fetching Wrong Endianness

**Symptom**: Every instruction is gibberish

**Wrong**:
```python
opcode = self.memory[self.pc] | (self.memory[self.pc + 1] << 8)  # Little-endian ❌
```

**Right**:
```python
opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]  # Big-endian ✓
```

**How to detect**:
```python
# Load test ROM and check first opcode
rom = [0x60, 0x05]  # Should be 0x6005
opcode = (rom[0] << 8) | rom[1]
print(f"{opcode:04X}")  # Should print "6005", not "0560"
```

### Bug 2: PC Incremented Twice

**Symptom**: Emulator skips every other instruction

**Wrong**:
```python
def cycle(self):
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
    self.pc += 2
    self.execute_opcode(opcode)

def op_1NNN(self, nnn):
    self.pc = nnn + 2  # ❌ Adding 2 again!
```

**Right**:
```python
def op_1NNN(self, nnn):
    self.pc = nnn  # ✓ Just set PC
```

**How to detect**: Log PC before and after each instruction. If it jumps by 4 instead of 2, you're incrementing twice.

### Bug 3: Carry Flag Not Set

**Symptom**: Arithmetic opcodes fail tests

**Wrong**:
```python
def op_8XY4(self, x, y):
    self.V[x] = (self.V[x] + self.V[y]) & 0xFF  # ❌ Forgot VF!
```

**Right**:
```python
def op_8XY4(self, x, y):
    result = self.V[x] + self.V[y]
    self.V[0xF] = 1 if result > 255 else 0  # ✓ Set carry
    self.V[x] = result & 0xFF
```

**How to detect**: Test ROM specifically for flags (flags_test.ch8)

### Bug 4: Sprite Drawing XOR Missing

**Symptom**: Sprites don't erase when drawn twice

**Wrong**:
```python
if sprite_pixel == 1:
    self.display[y][x] = 1  # ❌ Always set to 1
```

**Right**:
```python
if sprite_pixel == 1:
    self.display[y][x] ^= 1  # ✓ XOR (toggle)
```

**How to detect**: Draw the same sprite twice. It should disappear.

### Bug 5: Timer Not Decrementing

**Symptom**: Delays never end

**Wrong**:
```python
def update_timers(self):
    if self.delay_timer > 0:
        self.delay_timer - 1  # ❌ Forgot assignment!
```

**Right**:
```python
def update_timers(self):
    if self.delay_timer > 0:
        self.delay_timer -= 1  # ✓ Decrement
```

**How to detect**: Set delay timer to 10, count frames. Should reach 0 in 10 frames (at 60 FPS).

### Bug 6: Stack Overflow/Underflow

**Symptom**: Crashes on deep subroutine calls

**Wrong**:
```python
def op_2NNN(self, nnn):
    self.sp += 1
    self.stack[self.sp] = self.pc  # ❌ SP already incremented!
    self.pc = nnn
```

**Right**:
```python
def op_2NNN(self, nnn):
    self.stack[self.sp] = self.pc  # ✓ Store at current SP
    self.sp += 1                   # Then increment
    self.pc = nnn
```

**How to detect**: Add bounds checking:
```python
if self.sp >= 16:
    raise RuntimeError(f"Stack overflow! SP={self.sp}")
if self.sp < 0:
    raise RuntimeError(f"Stack underflow! SP={self.sp}")
```

### Bug 7: Signed vs Unsigned

**Symptom**: Negative numbers appear

**Wrong**:
```python
self.V[x] = self.V[x] - self.V[y]  # May go negative! ❌
```

**Right**:
```python
self.V[x] = (self.V[x] - self.V[y]) & 0xFF  # ✓ Wrap to 0-255
```

**How to detect**: All register values should be 0-255. If you see negative numbers, you have a sign issue.

## Test-Driven Development

Write tests before (or alongside) implementation:

```python
import unittest

class TestCHIP8(unittest.TestCase):
    def setUp(self):
        self.cpu = CHIP8()

    def test_op_6XNN(self):
        """Test LD Vx, byte"""
        self.cpu.memory[0x200] = 0x61
        self.cpu.memory[0x201] = 0x23
        self.cpu.cycle()

        self.assertEqual(self.cpu.V[1], 0x23)
        self.assertEqual(self.cpu.pc, 0x202)

    def test_op_8XY4_no_carry(self):
        """Test ADD Vx, Vy without carry"""
        self.cpu.V[0] = 5
        self.cpu.V[1] = 10
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x14
        self.cpu.cycle()

        self.assertEqual(self.cpu.V[0], 15)
        self.assertEqual(self.cpu.V[0xF], 0)  # No carry

    def test_op_8XY4_with_carry(self):
        """Test ADD Vx, Vy with carry"""
        self.cpu.V[0] = 255
        self.cpu.V[1] = 1
        self.cpu.memory[0x200] = 0x80
        self.cpu.memory[0x201] = 0x14
        self.cpu.cycle()

        self.assertEqual(self.cpu.V[0], 0)  # Wrapped
        self.assertEqual(self.cpu.V[0xF], 1)  # Carry set

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest test_chip8.py
```

## Automated Testing

### Create Test ROMs Programmatically

```python
def make_test_rom_8XY4():
    """Test ROM for ADD opcode with carry"""
    instructions = [
        0x60FF,  # V0 = 255
        0x6101,  # V1 = 1
        0x8014,  # V0 = V0 + V1 (should be 0 with carry)
        0x0000,  # HALT
    ]

    rom = bytearray()
    for instr in instructions:
        rom.append((instr >> 8) & 0xFF)
        rom.append(instr & 0xFF)

    return rom

# Test it
cpu = CHIP8()
cpu.load_rom(make_test_rom_8XY4())
cpu.run()

assert cpu.V[0] == 0, "V0 should be 0"
assert cpu.V[0xF] == 1, "VF should be 1 (carry)"
print("✓ 8XY4 carry test passed!")
```

### Regression Testing

Keep a suite of ROMs that test all functionality:

```python
test_roms = [
    ('test_arithmetic.ch8', lambda cpu: cpu.V[0] == 8),
    ('test_sprites.ch8', lambda cpu: cpu.display[0][0] == 1),
    ('test_jumps.ch8', lambda cpu: cpu.pc == 0x300),
]

for rom_name, check in test_roms:
    cpu = CHIP8()
    cpu.load_rom(rom_name)
    cpu.run()

    if check(cpu):
        print(f"✓ {rom_name} passed")
    else:
        print(f"✗ {rom_name} FAILED")
```

## Performance Profiling

### Find Bottlenecks

```python
import cProfile
import pstats

# Profile the emulator
profiler = cProfile.Profile()
profiler.enable()

emulator.run()

profiler.disable()

# Print stats
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions
```

### Timing Analysis

```python
import time

start_time = time.time()
cycles = 0

while cycles < 100000:
    emulator.cycle()
    cycles += 1

elapsed = time.time() - start_time
hz = cycles / elapsed

print(f"Executed {cycles} cycles in {elapsed:.2f}s")
print(f"Performance: {hz:.0f} Hz")
```

## Resources

### Test ROMs
- **[Timendus Test Suite](https://github.com/Timendus/chip8-test-suite)**: Best comprehensive test suite
- **[BC_test](https://github.com/daniel5151/AC8E/blob/master/roms/BC_test.ch8)**: Classic test ROM
- **[Octo Test Programs](https://github.com/JohnEarnest/Octo/tree/gh-pages/examples)**: Many examples

### Debugging Tools
- **[Octo](https://johnearnest.github.io/Octo/)**: Web IDE with debugger
- **[CHIP-8 Disassembler](https://github.com/craigthomas/Chip8Disassembler)**: Examine ROM contents

### Community
- **[/r/EmuDev](https://reddit.com/r/emudev)**: Ask for help
- **[EmuDev Discord](https://discord.gg/dkmJAes)**: Real-time assistance

## Checklist: Is My Emulator Working?

- [ ] Loads ROMs without crashing
- [ ] Executes basic opcodes (6XNN, 7XNN, ANNN)
- [ ] Control flow works (1NNN, 2NNN, 00EE)
- [ ] Arithmetic with carry works (8XY4)
- [ ] Can draw sprites (DXYN)
- [ ] Sprites XOR correctly (can erase)
- [ ] Timers count down at 60Hz
- [ ] Input works (EX9E, EXA1, FX0A)
- [ ] Passes BC_test.ch8
- [ ] Passes Timendus test suite
- [ ] Runs at least one game (Pong recommended)

If you can check all these boxes, congratulations! You have a working CHIP-8 emulator!

---

**Next Steps**: Try implementing SUPER-CHIP extensions, or move on to a more complex system like Space Invaders or Game Boy!

**See also**: [/r/EmuDev wiki](https://www.reddit.com/r/EmuDev/wiki/index) for next projects.
