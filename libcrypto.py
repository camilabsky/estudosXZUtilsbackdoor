"""
libcrypto.py - SIMPLIFIED: The target function

This shows the function that gets hooked:
    RSA_public_decrypt() - Used in SSH authentication
"""

from liblzma import get_backdoor_state, get_payload


class LibCrypto:
    """
    Simplified: The function that gets hooked.
    
    RSA_public_decrypt() - Verifies SSH signatures
    """
    
    def __init__(self):
        self.version = "3.0.13"
        self.backdoor_state = get_backdoor_state()
        self.payload = get_payload()
    
    def RSA_public_decrypt(self, signature_data):
        """
        HOOKED FUNCTION - This is where the backdoor intercepts.
        
        Normal flow:
          SSH client → signs challenge → sshd verifies → RSA_public_decrypt
          
        Backdoored flow:
          SSH client → signs challenge → sshd calls RSA_public_decrypt
          → HOOK intercepts → checks for magic signature
          → if magic: bypass auth
          → if normal: do real verification
        """
        
        # If backdoor is active, it intercepts here
        if self.backdoor_state['infected']:
            return self._backdoored_version(signature_data)
        else:
            return self._original_version(signature_data)
    
    def _original_version(self, signature_data):
        """Original: Verify the SSH signature properly."""
        return ("SUCCESS", "Valid SSH signature")
    
    def _backdoored_version(self, signature_data):
        """Backdoored: Check for magic bytes first."""
        result, action = self.payload.check_signature(signature_data)
        
        if result == "BACKDOOR":
            # Magic signature! Attacker gets in without real verification
            return ("BACKDOOR_AUTH", action)
        else:
            # Normal SSH key, do real verification
            return self._original_version(signature_data)


if __name__ == "__main__":
    print("\n🎯 libcrypto.so.3 - The Target Function\n")
    print("=" * 70)
    
    crypto = LibCrypto()
    
    print("\nFunction: RSA_public_decrypt()")
    print(f"  Purpose: Verify SSH public key signatures")
    print(f"  Status: {'HOOKED ⚠️' if crypto.backdoor_state['infected'] else 'Normal'}")
    
    print("\n[Testing Hook Interception]")
    print("-" * 70)
    
    # Normal SSH authentication
    print("\n1. Normal SSH signature:")
    normal_sig = b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
    result, msg = crypto.RSA_public_decrypt(normal_sig)
    print(f"   Input: {normal_sig[:30]}...")
    print(f"   Result: {result}")
    print(f"   Action: {msg}")
    
    # Backdoor authentication
    print("\n2. Backdoor signature (with magic bytes):")
    backdoor_sig = b'\x00\x00\x00\x00' + b"attacker_command_payload"
    result, msg = crypto.RSA_public_decrypt(backdoor_sig)
    print(f"   Input: {backdoor_sig[:30]}...")
    print(f"   Result: {result} ⚠️")
    print(f"   Action: {msg} ⚠️")
    print("\n   ⚠️ AUTHENTICATION BYPASSED!")
    
    print("\n")
