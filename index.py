#!/usr/bin/env python3
"""
index.py - Study Guide and File Navigator

Run this to get oriented and choose what to study.
"""

print("\n" + "=" * 70)
print(" " * 15 + "📚 XZ UTILS BACKDOOR STUDY GUIDE")
print("=" * 70)
print()

print("Welcome! This repo helps you understand the XZ Utils backdoor")
print("infection mechanism through simplified, educational code.")
print()

print("=" * 70)
print("🎯 RECOMMENDED STUDY PATH")
print("=" * 70)
print()

print("1️⃣  START HERE - Complete Demo")
print("   $ python3 sshd.py")
print("   → See the complete infection from start to finish")
print("   → Shows library loading, hook installation, auth bypass")
print("   → Best entry point for understanding the attack")
print()

print("2️⃣  Visual Walkthrough")
print("   $ python3 infection_flow.py")
print("   → Interactive step-by-step demonstration")
print("   → Animated with memory layout diagrams")
print("   → Great for presentations")
print()

print("3️⃣  Core Mechanism")
print("   $ python3 liblzma.py")
print("   → THE KEY FILE - shows the 3-step infection")
print("   → Constructor execution, hook installation, payload")
print("   → Study this to understand how it really works")
print()

print("4️⃣  Dependency Chain")
print("   $ python3 libsystemd.py")
print("   → Why does sshd load liblzma?")
print("   → The unexpected dependency that enabled the attack")
print()

print("5️⃣  Hook Target")
print("   $ python3 libcrypto.py")
print("   → The RSA_public_decrypt() function that gets hooked")
print("   → How signatures are intercepted")
print()

print("6️⃣  Build-Time Injection (Advanced)")
print("   $ python3 build_process.py")
print("   → How the backdoor was inserted during compilation")
print("   → Modified m4 macros and obfuscated test files")
print()

print("=" * 70)
print("📖 DOCUMENTATION")
print("=" * 70)
print()

print("📄 README.md")
print("   → Complete overview with technical details")
print()

print("📄 INFECTION_MECHANISM.md")
print("   → Quick reference guide")
print("   → Summary of the 3-step infection")
print("   → Key technical points table")
print()

print("=" * 70)
print("🔑 KEY CONCEPTS TO UNDERSTAND")
print("=" * 70)
print()

concepts = [
    ("Constructor", "__attribute__((constructor))", "Runs when library loads, BEFORE main()"),
    ("IFUNC", "__attribute__((ifunc))", "Indirect function resolution at runtime"),
    ("dlsym()", "dlsym(RTLD_DEFAULT, func)", "Find function address in memory"),
    ("mprotect()", "mprotect(addr, size, PROT_WRITE)", "Make code memory writable"),
    ("JMP Hook", "E9 XX XX XX XX (opcode)", "x86-64 relative jump instruction"),
    ("Magic Sig", "\\x00\\x00\\x00\\x00", "Attacker identification bytes"),
]

for name, code, desc in concepts:
    print(f"  • {name:12} {code:35} → {desc}")

print()
print("=" * 70)
print("💡 THE INFECTION IN 3 STEPS")
print("=" * 70)
print()

print("  STEP 1: Library Load")
print("    → liblzma.so loads into sshd process")
print("    → Constructor runs BEFORE main()")
print()

print("  STEP 2: Hook Installation")
print("    → dlsym() finds RSA_public_decrypt()")
print("    → mprotect() makes memory writable")
print("    → JMP instruction redirects to backdoor")
print()

print("  STEP 3: Backdoor Active")
print("    → All SSH auth goes through hook")
print("    → Magic signature → bypass auth")
print("    → Normal signature → real verification")
print()

print("=" * 70)
print("🎓 LEARNING OBJECTIVES")
print("=" * 70)
print()

objectives = [
    "Understand constructor functions and early execution",
    "Learn how dynamic linking and IFUNC resolvers work",
    "See how runtime function hooking is implemented",
    "Recognize supply chain attack patterns",
    "Appreciate the importance of performance monitoring",
]

for i, obj in enumerate(objectives, 1):
    print(f"  {i}. {obj}")

print()
print("=" * 70)
print("🚀 QUICK START")
print("=" * 70)
print()
print("  $ python3 sshd.py          # Run complete demo")
print("  $ python3 infection_flow.py # Interactive visual")
print()
print("=" * 70)
print()
