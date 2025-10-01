"""Widget factory for creating themed components"""
from typing import Optional, Callable, Union
import tkinter as tk
from tkinter import ttk

from ..themes.theme_manager import ThemeManager


class WidgetFactory:
    """Factory for creating consistently themed widgets"""
    
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        
    def create_button(self, parent: Union[tk.Widget, tk.Tk], text: str, command: Optional[Callable] = None, 
                     style: str = 'TButton', width: Optional[int] = None) -> ttk.Button:
        """Create a themed button"""
        if command is not None and width is not None:
            return ttk.Button(parent, text=text, style=style, command=command, width=width)
        elif command is not None:
            return ttk.Button(parent, text=text, style=style, command=command)
        elif width is not None:
            return ttk.Button(parent, text=text, style=style, width=width)
        else:
            return ttk.Button(parent, text=text, style=style)
        
    def create_label(self, parent: Union[tk.Widget, tk.Tk], text: str, style: str = 'TLabel') -> ttk.Label:
        """Create a themed label"""
        return ttk.Label(parent, text=text, style=style)
        
    def create_frame(self, parent: Union[tk.Widget, tk.Tk], style: str = 'TFrame', 
                    padding: Optional[str] = None) -> ttk.Frame:
        """Create a themed frame"""
        if padding is not None:
            return ttk.Frame(parent, style=style, padding=padding)
        else:
            return ttk.Frame(parent, style=style)
        
    def create_labelframe(self, parent: Union[tk.Widget, tk.Tk], text: str, 
                         style: str = 'TLabelFrame') -> ttk.LabelFrame:
        """Create a themed labelframe"""
        return ttk.LabelFrame(parent, text=text, style=style)
        
    def create_state_button(self, parent: tk.Widget, state_code: str, state_name: str,
                           command: Optional[Callable] = None) -> ttk.Button:
        """Create a state selection button"""
        button_text = f"{state_code}\n{state_name}"
        
        if command is not None:
            return ttk.Button(parent, text=button_text, style='State.TButton', 
                            command=lambda: command(state_code))
        else:
            return ttk.Button(parent, text=button_text, style='State.TButton')