# XZ Utils Backdoor (CVE-2024-3094) - Infection Mechanism Study

**SIMPLIFIED** educational demonstration focusing on the **infection mechanism** of the XZ Utils backdoor.

## 📋 Overview

This repository contains **simplified Python files** that clearly demonstrate how the backdoor infects a system and hooks SSH authentication. Perfect for studying the attack mechanism step-by-step.

## 🔗 The Infection Chain

```
sshd starts
  ↓
Loads libsystemd-shared.so (for sd_notify)
  ↓
Loads liblzma.so.5.6.0 (for journal compression) ⚠️ BACKDOORED
  ↓
Constructor runs: _init_backdoor() [BEFORE main!]
  ↓
Hooks RSA_public_decrypt() in libcrypto.so.3
  ↓
Backdoor is ACTIVE - waiting for magic signature
```

## 📁 File Structure (Simplified for Learning)

### Core Files (Study in order):

1. **`liblzma.py`** - ⭐ **THE INFECTION MECHANISM** ⭐
   - Shows the 3-step infection process
   - **Step 1**: Library loads (constructor runs BEFORE main)
   - **Step 2**: Hook installation (dlsym + mprotect + JMP)
   - **Step 3**: Backdoor active (monitoring RSA calls)
   - Simple payload handler for magic signature detection

2. **`libsystemd.py`** - The dependency bridge
   - Shows WHY sshd loads liblzma (journal compression)
   - Demonstrates the infection trigger
   - Clean and focused on the dependency chain

3. **`libcrypto.py`** - The hooked function
   - Shows RSA_public_decrypt() before and after hooking
   - Demonstrates signature interception
   - Clear comparison: normal vs backdoor authentication

4. **`sshd.py`** - Complete demonstration
   - Ties everything together
   - Shows full infection flow
   - Tests both normal and backdoor authentication
   - **Run this to see everything in action**

5. **`infection_flow.py`** - 🎬 Interactive visual demo
   - Step-by-step animated demonstration
   - Shows memory layout and hook installation
   - Great for presentations and learning

6. **`build_process.py`** - Build-time injection (advanced)
   - How the backdoor was injected during compilation
   - Modified m4 macros and test files
   - For deeper study after understanding infection

## 🔬 The Infection Mechanism (Simplified)

### Three-Step Infection Process

**STEP 1: Library Load**
- When `liblzma.so` loads, constructor runs automatically
- Uses `__attribute__((constructor))` - runs BEFORE main()
- This is the key: code executes just by loading the library!

```c
__attribute__((constructor))
void _init_backdoor(void) {
    // This runs automatically when liblzma.so loads
    install_hook();
}
```

**STEP 2: Hook Installation**
- Find `RSA_public_decrypt()` address using `dlsym()`
- Make memory writable using `mprotect()`
- Write JMP instruction: `E9 XX XX XX XX`
- JMP redirects to backdoor handler

```c
void *rsa = dlsym(RTLD_DEFAULT, "RSA_public_decrypt");
mprotect(rsa, 4096, PROT_READ|PROT_WRITE|PROT_EXEC);
unsigned char jmp[5] = {0xE9, ...};  // JMP opcode
memcpy(rsa, jmp, 5);  // Install hook
```

**STEP 3: Interception**
- Every SSH authentication now goes through backdoor
- Check signature for magic bytes: `\x00\x00\x00\x00`
- If magic: execute attacker command, return success
- If normal: pass through to real RSA verification

### The Critical Dependency

**Why did sshd load liblzma?**
```
sshd
 └─ calls sd_notify() [Debian/Fedora patch]
     └─ loads libsystemd-shared.so
         └─ needs XZ compression for journald
             └─ loads liblzma.so ⚠️ BACKDOOR ACTIVATES HERE
```

This unexpected dependency chain is what made the attack possible!

## 🚀 Quick Start - Study the Infection

### 1. Start Here - Complete Demo
```bash
python3 sshd.py
```
**Best starting point!** Shows the complete infection from start to finish:
- Library loading sequence
- Constructor execution
- Hook installation
- Normal vs backdoor authentication

### 2. Interactive Visual Demo
```bash
python3 infection_flow.py
```
Step-by-step visual walkthrough with animations. Great for understanding the flow!

### 3. Study Individual Components
```bash
# The core infection mechanism
python3 liblzma.py

# The dependency bridge
python3 libsystemd.py

# The hooked function
python3 libcrypto.py
```

### 4. Advanced - Build-Time Injection
```bash
python3 build_process.py
```
How the backdoor was inserted during compilation (study this last).

## 🎯 Key Technical Points

### Why This Worked

1. **Unexpected Dependency**: Debian/Fedora patched OpenSSH to call `sd_notify()`, creating sshd → libsystemd link
2. **Legitimate Need**: libsystemd uses liblzma for journal compression
3. **Early Execution**: IFUNC resolvers run before `main()`, during dynamic linking
4. **Code Reuse**: Used existing OpenSSL functions, just intercepted them
5. **Obfuscation**: Payload hidden in "corrupt" test files that appeared legitimate

### Functions Involved

| Library | Function | Purpose in Attack |
|---------|----------|------------------|
| liblzma | `crc64_clmul()` | IFUNC resolver installed here |
| liblzma | `_backdoor_init()` | Constructor that runs before main() |
| libcrypto | `RSA_public_decrypt()` | **Target function** - hooked |
| libsystemd | `sd_notify()` | Creates the dependency link |
| libc | `dlsym()` | Find RSA function address |
| libc | `mprotect()` | Make code writable for hook |

### The Build-Time Injection

```
tests/files/bad-3-corrupt_lzma2.xz
         ↓ (extracted during ./configure)
    m4/build-to-host.m4
         ↓ (generates modified source)
src/liblzma/check/crc64_fast.c
         ↓ (compiled with backdoor)
    liblzma.so.5.6.0
         ↓ (installed to /usr/lib)
    BACKDOOR ACTIVE
```

## 📚 Educational Value

This demonstrates:

- **Supply chain attacks**: 2+ years of trust building
- **Build system exploitation**: Malicious m4 macros
- **Dynamic linking attacks**: IFUNC resolvers
- **Function hooking**: Runtime code modification
- **Obfuscation techniques**: Binary test files
- **Responsible disclosure**: How Andres Freund's vigilance saved the day

## ⚠️ Affected Systems

- **Debian sid** (unstable) - liblzma 5.6.0/5.6.1
- **Fedora 40/41** (rawhide) - liblzma 5.6.0/5.6.1
- **Arch Linux** (briefly) - quickly reverted
- **NOT AFFECTED**: Stable distributions (caught before release)

## 🛡️ Detection

Check your system:
```bash
# Check XZ version
xz --version

# If 5.6.0 or 5.6.1, check for backdoor
strings /usr/lib/x86_64-linux-gnu/liblzma.so.5 | grep -i "bad-3-corrupt"

# Check if sshd links to liblzma
ldd /usr/sbin/sshd | grep liblzma
```

## 🔗 References

- **CVE-2024-3094**: https://nvd.nist.gov/vuln/detail/CVE-2024-3094
- **Original Disclosure**: https://www.openwall.com/lists/oss-security/2024/03/29/4
- **Technical Analysis**: https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27
- **Andres Freund's Discovery**: https://mastodon.social/@AndresFreundTec/112180406142695845

## 👨‍💻 Hero

**Andres Freund** (PostgreSQL developer, Microsoft engineer) discovered this backdoor on **March 29, 2024**, by noticing a 500ms SSH login delay during routine performance testing. His curiosity and debugging skills with Valgrind prevented a catastrophic supply chain attack.

---

**⚠️ DISCLAIMER**: This is for educational purposes only. The actual backdoor was highly sophisticated with additional obfuscation and anti-analysis techniques not fully replicated here.
# XZ Utils Backdoor (CVE-2024-3094) - Infection Mechanism Study

**SIMPLIFIED** educational demonstration focusing on the **infection mechanism** of the XZ Utils backdoor.

## 📋 Overview

This repository contains **simplified Python files** that clearly demonstrate how the backdoor infects a system and hooks SSH authentication. Perfect for studying the attack mechanism step-by-step.

## 🔗 The Infection Chain

```
sshd starts
   ↓
Loads libsystemd-shared.so (for sd_notify)
   ↓
Loads liblzma.so.5.6.0 (for journal compression) ⚠️ BACKDOORED
   ↓
Constructor runs: _init_backdoor() [BEFORE main!]
   ↓
Hooks RSA_public_decrypt() in libcrypto.so.3
   ↓
Backdoor is ACTIVE - waiting for magic signature
```

## 📁 File Structure (Simplified for Learning)

### Core Files (Study in order):

1. **`liblzma.py`** - ⭐ **THE INFECTION MECHANISM** ⭐
    - Shows the 3-step infection process
    - **Step 1**: Library loads (constructor runs BEFORE main)
    - **Step 2**: Hook installation (dlsym + mprotect + JMP)
    - **Step 3**: Backdoor active (monitoring RSA calls)
    - Simple payload handler for magic signature detection

2. **`libsystemd.py`** - The dependency bridge
    - Shows WHY sshd loads liblzma (journal compression)
    - Demonstrates the infection trigger
    - Clean and focused on the dependency chain

3. **`libcrypto.py`** - The hooked function
    - Shows RSA_public_decrypt() before and after hooking
    - Demonstrates signature interception
    - Clear comparison: normal vs backdoor authentication

4. **`sshd.py`** - Complete demonstration
    - Ties everything together
    - Shows full infection flow
    - Tests both normal and backdoor authentication
    - **Run this to see everything in action**

5. **`infection_flow.py`** - 🎬 Interactive visual demo
    - Step-by-step animated demonstration
    - Shows memory layout and hook installation
    - Great for presentations and learning

6. **`build_process.py`** - Build-time injection (advanced)
    - How the backdoor was injected during compilation
    - Modified m4 macros and test files
    - For deeper study after understanding infection

## 🔬 The Infection Mechanism (Simplified)

### Three-Step Infection Process

**STEP 1: Library Load**
- When `liblzma.so` loads, constructor runs automatically
- Uses `__attribute__((constructor))` - runs BEFORE main()
- This is the key: code executes just by loading the library!

```c
__attribute__((constructor))
void _init_backdoor(void) {
      // This runs automatically when liblzma.so loads
      install_hook();
}
```

**STEP 2: Hook Installation**
- Find `RSA_public_decrypt()` address using `dlsym()`
- Make memory writable using `mprotect()`
- Write JMP instruction: `E9 XX XX XX XX`
- JMP redirects to backdoor handler

```c
void *rsa = dlsym(RTLD_DEFAULT, "RSA_public_decrypt");
mprotect(rsa, 4096, PROT_READ|PROT_WRITE|PROT_EXEC);
unsigned char jmp[5] = {0xE9, ...};  // JMP opcode
memcpy(rsa, jmp, 5);  // Install hook
```

**STEP 3: Interception**
- Every SSH authentication now goes through backdoor
- Check signature for magic bytes: `\x00\x00\x00\x00`
- If magic: execute attacker command, return success
- If normal: pass through to real RSA verification

### The Critical Dependency

**Why did sshd load liblzma?**
```
sshd
 └─ calls sd_notify() [Debian/Fedora patch]
       └─ loads libsystemd-shared.so
             └─ needs XZ compression for journald
                   └─ loads liblzma.so ⚠️ BACKDOOR ACTIVATES HERE
```

This unexpected dependency chain is what made the attack possible!

## 🚀 Quick Start - Study the Infection

### 1. Start Here - Complete Demo
```bash
python3 sshd.py
```
**Best starting point!** Shows the complete infection from start to finish:
- Library loading sequence
- Constructor execution
- Hook installation
- Normal vs backdoor authentication

### 2. Interactive Visual Demo
```bash
python3 infection_flow.py
```
Step-by-step visual walkthrough with animations. Great for understanding the flow!

### 3. Study Individual Components
```bash
# The core infection mechanism
python3 liblzma.py

# The dependency bridge
python3 libsystemd.py

# The hooked function
python3 libcrypto.py
```

### 4. Advanced - Build-Time Injection
```bash
python3 build_process.py
```
How the backdoor was inserted during compilation (study this last).

## 📚 Study Guide and Navigation

### 🎯 Recommended Study Path

**1️⃣ START HERE - Complete Demo**
```bash
python3 sshd.py
```
→ See the complete infection from start to finish  
→ Shows library loading, hook installation, auth bypass  
→ Best entry point for understanding the attack

**2️⃣ Visual Walkthrough**
```bash
python3 infection_flow.py
```
→ Interactive step-by-step demonstration  
→ Animated with memory layout diagrams  
→ Great for presentations

**3️⃣ Core Mechanism**
```bash
python3 liblzma.py
```
→ THE KEY FILE - shows the 3-step infection  
→ Constructor execution, hook installation, payload  
→ Study this to understand how it really works

**4️⃣ Dependency Chain**
```bash
python3 libsystemd.py
```
→ Why does sshd load liblzma?  
→ The unexpected dependency that enabled the attack

**5️⃣ Hook Target**
```bash
python3 libcrypto.py
```
→ The RSA_public_decrypt() function that gets hooked  
→ How signatures are intercepted

**6️⃣ Build-Time Injection (Advanced)**
```bash
python3 build_process.py
```
→ How the backdoor was inserted during compilation  
→ Modified m4 macros and obfuscated test files

### 📖 Documentation

- **README.md** - Complete overview with technical details
- **INFECTION_MECHANISM.md** - Quick reference guide with summary of the 3-step infection and key technical points table

### 🔑 Key Concepts to Understand

| Concept | Code Example | Description |
|---------|--------------|-------------|
| **Constructor** | `__attribute__((constructor))` | Runs when library loads, BEFORE main() |
| **IFUNC** | `__attribute__((ifunc))` | Indirect function resolution at runtime |
| **dlsym()** | `dlsym(RTLD_DEFAULT, func)` | Find function address in memory |
| **mprotect()** | `mprotect(addr, size, PROT_WRITE)` | Make code memory writable |
| **JMP Hook** | `E9 XX XX XX XX (opcode)` | x86-64 relative jump instruction |
| **Magic Sig** | `\x00\x00\x00\x00` | Attacker identification bytes |

### 💡 The Infection in 3 Steps

**STEP 1: Library Load**
- liblzma.so loads into sshd process
- Constructor runs BEFORE main()

**STEP 2: Hook Installation**
- dlsym() finds RSA_public_decrypt()
- mprotect() makes memory writable
- JMP instruction redirects to backdoor

**STEP 3: Backdoor Active**
- All SSH auth goes through hook
- Magic signature → bypass auth
- Normal signature → real verification

### 🎓 Learning Objectives

1. Understand constructor functions and early execution
2. Learn how dynamic linking and IFUNC resolvers work
3. See how runtime function hooking is implemented
4. Recognize supply chain attack patterns
5. Appreciate the importance of performance monitoring

## 🎯 Key Technical Points

### Why This Worked

1. **Unexpected Dependency**: Debian/Fedora patched OpenSSH to call `sd_notify()`, creating sshd → libsystemd link
2. **Legitimate Need**: libsystemd uses liblzma for journal compression
3. **Early Execution**: IFUNC resolvers run before `main()`, during dynamic linking
4. **Code Reuse**: Used existing OpenSSL functions, just intercepted them
5. **Obfuscation**: Payload hidden in "corrupt" test files that appeared legitimate

### Functions Involved

| Library | Function | Purpose in Attack |
|---------|----------|------------------|
| liblzma | `crc64_clmul()` | IFUNC resolver installed here |
| liblzma | `_backdoor_init()` | Constructor that runs before main() |
| libcrypto | `RSA_public_decrypt()` | **Target function** - hooked |
| libsystemd | `sd_notify()` | Creates the dependency link |
| libc | `dlsym()` | Find RSA function address |
| libc | `mprotect()` | Make code writable for hook |

### The Build-Time Injection

```
tests/files/bad-3-corrupt_lzma2.xz
             ↓ (extracted during ./configure)
      m4/build-to-host.m4
             ↓ (generates modified source)
src/liblzma/check/crc64_fast.c
             ↓ (compiled with backdoor)
      liblzma.so.5.6.0
             ↓ (installed to /usr/lib)
      BACKDOOR ACTIVE
```

## 📚 Educational Value

This demonstrates:

- **Supply chain attacks**: 2+ years of trust building
- **Build system exploitation**: Malicious m4 macros
- **Dynamic linking attacks**: IFUNC resolvers
- **Function hooking**: Runtime code modification
- **Obfuscation techniques**: Binary test files
- **Responsible disclosure**: How Andres Freund's vigilance saved the day

## ⚠️ Affected Systems

- **Debian sid** (unstable) - liblzma 5.6.0/5.6.1
- **Fedora 40/41** (rawhide) - liblzma 5.6.0/5.6.1
- **Arch Linux** (briefly) - quickly reverted
- **NOT AFFECTED**: Stable distributions (caught before release)

## 🛡️ Detection

Check your system:
```bash
# Check XZ version
xz --version

# If 5.6.0 or 5.6.1, check for backdoor
strings /usr/lib/x86_64-linux-gnu/liblzma.so.5 | grep -i "bad-3-corrupt"

# Check if sshd links to liblzma
ldd /usr/sbin/sshd | grep liblzma
```

## 🔗 References

- **CVE-2024-3094**: https://nvd.nist.gov/vuln/detail/CVE-2024-3094
- **Original Disclosure**: https://www.openwall.com/lists/oss-security/2024/03/29/4
- **Technical Analysis**: https://gist.github.com/thesamesam/223949d5a074ebc3dce9ee78baad9e27
- **Andres Freund's Discovery**: https://mastodon.social/@AndresFreundTec/112180406142695845
- text wolves in the repository

## 👨‍💻 Hero

**Andres Freund** (PostgreSQL developer, Microsoft engineer) discovered this backdoor on **March 29, 2024**, by noticing a 500ms SSH login delay during routine performance testing. His curiosity and debugging skills with Valgrind prevented a catastrophic supply chain attack.

---

**⚠️ DISCLAIMER**: This is for educational purposes only. The actual backdoor was highly sophisticated with additional obfuscation and anti-analysis techniques not fully replicated here.
