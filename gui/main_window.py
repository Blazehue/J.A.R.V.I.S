"""
Main GUI Window for Jarvis V2
"""

import customtkinter as ctk
from typing import Optional
from utils.logger import get_logger
from utils.config_manager import get_config

logger = get_logger()
config = get_config()


class JarvisGUI:
    """Main GUI for Jarvis"""
    
    def __init__(self, jarvis):
        self.jarvis = jarvis
        
        # Get GUI config
        self.theme = config.get('gui.theme', 'dark')
        self.width = config.get('gui.window_width', 800)
        self.height = config.get('gui.window_height', 600)
        
        # Set appearance
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Jarvis V2 - Desktop AI Assistant")
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Setup UI
        self._setup_ui()
        
        # Register callbacks
        self.jarvis.on_command(self._on_command)
        self.jarvis.on_response(self._on_response)
        
        logger.info("GUI initialized")
    
    def _setup_ui(self):
        """Setup the user interface"""
        
        # Header
        header_frame = ctk.CTkFrame(self.root)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="J.A.R.V.I.S.",
            font=("Arial", 32, "bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Just A Rather Very Intelligent System",
            font=("Arial", 12)
        )
        subtitle_label.pack()
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="● ONLINE",
            font=("Arial", 10),
            text_color="green"
        )
        self.status_label.pack(pady=5)
        
        # Chat display area
        chat_frame = ctk.CTkFrame(self.root)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            font=("Consolas", 11),
            wrap="word"
        )
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        self.chat_display.configure(state="disabled")
        
        # Input area
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(fill="x", padx=10, pady=10)
        
        self.command_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter command or say 'hey jarvis'...",
            font=("Arial", 12),
            height=40
        )
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.command_entry.bind("<Return>", self._on_enter_pressed)
        
        # Send button
        self.send_button = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self._on_send_clicked,
            width=100,
            height=40
        )
        self.send_button.pack(side="left")
        
        # Voice button
        self.voice_button = ctk.CTkButton(
            input_frame,
            text="🎤 Voice",
            command=self._on_voice_clicked,
            width=100,
            height=40,
            fg_color="darkblue"
        )
        self.voice_button.pack(side="left", padx=(5, 0))
        
        # Control buttons
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Wake word toggle
        if self.jarvis.wake_word_detector:
            self.wake_word_var = ctk.BooleanVar(value=False)
            self.wake_word_toggle = ctk.CTkSwitch(
                control_frame,
                text="Wake Word Detection",
                variable=self.wake_word_var,
                command=self._toggle_wake_word
            )
            self.wake_word_toggle.pack(side="left", padx=5)
        
        # Voice toggle
        self.voice_var = ctk.BooleanVar(value=config.get('voice.enabled', True))
        self.voice_toggle = ctk.CTkSwitch(
            control_frame,
            text="Voice Enabled",
            variable=self.voice_var,
            command=self._toggle_voice
        )
        self.voice_toggle.pack(side="left", padx=5)
        
        # Clear button
        clear_button = ctk.CTkButton(
            control_frame,
            text="Clear",
            command=self._clear_chat,
            width=80
        )
        clear_button.pack(side="right", padx=5)
        
        # Initial greeting
        greeting = "Good morning, sir. Jarvis online and ready. All systems operational."
        self._append_to_chat("JARVIS", greeting, "green")
    
    def _append_to_chat(self, sender: str, message: str, color: str = "white"):
        """Append message to chat display"""
        self.chat_display.configure(state="normal")
        
        # Add sender
        self.chat_display.insert("end", f"\n{sender}: ", color)
        
        # Add message
        self.chat_display.insert("end", f"{message}\n")
        
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")
    
    def _on_enter_pressed(self, event):
        """Handle Enter key press"""
        self._on_send_clicked()
    
    def _on_send_clicked(self):
        """Handle send button click"""
        command = self.command_entry.get().strip()
        
        if not command:
            return
        
        # Clear input
        self.command_entry.delete(0, "end")
        
        # Display user command
        self._append_to_chat("YOU", command, "cyan")
        
        # Process command
        self.jarvis.process_command(command, speak_response=self.voice_var.get())
    
    def _on_voice_clicked(self):
        """Handle voice button click"""
        self._append_to_chat("SYSTEM", "Listening...", "yellow")
        self.root.update()
        
        # Process voice command
        result = self.jarvis.process_voice_command()
        
        if result.get('success') is False and result.get('error') == 'timeout':
            self._append_to_chat("SYSTEM", "No speech detected", "yellow")
    
    def _on_command(self, command: str):
        """Callback when command is received"""
        # Already displayed in _on_send_clicked
        pass
    
    def _on_response(self, result: dict):
        """Callback when response is generated"""
        response = result.get('response', '')
        success = result.get('success', False)
        
        color = "green" if success else "red"
        self._append_to_chat("JARVIS", response, color)
    
    def _toggle_wake_word(self):
        """Toggle wake word detection"""
        if self.wake_word_var.get():
            self.jarvis.start_wake_word_detection()
            self._append_to_chat("SYSTEM", "Wake word detection enabled", "yellow")
        else:
            if self.jarvis.wake_word_detector:
                self.jarvis.wake_word_detector.stop()
            self._append_to_chat("SYSTEM", "Wake word detection disabled", "yellow")
    
    def _toggle_voice(self):
        """Toggle voice features"""
        enabled = self.voice_var.get()
        config.set('voice.enabled', enabled, save=False)
        
        status = "enabled" if enabled else "disabled"
        self._append_to_chat("SYSTEM", f"Voice features {status}", "yellow")
    
    def _clear_chat(self):
        """Clear chat display"""
        self.chat_display.configure(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.configure(state="disabled")
    
    def run(self):
        """Run the GUI"""
        logger.info("Starting GUI main loop")
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Start main loop
        self.root.mainloop()
    
    def _on_closing(self):
        """Handle window closing"""
        logger.info("GUI closing")
        self.jarvis.stop()
        self.root.destroy()
