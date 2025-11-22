"""
build_process.py - How the backdoor was injected during build time

This shows the actual build-time manipulation that inserted the backdoor.
The attack didn't just add malicious code - it modified the build system itself.
"""


class TestFile:
    """
    The malicious test files that contained the payload.
    
    Files in tests/files/:
    - bad-3-corrupt_lzma2.xz (contained binary backdoor payload)
    - good-large_compressed.lzma (also modified)
    
    These appeared to be legitimate test files for the compression library,
    but actually contained obfuscated x86-64 shellcode.
    """
    
    def __init__(self, filename):
        self.filename = filename
        self.appears_legitimate = True
        self.actual_content = "binary_shellcode"
    
    def extract_payload(self):
        """
        During build, modified scripts extracted payload from these files.
        
        The extraction happened in:
        - m4/build-to-host.m4 (modified autoconf macro)
        - Modified by commits from Jia Tan in early 2024
        """
        return {
            'shellcode': b'\x31\xc0...',  # x86-64 assembly
            'rsa_key': b'ed448_public_key',  # C2 authentication key
            'hook_code': 'IFUNC_resolver_modification'
        }


class BuildScript:
    """
    The modified build scripts that injected the backdoor.
    
    Modified files:
    - m4/build-to-host.m4
    - tests/Makefile.am  
    - CMakeLists.txt (also modified)
    """
    
    def __init__(self):
        self.stage = "configure"
        self.malicious_m4_macro = """
# This m4 macro was modified to extract and inject payload
gl_BUILD_TO_HOST([
    # Legitimate-looking autoconf code
    # ... but with obfuscated bash commands that:
    # 1. Extract data from bad-3-corrupt_lzma2.xz
    # 2. Decode the obfuscated payload
    # 3. Inject into liblzma source before compilation
])
"""
    
    def run_configure(self):
        """
        ./configure step - where m4 macros execute.
        
        The modified build-to-host.m4 macro runs during ./configure
        and extracts the backdoor payload.
        """
        steps = [
            "1. autoconf processes m4 macros",
            "2. build-to-host.m4 executes (contains malicious code)",
            "3. Extracts binary data from tests/files/bad-3-corrupt_lzma2.xz",
            "4. Decodes obfuscated shellcode",
            "5. Generates modified source files",
            "6. Creates modified crc64_fast.c with IFUNC hook"
        ]
        return "\n".join(steps)
    
    def run_make(self):
        """
        make step - compiles the modified source with backdoor.
        
        The backdoor code gets compiled into liblzma.so
        """
        steps = [
            "1. Compiles legitimate XZ Utils code",
            "2. Compiles injected backdoor code",
            "3. Links into liblzma.so.5.6.0",
            "4. Backdoor is now in the binary",
            "5. make install places liblzma.so in /usr/lib"
        ]
        return "\n".join(steps)


class SourceModification:
    """
    How the source code was modified to include the backdoor.
    
    The key file modified was:
    src/liblzma/check/crc64_fast.c
    
    This file implements CRC64 checksums for LZMA, and the attacker
    added IFUNC resolvers here.
    """
    
    def __init__(self):
        self.target_file = "src/liblzma/check/crc64_fast.c"
        self.original_size = 4096  # bytes
        self.modified_size = 10240  # bytes (backdoor added ~6KB)
    
    def show_modification(self):
        """Show the type of code that was injected."""
        return """
Modified: src/liblzma/check/crc64_fast.c
═════════════════════════════════════════════════════════════════

ORIGINAL CODE (Legitimate CRC64 implementation):
─────────────────────────────────────────────────────────────────
uint64_t crc64_fast(const uint8_t *buf, size_t len) {
    uint64_t crc = 0xFFFFFFFFFFFFFFFF;
    
    for (size_t i = 0; i < len; i++) {
        crc = crc64_table[(crc ^ buf[i]) & 0xFF] ^ (crc >> 8);
    }
    
    return crc ^ 0xFFFFFFFFFFFFFFFF;
}
─────────────────────────────────────────────────────────────────

MODIFIED CODE (With IFUNC backdoor):
─────────────────────────────────────────────────────────────────
#include <dlfcn.h>
#include <sys/mman.h>

// Obfuscated backdoor payload (extracted at build time)
static const unsigned char _payload[] = {
    0x31, 0xc0, 0x48, 0x8b, 0x05, 0x00, 0x00, 0x00, 0x00,
    // ... 6KB of obfuscated x86-64 shellcode ...
};

// IFUNC resolver - runs before main()
static void *(*_RSA_public_decrypt)(void) __attribute__((ifunc("_backdoor_init")));

static void *_backdoor_init(void) {
    // This runs during dynamic linking, before main()
    
    // 1. Find RSA_public_decrypt in libcrypto
    void *libcrypto = dlopen("libcrypto.so.3", RTLD_LAZY);
    void *rsa_func = dlsym(libcrypto, "RSA_public_decrypt");
    
    // 2. Make it writable
    mprotect(rsa_func, 4096, PROT_READ|PROT_WRITE|PROT_EXEC);
    
    // 3. Install hook - write JMP instruction
    unsigned char hook[] = {
        0xE9, 0x00, 0x00, 0x00, 0x00  // JMP relative
    };
    *(uint32_t*)(hook + 1) = (uint32_t)((char*)_backdoor_handler - (char*)rsa_func - 5);
    memcpy(rsa_func, hook, 5);
    
    // 4. Return pointer to legitimate CRC function
    return crc64_clmul;
}

static void *_backdoor_handler(int flen, const unsigned char *from,
                               unsigned char *to, void *rsa, int padding) {
    // Check for magic signature
    if (from[0] == 0x00 && from[1] == 0x00 && from[2] == 0x00 && from[3] == 0x00) {
        // Magic Ed448 signature detected
        
        // Verify attacker's signature with embedded public key
        // Extract command from signature data
        // Execute command as root
        
        // Return success without actually verifying
        return (void*)1;  // Success
    }
    
    // Normal SSH key - call original RSA_public_decrypt
    // (after unhooking, calling, and re-hooking)
    return call_original_rsa(flen, from, to, rsa, padding);
}

// Rest of legitimate CRC64 code...
uint64_t crc64_fast(const uint8_t *buf, size_t len) {
    // ... same as before ...
}
─────────────────────────────────────────────────────────────────
"""


class BuildTimeline:
    """Timeline of malicious commits that enabled the backdoor."""
    
    def __init__(self):
        self.commits = [
            {
                'date': '2022-05-19',
                'author': 'Jia Tan',
                'message': 'Tests: Add test files for LZMA_FILTER_LZMA2',
                'content': 'Added bad-3-corrupt_lzma2.xz (contains encoded payload)'
            },
            {
                'date': '2023-07-07',
                'author': 'Jia Tan',
                'message': 'Build: Update build-to-host.m4',
                'content': 'Modified m4 macro to extract payload during configure'
            },
            {
                'date': '2024-02-15',
                'author': 'Jia Tan',
                'message': 'Tests: Update test file',
                'content': 'Updated test file with final payload version'
            },
            {
                'date': '2024-02-24',
                'author': 'Jia Tan',
                'message': 'Release xz-5.6.0',
                'content': '⚠️ First backdoored release'
            },
            {
                'date': '2024-03-09',
                'author': 'Jia Tan',
                'message': 'Release xz-5.6.1',
                'content': '⚠️ Updated backdoored release'
            },
            {
                'date': '2024-03-29',
                'author': 'Andres Freund',
                'message': '[oss-security] Backdoor discovered',
                'content': '✓ Backdoor publicly disclosed, attack stopped'
            }
        ]
    
    def show_timeline(self):
        """Display the timeline of malicious activity."""
        output = ["Build-Time Injection Timeline:", "=" * 70, ""]
        
        for commit in self.commits:
            output.append(f"[{commit['date']}] {commit['author']}")
            output.append(f"  {commit['message']}")
            output.append(f"  → {commit['content']}")
            output.append("")
        
        return "\n".join(output)


def demonstrate_build_process():
    """Show the complete build-time injection process."""
    
    print("=" * 70)
    print("XZ UTILS BACKDOOR - Build-Time Injection Process")
    print("=" * 70)
    
    # Timeline
    timeline = BuildTimeline()
    print("\n" + timeline.show_timeline())
    
    # Test file
    print("\n[Malicious Test File]")
    test_file = TestFile("tests/files/bad-3-corrupt_lzma2.xz")
    payload = test_file.extract_payload()
    print(f"File: {test_file.filename}")
    print(f"Appears legitimate: {test_file.appears_legitimate}")
    print(f"Actual content: Obfuscated backdoor payload")
    print(f"Payload components: {list(payload.keys())}")
    
    # Build process
    print("\n[Build Process Manipulation]")
    build = BuildScript()
    print("\nConfigure step (./configure):")
    print(build.run_configure())
    print("\nMake step (make):")
    print(build.run_make())
    
    # Source modification
    print("\n[Source Code Modification]")
    source = SourceModification()
    print(source.show_modification())
    
    print("\n" + "=" * 70)
    print("RESULT: Backdoored liblzma.so.5.6.0 installed to /usr/lib")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_build_process()
