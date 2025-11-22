"""
libsystemd.py - SIMPLIFIED: The dependency bridge

This shows how sshd links to the backdoored library:
    sshd → libsystemd → liblzma (BACKDOORED)
    
The key: libsystemd uses liblzma for journal compression
"""

from liblzma import get_backdoor_state, _init_backdoor

print("\n[libsystemd.so Loading...]")
print("├─ Need: XZ compression for systemd journal")
print("├─ Loading: liblzma.so.5.6.0")
print("└─ ⚠️  This triggers the backdoor infection!")


class LibSystemd:
    """
    Simplified: The bridge that links sshd to the backdoor.
    
    WHY THIS MATTERS:
    - libsystemd needs XZ compression for journals
    - So it links to liblzma.so
    - When sshd loads libsystemd → liblzma loads → backdoor activates
    """
    
    def __init__(self):
        self.version = "255"
        self.needs_compression = True
        
        # THIS IS THE KEY MOMENT
        # When libsystemd loads, it needs liblzma for compression
        # This triggers the backdoor infection
        if self.needs_compression:
            _init_backdoor()  # ← BACKDOOR INFECTS HERE
            self.backdoor_state = get_backdoor_state()
    
    def sd_notify(self, message):
        """
        Notify systemd (called by sshd).
        
        This is legitimate, but the act of loading libsystemd
        already triggered the backdoor.
        """
        return f"[systemd] {message}"
    
    def show_infection_status(self):
        """Show if backdoor infected via this library."""
        print("\n[Infection Status via libsystemd]")
        print(f"├─ Backdoor infected: {self.backdoor_state['infected']}")
        print(f"├─ Hooked function: {self.backdoor_state['hooked_function']}")
        print(f"└─ Infection step: {self.backdoor_state['step']}/3")


if __name__ == "__main__":
    print("\n🔗 libsystemd-shared.so - The Dependency Bridge\n")
    print("=" * 70)
    
    print("\nDependency Chain:")
    print("  sshd")
    print("    ↓ (calls sd_notify)")
    print("  libsystemd-shared.so")
    print("    ↓ (needs XZ compression)")
    print("  liblzma.so.5.6.0  ⚠️  BACKDOORED")
    print("=" * 70)
    
    # Creating LibSystemd triggers the infection
    print("\n[Creating LibSystemd instance...]")
    systemd = LibSystemd()
    
    # Show infection status
    systemd.show_infection_status()
    
    print("\n")
