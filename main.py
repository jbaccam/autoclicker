import customtkinter
import keyboard
import threading
import time
from pynput.mouse import Controller, Button

customtkinter.set_appearance_mode("dark")  # set dark mode theme
customtkinter.set_default_color_theme("dark-blue")  # set color theme

root = customtkinter.CTk()  # create main application window
root.geometry("750x650")  # set window size
root.title("Jay's AutoClicker")  # set window title

# Mouse controller
mouse = Controller()

# Global Variables
clicking = False  # flag to track clicking state
click_thread = None  # thread for handling clicks
click_speed = 1 / 10  # default CPS (10 CPS)
toggle_key = ""  # stores toggle key
hold_key = ""  # stores hold key
force_quit_key = "esc"  # default force quit key
toggle_handler = None  # handler for toggle key events
hold_handler = None  # handler for hold key press event
hold_release_handler = None  # handler for hold key release event

# Clicking functionality

def click_mouse():
    # runs the clicking loop in a separate thread.
    global clicking
    while clicking:
        if click_type_var.get() == "left":
            mouse.click(Button.left)  # left click action
        else:
            mouse.click(Button.right)  # right click action
        time.sleep(click_speed)  # uses CPS-based delay

def start_clicking():
    # starts clicking based on Hold/Toggle mode.
    global clicking, click_thread
    if mode_var.get() == "toggle":
        # For toggle mode, we don't want to start multiple threads on repeated key presses.
        # The toggle_clicking() function will handle starting/stopping.
        pass  
    elif mode_var.get() == "hold":
        if not clicking:  # only start if not already clicking
            clicking = True
            click_thread = threading.Thread(target=click_mouse, daemon=True)
            click_thread.start()

def stop_clicking():
    # stops clicking when the key is released for Hold mode.
    global clicking
    if mode_var.get() == "hold":
        clicking = False  # stop clicking when key is released

def toggle_clicking():
    # toggles clicking on/off in Toggle mode.
    global clicking, click_thread
    if clicking:
        clicking = False
    else:
        clicking = True
        click_thread = threading.Thread(target=click_mouse, daemon=True)
        click_thread.start()

# speed slider

def update_speed(value):
    # updates click speed based on CPS slider movement.
    global click_speed
    cps = float(value)  # convert slider value to CPS
    if cps > 0:
        click_speed = 1 / cps  # convert CPS to delay
    speed_display_label.configure(text=f"Speed: {cps:.1f} CPS")  # update UI

# Hotkey binding

def normalize_key(key):
    # converts key names to lowercase to avoid errors.
    return key.strip().lower()  # ensure key names are standardized

def bind_toggle_key():
    # binds a hotkey for toggling the auto-clicker ON/OFF.
    global toggle_key, toggle_handler
    key = toggle_key_entry.get()
    if key:
        key = normalize_key(key)  # convert to lowercase for compatibility
        if toggle_key:
            if toggle_handler is not None:
                keyboard.unhook(toggle_handler)  # remove old toggle handler if already set
        toggle_key = key
        toggle_handler = keyboard.on_release_key(toggle_key, lambda e: toggle_clicking())
        toggle_key_label_display.configure(text=f"Toggle Key: {toggle_key.upper()}")  # update UI

def bind_hold_key():
    # binds a hotkey for holding down the left click.
    global hold_key, hold_handler, hold_release_handler
    key = hold_key_entry.get().strip().lower()  # Normalize the key
    if not key:
        return  # prevents empty key errors
    hold_key = key  # update hold key
    if hold_handler is not None:
        keyboard.unhook(hold_handler)
    if hold_release_handler is not None:
        keyboard.unhook(hold_release_handler)
    # For hold mode, start clicking on key press and stop on key release
    hold_handler = keyboard.on_press_key(hold_key, lambda e: start_clicking(), suppress=False)
    hold_release_handler = keyboard.on_release_key(hold_key, lambda e: stop_clicking(), suppress=False)
    hold_key_label_display.configure(text=f"Hold Key: {hold_key.upper()}")  # Update UI

# Force quit feature

def force_quit():
    #Force quits all clicking.
    global clicking
    clicking = False
    mouse.release(Button.left)  # Release mouse if stuck
    print("Force Quit Activated! Stopping all clicks.")

keyboard.add_hotkey(force_quit_key, force_quit)  # bind force quit to escape key

# UI Goodies

frame = customtkinter.CTkFrame(master=root)  # create main frame
frame.pack(pady=20, padx=50, fill="both", expand=True)  # add padding and expand frame

label = customtkinter.CTkLabel(master=frame, text="Jay's AutoClicker", font=("Arial", 18))  # main title
label.pack(pady=12, padx=10)

# Click Type Selection (left or right click)
click_type_var = customtkinter.StringVar(value="left")  # default to left click

left_click_rb = customtkinter.CTkRadioButton(frame, text="Left Click", variable=click_type_var, value="left")  # left click option
left_click_rb.pack(pady=5)

right_click_rb = customtkinter.CTkRadioButton(frame, text="Right Click", variable=click_type_var, value="right")  # right click option
right_click_rb.pack(pady=5)

# Click Speed Slider (cps based)

speed_label = customtkinter.CTkLabel(frame, text="Click Speed (CPS - Clicks Per Second)")  # label for CPS slider
speed_label.pack(pady=5)

speed_slider = customtkinter.CTkSlider(frame, from_=1, to=50, command=update_speed)  # cps slider (calls update_speed)
speed_slider.pack(pady=5)
speed_slider.set(10)  # default CPS (10 CPS)

speed_display_label = customtkinter.CTkLabel(frame, text="Speed: 10.0 CPS")  # shows live CPS
speed_display_label.pack(pady=5)

# Togle hotkey

toggle_key_label = customtkinter.CTkLabel(frame, text="Set Toggle Hotkey:")  # Label for toggle hotkey
toggle_key_label.pack(pady=5)

toggle_key_entry = customtkinter.CTkEntry(frame, width=100)  # Input field for toggle hotkey
toggle_key_entry.pack(pady=5)

bind_toggle_button = customtkinter.CTkButton(frame, text="Bind Toggle Key", command=bind_toggle_key)  # Button to bind toggle key
bind_toggle_button.pack(pady=5)

toggle_key_label_display = customtkinter.CTkLabel(frame, text="Toggle Key: None")  # Displays current toggle key
toggle_key_label_display.pack(pady=5)

# Hold key

hold_key_label = customtkinter.CTkLabel(frame, text="Set Hold Key:")  # Label for hold key
hold_key_label.pack(pady=5)

hold_key_entry = customtkinter.CTkEntry(frame, width=100)  # Input field for hold key
hold_key_entry.pack(pady=5)

bind_hold_button = customtkinter.CTkButton(frame, text="Bind Hold Key", command=bind_hold_key)  # Button to bind hold key
bind_hold_button.pack(pady=5)

hold_key_label_display = customtkinter.CTkLabel(frame, text="Hold Key: None")  # Displays current hold key
hold_key_label_display.pack(pady=5)

# Hold/Toggle Mode Selection

mode_var = customtkinter.StringVar(value="hold")  # Default mode is hold

hold_rb = customtkinter.CTkRadioButton(frame, text="Hold Mode", variable=mode_var, value="hold")  # Hold mode option
hold_rb.pack(pady=5)

toggle_rb = customtkinter.CTkRadioButton(frame, text="Toggle Mode", variable=mode_var, value="toggle")  # Toggle mode option
toggle_rb.pack(pady=5)

# Force Quit Instructions
force_quit_label = customtkinter.CTkLabel(frame, text="Press 'Esc' to Force Quit", font=("Arial", 12))
force_quit_label.pack(pady=10)

root.mainloop()  # Run the main application loop
