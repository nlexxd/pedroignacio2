import network
import struct
from machine import Pin


class WalkerBotV1:
    """
    WalkerBot V1 Remote Control Handler via ESP-NOW
    Receives and decodes button inputs from the WalkerBot remote
    
    Packet format (same as ESP32 C++ version):
    - uint32_t seq (sequence number)
    - uint8_t buttons (bit0=up, 1=left, 2=right, 3=down, 4=a, 5=b)
    """
    
    # Button bit positions
    BTN_UP = 0
    BTN_LEFT = 1
    BTN_RIGHT = 2
    BTN_DOWN = 3
    BTN_A = 4
    BTN_B = 5
    
    def __init__(self, channel: int = 1):
        """
        Initialize ESP-NOW receiver
        
        channel: WiFi channel (1-13, must match sender)
        mac_address: Target remote MAC (optional, for filtering)
        """
        self.channel = channel
        self.last_buttons = 0
        self.last_seq = 0
        self.last_sender_mac = None
        self.connected = False
        
        # Initialize WiFi in STA mode for ESP-NOW
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        self.wifi.disconnect()
        
        # Initialize ESP-NOW
        self._init_espnow()
    
    def _init_espnow(self):
        """Initialize ESP-NOW communication"""
        try:
            import espnow
            self.esp_now = espnow.ESPNow()
            self.esp_now.active(True)
            
            print(f"[OK] ESP-NOW initialized on channel {self.channel}")
        except ImportError:
            print("[ERROR] espnow module not available")
            print("[INFO] Compile MicroPython with CONFIG_MICROPY_ESPNOW=1")
            self.esp_now = None
    
    def read_command(self) -> str:
        """
        Read incoming ESP-NOW packet
        Returns dict with button states or None if no data
        """
        if not self.esp_now:
            return None
        
        try:
            # Try to receive data without blocking (timeout=0)
            mac, msg = self.esp_now.irecv(0)
            
            if mac is not None and msg is not None and len(msg) == 5:
                # Unpack: '<I' = uint32 (little-endian), 'B' = uint8
                seq, buttons = struct.unpack('<IB', msg)
                
                self.last_seq = seq
                self.last_buttons = buttons
                self.last_sender_mac = mac
                self.connected = True
                
                parsed_buttons = self._parse_buttons(buttons)
            
                buttons_pressed = [btn for btn, pressed in parsed_buttons.items() if pressed]
                buttons_pressed_str = "+".join(buttons_pressed) if buttons_pressed else "none"

                return buttons_pressed_str

        except Exception as e:
            print(f"[ERROR] Reading ESP-NOW: {e}")
        
        return None
    
    def _parse_buttons(self, buttons: int) -> dict:
        """Convert button byte to dictionary"""
        return {
            "up": bool(buttons & (1 << self.BTN_UP)),
            "left": bool(buttons & (1 << self.BTN_LEFT)),
            "right": bool(buttons & (1 << self.BTN_RIGHT)),
            "down": bool(buttons & (1 << self.BTN_DOWN)),
            "a": bool(buttons & (1 << self.BTN_A)),
            "b": bool(buttons & (1 << self.BTN_B)),
        }
    
    def get_direction(self) -> str:
        """Get current direction (up, down, left, right, none)"""
        buttons = self._parse_buttons(self.last_buttons)
        
        if buttons["up"]:
            return "up"
        elif buttons["down"]:
            return "down"
        elif buttons["left"]:
            return "left"
        elif buttons["right"]:
            return "right"
        return "none"
    
    def is_a_pressed(self) -> bool:
        """Check if button A is pressed"""
        return bool(self.last_buttons & (1 << self.BTN_A))
    
    def is_b_pressed(self) -> bool:
        """Check if button B is pressed"""
        return bool(self.last_buttons & (1 << self.BTN_B))
    
    def get_status(self) -> dict:
        """Get complete status of last received command"""
        buttons = self._parse_buttons(self.last_buttons)
        return {
            "sequence": self.last_seq,
            "sender_mac": self._format_mac(self.last_sender_mac) if self.last_sender_mac else None,
            "buttons": buttons,
            "direction": self.get_direction(),
            "connected": self.connected
        }
    
    def get_raw_buttons(self) -> int:
        """Get raw button byte (for direct bit manipulation)"""
        return self.last_buttons
    
    def is_button_pressed(self, button: int) -> bool:
        """Check if specific button bit is pressed"""
        if 0 <= button <= 5:
            return bool(self.last_buttons & (1 << button))
        return False
    
    def set_channel(self, channel: int):
        """Change WiFi channel (1-13)"""
        if 1 <= channel <= 13:
            self.channel = channel
            print(f"[OK] Channel changed to {channel}")
        else:
            print("[ERROR] Invalid channel (must be 1-13)")
    
    @staticmethod
    def _format_mac(mac_bytes) -> str:
        """Convert MAC bytes to string format (XX:XX:XX:XX:XX:XX)"""
        if not mac_bytes:
            return None
        return ':'.join(f'{b:02X}' for b in mac_bytes)
    
    def print_status(self):
        """Debug: Print current status"""
        status = self.get_status()
        print(f"Seq: {status['sequence']}")
        print(f"MAC: {status['sender_mac']}")
        print(f"Dir: {status['direction']}")
        buttons = status['buttons']
        print(f"Btn: U={buttons['up']} L={buttons['left']} R={buttons['right']} D={buttons['down']} A={buttons['a']} B={buttons['b']}")
        print(f"Con: {status['connected']}")
