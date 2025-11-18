# CHIP-8 ROMs and Test Programs

This directory contains CHIP-8 programs for testing and playing.

## Test Programs

### test-simple.ch8
A minimal test program that demonstrates basic CHIP-8 functionality:
- Clears the screen
- Draws a sprite (number '5')
- Waits indefinitely

Use this to verify your emulator can:
- Load ROMs
- Execute opcodes
- Render graphics

## Where to Find More ROMs

### Free CHIP-8 Games and Demos

1. **[CHIP-8 Archive](https://johnearnest.github.io/chip8Archive/)**
   - Large collection of games
   - Playable in browser
   - Downloadable ROMs

2. **[CHIP-8 Games Pack](https://www.zophar.net/pdroms/chip8.html)**
   - Classic CHIP-8 games
   - Pong, Space Invaders, Tetris, etc.

3. **[David Winter's CHIP-8 Collection](http://www.pong-story.com/chip8/)**
   - Many classic games
   - Well-tested ROMs

### Test ROMs (Essential for Development)

1. **[CHIP-8 Test Suite by Timendus](https://github.com/Timendus/chip8-test-suite)**
   - Comprehensive opcode tests
   - Visual feedback
   - Tests quirks and edge cases
   - **Highly recommended!**

2. **BC_test.ch8**
   - Tests all 35 opcodes
   - Shows pass/fail for each

3. **Flags Test**
   - Tests carry and borrow flags
   - Essential for arithmetic opcodes

## Popular CHIP-8 Games

### Pong
Classic two-player ping-pong game.
- **Controls**: 1/Q for left paddle up/down, 4/R for right paddle

### Space Invaders
Shoot descending aliens!
- **Controls**: Q/E to move, W to shoot

### Tetris
Classic block-stacking game.
- **Controls**: Q/E to rotate, A/D to move, S to drop

### Breakout
Break bricks with a ball!
- **Controls**: Q/E to move paddle

### Cave
Navigate through a scrolling cave.
- **Controls**: Press any key to ascend

## Creating Your Own CHIP-8 Programs

### Assemblers

1. **[Octo](https://johnearnest.github.io/Octo/)**
   - Web-based CHIP-8 IDE
   - Assembler, debugger, and emulator
   - Great for learning

2. **[chipper](https://github.com/andy-hanson/chipper)**
   - Command-line assembler
   - Simple syntax

### Example Program

```asm
; Simple CHIP-8 program
; Draws a sprite in the center of the screen

:main
  ; Set position
  v0 := 28  ; x = 28 (roughly center)
  v1 := 12  ; y = 12 (roughly center)

  ; Set sprite location
  i := sprite

  ; Draw sprite (8x5 pixels)
  sprite v0 v1 5

  ; Infinite loop
  jump main

:sprite
  0b11111111
  0b10000001
  0b10000001
  0b10000001
  0b11111111
```

Assemble with Octo and download the ROM!

## ROM File Format

CHIP-8 ROMs are **raw binary** files:
- No header, no metadata
- Just executable CHIP-8 instructions
- Loaded directly into memory at 0x200
- Typically 512 bytes to 3.5 KB

Example using hexdump:
```bash
$ hexdump -C pong.ch8 | head
00000000  6a 02 6b 0c 6c 3f 6d 0c  a2 ea da b6 dc d6 6e 00
```

Each pair of hex digits is one byte of the ROM.

## Testing Checklist

When testing your emulator, try these ROMs in order:

- [ ] test-simple.ch8 (basic functionality)
- [ ] BC_test.ch8 (opcode correctness)
- [ ] Flags test (arithmetic flags)
- [ ] Pong (input and game logic)
- [ ] Space Invaders (complex game)
- [ ] Tetris (timing and input)

If all of these work, your emulator is solid!

## Legal Note

CHIP-8 is a public domain specification from the 1970s. Most CHIP-8 programs are free or public domain, but always check the license before distributing.

## Contributing

Have a cool CHIP-8 program? Submit a PR!
- Include the .ch8 file
- Add description to this README
- Credit the original author
