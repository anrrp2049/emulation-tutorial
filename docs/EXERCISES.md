# Practical Exercises for Emulation Learning

Hands-on exercises to reinforce emulation and computer architecture concepts. Start from beginner and progress to advanced topics.

## 📚 How to Use These Exercises

1. **Work through them in order** - Each builds on previous concepts
2. **Try before checking solutions** - Learning happens through struggle
3. **Implement in code** - Reading isn't enough, you must build
4. **Test thoroughly** - Use test ROMs and edge cases
5. **Compare with others** - Study different approaches

---

## 🌱 Beginner Exercises

### Exercise 1: Binary and Hexadecimal Practice

**Goal**: Master number system conversions

**Tasks**:
1. Convert these decimal numbers to binary and hex:
   - 42
   - 128
   - 255
   - 1024

2. Convert these hex numbers to decimal and binary:
   - 0x1F
   - 0xFF
   - 0x100
   - 0xDEAD

3. Convert these binary numbers to decimal and hex:
   - 0b10101010
   - 0b11111111
   - 0b100000000
   - 0b1010101010101010

**Solution Check**:
```python
# Use Python to verify
print(f"42 = 0x{42:X} = 0b{42:b}")
print(f"0x1F = {0x1F} = 0b{0x1F:b}")
print(f"0b10101010 = {0b10101010} = 0x{0b10101010:X}")
```

### Exercise 2: Bitwise Operations

**Goal**: Understand bit manipulation

**Tasks**:
1. Manually calculate (then verify with code):
   ```
   0b1010 & 0b1100 = ?
   0b1010 | 0b0011 = ?
   0b1010 ^ 0b1111 = ?
   ~0b1010 (8-bit) = ?
   0b0001 << 3 = ?
   0b1000 >> 2 = ?
   ```

2. Extract nibbles from 0xABCD:
   - First nibble (leftmost)
   - Second nibble
   - Third nibble  
   - Fourth nibble (rightmost)

3. Combine these values into one 16-bit number:
   - First nibble: 0x6
   - X register: 0x1
   - NN value: 0x23
   - Result should be: 0x6123

**Solution**:
```python
opcode = 0xABCD
first  = (opcode & 0xF000) >> 12  # A
second = (opcode & 0x0F00) >> 8   # B
third  = (opcode & 0x00F0) >> 4   # C
fourth = (opcode & 0x000F)        # D

combined = (0x6 << 12) | (0x1 << 8) | 0x23  # 0x6123
```

### Exercise 3: Simple Stack Implementation

**Goal**: Understand stack data structure

**Tasks**:
1. Implement a stack class with these methods:
   - `push(value)` - Add to top
   - `pop()` - Remove and return top
   - `peek()` - Look at top without removing
   - `is_empty()` - Check if empty
   - `size()` - Get number of items

2. Implement these operations:
   ```python
   stack = Stack()
   stack.push(5)
   stack.push(10)
   stack.push(15)
   print(stack.pop())    # Should print 15
   print(stack.peek())   # Should print 10
   print(stack.size())   # Should print 2
   ```

3. Use your stack to reverse a list: `[1, 2, 3, 4, 5]`

**Bonus**: Implement using a fixed-size array (like CHIP-8's 16-level stack)

### Exercise 4: Memory Array

**Goal**: Understand memory addressing

**Tasks**:
1. Create a memory class:
   ```python
   class Memory:
       def __init__(self, size):
           self.memory = [0] * size
       
       def read_byte(self, address):
           # Implement this
           pass
       
       def write_byte(self, address, value):
           # Implement this
           pass
   ```

2. Add bounds checking (raise error if address out of range)

3. Implement `read_word(address)` that reads 2 bytes big-endian

4. Load this program into memory starting at 0x200:
   ```python
   program = [0x61, 0x05, 0x62, 0x0A]
   ```

5. Read back as 16-bit instructions

### Exercise 5: Opcode Decoder

**Goal**: Practice instruction decoding

**Tasks**:
Decode these CHIP-8 opcodes manually:

1. `0x6105` - What instruction? What are the operands?
2. `0x7203` - What instruction? What are the operands?
3. `0x8124` - What instruction? What are the operands?
4. `0xA300` - What instruction? What are the operands?
5. `0x1234` - What instruction? What are the operands?

Write a function:
```python
def decode_opcode(opcode):
    """Return instruction name and operands"""
    # Example: decode_opcode(0x6105) returns ("LD V1, 5", 1, 5)
    pass
```

---

## 🌿 Intermediate Exercises

### Exercise 6: Build a Minimal CPU

**Goal**: Implement fetch-decode-execute cycle

**Tasks**:
1. Create a CPU class with:
   - 4 registers (R0-R3)
   - 256 bytes of memory
   - Program counter
   - Implement these opcodes:
     - `0x1X NN`: Load register X with value NN
     - `0x2X NN`: Add NN to register X
     - `0x3X YY`: Jump to address YY
     - `0xFF`: Halt

2. Write a program that:
   - Sets R0 = 10
   - Sets R1 = 20
   - Adds 5 to R0
   - Halts

3. Implement a `run()` method that executes until halt

**Extension**: Add `0x4X YY`: Jump to YY if RX is zero

### Exercise 7: Implement CHIP-8 Arithmetic

**Goal**: Handle all arithmetic opcodes correctly

**Tasks**:
Implement these CHIP-8 opcodes:
1. `8XY0`: VX = VY
2. `8XY1`: VX = VX OR VY
3. `8XY2`: VX = VX AND VY
4. `8XY3`: VX = VX XOR VY
5. `8XY4`: VX = VX + VY, VF = carry
6. `8XY5`: VX = VX - VY, VF = NOT borrow
7. `8XY6`: VX = VX >> 1, VF = shifted bit
8. `8XY7`: VX = VY - VX, VF = NOT borrow
9. `8XYE`: VX = VX << 1, VF = shifted bit

**Test Cases**:
```python
# Test carry flag
V[0] = 200
V[1] = 100
execute(0x8014)  # ADD V0, V1
assert V[0] == 44  # 300 & 0xFF
assert V[0xF] == 1  # Carry set

# Test XOR
V[2] = 0b10101010
V[3] = 0b11110000
execute(0x8233)  # XOR V2, V3
assert V[2] == 0b01011010
```

### Exercise 8: Display System

**Goal**: Implement graphics rendering

**Tasks**:
1. Create a 64×32 display buffer (2D array)

2. Implement `clear_screen()` - Set all pixels to 0

3. Implement `draw_sprite(x, y, sprite_bytes)`:
   - Draw 8-pixel wide sprite at position (x, y)
   - XOR pixels (CHIP-8 behavior)
   - Return 1 if any pixel was erased, 0 otherwise
   - Wrap coordinates if they go off screen

4. Test with a simple sprite:
   ```python
   sprite = [
       0b11111111,  # ████████
       0b10000001,  # █      █
       0b10000001,  # █      █
       0b10000001,  # █      █
       0b11111111,  # ████████
   ]
   ```

5. Draw sprite at (10, 10), then draw again at same position (should erase)

### Exercise 9: Keyboard Input

**Goal**: Handle user input

**Tasks**:
1. Create a keyboard state array (16 keys, 0=up, 1=down)

2. Implement:
   - `is_key_pressed(key)`: Return True if key is down
   - `wait_for_key()`: Block until any key is pressed, return key number
   - `update_keys(pressed_keys)`: Update keyboard state

3. Map your keyboard to CHIP-8:
   ```
   1234 → 123C
   QWER → 456D
   ASDF → 789E
   ZXCV → A0BF
   ```

4. Implement these opcodes:
   - `EX9E`: Skip next instruction if key VX is pressed
   - `EXA1`: Skip next instruction if key VX is not pressed
   - `FX0A`: Wait for key press, store in VX

### Exercise 10: Timers

**Goal**: Implement timing mechanisms

**Tasks**:
1. Add delay_timer and sound_timer to your CPU

2. Implement 60Hz timer update:
   ```python
   def update_timers(self):
       if self.delay_timer > 0:
           self.delay_timer -= 1
       if self.sound_timer > 0:
           self.sound_timer -= 1
   ```

3. Call `update_timers()` 60 times per second in your main loop

4. Implement opcodes:
   - `FX07`: VX = delay_timer
   - `FX15`: delay_timer = VX
   - `FX18`: sound_timer = VX

5. Make a beep sound when sound_timer > 0

---

## 🌳 Advanced Exercises

### Exercise 11: Full CHIP-8 Emulator

**Goal**: Build complete working emulator

**Tasks**:
1. Implement all 35 CHIP-8 opcodes

2. Add font data (0-9, A-F sprites)

3. Create a main loop:
   - Execute N instructions per frame
   - Update timers at 60Hz
   - Handle input
   - Render display at 60 FPS

4. Test with these ROMs:
   - test-simple.ch8 (basic test)
   - BC_test.ch8 (opcode test)
   - Pong.ch8 (game)

5. Add debug mode:
   - Log each instruction
   - Show register state
   - Pause/step through execution

### Exercise 12: Debugging Tools

**Goal**: Build tools to help debug emulator

**Tasks**:
1. **Disassembler**: Convert ROM to assembly
   ```python
   def disassemble(rom_bytes):
       """Return list of (address, opcode, mnemonic)"""
       # Example: (0x200, 0x6105, "LD V1, 5")
       pass
   ```

2. **Memory Viewer**: Display memory in hex dump format
   ```
   0x200: 61 05 62 0A 81 24 00 00  | a.b...
   0x208: A3 00 D0 10 00 EE 00 00  | ......
   ```

3. **Register Watch**: Show register changes
   ```
   V0: 0x00 → 0x05  (+5)
   V1: 0x00 → 0x0A  (+10)
   ```

4. **Breakpoints**: Stop execution at address
   ```python
   def add_breakpoint(self, address):
       self.breakpoints.add(address)
   
   def check_breakpoint(self):
       if self.pc in self.breakpoints:
           self.paused = True
   ```

5. **Trace Log**: Save execution history to file

### Exercise 13: Save States

**Goal**: Implement save/load functionality

**Tasks**:
1. Save complete CPU state to file:
   - All registers
   - Memory
   - PC, SP, I
   - Timers
   - Display state
   - Keys

2. Serialize to JSON or binary format

3. Load state from file and resume execution

4. Add hotkeys:
   - F5: Quick save
   - F9: Quick load
   - Shift+F5: Save to slot
   - Shift+F9: Load from slot

5. Support multiple save slots (1-10)

### Exercise 14: Optimization

**Goal**: Make emulator faster

**Tasks**:
1. **Profile** your code:
   ```python
   import cProfile
   cProfile.run('emulator.run()')
   ```

2. Find bottlenecks - which functions take most time?

3. **Optimize**:
   - Cache decoded opcodes?
   - Use lookup table for opcodes?
   - Optimize display rendering?
   - Use numpy for display buffer?

4. **Benchmark**:
   - Instructions per second before
   - Instructions per second after
   - Target: 100,000+ IPS

5. **Profile again** - Did optimizations work?

### Exercise 15: Additional Features

**Goal**: Extend emulator with modern features

**Tasks**:
1. **Configurable Speed**:
   - Slider to adjust CPU speed
   - Preset: 1x, 2x, 5x, 10x, unlimited

2. **Rewind**:
   - Save state every N frames
   - Allow rewinding time
   - Like video player seeking

3. **Screen Recording**:
   - Save display frames to images
   - Generate GIF or video

4. **Cheats**:
   - Set register values
   - Modify memory
   - Infinite lives, etc.

5. **Statistics**:
   - Instructions executed
   - Cycle count
   - FPS counter
   - Opcode usage histogram

---

## 🚀 Expert Exercises

### Exercise 16: Different Architecture

**Goal**: Understand different CPU designs

**Tasks**:
1. Build an emulator for a different system:
   - **Stack-based VM** (like our simple_vm.py)
   - **Intel 8080** (follow Emulator 101)
   - **RISC-V subset** (RV32I base)

2. Compare architectures:
   - Register vs stack
   - Fixed vs variable length instructions
   - CISC vs RISC

3. Write a program that runs on both CHIP-8 and your new architecture

### Exercise 17: JIT Compilation

**Goal**: Implement dynamic recompilation

**Tasks**:
1. **Basic Block Detection**:
   - Identify sequences of instructions with no branches
   - Stop at jumps, calls, returns

2. **Code Generation**:
   - Convert basic block to Python code
   - Use `exec()` to create function
   - Cache compiled blocks

3. **Optimization**:
   - Constant folding: `LD V0, 5; ADD V0, 3` → `V0 = 8`
   - Dead code elimination
   - Register allocation

4. **Benchmark**:
   - Compare interpreter vs JIT
   - Should be 5-10x faster for compute-heavy code

5. **Invalidation**:
   - Handle self-modifying code
   - Clear cache when memory is written to

### Exercise 18: Cycle Accuracy

**Goal**: Match original hardware timing exactly

**Tasks**:
1. **Research**: Find cycle counts for each CHIP-8 instruction
   - Most take 1 cycle
   - Some (like DXYN) may take more

2. **Cycle Counter**:
   - Track cycles for each instruction
   - Account for memory access time
   - Consider display drawing time

3. **Timing**:
   - Execute exactly N cycles per frame
   - Don't just count instructions

4. **Test**:
   - Use timing-sensitive test ROMs
   - Compare with hardware measurements

5. **Audio Sync**:
   - Keep sound in sync with emulation
   - Buffer audio properly

### Exercise 19: Multi-System Emulator

**Goal**: Support multiple systems in one emulator

**Tasks**:
1. **Core Interface**:
   ```python
   class EmulatorCore:
       def reset(self): pass
       def cycle(self): pass
       def load_rom(self, data): pass
       def get_display(self): pass
       def set_keys(self, keys): pass
   ```

2. **Implement**:
   - CHIP8Core
   - SuperChip8Core (extended CHIP-8)
   - XO-CHIP Core (modern variant)

3. **Auto-detect** ROM type

4. **Unified UI** that works with all cores

5. **Plugin System** for adding new cores

### Exercise 20: WebAssembly Port

**Goal**: Run emulator in browser

**Tasks**:
1. **Rewrite in C/C++**:
   - Port your Python code to C
   - Keep same architecture

2. **Compile to WASM**:
   ```bash
   emcc chip8.c -o chip8.js -s WASM=1
   ```

3. **JavaScript Interface**:
   - Load ROM from file picker
   - Render to HTML5 canvas
   - Handle keyboard input

4. **Web UI**:
   - Upload ROM button
   - Control panel (speed, reset, etc.)
   - Mobile-friendly controls

5. **Deploy**:
   - Host on GitHub Pages
   - Share with community!

---

## 📝 Project Ideas

Apply your knowledge to complete projects:

### Project 1: CHIP-8 IDE
- Editor with syntax highlighting
- Integrated assembler
- Built-in emulator
- Debugger
- Export to ROM

### Project 2: Game Development
- Create original CHIP-8 games
- Use Octo or write in assembly
- Test on your emulator
- Share ROMs

### Project 3: Educational Tool
- Interactive tutorial system
- Step-by-step visualization
- Quizzes and challenges
- Track student progress

### Project 4: Accuracy Testing
- Create comprehensive test suite
- Test all edge cases
- Compare multiple emulators
- Document quirks

### Project 5: Hardware Implementation
- Build CHIP-8 on FPGA
- Use Verilog/VHDL
- MiSTer platform
- Compare with software emulation

---

## ✅ Self-Assessment Checklist

### Beginner Level
- [ ] Can convert between binary, decimal, and hex
- [ ] Understand bitwise operations
- [ ] Can extract parts of opcodes using masks
- [ ] Implemented a stack data structure
- [ ] Created simple memory array
- [ ] Decoded CHIP-8 opcodes manually

### Intermediate Level
- [ ] Built minimal CPU with fetch-decode-execute
- [ ] Implemented all CHIP-8 arithmetic opcodes
- [ ] Created display system with XOR drawing
- [ ] Handled keyboard input properly
- [ ] Implemented timers at 60Hz
- [ ] Tested with multiple ROMs

### Advanced Level
- [ ] Completed full CHIP-8 emulator (all 35 opcodes)
- [ ] Built debugging tools (disassembler, memory viewer)
- [ ] Implemented save states
- [ ] Optimized for performance
- [ ] Added modern features (rewind, recording, etc.)
- [ ] Passed all test ROMs

### Expert Level
- [ ] Emulated another architecture
- [ ] Implemented JIT compilation
- [ ] Achieved cycle accuracy
- [ ] Built multi-system emulator
- [ ] Created WebAssembly port
- [ ] Contributed to open source emulation projects

---

## 🎯 Challenge: Speedrun!

Can you build a working CHIP-8 emulator from scratch in:
- [ ] 1 week (beginner)
- [ ] 2 days (intermediate)
- [ ] 1 day (advanced)
- [ ] 4 hours (expert)

Time yourself and track progress. Good luck!

---

**Remember**: The goal isn't just to complete exercises, but to deeply understand the concepts. Take your time, experiment, and have fun!

**Get Help**: Join [/r/EmuDev](https://reddit.com/r/emudev) or [Discord](https://discord.gg/dkmJAes) if stuck!
