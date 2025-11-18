# CPU Emulation Deep Dive

Now that you understand the fundamentals, let's learn how to actually emulate a CPU in code.

## CPU State: What Must We Track?

A CPU's **state** is everything needed to resume execution at any point. For CHIP-8, we need:

```python
class CHIP8:
    def __init__(self):
        # Memory: 4KB RAM
        self.memory = [0] * 4096

        # Registers: 16 general purpose (V0-VF)
        # VF is used as flag register
        self.V = [0] * 16

        # Index register: for memory operations
        self.I = 0

        # Program counter: points to current instruction
        self.pc = 0x200  # Programs start at 0x200

        # Stack: for subroutine calls (16 levels)
        self.stack = [0] * 16
        self.sp = 0  # Stack pointer

        # Timers: count down at 60 Hz
        self.delay_timer = 0
        self.sound_timer = 0

        # Display: 64x32 monochrome (each pixel is 0 or 1)
        self.display = [[0] * 64 for _ in range(32)]

        # Input: 16 keys (0-F)
        self.keys = [0] * 16
```

**Key Point**: This is a **complete** representation of the CPU's state. If you save these values, you can resume execution exactly where you left off (this is how save states work!).

**Reference**: Compare with [6502 state](http://www.obelisk.me.uk/6502/registers.html) to see similarities.

## The Main Loop: Bringing It All Together

Every emulator has a main loop that runs continuously:

```python
def run(self):
    """Main emulation loop"""
    clock = pygame.time.Clock()

    while self.running:
        # Handle input (keyboard/controller)
        self.handle_input()

        # Execute several CPU cycles per frame
        # CHIP-8 runs at ~500 Hz, display at 60 Hz
        # So execute ~8-10 instructions per frame
        for _ in range(10):
            # Fetch-Decode-Execute
            self.cycle()

        # Update timers (60 Hz)
        self.update_timers()

        # Render display
        self.draw_screen()

        # Maintain 60 FPS
        clock.tick(60)
```

**The cycle() method is where the magic happens!**

## The Fetch-Decode-Execute Cycle in Code

Let's implement the CPU's heart:

```python
def cycle(self):
    """Execute one CPU cycle"""

    # FETCH: Read instruction from memory
    # CHIP-8 instructions are 2 bytes (big-endian)
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

    # Increment PC (will be modified by jumps/calls)
    self.pc += 2

    # DECODE & EXECUTE: Figure out what to do
    self.execute_opcode(opcode)
```

**Breaking down the FETCH**:
```python
# Memory at PC:     [0x61, 0x23]
# memory[pc]     = 0x61 = 0110 0001
# memory[pc + 1] = 0x23 = 0010 0011

# Shift first byte left 8 bits:
# 0x61 << 8 = 0x6100 = 0110 0001 0000 0000

# OR with second byte:
# 0x6100 | 0x23 = 0x6123 = 0110 0001 0010 0011

opcode = 0x6123  # Complete 16-bit instruction
```

**Why increment PC by 2?** CHIP-8 instructions are 2 bytes, so we move forward 2 addresses.

## Decoding Opcodes: Pattern Matching

CHIP-8 has 35 different instruction types. We need to decode the opcode and execute the right one:

```python
def execute_opcode(self, opcode):
    """Decode and execute a single opcode"""

    # Extract common values
    # First nibble usually identifies instruction type
    first_nibble = (opcode & 0xF000) >> 12

    # Extract register numbers
    x = (opcode & 0x0F00) >> 8   # Second nibble
    y = (opcode & 0x00F0) >> 4   # Third nibble

    # Extract byte and nibble values
    nn = opcode & 0x00FF         # Last byte
    nnn = opcode & 0x0FFF        # Last 12 bits (address)
    n = opcode & 0x000F          # Last nibble

    # Decode by pattern matching
    if opcode == 0x00E0:
        # CLS: Clear screen
        self.op_00E0()

    elif opcode == 0x00EE:
        # RET: Return from subroutine
        self.op_00EE()

    elif first_nibble == 0x1:
        # 1NNN: Jump to address NNN
        self.op_1NNN(nnn)

    elif first_nibble == 0x2:
        # 2NNN: Call subroutine at NNN
        self.op_2NNN(nnn)

    elif first_nibble == 0x3:
        # 3XNN: Skip if VX == NN
        self.op_3XNN(x, nn)

    elif first_nibble == 0x6:
        # 6XNN: Set VX = NN
        self.op_6XNN(x, nn)

    elif first_nibble == 0x7:
        # 7XNN: Set VX = VX + NN
        self.op_7XNN(x, nn)

    elif first_nibble == 0x8:
        # 8XY?: Arithmetic operations (last nibble determines which)
        self.decode_8XY_(opcode, x, y, n)

    elif first_nibble == 0xA:
        # ANNN: Set I = NNN
        self.op_ANNN(nnn)

    elif first_nibble == 0xD:
        # DXYN: Draw sprite
        self.op_DXYN(x, y, n)

    # ... (more opcodes)

    else:
        # Unknown opcode
        print(f"Unknown opcode: {opcode:04X}")
```

**Pattern**: Most CPUs work this way:
1. Extract instruction type (usually first few bits)
2. Extract parameters (register numbers, values, addresses)
3. Jump to handler for that instruction type

**Reference**: See [6502 opcode decoding](http://www.emulator101.com/6502-addressing-modes.html) for a more complex example.

## Implementing Individual Instructions

Let's implement several opcodes to see patterns:

### Simple: Set Register (6XNN)

```python
def op_6XNN(self, x, nn):
    """6XNN: Set VX = NN

    Example: 0x6A0F sets V[A] = 15
    """
    self.V[x] = nn
```

**That's it!** Most instructions are simple operations.

### Arithmetic: Add with Carry (8XY4)

```python
def op_8XY4(self, x, y):
    """8XY4: Set VX = VX + VY, set VF = carry

    VF (V[15]) is set to 1 if result overflows (>255), else 0
    Result is wrapped to 8 bits
    """
    result = self.V[x] + self.V[y]

    # Set carry flag
    if result > 255:
        self.V[0xF] = 1
    else:
        self.V[0xF] = 0

    # Store lower 8 bits
    self.V[x] = result & 0xFF
```

**Key concept**: The carry flag (VF) lets programs detect overflow. This is crucial for multi-byte arithmetic.

### Control Flow: Jump (1NNN)

```python
def op_1NNN(self, nnn):
    """1NNN: Jump to address NNN

    Set PC to NNN. Execution continues from there.
    """
    self.pc = nnn
```

**Why it works**: Remember we already incremented PC in `cycle()`. By setting PC here, the next `cycle()` will fetch from this new address.

### Stack Operations: Call Subroutine (2NNN)

```python
def op_2NNN(self, nnn):
    """2NNN: Call subroutine at NNN

    Push current PC to stack, then jump to NNN
    """
    # Save return address on stack
    self.stack[self.sp] = self.pc
    self.sp += 1

    # Jump to subroutine
    self.pc = nnn
```

**Return from Subroutine (00EE)**:
```python
def op_00EE(self):
    """00EE: Return from subroutine

    Pop return address from stack and jump to it
    """
    self.sp -= 1
    self.pc = self.stack[self.sp]
```

**Together, these enable function calls!**

```
Main program:
  0x200: 2300     CALL 0x300 (call function)
  0x202: 6A05     (execution resumes here after RET)

Function:
  0x300: 6100     (function code)
  0x302: 00EE     RET (return to 0x202)
```

**Book Reference**: "Code" by Petzold (Chapter 17) explains subroutines beautifully.

### Memory Operations: Load from Memory (FX65)

```python
def op_FX65(self, x):
    """FX65: Load V0-VX from memory starting at I

    Reads X+1 bytes from memory[I] into registers V[0] through V[X]
    """
    for i in range(x + 1):
        self.V[i] = self.memory[self.I + i]

    # CHIP-8 quirk: I is incremented
    # (Some interpreters don't do this - compatibility issue!)
    self.I += x + 1
```

**Important**: Different CHIP-8 implementations have subtle differences ("quirks"). Document your choices!

## The Most Complex Instruction: Draw Sprite (DXYN)

This instruction draws graphics. It's complex but illustrates important concepts:

```python
def op_DXYN(self, x, y, n):
    """DXYN: Draw sprite at (VX, VY), height N pixels

    Sprites are 8 pixels wide, N pixels tall
    Sprite data is read from memory[I]
    Pixels are XORed with screen (toggled)
    VF = 1 if any pixel is erased (collision), else 0
    """
    # Get position from registers
    x_pos = self.V[x] % 64  # Wrap to screen width
    y_pos = self.V[y] % 32  # Wrap to screen height

    # Reset collision flag
    self.V[0xF] = 0

    # Read N bytes of sprite data
    for row in range(n):
        # Get sprite row byte from memory
        sprite_byte = self.memory[self.I + row]

        # Each bit is a pixel (8 pixels wide)
        for col in range(8):
            # Extract bit: is this pixel on?
            sprite_pixel = (sprite_byte >> (7 - col)) & 1

            # Calculate screen position
            screen_x = (x_pos + col) % 64
            screen_y = (y_pos + row) % 32

            # XOR with screen pixel
            screen_pixel = self.display[screen_y][screen_x]

            if sprite_pixel == 1:
                # Collision: pixel was on and is being turned off
                if screen_pixel == 1:
                    self.V[0xF] = 1

                # Toggle pixel
                self.display[screen_y][screen_x] ^= 1
```

**Breaking down the bit extraction**:
```
sprite_byte = 0b11001100 = 0xCC

Bit 0 (leftmost):  (0xCC >> 7) & 1 = 1
Bit 1:             (0xCC >> 6) & 1 = 1
Bit 2:             (0xCC >> 5) & 1 = 0
Bit 3:             (0xCC >> 4) & 1 = 0
Bit 4:             (0xCC >> 3) & 1 = 1
Bit 5:             (0xCC >> 2) & 1 = 1
Bit 6:             (0xCC >> 1) & 1 = 0
Bit 7:             (0xCC >> 0) & 1 = 0

Result: ██  ██   (4 white pixels, 4 black)
```

**XOR toggling** allows sprites to be drawn and erased by drawing them twice:
```
Screen:  0  + Sprite: 1  = Result: 1  (draw)
Screen:  1  + Sprite: 1  = Result: 0  (erase)
```

## Handling Timers

CHIP-8 has two timers that count down at 60 Hz:

```python
def update_timers(self):
    """Decrease timers at 60 Hz"""
    if self.delay_timer > 0:
        self.delay_timer -= 1

    if self.sound_timer > 0:
        self.sound_timer -= 1
        # While sound_timer > 0, beep!
```

**Timing trick**: Call this once per frame (60 FPS) to get 60 Hz timer frequency.

## Input Handling

CHIP-8 has 16 keys (0-F), usually mapped to:

```
Original CHIP-8:     Modern keyboard:
1 2 3 C              1 2 3 4
4 5 6 D              Q W E R
7 8 9 E              A S D F
A 0 B F              Z X C V
```

```python
def handle_input(self):
    """Map keyboard to CHIP-8 keys"""
    # Mapping pygame keys to CHIP-8 keys
    key_map = {
        pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
        pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
        pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
        pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF,
    }

    # Reset all keys
    self.keys = [0] * 16

    # Check which keys are pressed
    pressed = pygame.key.get_pressed()
    for key, chip8_key in key_map.items():
        if pressed[key]:
            self.keys[chip8_key] = 1
```

**Wait for Key Press (FX0A)**:
```python
def op_FX0A(self, x):
    """FX0A: Wait for key press, store key in VX

    Execution halts until a key is pressed
    """
    key_pressed = False

    for i in range(16):
        if self.keys[i] == 1:
            self.V[x] = i
            key_pressed = True
            break

    # If no key pressed, repeat this instruction
    if not key_pressed:
        self.pc -= 2  # Go back to this instruction
```

**Clever trick**: By decrementing PC, we execute the same instruction again next cycle, creating a "wait" loop!

## Loading ROMs

Programs (ROMs) are loaded into memory starting at 0x200:

```python
def load_rom(self, filepath):
    """Load a CHIP-8 ROM file into memory"""
    with open(filepath, 'rb') as f:
        rom_data = f.read()

    # Load ROM into memory starting at 0x200
    for i, byte in enumerate(rom_data):
        self.memory[0x200 + i] = byte

    print(f"Loaded ROM: {len(rom_data)} bytes")
```

**Why 0x200?** Addresses 0x000-0x1FF are reserved for the CHIP-8 interpreter and font data.

## Font Data

CHIP-8 includes built-in font sprites (0-F), stored at 0x050-0x09F:

```python
def load_font(self):
    """Load built-in font into memory"""
    # Each character is 5 bytes (4x5 pixel font)
    fonts = [
        0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
        0x20, 0x60, 0x20, 0x20, 0x70,  # 1
        0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
        0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
        0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
        0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
        0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
        0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
        0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
        0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
        0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
        0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
        0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
        0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
        0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
        0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
    ]

    # Load at address 0x50
    for i, byte in enumerate(fonts):
        self.memory[0x50 + i] = byte
```

**Visualizing '0'**:
```
0xF0 = 1111 0000 = ████
0x90 = 1001 0000 = █  █
0x90 = 1001 0000 = █  █
0x90 = 1001 0000 = █  █
0xF0 = 1111 0000 = ████
```

## Performance Optimization (Advanced)

Once your emulator works, you can optimize:

### 1. Opcode Table (Faster Decoding)

```python
# Instead of if/elif chain, use function pointers
self.opcode_table = {
    0x00E0: self.op_00E0,
    0x00EE: self.op_00EE,
    # ... etc
}

def execute_opcode(self, opcode):
    handler = self.opcode_table.get(opcode)
    if handler:
        handler()
    else:
        self.decode_complex(opcode)
```

### 2. Dirty Rectangles (Faster Rendering)

Only redraw changed parts of screen:

```python
# Track which pixels changed
self.dirty_pixels = set()

def op_DXYN(self, x, y, n):
    # ... drawing code ...
    self.dirty_pixels.add((screen_x, screen_y))
```

### 3. JIT Compilation (Advanced)

Translate guest instructions to host instructions at runtime. This is how fast emulators (Dolphin, PCSX2) work!

**Reference**: "Game Engine Black Book: Wolfenstein 3D" discusses optimization techniques.

## Complete Opcode Reference

Here's every CHIP-8 opcode (for implementation):

| Opcode | Name | Description |
|--------|------|-------------|
| 0NNN | SYS | Call machine code (ignored in modern interpreters) |
| 00E0 | CLS | Clear screen |
| 00EE | RET | Return from subroutine |
| 1NNN | JP | Jump to NNN |
| 2NNN | CALL | Call subroutine at NNN |
| 3XNN | SE | Skip if VX == NN |
| 4XNN | SNE | Skip if VX != NN |
| 5XY0 | SE | Skip if VX == VY |
| 6XNN | LD | Set VX = NN |
| 7XNN | ADD | Set VX = VX + NN |
| 8XY0 | LD | Set VX = VY |
| 8XY1 | OR | Set VX = VX OR VY |
| 8XY2 | AND | Set VX = VX AND VY |
| 8XY3 | XOR | Set VX = VX XOR VY |
| 8XY4 | ADD | Set VX = VX + VY, VF = carry |
| 8XY5 | SUB | Set VX = VX - VY, VF = NOT borrow |
| 8XY6 | SHR | Set VX = VX SHR 1, VF = LSB |
| 8XY7 | SUBN | Set VX = VY - VX, VF = NOT borrow |
| 8XYE | SHL | Set VX = VX SHL 1, VF = MSB |
| 9XY0 | SNE | Skip if VX != VY |
| ANNN | LD | Set I = NNN |
| BNNN | JP | Jump to NNN + V0 |
| CXNN | RND | Set VX = random AND NN |
| DXYN | DRW | Draw sprite at (VX, VY), height N |
| EX9E | SKP | Skip if key VX is pressed |
| EXA1 | SKNP | Skip if key VX not pressed |
| FX07 | LD | Set VX = delay_timer |
| FX0A | LD | Wait for key, store in VX |
| FX15 | LD | Set delay_timer = VX |
| FX18 | LD | Set sound_timer = VX |
| FX1E | ADD | Set I = I + VX |
| FX29 | LD | Set I = sprite location for digit VX |
| FX33 | LD | Store BCD of VX at I, I+1, I+2 |
| FX55 | LD | Store V0-VX in memory starting at I |
| FX65 | LD | Load V0-VX from memory starting at I |

**Full specification**: [Cowgod's CHIP-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM)

## Debugging Your CPU

When things go wrong (and they will!), try:

### 1. Log Every Instruction

```python
def cycle(self):
    opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

    # Log before execution
    print(f"PC:{self.pc:03X} OP:{opcode:04X} I:{self.I:03X} V:{' '.join(f'{v:02X}' for v in self.V)}")

    self.pc += 2
    self.execute_opcode(opcode)
```

### 2. Compare with Known-Good Emulator

Run the same ROM on your emulator and a reference emulator, compare logs.

### 3. Use Test ROMs

- **BC_test.ch8**: Tests CHIP-8 opcodes systematically
- **test_opcode.ch8**: Visual tests for each instruction
- **Flags test**: Tests carry/borrow flags

### 4. Step-Through Mode

```python
# Execute one instruction per keypress
if debug_mode:
    input("Press Enter for next instruction...")
```

## Next Steps

You now understand CPU emulation! Next, let's put it all together and build the complete CHIP-8 emulator.

**Continue to**: [04-building-chip8.md](04-building-chip8.md)

## Additional Resources

- **[CHIP-8 Test Suite](https://github.com/Timendus/chip8-test-suite)**: Comprehensive tests
- **[Awesome CHIP-8](https://chip-8.github.io/links/)**: Curated CHIP-8 resources
- **[Writing a CHIP-8 Emulator](https://tobiasvl.github.io/blog/write-a-chip-8-emulator/)**: Another great guide

---

**Practice**: Try implementing 3-4 opcodes yourself before looking at the complete code. Start with simple ones like 6XNN (set register) and 1NNN (jump).
