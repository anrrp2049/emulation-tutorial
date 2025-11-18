#!/usr/bin/env python3
"""
CHIP-8 Emulator - Complete Implementation
==========================================

This is a fully functional CHIP-8 emulator that demonstrates all core emulation concepts:
- CPU fetch-decode-execute cycle
- Memory management
- Opcode implementation
- Graphics rendering
- Input handling
- Timing

CHIP-8 Specification:
- 4KB RAM (4096 bytes)
- 16 8-bit registers (V0-VF)
- 16-bit index register (I)
- 16-bit program counter (PC)
- 16-level stack
- 64x32 monochrome display
- 16-key hexadecimal keypad
- Two timers (delay and sound, both at 60Hz)

Usage:
    python chip8.py <rom_file>

References:
- Cowgod's CHIP-8 Technical Reference: http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
- CHIP-8 Extensions: https://chip-8.github.io/extensions/
"""

import sys
import random
import pygame
from typing import List


class CHIP8:
    """
    CHIP-8 Emulator Implementation

    This class represents the complete state and behavior of a CHIP-8 virtual machine.
    """

    # Display constants
    DISPLAY_WIDTH = 64
    DISPLAY_HEIGHT = 32
    SCALE = 10  # Scale factor for rendering (640x320 window)

    # Timing constants
    CPU_HZ = 500  # CPU cycles per second (configurable, 500-700 typical)
    TIMER_HZ = 60  # Timer frequency (fixed at 60Hz)
    FPS = 60  # Display refresh rate

    def __init__(self, debug=False):
        """
        Initialize the CHIP-8 emulator to its default state.

        Args:
            debug: If True, print debug information during execution
        """
        self.debug = debug

        # Memory: 4KB RAM (addresses 0x000 to 0xFFF)
        # 0x000-0x1FF: Reserved for interpreter and font data
        # 0x200-0xFFF: Program ROM and work RAM
        self.memory: List[int] = [0] * 4096

        # Registers: 16 general-purpose 8-bit registers V0-VF
        # VF (V[15]) is used as a flag register by some instructions
        self.V: List[int] = [0] * 16

        # Index register: 16-bit register used for memory operations
        self.I: int = 0

        # Program counter: Points to the current instruction in memory
        # Programs start at 0x200
        self.pc: int = 0x200

        # Stack: Stores return addresses for subroutine calls (16 levels)
        self.stack: List[int] = [0] * 16

        # Stack pointer: Points to the top of the stack
        self.sp: int = 0

        # Timers: Both count down at 60Hz when non-zero
        self.delay_timer: int = 0  # General purpose timer
        self.sound_timer: int = 0  # Beep while non-zero

        # Display: 64x32 pixels, monochrome (0 = off, 1 = on)
        self.display: List[List[int]] = [[0] * self.DISPLAY_WIDTH for _ in range(self.DISPLAY_HEIGHT)]

        # Input: 16-key hexadecimal keypad (0-F)
        self.keys: List[int] = [0] * 16

        # Control flags
        self.running: bool = True
        self.draw_flag: bool = False  # Set when display needs redrawing

        # Load font data into memory
        self.load_font()

        # Instruction cycle counter (for timing)
        self.cycle_count: int = 0

    def load_font(self):
        """
        Load built-in font sprites into memory at 0x050-0x09F.

        CHIP-8 includes sprites for hexadecimal digits 0-F.
        Each sprite is 5 bytes (4x5 pixels).
        Programs use these by setting I to the sprite's address.
        """
        # Font sprites: Each row is a byte where set bits = lit pixels
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

        # Load fonts starting at address 0x50
        for i, byte in enumerate(fonts):
            self.memory[0x50 + i] = byte

    def load_rom(self, filepath: str):
        """
        Load a CHIP-8 ROM file into memory starting at address 0x200.

        Args:
            filepath: Path to the ROM file

        The ROM file is raw binary data containing CHIP-8 instructions.
        """
        try:
            with open(filepath, 'rb') as f:
                rom_data = f.read()

            # Ensure ROM fits in available memory (0x200 to 0xFFF)
            max_size = 4096 - 0x200
            if len(rom_data) > max_size:
                raise ValueError(f"ROM too large: {len(rom_data)} bytes (max {max_size})")

            # Load ROM into memory
            for i, byte in enumerate(rom_data):
                self.memory[0x200 + i] = byte

            print(f"Loaded ROM: {filepath} ({len(rom_data)} bytes)")

        except FileNotFoundError:
            print(f"Error: ROM file not found: {filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading ROM: {e}")
            sys.exit(1)

    def cycle(self):
        """
        Execute one CPU cycle: Fetch, Decode, Execute.

        This is the heart of the emulator!

        1. FETCH: Read the instruction at PC
        2. DECODE: Figure out what the instruction means
        3. EXECUTE: Perform the operation
        4. UPDATE: Move PC to next instruction (may be modified by jumps)
        """
        # FETCH: Read 16-bit opcode from memory (big-endian)
        # CHIP-8 instructions are 2 bytes, stored in big-endian format
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]

        # Debug output
        if self.debug:
            self.print_debug(opcode)

        # Increment PC before execution
        # (Jump instructions will override this)
        self.pc += 2

        # Ensure PC stays within valid memory range
        self.pc &= 0xFFF

        # DECODE & EXECUTE: Process the opcode
        self.execute_opcode(opcode)

        # Increment cycle counter
        self.cycle_count += 1

    def execute_opcode(self, opcode: int):
        """
        Decode and execute a single opcode.

        This method uses pattern matching to identify the instruction
        and call the appropriate handler.

        Args:
            opcode: 16-bit instruction to execute
        """
        # Extract commonly used values from the opcode
        # Most instructions follow the pattern: TNNN or TXYN
        first_nibble = (opcode & 0xF000) >> 12  # Type identifier
        x = (opcode & 0x0F00) >> 8               # Register X
        y = (opcode & 0x00F0) >> 4               # Register Y
        n = opcode & 0x000F                      # 4-bit value
        nn = opcode & 0x00FF                     # 8-bit value
        nnn = opcode & 0x0FFF                    # 12-bit address

        # Decode by pattern matching on opcode structure
        # Some opcodes are exact matches, others match by nibble patterns

        if opcode == 0x00E0:
            # 00E0: CLS - Clear the display
            self.op_00E0()

        elif opcode == 0x00EE:
            # 00EE: RET - Return from subroutine
            self.op_00EE()

        elif first_nibble == 0x1:
            # 1NNN: JP addr - Jump to address NNN
            self.op_1NNN(nnn)

        elif first_nibble == 0x2:
            # 2NNN: CALL addr - Call subroutine at NNN
            self.op_2NNN(nnn)

        elif first_nibble == 0x3:
            # 3XNN: SE Vx, byte - Skip next instruction if VX == NN
            self.op_3XNN(x, nn)

        elif first_nibble == 0x4:
            # 4XNN: SNE Vx, byte - Skip next instruction if VX != NN
            self.op_4XNN(x, nn)

        elif first_nibble == 0x5:
            # 5XY0: SE Vx, Vy - Skip next instruction if VX == VY
            self.op_5XY0(x, y)

        elif first_nibble == 0x6:
            # 6XNN: LD Vx, byte - Set VX = NN
            self.op_6XNN(x, nn)

        elif first_nibble == 0x7:
            # 7XNN: ADD Vx, byte - Set VX = VX + NN
            self.op_7XNN(x, nn)

        elif first_nibble == 0x8:
            # 8XY?: Arithmetic and logic operations
            # Last nibble determines the operation
            self.decode_8XY_(opcode, x, y, n)

        elif first_nibble == 0x9:
            # 9XY0: SNE Vx, Vy - Skip next instruction if VX != VY
            self.op_9XY0(x, y)

        elif first_nibble == 0xA:
            # ANNN: LD I, addr - Set I = NNN
            self.op_ANNN(nnn)

        elif first_nibble == 0xB:
            # BNNN: JP V0, addr - Jump to NNN + V0
            self.op_BNNN(nnn)

        elif first_nibble == 0xC:
            # CXNN: RND Vx, byte - Set VX = random byte AND NN
            self.op_CXNN(x, nn)

        elif first_nibble == 0xD:
            # DXYN: DRW Vx, Vy, nibble - Draw sprite
            self.op_DXYN(x, y, n)

        elif first_nibble == 0xE:
            # EX??: Keypress instructions
            self.decode_EX__(opcode, x, nn)

        elif first_nibble == 0xF:
            # FX??: Various utility instructions
            self.decode_FX__(opcode, x, nn)

        else:
            print(f"Unknown opcode: {opcode:04X}")

    def decode_8XY_(self, opcode: int, x: int, y: int, n: int):
        """Decode and execute 8XY? arithmetic/logic opcodes"""
        if n == 0x0:
            # 8XY0: LD Vx, Vy - Set VX = VY
            self.V[x] = self.V[y]

        elif n == 0x1:
            # 8XY1: OR Vx, Vy - Set VX = VX OR VY
            self.V[x] |= self.V[y]
            self.V[x] &= 0xFF

        elif n == 0x2:
            # 8XY2: AND Vx, Vy - Set VX = VX AND VY
            self.V[x] &= self.V[y]

        elif n == 0x3:
            # 8XY3: XOR Vx, Vy - Set VX = VX XOR VY
            self.V[x] ^= self.V[y]
            self.V[x] &= 0xFF

        elif n == 0x4:
            # 8XY4: ADD Vx, Vy - Set VX = VX + VY, VF = carry
            self.op_8XY4(x, y)

        elif n == 0x5:
            # 8XY5: SUB Vx, Vy - Set VX = VX - VY, VF = NOT borrow
            self.op_8XY5(x, y)

        elif n == 0x6:
            # 8XY6: SHR Vx - Set VX = VX >> 1, VF = LSB before shift
            self.op_8XY6(x, y)

        elif n == 0x7:
            # 8XY7: SUBN Vx, Vy - Set VX = VY - VX, VF = NOT borrow
            self.op_8XY7(x, y)

        elif n == 0xE:
            # 8XYE: SHL Vx - Set VX = VX << 1, VF = MSB before shift
            self.op_8XYE(x, y)

        else:
            print(f"Unknown 8XY? opcode: {opcode:04X}")

    def decode_EX__(self, opcode: int, x: int, nn: int):
        """Decode and execute EX?? keypress opcodes"""
        if nn == 0x9E:
            # EX9E: SKP Vx - Skip next instruction if key VX is pressed
            if self.keys[self.V[x] & 0xF] == 1:
                self.pc += 2

        elif nn == 0xA1:
            # EXA1: SKNP Vx - Skip next instruction if key VX is not pressed
            if self.keys[self.V[x] & 0xF] == 0:
                self.pc += 2

        else:
            print(f"Unknown EX?? opcode: {opcode:04X}")

    def decode_FX__(self, opcode: int, x: int, nn: int):
        """Decode and execute FX?? utility opcodes"""
        if nn == 0x07:
            # FX07: LD Vx, DT - Set VX = delay timer
            self.V[x] = self.delay_timer

        elif nn == 0x0A:
            # FX0A: LD Vx, K - Wait for key press, store in VX
            self.op_FX0A(x)

        elif nn == 0x15:
            # FX15: LD DT, Vx - Set delay timer = VX
            self.delay_timer = self.V[x]

        elif nn == 0x18:
            # FX18: LD ST, Vx - Set sound timer = VX
            self.sound_timer = self.V[x]

        elif nn == 0x1E:
            # FX1E: ADD I, Vx - Set I = I + VX
            self.I += self.V[x]
            self.I &= 0xFFF  # Keep within 12-bit range

        elif nn == 0x29:
            # FX29: LD F, Vx - Set I = location of sprite for digit VX
            # Font sprites are 5 bytes each, starting at 0x50
            self.I = 0x50 + (self.V[x] & 0xF) * 5

        elif nn == 0x33:
            # FX33: LD B, Vx - Store BCD representation of VX
            self.op_FX33(x)

        elif nn == 0x55:
            # FX55: LD [I], Vx - Store V0-VX in memory starting at I
            self.op_FX55(x)

        elif nn == 0x65:
            # FX65: LD Vx, [I] - Load V0-VX from memory starting at I
            self.op_FX65(x)

        else:
            print(f"Unknown FX?? opcode: {opcode:04X}")

    # ============================================
    # OPCODE IMPLEMENTATIONS
    # ============================================

    def op_00E0(self):
        """00E0: CLS - Clear the display"""
        self.display = [[0] * self.DISPLAY_WIDTH for _ in range(self.DISPLAY_HEIGHT)]
        self.draw_flag = True

    def op_00EE(self):
        """00EE: RET - Return from subroutine"""
        self.sp -= 1
        self.pc = self.stack[self.sp]

    def op_1NNN(self, nnn: int):
        """1NNN: JP addr - Jump to address NNN"""
        self.pc = nnn

    def op_2NNN(self, nnn: int):
        """2NNN: CALL addr - Call subroutine at NNN"""
        self.stack[self.sp] = self.pc
        self.sp += 1
        self.pc = nnn

    def op_3XNN(self, x: int, nn: int):
        """3XNN: SE Vx, byte - Skip next instruction if VX == NN"""
        if self.V[x] == nn:
            self.pc += 2

    def op_4XNN(self, x: int, nn: int):
        """4XNN: SNE Vx, byte - Skip next instruction if VX != NN"""
        if self.V[x] != nn:
            self.pc += 2

    def op_5XY0(self, x: int, y: int):
        """5XY0: SE Vx, Vy - Skip next instruction if VX == VY"""
        if self.V[x] == self.V[y]:
            self.pc += 2

    def op_6XNN(self, x: int, nn: int):
        """6XNN: LD Vx, byte - Set VX = NN"""
        self.V[x] = nn

    def op_7XNN(self, x: int, nn: int):
        """7XNN: ADD Vx, byte - Set VX = VX + NN (no carry flag)"""
        self.V[x] = (self.V[x] + nn) & 0xFF

    def op_8XY4(self, x: int, y: int):
        """8XY4: ADD Vx, Vy - Set VX = VX + VY, VF = carry"""
        result = self.V[x] + self.V[y]
        self.V[0xF] = 1 if result > 255 else 0
        self.V[x] = result & 0xFF

    def op_8XY5(self, x: int, y: int):
        """8XY5: SUB Vx, Vy - Set VX = VX - VY, VF = NOT borrow"""
        self.V[0xF] = 1 if self.V[x] >= self.V[y] else 0
        self.V[x] = (self.V[x] - self.V[y]) & 0xFF

    def op_8XY6(self, x: int, y: int):
        """8XY6: SHR Vx - Set VX = VX >> 1, VF = LSB before shift"""
        # Note: Original CHIP-8 used VY, modern implementations use VX
        self.V[0xF] = self.V[x] & 0x1
        self.V[x] >>= 1

    def op_8XY7(self, x: int, y: int):
        """8XY7: SUBN Vx, Vy - Set VX = VY - VX, VF = NOT borrow"""
        self.V[0xF] = 1 if self.V[y] >= self.V[x] else 0
        self.V[x] = (self.V[y] - self.V[x]) & 0xFF

    def op_8XYE(self, x: int, y: int):
        """8XYE: SHL Vx - Set VX = VX << 1, VF = MSB before shift"""
        # Note: Original CHIP-8 used VY, modern implementations use VX
        self.V[0xF] = (self.V[x] & 0x80) >> 7
        self.V[x] = (self.V[x] << 1) & 0xFF

    def op_9XY0(self, x: int, y: int):
        """9XY0: SNE Vx, Vy - Skip next instruction if VX != VY"""
        if self.V[x] != self.V[y]:
            self.pc += 2

    def op_ANNN(self, nnn: int):
        """ANNN: LD I, addr - Set I = NNN"""
        self.I = nnn

    def op_BNNN(self, nnn: int):
        """BNNN: JP V0, addr - Jump to NNN + V0"""
        self.pc = nnn + self.V[0]

    def op_CXNN(self, x: int, nn: int):
        """CXNN: RND Vx, byte - Set VX = random byte AND NN"""
        self.V[x] = random.randint(0, 255) & nn

    def op_DXYN(self, x: int, y: int, n: int):
        """
        DXYN: DRW Vx, Vy, nibble - Draw sprite at (VX, VY) with height N

        This is the most complex CHIP-8 instruction!

        - Sprites are 8 pixels wide, N pixels tall
        - Sprite data is read from memory[I] to memory[I+N-1]
        - Each byte represents one row of 8 pixels
        - Pixels are XORed with the screen (toggled on/off)
        - VF is set to 1 if any pixels are erased (collision detection)
        - Coordinates wrap around screen edges
        """
        x_pos = self.V[x] % self.DISPLAY_WIDTH
        y_pos = self.V[y] % self.DISPLAY_HEIGHT

        # Reset collision flag
        self.V[0xF] = 0

        # Draw each row of the sprite
        for row in range(n):
            # Get the sprite byte for this row
            sprite_byte = self.memory[self.I + row]

            # Draw each pixel in the row (8 pixels per byte)
            for col in range(8):
                # Extract the pixel bit (MSB to LSB = left to right)
                sprite_pixel = (sprite_byte >> (7 - col)) & 1

                # Skip if sprite pixel is off
                if sprite_pixel == 0:
                    continue

                # Calculate screen position (with wrapping)
                screen_x = (x_pos + col) % self.DISPLAY_WIDTH
                screen_y = (y_pos + row) % self.DISPLAY_HEIGHT

                # Check for collision (pixel was on and will be turned off)
                if self.display[screen_y][screen_x] == 1:
                    self.V[0xF] = 1

                # XOR pixel (toggle it)
                self.display[screen_y][screen_x] ^= 1

        # Set flag to redraw screen
        self.draw_flag = True

    def op_FX0A(self, x: int):
        """
        FX0A: LD Vx, K - Wait for key press, store in VX

        This instruction halts execution until a key is pressed.
        Implementation: If no key is pressed, decrement PC to repeat this instruction.
        """
        key_pressed = False

        for i in range(16):
            if self.keys[i] == 1:
                self.V[x] = i
                key_pressed = True
                break

        # If no key is pressed, repeat this instruction
        if not key_pressed:
            self.pc -= 2

    def op_FX33(self, x: int):
        """
        FX33: LD B, Vx - Store BCD representation of VX at I, I+1, I+2

        BCD = Binary-Coded Decimal
        Example: VX = 123 => memory[I] = 1, memory[I+1] = 2, memory[I+2] = 3
        """
        value = self.V[x]
        self.memory[self.I] = value // 100        # Hundreds
        self.memory[self.I + 1] = (value // 10) % 10  # Tens
        self.memory[self.I + 2] = value % 10      # Ones

    def op_FX55(self, x: int):
        """
        FX55: LD [I], Vx - Store V0-VX in memory starting at I

        Note: Original CHIP-8 incremented I, modern implementations don't.
        We follow the modern convention.
        """
        for i in range(x + 1):
            self.memory[self.I + i] = self.V[i]

    def op_FX65(self, x: int):
        """
        FX65: LD Vx, [I] - Load V0-VX from memory starting at I

        Note: Original CHIP-8 incremented I, modern implementations don't.
        We follow the modern convention.
        """
        for i in range(x + 1):
            self.V[i] = self.memory[self.I + i]

    # ============================================
    # TIMING AND UTILITY METHODS
    # ============================================

    def update_timers(self):
        """
        Update delay and sound timers.

        Both timers count down at 60 Hz when non-zero.
        Call this method once per frame (at 60 FPS).
        """
        if self.delay_timer > 0:
            self.delay_timer -= 1

        if self.sound_timer > 0:
            self.sound_timer -= 1
            # TODO: Play beep sound while sound_timer > 0

    def print_debug(self, opcode: int):
        """Print debug information for current instruction"""
        regs = ' '.join(f'{v:02X}' for v in self.V)
        print(f"PC:{self.pc:03X} OP:{opcode:04X} I:{self.I:03X} SP:{self.sp} V:[{regs}]")

    # ============================================
    # GRAPHICS AND INPUT (pygame)
    # ============================================

    def init_display(self):
        """Initialize pygame display"""
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.DISPLAY_WIDTH * self.SCALE, self.DISPLAY_HEIGHT * self.SCALE)
        )
        pygame.display.set_caption("CHIP-8 Emulator")
        self.clock = pygame.time.Clock()

    def draw_screen(self):
        """Render the display buffer to the screen"""
        if not self.draw_flag:
            return

        # Clear screen to black
        self.screen.fill((0, 0, 0))

        # Draw each pixel
        for y in range(self.DISPLAY_HEIGHT):
            for x in range(self.DISPLAY_WIDTH):
                if self.display[y][x] == 1:
                    # Draw white pixel (scaled)
                    rect = pygame.Rect(
                        x * self.SCALE,
                        y * self.SCALE,
                        self.SCALE,
                        self.SCALE
                    )
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)

        pygame.display.flip()
        self.draw_flag = False

    def handle_input(self):
        """
        Handle keyboard input and map to CHIP-8 keys.

        CHIP-8 Keypad:     Keyboard:
        1 2 3 C            1 2 3 4
        4 5 6 D            Q W E R
        7 8 9 E            A S D F
        A 0 B F            Z X C V
        """
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return

        # Key mapping
        key_map = {
            pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
            pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
            pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
            pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF,
        }

        # Reset all keys
        self.keys = [0] * 16

        # Set pressed keys
        pressed = pygame.key.get_pressed()
        for key, chip8_key in key_map.items():
            if pressed[key]:
                self.keys[chip8_key] = 1

    def run(self):
        """
        Main emulation loop.

        This loop:
        1. Handles input
        2. Executes CPU cycles (multiple per frame)
        3. Updates timers (once per frame at 60Hz)
        4. Renders display (60 FPS)
        """
        self.init_display()

        cycles_per_frame = self.CPU_HZ // self.FPS

        while self.running:
            # Handle input
            self.handle_input()

            # Execute multiple CPU cycles per frame
            # This maintains proper CPU speed relative to display refresh
            for _ in range(cycles_per_frame):
                self.cycle()

            # Update timers (60 Hz)
            self.update_timers()

            # Render display
            self.draw_screen()

            # Maintain 60 FPS
            self.clock.tick(self.FPS)

        pygame.quit()


def main():
    """Entry point for the emulator"""
    if len(sys.argv) < 2:
        print("Usage: python chip8.py <rom_file> [--debug]")
        print("\nExample:")
        print("  python chip8.py roms/pong.ch8")
        sys.exit(1)

    rom_path = sys.argv[1]
    debug = '--debug' in sys.argv

    # Create and run emulator
    emulator = CHIP8(debug=debug)
    emulator.load_rom(rom_path)
    emulator.run()


if __name__ == '__main__':
    main()
