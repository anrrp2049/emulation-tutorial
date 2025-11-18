#!/usr/bin/env python3
"""
Generate a simple CHIP-8 test ROM

This script creates a minimal CHIP-8 program that:
1. Clears the screen
2. Draws the number '5' in the center
3. Loops forever

This is useful for testing basic emulator functionality.
"""

def make_test_rom():
    """
    Create a simple test ROM program.

    Program logic:
    1. CLS - Clear screen
    2. LD V0, 28 - Set x position (center-ish)
    3. LD V1, 12 - Set y position (center-ish)
    4. LD I, 0x50 + (5 * 5) - Point to font sprite for '5'
    5. DRW V0, V1, 5 - Draw the sprite
    6. JP 0x20A - Infinite loop
    """

    instructions = [
        0x00E0,  # 0x200: CLS - Clear screen
        0x601C,  # 0x202: LD V0, 28 - x position
        0x610C,  # 0x204: LD V1, 12 - y position
        0xA069,  # 0x206: LD I, 0x69 - Font '5' location (0x50 + 5*5)
        0xD015,  # 0x208: DRW V0, V1, 5 - Draw sprite
        0x120A,  # 0x20A: JP 0x20A - Infinite loop (stay here)
    ]

    # Convert instructions to bytes (big-endian)
    rom_bytes = bytearray()
    for instruction in instructions:
        rom_bytes.append((instruction >> 8) & 0xFF)  # High byte
        rom_bytes.append(instruction & 0xFF)          # Low byte

    return rom_bytes


def main():
    rom = make_test_rom()

    output_path = '../../roms/test-simple.ch8'

    with open(output_path, 'wb') as f:
        f.write(rom)

    print(f"Created test ROM: {output_path}")
    print(f"Size: {len(rom)} bytes")
    print("\nInstructions:")
    print("  00E0: Clear screen")
    print("  601C: V0 = 28 (x position)")
    print("  610C: V1 = 12 (y position)")
    print("  A069: I = 0x69 (font sprite for '5')")
    print("  D015: Draw sprite at (V0, V1), height 5")
    print("  120A: Jump to 0x20A (infinite loop)")
    print("\nTo test:")
    print("  python ../../src/chip8.py test-simple.ch8")


if __name__ == '__main__':
    main()
