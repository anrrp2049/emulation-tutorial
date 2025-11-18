# Building the CHIP-8 Emulator: Step-by-Step Guide

This guide walks you through building the CHIP-8 emulator from scratch, explaining each component.

## Prerequisites

Install Python dependencies:

```bash
pip install pygame numpy
```

That's it! Python and pygame are all we need.

## Architecture Overview

Our emulator has these main components:

```
┌─────────────────────────────────────┐
│         CHIP8 Class                 │
├─────────────────────────────────────┤
│  State:                             │
│  - memory[4096]                     │
│  - V[16] (registers)                │
│  - I, PC, SP                        │
│  - stack[16]                        │
│  - delay_timer, sound_timer         │
│  - display[32][64]                  │
│  - keys[16]                         │
├─────────────────────────────────────┤
│  Core Methods:                      │
│  - cycle()           ← Main loop    │
│  - execute_opcode()  ← Decode       │
│  - op_XXXX()         ← Execute      │
│  - update_timers()   ← 60Hz timing  │
├─────────────────────────────────────┤
│  I/O Methods:                       │
│  - draw_screen()     ← Graphics     │
│  - handle_input()    ← Keyboard     │
│  - load_rom()        ← File I/O     │
└─────────────────────────────────────┘
```

## Step 1: Initialize the CPU State

The `__init__` method sets up the initial state:

```python
def __init__(self):
    # Memory: 4KB (0x000 to 0xFFF)
    self.memory = [0] * 4096

    # Registers: V0-VF (VF is flag register)
    self.V = [0] * 16

    # Special registers
    self.I = 0       # Index register
    self.pc = 0x200  # Program counter (start at 0x200)

    # Stack for subroutine calls
    self.stack = [0] * 16
    self.sp = 0

    # Timers (count down at 60Hz)
    self.delay_timer = 0
    self.sound_timer = 0

    # Display (64x32 pixels)
    self.display = [[0] * 64 for _ in range(32)]

    # Input (16 keys)
    self.keys = [0] * 16
```

**Why 0x200 for PC?** The first 512 bytes (0x000-0x1FF) are reserved for the CHIP-8 interpreter itself and font data.

## Step 2: Load Font Data

CHIP-8 programs expect font sprites to be in memory:

```python
def load_font(self):
    fonts = [
        0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
        0x20, 0x60, 0x20, 0x20, 0x70,  # 1
        # ... (rest of font data)
    ]

    for i, byte in enumerate(fonts):
        self.memory[0x50 + i] = byte
```

These sprites let programs draw numbers using the `FX29` instruction.

## Step 3: Implement the Fetch-Decode-Execute Cycle

This is the **heart of the emulator**:

```python
def cycle(self):
    # FETCH: Read 16-bit opcode (big-endian)
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

    # Move to next instruction
    self.pc += 2

    # DECODE & EXECUTE
    self.execute_opcode(opcode)
```

**Breaking down the fetch**:
- `self.memory[self.pc]`: First byte (high byte)
- `<< 8`: Shift left 8 bits to make room
- `| self.memory[self.pc + 1]`: OR with second byte (low byte)
- Result: 16-bit instruction

Example:
```
memory[0x200] = 0x61  (binary: 0110 0001)
memory[0x201] = 0x23  (binary: 0010 0011)

Step 1: 0x61 << 8 = 0x6100
Step 2: 0x6100 | 0x23 = 0x6123

opcode = 0x6123 (SET V1 to 0x23)
```

## Step 4: Decode Opcodes

Extract parameters from the opcode:

```python
def execute_opcode(self, opcode):
    # Extract nibbles and values
    first_nibble = (opcode & 0xF000) >> 12
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    n = opcode & 0x000F
    nn = opcode & 0x00FF
    nnn = opcode & 0x0FFF

    # Pattern match on structure
    if opcode == 0x00E0:
        self.op_00E0()  # Clear screen
    elif first_nibble == 0x6:
        self.op_6XNN(x, nn)  # Set register
    # ... etc
```

**Masking and shifting**:
```
opcode = 0x6A0F

first_nibble:
  0x6A0F & 0xF000 = 0x6000
  0x6000 >> 12 = 0x6

x (second nibble):
  0x6A0F & 0x0F00 = 0x0A00
  0x0A00 >> 8 = 0x0A (register 10)

nn (last byte):
  0x6A0F & 0x00FF = 0x000F (value 15)

Result: Set V[10] = 15
```

## Step 5: Implement Simple Opcodes

Start with easy ones:

### 6XNN: Set Register
```python
def op_6XNN(self, x, nn):
    """Set VX = NN"""
    self.V[x] = nn
```

### 7XNN: Add to Register
```python
def op_7XNN(self, x, nn):
    """Set VX = VX + NN"""
    self.V[x] = (self.V[x] + nn) & 0xFF  # Wrap to 8 bits
```

### ANNN: Set Index Register
```python
def op_ANNN(self, nnn):
    """Set I = NNN"""
    self.I = nnn
```

## Step 6: Implement Control Flow

### 1NNN: Jump
```python
def op_1NNN(self, nnn):
    """Jump to address NNN"""
    self.pc = nnn
```

### 2NNN: Call Subroutine
```python
def op_2NNN(self, nnn):
    """Call subroutine at NNN"""
    # Save return address on stack
    self.stack[self.sp] = self.pc
    self.sp += 1
    # Jump to subroutine
    self.pc = nnn
```

### 00EE: Return
```python
def op_00EE(self):
    """Return from subroutine"""
    # Pop return address from stack
    self.sp -= 1
    self.pc = self.stack[self.sp]
```

**How subroutines work**:
```
Main program at 0x200:
  2300   CALL 0x300  → Stack[0] = 0x202, PC = 0x300

Subroutine at 0x300:
  6100   ...do stuff...
  00EE   RET         → PC = Stack[0] = 0x202

Execution resumes at 0x202
```

## Step 7: Implement Arithmetic

### 8XY4: Add with Carry
```python
def op_8XY4(self, x, y):
    """VX = VX + VY, VF = carry"""
    result = self.V[x] + self.V[y]

    # Set carry flag
    self.V[0xF] = 1 if result > 255 else 0

    # Store lower 8 bits
    self.V[x] = result & 0xFF
```

**Why the carry flag?**
It lets programs do multi-byte arithmetic:

```
Add two 16-bit numbers stored as bytes:
  Low:  V0 = 0xFF, V2 = 0x01
  High: V1 = 0x00, V3 = 0x00

8024  ADD V0, V2    → V0 = 0x00, VF = 1 (carried)
8134  ADD V1, V3    → V1 = 0x00
8F14  ADD V1, VF    → V1 = 0x01 (add the carry)

Result: 0x0100 = 256 ✓
```

## Step 8: Implement Graphics (DXYN)

This is the most complex instruction:

```python
def op_DXYN(self, x, y, n):
    """Draw sprite at (VX, VY) with height N"""
    x_pos = self.V[x] % 64
    y_pos = self.V[y] % 32

    self.V[0xF] = 0  # Reset collision flag

    # Draw N rows
    for row in range(n):
        sprite_byte = self.memory[self.I + row]

        # Draw 8 pixels in this row
        for col in range(8):
            # Extract pixel bit
            sprite_pixel = (sprite_byte >> (7 - col)) & 1

            if sprite_pixel:
                screen_x = (x_pos + col) % 64
                screen_y = (y_pos + row) % 32

                # Check collision
                if self.display[screen_y][screen_x] == 1:
                    self.V[0xF] = 1

                # XOR pixel (toggle)
                self.display[screen_y][screen_x] ^= 1

    self.draw_flag = True
```

**How sprite drawing works**:

```
Sprite data in memory (3 bytes = 3 rows):
  memory[I]   = 0b11000011 = 0xC3
  memory[I+1] = 0b11000011 = 0xC3
  memory[I+2] = 0b11111111 = 0xFF

Draws (█ = pixel on):
  ██    ██
  ██    ██
  ████████
```

Each bit = one pixel. XOR means drawing twice erases!

## Step 9: Implement Input

Map keyboard to CHIP-8's 16-key hexadecimal keypad:

```python
def handle_input(self):
    key_map = {
        pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
        pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
        pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
        pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF,
    }

    self.keys = [0] * 16
    pressed = pygame.key.get_pressed()

    for key, chip8_key in key_map.items():
        if pressed[key]:
            self.keys[chip8_key] = 1
```

### FX0A: Wait for Key Press
```python
def op_FX0A(self, x):
    """Wait for keypress, store in VX"""
    key_pressed = False

    for i in range(16):
        if self.keys[i] == 1:
            self.V[x] = i
            key_pressed = True
            break

    # Clever trick: repeat instruction if no key pressed
    if not key_pressed:
        self.pc -= 2
```

## Step 10: Implement Timers

Both timers count down at 60Hz:

```python
def update_timers(self):
    """Call this once per frame (60 FPS)"""
    if self.delay_timer > 0:
        self.delay_timer -= 1

    if self.sound_timer > 0:
        self.sound_timer -= 1
        # TODO: Beep while sound_timer > 0
```

Programs use timers for:
- **Delay timer**: Game timing, animation
- **Sound timer**: Play beep sounds

## Step 11: Rendering

Use pygame to draw the 64x32 display:

```python
def draw_screen(self):
    """Render display buffer to window"""
    if not self.draw_flag:
        return

    self.screen.fill((0, 0, 0))  # Black background

    for y in range(32):
        for x in range(64):
            if self.display[y][x] == 1:
                # Draw scaled white pixel
                rect = pygame.Rect(x * 10, y * 10, 10, 10)
                pygame.draw.rect(self.screen, (255, 255, 255), rect)

    pygame.display.flip()
    self.draw_flag = False
```

**Scaling**: Each CHIP-8 pixel becomes a 10x10 pixel square, giving us a 640x320 window.

## Step 12: Main Loop

Tie everything together:

```python
def run(self):
    """Main emulation loop"""
    self.init_display()

    cycles_per_frame = 500 // 60  # ~8 CPU cycles per frame

    while self.running:
        # 1. Handle input
        self.handle_input()

        # 2. Execute CPU cycles
        for _ in range(cycles_per_frame):
            self.cycle()

        # 3. Update timers (60 Hz)
        self.update_timers()

        # 4. Render display
        self.draw_screen()

        # 5. Maintain 60 FPS
        self.clock.tick(60)
```

**Timing breakdown**:
- CPU runs at ~500 Hz (instructions per second)
- Display refreshes at 60 Hz (frames per second)
- So we execute ~8 instructions per frame (500 / 60 ≈ 8)

## Step 13: Load ROMs

Read a ROM file into memory:

```python
def load_rom(self, filepath):
    """Load ROM into memory at 0x200"""
    with open(filepath, 'rb') as f:
        rom_data = f.read()

    for i, byte in enumerate(rom_data):
        self.memory[0x200 + i] = byte
```

ROM files are just raw binary:
```
$ hexdump -C pong.ch8 | head
00000000  6a 02 6b 0c 6c 3f 6d 0c  a2 ea da b6 dc d6 6e 00  |j.k.l?m.........n.|
00000010  22 d4 66 03 68 02 60 60  f0 15 f0 07 30 00 12 1a  |".f.h.``.....0...|
                     ↑ These bytes become opcodes
```

## Testing Your Emulator

### Test 1: Clear Screen

Minimal program to test basic functionality:

```
Program (4 bytes):
  00E0  ; Clear screen
  00E0  ; Clear screen again
```

What you should see:
- Screen should be black
- No crashes

### Test 2: Draw Sprite

```
Program:
  6000  ; V0 = 0 (x position)
  6100  ; V1 = 0 (y position)
  A202  ; I = 0x202 (sprite location)
  D015  ; Draw sprite at (V0, V1), height 5
  1208  ; Jump to 0x208 (infinite loop)

Sprite data at 0x202:
  F090 90F0 F000  ; Font '0'
```

What you should see:
- Number '0' in top-left corner

### Test 3: Input

```
Program:
  600A  ; V0 = 10
  F00A  ; Wait for key, store in V0
  A202  ; I = 0x202
  F029  ; I = sprite for digit in V0
  6010  ; V0 = 16 (x)
  6108  ; V1 = 8 (y)
  D015  ; Draw sprite
  120A  ; Loop forever
```

What you should do:
1. Run the program
2. Press a key (e.g., '5')
3. Should display that digit

## Debugging Tips

### 1. Add Logging

```python
def cycle(self):
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

    # Log every instruction
    print(f"PC:{self.pc:03X} OP:{opcode:04X}")

    self.pc += 2
    self.execute_opcode(opcode)
```

### 2. Compare with Reference

Run the same ROM on:
- Your emulator (with logging)
- A working emulator (with logging if possible)
- Compare the logs instruction-by-instruction

### 3. Use Test ROMs

Download these:
- **BC_test.ch8**: Tests all opcodes systematically
- **test_opcode.ch8**: Visual test of each instruction
- **Flags test**: Tests carry/borrow flags

Available at: [CHIP-8 Test Suite](https://github.com/Timendus/chip8-test-suite)

### 4. Common Bugs

**PC not incrementing**:
```python
# Wrong: opcode handlers also increment PC
def op_1NNN(self, nnn):
    self.pc = nnn
    self.pc += 2  # BUG! Already incremented in cycle()

# Right: Just set PC
def op_1NNN(self, nnn):
    self.pc = nnn
```

**Endianness wrong**:
```python
# Wrong: little-endian
opcode = self.memory[self.pc] | (self.memory[self.pc + 1] << 8)

# Right: big-endian
opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
```

**Carry flag not set**:
```python
# Wrong: forgot to set VF
def op_8XY4(self, x, y):
    self.V[x] = (self.V[x] + self.V[y]) & 0xFF

# Right: set carry flag
def op_8XY4(self, x, y):
    result = self.V[x] + self.V[y]
    self.V[0xF] = 1 if result > 255 else 0
    self.V[x] = result & 0xFF
```

## Performance Tuning (Optional)

Once it works, make it faster:

### 1. Reduce Logging
Remove debug prints in production.

### 2. Dirty Rectangles
Only redraw changed pixels.

### 3. Increase CPU Speed
```python
cycles_per_frame = 1000 // 60  # 1000 Hz instead of 500 Hz
```

Some games run better at higher speeds.

### 4. Profile Your Code
```python
import cProfile
cProfile.run('emulator.run()')
```

Find bottlenecks!

## Next Steps: Beyond CHIP-8

Once you've mastered CHIP-8, try:

### 1. CHIP-8 Variants
- **SUPER-CHIP**: Higher resolution (128x64), more instructions
- **XO-CHIP**: Modern variant with audio, color

### 2. Space Invaders (Intel 8080)
- More realistic CPU
- ~80 opcodes vs CHIP-8's 35
- Interrupts for timing
- Guide: [Emulator 101](http://www.emulator101.com/)

### 3. Game Boy (Sharp LR35902)
- Complex PPU (Picture Processing Unit)
- Memory bank controllers
- Well-documented
- Guide: [Pandocs](https://gbdev.io/pandocs/)

### 4. NES (6502 CPU)
- Separate CPU and PPU
- Multiple mappers
- Huge game library
- Guide: [NESDev Wiki](http://wiki.nesdev.com/)

## Complete Implementation

The full, working code is in `src/chip8.py`. Study it to see all the pieces together!

Run it:
```bash
python src/chip8.py roms/test.ch8
```

## Additional Resources

- **[CHIP-8 Archive](https://johnearnest.github.io/chip8Archive/)**: Play CHIP-8 games online
- **[Awesome CHIP-8](https://chip-8.github.io/links/)**: Curated resources
- **[/r/EmuDev](https://reddit.com/r/emudev)**: Ask questions!

---

**Congratulations!** You've built a complete emulator. You now understand:
- How CPUs work at a fundamental level
- Fetch-decode-execute cycles
- Memory mapping and addressing
- Opcode implementation
- Graphics and input systems

This knowledge applies to **all** emulation projects!

**Next**: [05-testing-debugging.md](05-testing-debugging.md) for advanced debugging techniques.
