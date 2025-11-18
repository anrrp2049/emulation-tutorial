# Quick Start Guide

Get up and running with the CHIP-8 emulator in 5 minutes!

## Installation

### 1. Install Python
Make sure you have Python 3.8+ installed:
```bash
python --version  # Should show 3.8 or higher
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

That's it! Only pygame is needed.

## Running the Emulator

### Try the Test Program
```bash
python src/chip8.py roms/test-simple.ch8
```

You should see a window with the number "5" displayed.

**Controls**:
- `ESC`: Quit

### Run with Debug Mode
```bash
python src/chip8.py roms/test-simple.ch8 --debug
```

Prints every instruction executed.

## Learning Path

### 1. Understand the Basics (30 min)
Read [docs/01-core-concepts.md](docs/01-core-concepts.md)

Learn:
- What emulation is
- Fetch-decode-execute cycle
- Opcodes and registers
- Memory organization

### 2. See It In Action (15 min)
Run the step-by-step tutorial:
```bash
python src/tutorial/step1_basic_cpu.py
```

Watch the emulator execute instructions one by one!

### 3. Study the Code (1-2 hours)
Open [src/chip8.py](src/chip8.py) and read through it.

Key sections to understand:
- `__init__`: Initial CPU state
- `cycle()`: Fetch-decode-execute loop
- `execute_opcode()`: Instruction decoding
- `op_XXXX()`: Individual instruction implementations
- `run()`: Main emulation loop

### 4. Build Your Own (3-6 hours)
Follow [docs/04-building-chip8.md](docs/04-building-chip8.md)

Build the emulator from scratch, step by step!

## Getting Test ROMs

### From Online Archives
1. **[CHIP-8 Archive](https://johnearnest.github.io/chip8Archive/)**
   - Click "Download" on any game
   - Save to `roms/` folder
   - Run with `python src/chip8.py roms/game.ch8`

2. **[Zophar's Domain](https://www.zophar.net/pdroms/chip8.html)**
   - Download ROM packs
   - Extract to `roms/`

### Test ROMs (Essential!)
1. **[CHIP-8 Test Suite](https://github.com/Timendus/chip8-test-suite)**
   ```bash
   cd roms/
   git clone https://github.com/Timendus/chip8-test-suite.git
   cd ..
   python src/chip8.py roms/chip8-test-suite/bin/1-chip8-logo.ch8
   ```

## Keyboard Controls

CHIP-8 has a 16-key hexadecimal keypad. We map it to:

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

## Popular Games to Try

### Pong (Easy)
```bash
# Download from CHIP-8 Archive, then:
python src/chip8.py roms/pong.ch8
```
- Player 1: `1` (up), `Q` (down)
- Player 2: `4` (up), `R` (down)

### Space Invaders (Medium)
```bash
python src/chip8.py roms/invaders.ch8
```
- `Q`/`E`: Move
- `W`: Shoot

### Tetris (Hard)
```bash
python src/chip8.py roms/tetris.ch8
```
- `Q`/`E`: Rotate
- `A`/`D`: Move
- `S`: Drop

## Troubleshooting

### "No module named 'pygame'"
```bash
pip install pygame
```

### "ROM file not found"
Make sure you're running from the repository root:
```bash
pwd  # Should end in /emulation-tutorial
python src/chip8.py roms/test-simple.ch8
```

### Black screen / nothing happens
- The ROM might be waiting for input
- Try pressing keys (`1`, `2`, `3`, etc.)
- Some ROMs are silent/empty - try a different one

### Emulator is too slow/fast
Edit `src/chip8.py` and change:
```python
CPU_HZ = 500  # Try 200-1000
```

Higher = faster, lower = slower.

## Next Steps

### Modify the Emulator
Try these exercises:

1. **Add sound**: Make it beep when sound_timer > 0
2. **Change colors**: Make pixels green instead of white
3. **Add pause**: Press `P` to pause/resume
4. **Save states**: Press `F5` to save, `F9` to load

### Learn More
- Read [docs/02-cpu-emulation.md](docs/02-cpu-emulation.md)
- Study [docs/05-testing-debugging.md](docs/05-testing-debugging.md)
- Join [/r/EmuDev](https://reddit.com/r/emudev)

### Build Something Harder
After CHIP-8, try:
1. **Space Invaders** (Intel 8080) - [Emulator 101](http://www.emulator101.com/)
2. **Game Boy** - [Pandocs](https://gbdev.io/pandocs/)
3. **NES** - [NESDev Wiki](http://wiki.nesdev.com/)

## Resources Quick Links

### Documentation
- [Core Concepts](docs/01-core-concepts.md) - Start here!
- [CPU Emulation](docs/02-cpu-emulation.md) - How CPUs work
- [Memory Systems](docs/03-memory-systems.md) - Understanding memory
- [Building CHIP-8](docs/04-building-chip8.md) - Step-by-step guide
- [Testing & Debugging](docs/05-testing-debugging.md) - Fix bugs

### External Resources
- [CHIP-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) - Official spec
- [Octo](https://johnearnest.github.io/Octo/) - CHIP-8 IDE
- [/r/EmuDev](https://reddit.com/r/emudev) - Community
- [Awesome CHIP-8](https://chip-8.github.io/links/) - More resources

### Books (Recommended)
- **"Code"** by Charles Petzold - How computers work (beginner-friendly)
- **"Computer Systems: A Programmer's Perspective"** - Deep dive (advanced)
- **"But How Do It Know?"** by J. Clark Scott - CPU basics (visual)

## Get Help

### Common Issues
Check [docs/05-testing-debugging.md](docs/05-testing-debugging.md)

### Ask Questions
- [/r/EmuDev](https://reddit.com/r/emudev) - Reddit community
- [EmuDev Discord](https://discord.gg/dkmJAes) - Real-time chat
- [GitHub Issues](link-to-your-repo/issues) - Bug reports

## Contributing

Found a bug? Have an improvement?
1. Fork the repository
2. Make your changes
3. Submit a pull request

All contributions welcome!

---

**Happy emulating!** 🎮

Start with [docs/01-core-concepts.md](docs/01-core-concepts.md) when you're ready to learn!
