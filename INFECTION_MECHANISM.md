# Quick Reference: XZ Utils Backdoor Infection Mechanism

## 🎯 The 3-Step Infection

### Step 1: Library Load (Constructor)
```
When:   liblzma.so loads into any process
How:    __attribute__((constructor)) in C
Effect: _init_backdoor() runs BEFORE main()
```

### Step 2: Hook Installation
```
What:   Find and modify RSA_public_decrypt()
Tools:  dlsym() + mprotect() + memcpy()
Code:   Write JMP instruction (E9 opcode)
Result: Function redirects to backdoor handler
```

### Step 3: Backdoor Active
```
Target: SSH authentication via RSA_public_decrypt()
Check:  Signature starts with \x00\x00\x00\x00?
  YES → Execute attacker command, return success
  NO  → Pass through to real RSA verification
```

## 🔗 Why It Worked

### The Dependency Chain
```
sshd (needs to notify systemd)
  ↓
libsystemd (needs to compress journals)
  ↓
liblzma (provides XZ compression)
  ↓
CONSTRUCTOR RUNS → BACKDOOR INSTALLS
```

### Key Insight
- Debian/Fedora patched sshd to call `sd_notify()`
- This created an unexpected link to libsystemd
- libsystemd uses liblzma for journal compression
- Loading liblzma triggers the backdoor constructor
- Constructor hooks RSA before main() even starts!

## 🧪 Test It Yourself

```bash
# Complete demo (best starting point)
python3 sshd.py

# Interactive visual walkthrough
python3 infection_flow.py

# Study individual components
python3 liblzma.py      # Core infection mechanism
python3 libsystemd.py   # Dependency bridge
python3 libcrypto.py    # Hooked RSA function
```

## 📊 What You'll See

### Normal Authentication
```
User: alice
Signature: ssh-rsa AAAA...
  → RSA_public_decrypt() called
  → Hook intercepts
  → No magic bytes detected
  → Pass to real RSA verification
  → ✓ Authentication succeeds normally
```

### Backdoor Authentication
```
User: attacker
Signature: \x00\x00\x00\x00...
  → RSA_public_decrypt() called
  → Hook intercepts
  → MAGIC BYTES DETECTED! ⚠️
  → Extract command from signature
  → Execute as root
  → Return success WITHOUT verification
  → ⚠️ ATTACKER HAS ROOT ACCESS
```

## 🔑 Key Technical Points

| Concept | Implementation | Purpose |
|---------|---------------|---------|
| Constructor | `__attribute__((constructor))` | Run code when library loads |
| IFUNC | `__attribute__((ifunc))` | Indirect function resolution |
| dlsym() | `dlsym(RTLD_DEFAULT, "RSA_public_decrypt")` | Find function address |
| mprotect() | `mprotect(addr, size, PROT_WRITE)` | Make code writable |
| JMP hook | `E9 XX XX XX XX` | Redirect function to backdoor |
| Magic signature | `\x00\x00\x00\x00...` | Identify attacker |

## 🎓 Learning Path

1. **Start**: Run `python3 sshd.py` - see complete flow
2. **Understand**: Run `python3 infection_flow.py` - visual demo
3. **Deep dive**: Study `liblzma.py` - the infection mechanism
4. **Context**: Read `libsystemd.py` - the dependency chain
5. **Target**: Review `libcrypto.py` - the hooked function
6. **Advanced**: Explore `build_process.py` - build-time injection

## ⚠️ Why This Matters

This attack demonstrates:
- **Supply chain security**: 2+ years of trust building
- **Constructor abuse**: Code runs before main()
- **Function hooking**: Runtime code modification
- **Dependency exploitation**: Unexpected library links
- **Near miss**: Caught before reaching stable distros

## 🦸 The Hero

**Andres Freund** noticed a 500ms SSH login delay during performance testing.
His curiosity and debugging with Valgrind saved the internet.

---

**Date**: March 29, 2024  
**CVE**: CVE-2024-3094  
**CVSS**: 10.0 (Critical)  
**Status**: Caught before widespread deployment ✓
