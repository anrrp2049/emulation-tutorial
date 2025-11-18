# Comprehensive Emulation & Computer Architecture Resources

This is an extensive, curated list of resources for learning computer architecture and emulation development, organized by topic and skill level.

## 🎓 Complete Learning Paths

### Path 1: From Zero to Emulator Developer (Beginner)
**Total time: 3-6 months**

1. **Week 1-2**: "Code" by Charles Petzold (book)
   - Understand how computers work fundamentally
   - No prerequisites needed

2. **Week 3-6**: [Nand to Tetris](https://www.nand2tetris.org/) (FREE course)
   - Build a computer from logic gates
   - Implement an assembler and VM
   - **Highly recommended!**

3. **Week 7-8**: This CHIP-8 tutorial
   - Your first real emulator
   - Practical hands-on experience

4. **Week 9-12**: [Emulator 101](http://www.emulator101.com/)
   - Space Invaders (Intel 8080)
   - More realistic CPU

5. **Month 4+**: Game Boy emulation
   - Follow [Pandocs](https://gbdev.io/pandocs/)
   - Join [gbdev community](https://gbdev.io/)

### Path 2: Computer Architecture Deep Dive (Intermediate)
**Total time: 6-12 months**

1. **"Computer Systems: A Programmer's Perspective" (CS:APP)**
   - Industry-standard textbook
   - Deep understanding of systems

2. **[MIT 6.004 - Computation Structures](https://6004.mit.edu/)** (FREE)
   - Complete computer architecture course
   - Video lectures available

3. **[Computer Organization and Design](https://www.elsevier.com/books/computer-organization-and-design-risc-v-edition/patterson/978-0-12-820331-6)** (RISC-V Edition)
   - Patterson & Hennessy classic
   - RISC-V edition is modern and relevant

4. **Implement multiple emulators**:
   - CHIP-8 → 8080 → Game Boy → NES → RISC-V

### Path 3: Professional Emulation Development (Advanced)
**Total time: 12+ months**

1. **Cycle-accurate emulation**
   - Study existing accurate emulators
   - [Higan](https://github.com/higan-emu/higan) source code

2. **Dynamic recompilation (JIT)**
   - [Dolphin Emulator](https://github.com/dolphin-emu/dolphin) architecture docs
   - LLVM/JIT compilation techniques

3. **Hardware verification**
   - [FPGA implementations](https://github.com/MiSTer-devel/Main_MiSTer/wiki)
   - Verilog/VHDL basics

## 📚 Books (Organized by Topic)

### Beginner-Friendly (Start Here!)

**"Code: The Hidden Language of Computer Hardware and Software"** - Charles Petzold
- **Why**: Best introduction to computing, period
- **Prerequisites**: None
- **Topics**: Binary, logic gates, CPU basics, memory
- **Price**: ~$25
- **Alternative**: [Available at libraries]

**"But How Do It Know?"** - J. Clark Scott
- **Why**: Visual explanation of CPU internals
- **Prerequisites**: None
- **Topics**: CPU components, instruction execution
- **Price**: ~$12
- **Note**: Very accessible, uses diagrams

**"Digital Computer Electronics"** - Albert Malvino & Jerald Brown
- **Why**: Hands-on approach to digital logic
- **Prerequisites**: Basic electronics helpful
- **Topics**: Logic gates, flip-flops, simple CPU design
- **Price**: ~$30

### Intermediate (Core Knowledge)

**"Computer Systems: A Programmer's Perspective" (CS:APP)** - Bryant & O'Hallaron
- **Why**: Industry standard, used at top universities
- **Prerequisites**: C programming
- **Topics**: Assembly, memory hierarchy, linking, I/O, concurrency
- **Price**: ~$100 (worth it!)
- **Free alternative**: [CMU course materials](http://csapp.cs.cmu.edu/)

**"Computer Organization and Design"** (RISC-V Edition) - Patterson & Hennessy
- **Why**: The architecture bible, RISC-V is modern and open
- **Prerequisites**: Basic programming
- **Topics**: Instruction sets, pipelining, memory, I/O
- **Price**: ~$90
- **Free**: RISC-V specs at [riscv.org](https://riscv.org/technical/specifications/)

**"The Elements of Computing Systems"** - Nisan & Schocken
- **Why**: Companion to Nand to Tetris course
- **Prerequisites**: None
- **Topics**: Complete computer from scratch
- **Price**: ~$40
- **Free alternative**: [Nand2Tetris website](https://www.nand2tetris.org/)

### Advanced (Deep Expertise)

**"Computer Architecture: A Quantitative Approach"** - Hennessy & Patterson
- **Why**: Graduate-level, comprehensive
- **Prerequisites**: Solid CS background
- **Topics**: Advanced pipelining, ILP, memory hierarchy, multiprocessors
- **Price**: ~$95

**"Modern Processor Design: Fundamentals of Superscalar Processors"** - Shen & Lipasti
- **Why**: Modern CPU techniques
- **Prerequisites**: Computer architecture basics
- **Topics**: Superscalar execution, branch prediction, out-of-order execution
- **Price**: ~$85

**"Compilers: Principles, Techniques, and Tools"** (Dragon Book) - Aho, Lam, Sethi, Ullman
- **Why**: Essential for JIT/recompilation
- **Prerequisites**: Data structures, algorithms
- **Topics**: Parsing, optimization, code generation
- **Price**: ~$100

### Specialized Topics

**"Game Engine Black Book: Wolfenstein 3D"** - Fabien Sanglard
- **Why**: Reverse engineering + optimization masterclass
- **Prerequisites**: C programming
- **Topics**: DOS internals, VGA, optimization, 3D rendering
- **Price**: ~$45
- **Note**: Available free at [fabiensanglard.net](https://fabiensanglard.net/)

**"Game Engine Black Book: DOOM"** - Fabien Sanglard
- **Why**: More advanced than Wolfenstein
- **Prerequisites**: Same as above
- **Topics**: BSP trees, networking, sound, more complex rendering
- **Price**: ~$45

**"Programming the 65816"** - Eyes & Lichty
- **Why**: Deep dive into SNES CPU
- **Prerequisites**: Assembly basics
- **Topics**: 65816 assembly, addressing modes, optimization
- **Price**: ~$50 (used)
- **Note**: Hard to find, but excellent

**"Hacker's Delight"** - Henry Warren
- **Why**: Bit manipulation wizardry
- **Prerequisites**: Programming basics
- **Topics**: Bit tricks, optimization, clever algorithms
- **Price**: ~$60
- **Use**: Essential for efficient emulation

## 🌐 Free Online Courses

### Complete Courses (Video Lectures)

**[Nand to Tetris (Build a Modern Computer from First Principles)](https://www.nand2tetris.org/)**
- **Provider**: Hebrew University / Coursera
- **Level**: Beginner to Intermediate
- **Length**: ~40 hours
- **Topics**: Logic gates → ALU → CPU → Assembler → VM → Compiler
- **Why**: Best bottom-up computer science course
- **Certificate**: Available on Coursera (paid)

**[MIT 6.004 - Computation Structures](https://6004.mit.edu/)**
- **Provider**: MIT OpenCourseWare
- **Level**: Intermediate
- **Length**: Full semester
- **Topics**: Digital design, CPU architecture, caches, pipelining
- **Videos**: [YouTube playlist](https://www.youtube.com/playlist?list=PLUl4u3cNGP62WVs95MNq3dQBqY2vGOtQ2)
- **Labs**: RISC-V CPU design

**[Berkeley CS61C - Great Ideas in Computer Architecture](https://cs61c.org/)**
- **Provider**: UC Berkeley
- **Level**: Intermediate
- **Length**: Full semester
- **Topics**: C, RISC-V assembly, CPU design, caches, parallelism
- **Videos**: [YouTube](https://www.youtube.com/c/CS61C)
- **Projects**: RISC-V emulator, CPU in Logisim

**[Coursera: Computer Architecture](https://www.coursera.org/learn/comparch)**
- **Provider**: Princeton University
- **Level**: Intermediate to Advanced
- **Length**: 10 weeks
- **Topics**: Pipelining, caches, virtual memory, multicore
- **Certificate**: Paid (~$50)

**[From Nand to Raytracing](https://github.com/ghaetinger/from-nand-to-raytracing)**
- **Provider**: Community project
- **Level**: Advanced
- **Length**: Self-paced
- **Topics**: Extends Nand2Tetris to graphics
- **Note**: Work in progress but excellent

### Specialized Courses

**[Digital Electronics and Computer Architecture (ETH Zurich)](https://safari.ethz.ch/digitaltechnik/spring2021/doku.php)**
- **Provider**: ETH Zurich
- **Level**: Intermediate
- **Topics**: Digital logic, RISC-V design
- **Videos**: Free on website

**[Onur Mutlu's Lecture Series](https://www.youtube.com/c/OnurMutluLectures)**
- **Provider**: ETH Zurich / CMU
- **Level**: Advanced
- **Topics**: Memory systems, computer architecture research
- **Free**: All on YouTube
- **Note**: Cutting-edge research topics

**[Ben Eater's 8-bit Computer](https://eater.net/8bit)**
- **Provider**: Ben Eater (YouTube)
- **Level**: Beginner to Intermediate
- **Length**: ~60 videos
- **Topics**: Build breadboard computer from scratch
- **Kit**: Available for purchase (~$200)
- **Why**: Incredibly visual and hands-on

## 🔗 Essential Websites & Communities

### Emulation Development

**[/r/EmuDev](https://www.reddit.com/r/EmuDev/)**
- Active subreddit for emulator developers
- Weekly question threads
- Project showcases
- [Wiki with resources](https://www.reddit.com/r/EmuDev/wiki/index)

**[EmuDev Discord](https://discord.gg/dkmJAes)**
- Real-time help and discussion
- Very active and helpful community
- Channels for different systems

**[Emulator 101](http://www.emulator101.com/)**
- Space Invaders emulation tutorial
- Intel 8080 CPU
- Step-by-step guide

**[How to Write a Computer Emulator](http://fms.komkon.org/EMUL8/HOWTO.html)**
- Classic emulation guide by Marat Fayzullin
- General principles
- Multiple system examples

**[Emulation General Wiki](https://emulation.gametechwiki.com/)**
- Comprehensive emulator database
- Accuracy comparisons
- System specifications

### CPU Documentation

**[6502.org](http://www.6502.org/)**
- Complete 6502 CPU documentation
- Used in: NES, Apple II, Commodore 64, Atari 2600
- Tutorials, datasheets, forums

**[Z80 Heaven](http://z80-heaven.wikidot.com/)**
- Z80 CPU documentation and tutorials
- Used in: Game Boy, Sega Master System
- Assembly programming guides

**[RISC-V International](https://riscv.org/)**
- Complete RISC-V specifications (FREE!)
- Modern, clean instruction set
- Growing emulation ecosystem

**[ARM Architecture Reference Manual](https://developer.arm.com/documentation/)**
- Official ARM documentation
- Required for Game Boy Advance, Nintendo DS
- Some parts free, some require account

**[Intel Software Developer Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)**
- Complete x86/x64 documentation
- FREE download
- Thousands of pages, very detailed

### System-Specific Resources

**Game Boy**
- **[Pandocs](https://gbdev.io/pandocs/)**: THE Game Boy reference
- **[gbdev.io](https://gbdev.io/)**: Community hub
- **[Awesome Game Boy Dev](https://github.com/gbdev/awesome-gbdev)**: Curated resources
- **[Emulator Development Discord](https://discord.gg/gpBxq85)**: Active community

**NES**
- **[NESDev Wiki](http://wiki.nesdev.com/)**: Comprehensive NES documentation
- **[NESDev Forums](https://forums.nesdev.org/)**: Very active community
- **[6502 Assembly Tutorial](https://skilldrick.github.io/easy6502/)**: Interactive!

**SNES**
- **[SNES Dev Wiki](https://wiki.superfamicom.org/)**: SNES documentation
- **[SNES Dev Manual](https://archive.org/details/SNESDevManual)**: Official dev docs

**Sega Genesis**
- **[Mega Drive Dev Wiki](https://wiki.megadrive.org/)**: Genesis/MD documentation
- **[68000 Programmer's Reference](http://68k.hax.com/)**: Motorola 68000 CPU

**PlayStation**
- **[PSX-SPX](https://psx-spx.consoledev.net/)**: PS1 hardware specifications
- **[No$ PSX](https://problemkaputt.de/psx-spx.htm)**: Alternative detailed specs

**Arcade**
- **[MAME Source](https://github.com/mamedev/mame)**: Study driver implementations
- **[Arcade Hardware Database](https://www.arcade-museum.com/)**: Schematics and info

### Learning Platforms

**[OSDev Wiki](https://wiki.osdev.org/)**
- Operating system development
- Low-level programming
- Hardware interfaces
- Bootloaders, kernels, drivers

**[CPU Land](https://cpu.land/)**
- Modern, interactive guide to how CPUs work
- Beautiful visualizations
- Free and comprehensive

**[Visual 6502](http://www.visual6502.org/)**
- Interactive 6502 transistor-level simulation
- See exactly how the CPU works
- Incredible educational tool

**[The 8-Bit Guy](https://www.youtube.com/c/The8BitGuy)**
- Vintage computer restoration and programming
- Great for understanding old hardware

**[Computerphile](https://www.youtube.com/user/Computerphile)**
- Computer science concepts explained
- Professor interviews
- Various CS topics

## 🛠️ Tools & Software

### Emulation Development

**[Ghidra](https://ghidra-sre.org/)** (FREE)
- NSA's reverse engineering tool
- Disassembler and decompiler
- Essential for understanding ROMs

**[Radare2](https://rada.re/)** (FREE)
- Open-source reverse engineering framework
- Scriptable and powerful
- Steep learning curve

**[IDA Pro](https://hex-rays.com/ida-pro/)**
- Industry standard disassembler
- Paid (~$600+) but has free version
- Very powerful

**[Binary Ninja](https://binary.ninja/)**
- Modern disassembler
- Good alternative to IDA
- Paid (~$300) with educational discounts

**[Octo](https://johnearnest.github.io/Octo/)** (FREE)
- CHIP-8 IDE in browser
- Assembler, debugger, emulator
- Perfect for testing

**[ASM80](https://www.asm80.com/)** (FREE)
- Online assembler for multiple CPUs
- Includes 8080, Z80, 6502, 6809
- Great for quick tests

### Hardware Simulation

**[Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution)** (FREE)
- Digital circuit simulator
- Build CPUs visually
- Used in many university courses

**[Digital](https://github.com/hneemann/Digital)** (FREE)
- Modern circuit simulator
- Better than Logisim in many ways
- Great for CPU design

**[Verilog/VHDL Simulators](https://www.edaplayground.com/)** (FREE)
- Hardware description languages
- For FPGA development
- Online playground available

**[QEMU](https://www.qemu.org/)** (FREE)
- Full system emulator
- Study the source code
- Supports many architectures

### Debugging

**[GDB](https://www.gnu.org/software/gdb/)** (FREE)
- The GNU debugger
- Essential for debugging emulators
- Works with many architectures

**[RetroDebugger](https://github.com/sunsided/retrodebugger)** (FREE)
- Multi-platform retro debugger
- C64, Atari, NES support
- Great for learning

**[BizHawk](https://github.com/TASEmulators/BizHawk)** (FREE)
- Multi-system emulator with debugging
- Used for tool-assisted speedruns
- Excellent debugging features

**[Mesen](https://www.mesen.ca/)** (FREE)
- NES/SNES emulator with amazing debugger
- Best-in-class debugging tools
- Study for emulator features

## 📖 Online Documentation

### CPU Datasheets

**8-bit CPUs**
- [6502 Datasheet](http://archive.6502.org/datasheets/mos_6502_preliminary_nov_1975.pdf)
- [Z80 User Manual](http://www.zilog.com/docs/z80/um0080.pdf)
- [Intel 8080 Manual](http://bitsavers.org/components/intel/MCS80/9800301D_8080_8085_Assembly_Language_Programming_Manual_May81.pdf)

**16-bit CPUs**
- [68000 Programmer's Reference](http://68k.hax.com/)
- [65816 Reference](http://www.obelisk.me.uk/65816/)
- [Intel 8086 Manual](https://edge.edx.org/c4x/BITSPilani/EEE231/asset/8086_family_Users_Manual_1_.pdf)

**Modern CPUs**
- [RISC-V Specs](https://riscv.org/technical/specifications/)
- [ARM Cortex-M](https://developer.arm.com/documentation/ddi0403/latest/)
- [Intel x86](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)

### Graphics Hardware

**Retro Graphics**
- [VGA Hardware](http://www.osdever.net/FreeVGA/vga/vga.htm)
- [CGA/EGA Documentation](http://www.minuszerodegrees.net/video/video.htm)

**Console Graphics**
- [NES PPU](https://wiki.nesdev.com/w/index.php/PPU)
- [Game Boy PPU](https://gbdev.io/pandocs/pixel_fifo.html)
- [SNES PPU](https://problemkaputt.de/fullsnes.htm#snesppu)
- [Genesis VDP](https://wiki.megadrive.org/index.php?title=VDP)

### Sound Hardware

**Sound Chips**
- [SID (C64)](https://www.waitingforfriday.com/?p=661)
- [NES APU](https://wiki.nesdev.com/w/index.php/APU)
- [Game Boy Sound](https://gbdev.io/pandocs/Audio.html)
- [YM2612 (Genesis)](http://www.smspower.org/maxim/Documents/YM2612)

## 🎯 Project Ideas (Progressive Difficulty)

### Tier 1: Foundation (1-2 weeks each)

1. **Simple Stack Machine**
   - PUSH, POP, ADD, SUB
   - 10-15 instructions
   - Great for understanding VM basics

2. **CHIP-8** (This tutorial!)
   - 35 instructions
   - Graphics and input
   - Excellent first project

3. **Brainfuck Interpreter**
   - Only 8 instructions
   - Turing complete
   - Very simple

### Tier 2: Intermediate (1-3 months each)

4. **Space Invaders (Intel 8080)**
   - Realistic CPU (~80 opcodes)
   - Interrupts
   - [Follow Emulator 101](http://www.emulator101.com/)

5. **CHIP-8 Extensions**
   - SUPER-CHIP (128x64, more instructions)
   - XO-CHIP (audio, color)
   - Good practice before moving on

6. **LC-3 (Learning Computer 3)**
   - Educational CPU
   - Well-documented
   - [Textbook available](https://www.amazon.com/Introduction-Computing-Systems-Gates-Beyond/dp/0072467509)

### Tier 3: Advanced (3-6 months each)

7. **Game Boy**
   - Complex PPU
   - Memory banking
   - Large community
   - [Excellent docs](https://gbdev.io/pandocs/)

8. **NES**
   - 6502 CPU
   - Separate PPU
   - Mappers add complexity
   - Huge game library

9. **RISC-V**
   - Modern, clean ISA
   - Good for learning modern techniques
   - [Spec is free](https://riscv.org/technical/specifications/)

### Tier 4: Expert (6+ months each)

10. **Game Boy Advance**
    - ARM7TDMI CPU
    - Mode 7 graphics
    - DMA, timers, interrupts

11. **SNES**
    - 65816 CPU
    - Complex PPU
    - Multiple co-processors (SA-1, SuperFX, etc.)

12. **PlayStation**
    - MIPS R3000A CPU
    - GPU with 3D capabilities
    - CD-ROM drive
    - Complex architecture

### Research Projects

13. **JIT Recompiler**
    - Dynamic recompilation
    - LLVM backend
    - 10x+ speed improvements

14. **Cycle-Accurate Emulation**
    - Hardware-perfect timing
    - Pass timing tests
    - Required for some games

15. **FPGA Implementation**
    - Hardware description (Verilog/VHDL)
    - Real hardware
    - MiSTer platform

## 🎓 University Courses (Free Materials)

**[CMU 15-213: Introduction to Computer Systems](http://www.cs.cmu.edu/~213/)**
- Complete course materials
- Lectures, labs, assignments
- Uses CS:APP textbook

**[Stanford CS107: Computer Organization & Systems](https://web.stanford.edu/class/cs107/)**
- C programming and systems
- Memory, pointers, assembly

**[UC Berkeley CS152: Computer Architecture and Engineering](https://inst.eecs.berkeley.edu/~cs152/)**
- Advanced architecture topics
- RISC-V focus

**[MIT 6.172: Performance Engineering](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/)**
- Optimization techniques
- Profiling, parallelization
- Directly applicable to emulation

**[Georgia Tech CS 6290: High Performance Computer Architecture](https://omscs.gatech.edu/cs-6290-high-performance-computer-architecture)**
- Graduate-level architecture
- Advanced topics

## 🔬 Research Papers (Freely Available)

**Foundational**
- "RISC-V: An Open Standard for SoCs" - Waterman et al.
- "The Case for RISC" - Patterson & Ditzel

**Emulation Techniques**
- "Dynamo: A Transparent Dynamic Optimization System" (JIT)
- "QEMU, a Fast and Portable Dynamic Translator"

**Find at**:
- [Google Scholar](https://scholar.google.com/)
- [arXiv](https://arxiv.org/)
- [ACM Digital Library](https://dl.acm.org/) (many papers free)

## 💡 Practical Applications of Emulation Knowledge

### Career Paths

1. **Embedded Systems Engineering**
   - Understanding low-level hardware
   - Firmware development
   - Debugging hardware/software interface

2. **Compiler Development**
   - Code generation for different architectures
   - Optimization techniques
   - Understanding target platforms

3. **Virtualization/Cloud**
   - VMware, QEMU, VirtualBox
   - Container technology (Docker)
   - Understanding system boundaries

4. **Security Research**
   - Reverse engineering malware
   - Finding vulnerabilities
   - Understanding exploit techniques

5. **Game Development**
   - Console programming
   - Platform-specific optimization
   - Understanding hardware limits

6. **Digital Preservation**
   - Keeping old software running
   - Museums and archives
   - Cultural preservation

### Transferable Skills

- **Low-level debugging**: Finding subtle bugs
- **Performance optimization**: Making code fast
- **Reading specifications**: Working from datasheets
- **Reverse engineering**: Understanding unknown systems
- **Bitwise operations**: Efficient data manipulation
- **State management**: Complex system state
- **Testing methodologies**: Ensuring correctness

## 🏆 Challenge Problems

Test your knowledge:

1. **Implement a CPU feature**:
   - Add breakpoints to CHIP-8
   - Implement save states
   - Add rewind/replay

2. **Optimize for speed**:
   - Profile your emulator
   - Implement opcode caching
   - Try JIT compilation

3. **Add debugging features**:
   - Disassembler
   - Memory viewer
   - Register watch

4. **Port to another language**:
   - C++ for speed
   - Rust for safety
   - JavaScript for web

5. **Implement another architecture**:
   - 6502 variant
   - RISC-V subset
   - Custom ISA

## 📱 Mobile/Web Resources

**Mobile Apps**
- **iCircuit** (iOS): Circuit simulator on phone
- **Assembly Programming** (Android): ARM assembly on mobile
- **Programmer's Toolkit** (iOS/Android): Hex/binary calculator

**Web Tools**
- [Compiler Explorer](https://godbolt.org/): See assembly from C/C++
- [CPU Simulator](https://cpusim.github.io/): Web-based CPU sim
- [Emulator.online](https://emulator.online/): Run emulators in browser

## 🎮 Game Development Perspective

Understanding emulation helps with:

**Console Programming**
- Nintendo Switch development
- PlayStation/Xbox optimization
- Understanding platform constraints

**Retro Game Development**
- NES homebrew ([NESmaker](https://www.thenew8bitheroes.com/))
- Game Boy homebrew ([GBDK](https://github.com/gbdk-2020/gbdk-2020))
- Writing for actual hardware

**Performance Optimization**
- Cache-friendly code
- SIMD operations
- Platform-specific tricks

## 🌟 Notable Open-Source Emulators to Study

**Learning from the best**:

- **[Dolphin](https://github.com/dolphin-emu/dolphin)**: GameCube/Wii (C++)
  - Professional architecture
  - JIT recompilation
  - Excellent documentation

- **[FCEUX](https://github.com/TASEmulators/fceux)**: NES (C++)
  - Very readable code
  - Good for learning NES

- **[SameBoy](https://github.com/LIJI32/SameBoy)**: Game Boy (C)
  - Extremely accurate
  - Clean, educational code

- **[Mesen](https://github.com/SourMesen/Mesen2)**: NES/SNES (C++)
  - Amazing debugger
  - High accuracy

- **[Unicorn](https://github.com/unicorn-engine/unicorn)**: Multi-arch CPU (C)
  - Based on QEMU
  - Used for security research

## 📊 Roadmap Summary

```
Month 1-2:   CHIP-8 + Fundamentals
Month 3-4:   8080 + Computer Architecture
Month 5-6:   Game Boy + Advanced Topics
Month 7-12:  NES/SNES + Optimization
Year 2+:     PS1/N64 or JIT/FPGA
```

## 🎯 Quick Reference

**Best single resource**: Nand to Tetris (free)
**Best book**: "Code" by Petzold for beginners, CS:APP for depth
**Best community**: /r/EmuDev + Discord
**Best first project**: CHIP-8 (you're here!)
**Best second project**: Space Invaders (8080)
**Best long-term project**: Game Boy

---

**Remember**: Emulation is a marathon, not a sprint. Take your time, understand deeply, and enjoy the journey!

**Questions?** Join [/r/EmuDev](https://www.reddit.com/r/EmuDev/) or [Discord](https://discord.gg/dkmJAes)!
