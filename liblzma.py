"""
liblzma.py - SIMPLIFIED: The infection mechanism

This shows EXACTLY how the backdoor infects the system:
1. Library loads (before main())
2. Constructor function runs automatically
3. IFUNC resolver hooks RSA function
4. Backdoor is now active
"""

# ==============================================================================
# INFECTION MECHANISM - This is the key part!
# ==============================================================================

class InfectionMechanism:
    """
    The backdoor infection happens in 3 steps:
    
    STEP 1: Library Load
        - When liblzma.so is loaded by any process
        - Constructor runs BEFORE main() starts
        
    STEP 2: Hook Installation
        - Find RSA_public_decrypt() in libcrypto
        - Modify the function to redirect to backdoor
        
    STEP 3: Interception
        - Every SSH authentication now goes through backdoor
        - Backdoor checks for magic signature
    """
    
    def __init__(self):
        self.step = 0
        self.hooked_function = None
        self.backdoor_active = False
    
    def step1_library_loads(self):
        """
        STEP 1: Dynamic linker loads liblzma.so
        
        In C, this would be:
            __attribute__((constructor))
            void _init_backdoor(void) {
                // This runs automatically when .so loads
            }
        """
        self.step = 1
        print("\n[STEP 1: Library Load]")
        print("├─ liblzma.so.5.6.0 loaded into process")
        print("├─ __attribute__((constructor)) triggers")
        print("└─ _init_backdoor() runs (before main!)")
        return True
    
    def step2_install_hook(self):
        """
        STEP 2: Hook the RSA function
        
        In C, this would be:
            void *rsa_func = dlsym(RTLD_DEFAULT, "RSA_public_decrypt");
            mprotect(rsa_func, PAGE_SIZE, PROT_READ|PROT_WRITE|PROT_EXEC);
            
            // Write JMP instruction
            unsigned char jmp[5] = {0xE9, ...};  // JMP relative
            memcpy(rsa_func, jmp, 5);
        """
        self.step = 2
        print("\n[STEP 2: Install Hook]")
        print("├─ dlsym(): Find RSA_public_decrypt address → 0x7f8a2c400000")
        print("├─ mprotect(): Make memory writable")
        print("├─ Write JMP instruction: E9 XX XX XX XX")
        print("│  (Redirects to backdoor handler)")
        print("└─ Hook installed!")
        
        self.hooked_function = "RSA_public_decrypt"
        return True
    
    def step3_backdoor_active(self):
        """
        STEP 3: Backdoor is now active
        
        Every call to RSA_public_decrypt() now goes through backdoor.
        """
        self.step = 3
        self.backdoor_active = True
        print("\n[STEP 3: Backdoor Active]")
        print("├─ RSA_public_decrypt() is now hooked")
        print("├─ All SSH authentication monitored")
        print("└─ Waiting for magic signature...")
        return True
    
    def demonstrate_infection(self):
        """Run complete infection sequence."""
        print("=" * 60)
        print("BACKDOOR INFECTION MECHANISM")
        print("=" * 60)
        
        self.step1_library_loads()
        self.step2_install_hook()
        self.step3_backdoor_active()
        
        print("\n" + "=" * 60)
        print("✓ INFECTION COMPLETE")
        print(f"✓ Hooked function: {self.hooked_function}")
        print(f"✓ Backdoor active: {self.backdoor_active}")
        print("=" * 60)


# ==============================================================================
# PAYLOAD HANDLER - What happens when backdoor triggers
# ==============================================================================

class BackdoorPayload:
    """Simplified payload handler."""
    
    MAGIC_SIGNATURE = b'\x00\x00\x00\x00'  # Magic bytes
    
    def check_signature(self, ssh_signature):
        """Check if this is a backdoor authentication attempt."""
        if ssh_signature.startswith(self.MAGIC_SIGNATURE):
            return "BACKDOOR", "Execute attacker command"
        return "NORMAL", "Verify real SSH key"


# ==============================================================================
# GLOBAL STATE
# ==============================================================================

_infection = InfectionMechanism()
_payload = BackdoorPayload()

def _init_backdoor():
    """Constructor - runs when library loads."""
    _infection.demonstrate_infection()

def get_backdoor_state():
    """Get infection status."""
    return {
        'infected': _infection.backdoor_active,
        'hooked_function': _infection.hooked_function,
        'step': _infection.step
    }

def get_payload():
    """Get payload handler."""
    return _payload


if __name__ == "__main__":
    print("\n🦠 liblzma.so.5.6.0 - Demonstrating Infection Mechanism\n")
    
    # Simulate library initialization
    _init_backdoor()
    
    # Test payload
    print("\n\n[Testing Payload Handler]")
    print("-" * 60)
    
    normal_sig = b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQAB..."
    result, action = _payload.check_signature(normal_sig)
    print(f"Normal SSH key:    {result} → {action}")
    
    backdoor_sig = b'\x00\x00\x00\x00' + b"attacker_command"
    result, action = _payload.check_signature(backdoor_sig)
    print(f"Backdoor signature: {result} → {action} ⚠️")
    
    print("\n")
