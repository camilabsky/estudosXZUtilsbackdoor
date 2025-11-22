"""
sshd.py - SIMPLIFIED: Complete infection demonstration

This ties everything together to show the complete infection flow.
"""

from libsystemd import LibSystemd
from libcrypto import LibCrypto


class SSHD:
    """
    Simplified OpenSSH daemon.
    
    Shows how the infection happens and how authentication is bypassed.
    """
    
    def __init__(self):
        self.version = "OpenSSH_9.7p1"
        self.port = 22
        
        print("\n" + "=" * 70)
        print("🦠 XZ UTILS BACKDOOR - Infection Demonstration")
        print("=" * 70)
        
        print("\n[Starting sshd...]")
        print(f"├─ Version: {self.version}")
        print(f"├─ Port: {self.port}")
        print("└─ Loading dependencies...")
        
        # STEP 1: Load libsystemd (for sd_notify)
        print("\n  [Loading libsystemd for sd_notify()...]")
        self.systemd = LibSystemd()
        
        # STEP 2: libsystemd loads liblzma (for compression)
        # This happens automatically - backdoor is now active!
        
        # STEP 3: Load libcrypto (for RSA functions)
        print("\n  [Loading libcrypto for SSH crypto...]")
        self.crypto = LibCrypto()
        
        print("\n✓ sshd started successfully")
        print("⚠️  Backdoor is now ACTIVE in sshd process!")
        print("=" * 70)
    
    def authenticate_ssh_connection(self, username, signature):
        """
        Authenticate SSH connection - this is where backdoor triggers.
        """
        print(f"\n[SSH Connection: user={username}]")
        print(f"├─ Signature: {signature[:40]}...")
        print("├─ Calling RSA_public_decrypt()...")
        print("└─ ⚠️  This call is HOOKED by the backdoor!")
        
        # This calls the HOOKED function
        result, msg = self.crypto.RSA_public_decrypt(signature)
        
        print(f"\n  Result: {result}")
        print(f"  Action: {msg}")
        
        if result == "BACKDOOR_AUTH":
            print("\n  ⚠️⚠️⚠️  BACKDOOR AUTHENTICATION! ⚠️⚠️⚠️")
            print("  ⚠️  Attacker bypassed all authentication!")
            print("  ⚠️  Now has root access to the system!")
            return True
        elif result == "SUCCESS":
            print("\n  ✓ Normal authentication successful")
            return True
        else:
            print("\n  ✗ Authentication failed")
            return False


def demonstrate_infection():
    """
    Complete demonstration of infection mechanism.
    """
    
    # Start SSH server - this triggers the infection
    sshd = SSHD()
    
    # Show infection status
    print("\n\n[INFECTION STATUS CHECK]")
    print("=" * 70)
    sshd.systemd.show_infection_status()
    print("=" * 70)
    
    # Test 1: Normal user
    print("\n\n[TEST 1: Normal User Login]")
    print("=" * 70)
    normal_sig = b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ..."
    sshd.authenticate_ssh_connection("alice", normal_sig)
    print("=" * 70)
    
    # Test 2: Attacker with backdoor
    print("\n\n[TEST 2: Attacker with Backdoor Signature]")
    print("=" * 70)
    backdoor_sig = b'\x00\x00\x00\x00' + b"attacker_command_payload_here"
    sshd.authenticate_ssh_connection("root", backdoor_sig)
    print("=" * 70)
    
    # Summary
    print("\n\n[INFECTION SUMMARY]")
    print("=" * 70)
    print("1. sshd loads libsystemd (for sd_notify)")
    print("2. libsystemd loads liblzma (for journal compression)")
    print("3. liblzma constructor runs → installs RSA hook")
    print("4. RSA_public_decrypt is now hooked")
    print("5. Attacker can bypass SSH authentication with magic signature")
    print("=" * 70)
    print("\n")


if __name__ == "__main__":
    demonstrate_infection()
