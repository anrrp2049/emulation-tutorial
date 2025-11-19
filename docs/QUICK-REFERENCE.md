# CHIP-8 Quick Reference Card

A concise reference for CHIP-8 emulation. Print this out for quick lookup!

## 📊 System Specifications

| Component | Specification |
|-----------|--------------|
| **Memory** | 4096 bytes (4KB), addresses 0x000-0xFFF |
| **Registers** | 16 × 8-bit (V0-VF), VF = flags |
| **Index Register** | 16-bit (I) |
| **Program Counter** | 16-bit (PC), starts at 0x200 |
| **Stack** | 16 levels, 16-bit addresses |
| **Stack Pointer** | 8-bit (SP) |
| **Timers** | 2 × 8-bit (delay, sound), 60Hz |
| **Display** | 64×32 pixels, monochrome |
| **Keypad** | 16 keys (0-F) |
| **Instructions** | 35 opcodes, 2 bytes each, big-endian |

## 🗺️ Memory Map

```
┌──────────────────┐ 0xFFF
│                  │
│  Program & RAM   │ ← Programs can use this
│                  │
├──────────────────┤ 0x200 ← PC starts here
│  Reserved for    │
│  Interpreter     │
├──────────────────┤ 0x050
│  Font Data       │ ← Built-in 0-F sprites
│  (80 bytes)      │
└──────────────────┘ 0x000
```

## 🎮 Keyboard Layout

```
CHIP-8 Keypad:          Your Keyboard:
┌───┬───┬───┬───┐      ┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ C │      │ 1 │ 2 │ 3 │ 4 │
├───┼───┼───┼───┤      ├───┼───┼───┼───┤
│ 4 │ 5 │ 6 │ D │      │ Q │ W │ E │ R │
├───┼───┼───┼───┤      ├───┼───┼───┼───┤
│ 7 │ 8 │ 9 │ E │      │ A │ S │ D │ F │
├───┼───┼───┼───┤      ├───┼───┼───┼───┤
│ A │ 0 │ B │ F │      │ Z │ X │ C │ V │
└───┴───┴───┴───┘      └───┴───┴───┴───┘
```

## 📋 Complete Opcode Table

| Opcode | Mnemonic | Description |
|--------|----------|-------------|
| `0NNN` | SYS | Call machine code (usually ignored) |
| `00E0` | CLS | Clear screen |
| `00EE` | RET | Return from subroutine |
| `1NNN` | JP NNN | Jump to address NNN |
| `2NNN` | CALL NNN | Call subroutine at NNN |
| `3XNN` | SE VX, NN | Skip if VX == NN |
| `4XNN` | SNE VX, NN | Skip if VX != NN |
| `5XY0` | SE VX, VY | Skip if VX == VY |
| `6XNN` | LD VX, NN | Set VX = NN |
| `7XNN` | ADD VX, NN | Set VX = VX + NN |
| `8XY0` | LD VX, VY | Set VX = VY |
| `8XY1` | OR VX, VY | Set VX = VX OR VY |
| `8XY2` | AND VX, VY | Set VX = VX AND VY |
| `8XY3` | XOR VX, VY | Set VX = VX XOR VY |
| `8XY4` | ADD VX, VY | Set VX = VX + VY, VF = carry |
| `8XY5` | SUB VX, VY | Set VX = VX - VY, VF = NOT borrow |
| `8XY6` | SHR VX | Set VX = VX >> 1, VF = shifted bit |
| `8XY7` | SUBN VX, VY | Set VX = VY - VX, VF = NOT borrow |
| `8XYE` | SHL VX | Set VX = VX << 1, VF = shifted bit |
| `9XY0` | SNE VX, VY | Skip if VX != VY |
| `ANNN` | LD I, NNN | Set I = NNN |
| `BNNN` | JP V0, NNN | Jump to NNN + V0 |
| `CXNN` | RND VX, NN | Set VX = random & NN |
| `DXYN` | DRW VX, VY, N | Draw sprite at (VX,VY), height N |
| `EX9E` | SKP VX | Skip if key VX is pressed |
| `EXA1` | SKNP VX | Skip if key VX is not pressed |
| `FX07` | LD VX, DT | Set VX = delay timer |
| `FX0A` | LD VX, K | Wait for key, store in VX |
| `FX15` | LD DT, VX | Set delay timer = VX |
| `FX18` | LD ST, VX | Set sound timer = VX |
| `FX1E` | ADD I, VX | Set I = I + VX |
| `FX29` | LD F, VX | Set I = location of sprite for digit VX |
| `FX33` | LD B, VX | Store BCD of VX in I, I+1, I+2 |
| `FX55` | LD [I], VX | Store V0-VX in memory starting at I |
| `FX65` | LD VX, [I] | Load V0-VX from memory starting at I |

## 🔍 Opcode Decoding Patterns

```python
opcode = 0xABCD  # Example opcode

# Extract parts
first  = (opcode & 0xF000) >> 12  # A (opcode category)
x      = (opcode & 0x0F00) >> 8   # B (X register)
y      = (opcode & 0x00F0) >> 4   # C (Y register)
n      = (opcode & 0x000F)        # D (4-bit value)
nn     = (opcode & 0x00FF)        # CD (8-bit value)
nnn    = (opcode & 0x0FFF)        # BCD (12-bit address)
```

### Decoding Strategy

1. **Exact match**: `00E0`, `00EE`
2. **First nibble**: `1NNN`, `2NNN`, `3XNN`, `6XNN`, `7XNN`, `ANNN`, etc.
3. **First + last**: `8XY0` through `8XYE`, `5XY0`, `9XY0`
4. **First + last byte**: `EX9E`, `EXA1`, `FX07` through `FX65`

## 🎨 Display System

- **Resolution**: 64×32 pixels
- **Colors**: Monochrome (0 = off, 1 = on)
- **Draw method**: XOR (drawing over existing pixels toggles them)
- **Sprites**: 8 pixels wide, 1-15 pixels tall
- **Collision**: VF = 1 if any pixel was turned off

### Draw Algorithm (DXYN)

```python
def draw_sprite(x, y, height):
    VF = 0
    for row in range(height):
        sprite_byte = memory[I + row]
        for col in range(8):
            if (sprite_byte & (0x80 >> col)) != 0:
                px = (x + col) % 64
                py = (y + row) % 32
                if display[py][px] == 1:
                    VF = 1  # Collision
                display[py][px] ^= 1
    V[0xF] = VF
```

## ⏱️ Timing

| Component | Frequency | Notes |
|-----------|-----------|-------|
| **CPU** | ~500 Hz | Configurable (200-700 typical) |
| **Timers** | 60 Hz | Fixed, decrements when > 0 |
| **Display** | 60 Hz | Match timer frequency |
| **Sound** | 60 Hz | Beep when sound_timer > 0 |

### Implementation

```python
# Main loop at 60 FPS
clock.tick(60)

# Execute multiple cycles per frame
cycles_per_frame = CPU_HZ / 60  # e.g., 500/60 ≈ 8
for _ in range(cycles_per_frame):
    cpu.cycle()

# Update timers once per frame
cpu.update_timers()
```

## 🔢 Number Systems

### Conversions

| Decimal | Binary | Hex |
|---------|--------|-----|
| 0 | 0b0000 | 0x0 |
| 1 | 0b0001 | 0x1 |
| 8 | 0b1000 | 0x8 |
| 15 | 0b1111 | 0xF |
| 16 | 0b00010000 | 0x10 |
| 255 | 0b11111111 | 0xFF |
| 4096 | 0b1000000000000 | 0x1000 |

### Bit Operations

| Operation | Symbol | Example |
|-----------|--------|---------|
| AND | `&` | `0b1010 & 0b1100 = 0b1000` |
| OR | `\|` | `0b1010 \| 0b0011 = 0b1011` |
| XOR | `^` | `0b1010 ^ 0b1111 = 0b0101` |
| NOT | `~` | `~0b1010 = 0b0101` (8-bit) |
| Left Shift | `<<` | `0b0001 << 3 = 0b1000` |
| Right Shift | `>>` | `0b1000 >> 2 = 0b0010` |

## 🐛 Common Issues & Solutions

### Black Screen
- ✓ Check ROM loading (starts at 0x200)
- ✓ Verify display rendering loop
- ✓ Test with test-simple.ch8

### Graphics Glitches
- ✓ Verify XOR draw logic
- ✓ Check coordinate wrapping (% 64, % 32)
- ✓ Sprite data read from I register

### Wrong Behavior
- ✓ Log all instructions
- ✓ Compare with reference emulator
- ✓ Check flag register (VF) handling

### Timing Issues
- ✓ Timers decrement at 60Hz, not every cycle
- ✓ CPU runs at ~500Hz
- ✓ Display refreshes at 60 FPS

## 🔧 Opcode Implementation Template

```python
def execute_opcode(self, opcode):
    # Decode
    first = (opcode & 0xF000) >> 12
    x = (opcode & 0x0F00) >> 8
    y = (opcode & 0x00F0) >> 4
    n = opcode & 0x000F
    nn = opcode & 0x00FF
    nnn = opcode & 0x0FFF
    
    # Execute by pattern
    if opcode == 0x00E0:
        # CLS: Clear screen
        self.display = [[0]*64 for _ in range(32)]
    
    elif opcode == 0x00EE:
        # RET: Return from subroutine
        self.sp -= 1
        self.pc = self.stack[self.sp]
    
    elif first == 0x1:
        # 1NNN: Jump
        self.pc = nnn
    
    elif first == 0x6:
        # 6XNN: Load immediate
        self.V[x] = nn
    
    elif first == 0x7:
        # 7XNN: Add immediate
        self.V[x] = (self.V[x] + nn) & 0xFF
    
    elif first == 0x8:
        if n == 0x4:
            # 8XY4: Add with carry
            result = self.V[x] + self.V[y]
            self.V[0xF] = 1 if result > 255 else 0
            self.V[x] = result & 0xFF
    
    # ... more opcodes
```

## 📚 Essential Resources

### Documentation
- [Cowgod's CHIP-8 Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) - THE specification
- [CHIP-8 Extensions](https://chip-8.github.io/extensions/) - Modern reference
- [Mastering CHIP-8](http://mattmik.com/files/chip8/mastering/chip8.html) - Detailed guide

### Test ROMs
- [Timendus Test Suite](https://github.com/Timendus/chip8-test-suite) - Comprehensive tests
- [CHIP-8 Archive](https://johnearnest.github.io/chip8Archive/) - Games and demos

### Tools
- [Octo](https://johnearnest.github.io/Octo/) - Web-based IDE
- [Awesome CHIP-8](https://chip-8.github.io/links/) - Curated links

### Community
- [/r/EmuDev](https://reddit.com/r/emudev) - Reddit community
- [EmuDev Discord](https://discord.gg/dkmJAes) - Real-time chat

## 🎯 Debugging Checklist

### Basic Functionality
- [ ] Loads ROM into memory at 0x200
- [ ] PC starts at 0x200
- [ ] Fetches 2 bytes per instruction (big-endian)
- [ ] Increments PC by 2 after fetch
- [ ] Implements all 35 opcodes

### Arithmetic
- [ ] ADD sets carry flag correctly (8XY4)
- [ ] SUB sets borrow flag correctly (8XY5, 8XY7)
- [ ] Shift operations set VF (8XY6, 8XYE)
- [ ] All results wrapped to 8 bits (& 0xFF)

### Graphics
- [ ] Display is 64×32 pixels
- [ ] CLS clears all pixels
- [ ] DXYN uses XOR drawing
- [ ] Sprites wrap at screen edges
- [ ] Collision detection sets VF

### Control Flow
- [ ] Jumps set PC correctly
- [ ] Calls push PC to stack
- [ ] Returns pop PC from stack
- [ ] Skips increment PC by 4 (skip next instruction)

### Timers
- [ ] Both timers decrement at 60Hz
- [ ] Only decrement when > 0
- [ ] Sound beeps when sound_timer > 0

### Input
- [ ] All 16 keys mapped
- [ ] SKP/SKNP skip correctly
- [ ] FX0A blocks until key press

## 💡 Optimization Tips

1. **Opcode lookup table** instead of if/elif chain
2. **Cache decoded opcodes** for repeated execution
3. **Use numpy** for display buffer (faster)
4. **Hardware acceleration** for rendering (OpenGL/SDL)
5. **Profile before optimizing** - measure, don't guess!

## 🏁 Getting Started (5 Minutes)

```bash
# Clone repo
git clone <repo-url>
cd emulation-tutorial

# Install dependencies
pip install pygame numpy

# Run test
python src/chip8.py roms/test-simple.ch8

# Try step-by-step tutorial
python src/tutorial/step1_basic_cpu.py
```

## 📖 Learning Path

1. Read [docs/01-core-concepts.md](01-core-concepts.md)
2. Study [src/chip8.py](../src/chip8.py)
3. Run [src/tutorial/step1_basic_cpu.py](../src/tutorial/step1_basic_cpu.py)
4. Build your own following [docs/04-building-chip8.md](04-building-chip8.md)
5. Test with ROMs from [roms/](../roms/)
6. Join [/r/EmuDev](https://reddit.com/r/emudev)!

---

**Print this page for quick reference while coding!** 📄
