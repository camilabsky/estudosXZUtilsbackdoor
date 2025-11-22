#!/usr/bin/env python3
"""
infection_flow.py - Visual flow diagram of the infection mechanism

Run this to see a step-by-step visual representation.
"""

import time
import sys


def print_slow(text, delay=0.03):
    """Print text with a typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_box(title, content, color=""):
    """Print a nice box."""
    width = 70
    print("┌" + "─" * (width - 2) + "┐")
    print(f"│ {title:^{width-4}} │")
    print("├" + "─" * (width - 2) + "┤")
    for line in content:
        print(f"│ {line:<{width-4}} │")
    print("└" + "─" * (width - 2) + "┘")


def demonstrate_infection_visual():
    """Visual demonstration of the infection mechanism."""
    
    print("\n")
    print("=" * 70)
    print(" " * 15 + "🦠 XZ UTILS BACKDOOR INFECTION 🦠")
    print("=" * 70)
    print("\n")
    
    # Step 1: System boot
    print("⏱️  STEP 1: System Boot / SSH Service Start")
    print("─" * 70)
    print()
    time.sleep(0.5)
    print_slow("  $ systemctl start sshd", 0.05)
    time.sleep(0.5)
    print("  ├─ Starting OpenSSH daemon...")
    time.sleep(0.5)
    print("  ├─ Loading shared libraries...")
    time.sleep(0.5)
    print("  └─ Calling sd_notify() to inform systemd")
    print()
    input("  Press ENTER to continue...")
    
    # Step 2: Library loading
    print("\n")
    print("📚 STEP 2: Dynamic Library Loading")
    print("─" * 70)
    print()
    time.sleep(0.5)
    
    print("  sshd process")
    time.sleep(0.3)
    print("    ↓")
    time.sleep(0.3)
    print("    ↓ dlopen(libsystemd-shared.so)")
    time.sleep(0.3)
    print("    ↓")
    time.sleep(0.3)
    print("  libsystemd-shared.so")
    time.sleep(0.3)
    print("    ↓")
    time.sleep(0.3)
    print("    ↓ NEEDED: liblzma.so.5 (for journal compression)")
    time.sleep(0.3)
    print("    ↓")
    time.sleep(0.3)
    print("  liblzma.so.5.6.0  ⚠️  BACKDOORED")
    time.sleep(0.5)
    print()
    input("  Press ENTER to continue...")
    
    # Step 3: Constructor execution
    print("\n")
    print("🔧 STEP 3: Constructor Execution (BEFORE main!)")
    print("─" * 70)
    print()
    time.sleep(0.5)
    
    print("  Dynamic linker loads liblzma.so.5.6.0")
    time.sleep(0.5)
    print("    ↓")
    time.sleep(0.3)
    print("  __attribute__((constructor)) triggers")
    time.sleep(0.5)
    print("    ↓")
    time.sleep(0.3)
    print("  _init_backdoor() executes")
    time.sleep(0.5)
    print()
    print("  What _init_backdoor() does:")
    time.sleep(0.3)
    print("    1. Extract payload from embedded data")
    time.sleep(0.3)
    print("    2. Use dlsym() to find RSA_public_decrypt")
    time.sleep(0.3)
    print("    3. Use mprotect() to make code writable")
    time.sleep(0.3)
    print("    4. Write JMP hook: E9 XX XX XX XX")
    time.sleep(0.3)
    print("    5. JMP redirects to backdoor handler")
    time.sleep(0.5)
    print()
    input("  Press ENTER to continue...")
    
    # Step 4: Hook installed
    print("\n")
    print("🪝 STEP 4: Hook Installed")
    print("─" * 70)
    print()
    time.sleep(0.5)
    
    print_box("Memory Layout", [
        "sshd process (PID 1234)",
        "",
        "0x7f...000: libcrypto.so.3",
        "  RSA_public_decrypt:",
        "    [55 48 89 e5 ...]  ← Original",
        "    [E9 XX XX XX XX]   ← NOW: JMP to backdoor",
        "",
        "0x7f...000: liblzma.so.5.6.0",
        "  _backdoor_handler:",
        "    [48 83 ec 28 ...]  ← Hook target",
        "    [...payload...]",
    ])
    print()
    time.sleep(1)
    print("  ✓ RSA_public_decrypt is now HOOKED")
    time.sleep(0.5)
    print("  ✓ Backdoor is ACTIVE")
    time.sleep(0.5)
    print("  ✓ Waiting for SSH connections...")
    print()
    input("  Press ENTER to continue...")
    
    # Step 5: SSH Authentication
    print("\n")
    print("🔐 STEP 5: SSH Authentication Attempt")
    print("─" * 70)
    print()
    time.sleep(0.5)
    
    print("  [Normal User]")
    time.sleep(0.3)
    print("    Client sends: ssh-rsa AAAA... (normal key)")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    sshd: RSA_public_decrypt(signature)")
    time.sleep(0.5)
    print("      ↓ [HOOKED!]")
    time.sleep(0.3)
    print("    Backdoor checks: No magic bytes")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    Call original RSA function")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    ✓ Normal authentication proceeds")
    print()
    time.sleep(1)
    
    print("  [Attacker]")
    time.sleep(0.3)
    print("    Client sends: \\x00\\x00\\x00\\x00... (magic signature)")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    sshd: RSA_public_decrypt(signature)")
    time.sleep(0.5)
    print("      ↓ [HOOKED!]")
    time.sleep(0.3)
    print("    Backdoor checks: MAGIC BYTES DETECTED! ⚠️")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    Extract command from signature")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    Execute command as root")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    Return SUCCESS (without real verification!)")
    time.sleep(0.5)
    print("      ↓")
    time.sleep(0.3)
    print("    ⚠️⚠️⚠️  ATTACKER HAS ROOT ACCESS  ⚠️⚠️⚠️")
    print()
    time.sleep(1)
    input("  Press ENTER to continue...")
    
    # Summary
    print("\n")
    print("=" * 70)
    print(" " * 25 + "📊 SUMMARY")
    print("=" * 70)
    print()
    
    print_box("Key Technical Points", [
        "",
        "1. IFUNC Resolver: __attribute__((ifunc))",
        "   → Runs during dynamic linking, BEFORE main()",
        "",
        "2. Constructor: __attribute__((constructor))",
        "   → Runs when .so loads, installs hook",
        "",
        "3. Hook Mechanism: JMP instruction (E9 opcode)",
        "   → Redirects RSA_public_decrypt to backdoor",
        "",
        "4. Magic Signature: \\x00\\x00\\x00\\x00...",
        "   → Attacker's special Ed448 signature",
        "",
        "5. Dependency Chain: sshd → libsystemd → liblzma",
        "   → Unexpected link created by systemd patch",
        "",
    ])
    
    print()
    print("=" * 70)
    print(" " * 15 + "🎓 Infection Mechanism Complete!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        demonstrate_infection_visual()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.\n")
