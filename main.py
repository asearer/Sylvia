"""
main.py

Entry point for SylviaBot. Allows selection between CLI and API interface.
"""

import argparse
from src.interface import cli
import uvicorn
import threading
from src.bot.sylvia import SylviaBot
import matplotlib
matplotlib.use('TkAgg')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SylviaBot")
    parser.add_argument("--mode", choices=["cli", "api", "gui"], default="cli", help="Interface mode")
    parser.add_argument("--model", type=str, help="Path to trained model or corpus")
    args = parser.parse_args()

    if args.mode == "cli":
        cli.start_cli(model_path=args.model)
    elif args.mode == "api":
        uvicorn.run("src.interface.api:app", host="0.0.0.0", port=8000, reload=True)
    elif args.mode == "gui":
        import tkinter as tk
        from tkinter import scrolledtext
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from personality.ai_personality.personality.visualizer_gui import PersonalityGUIVisualizer
        bot = SylviaBot()
        visualizer = PersonalityGUIVisualizer(bot.personality)
        visualizer.fig.tight_layout()  # Prevent overlapping of graphs

        # Tkinter GUI setup
        root = tk.Tk()
        root.title("Sylvia Chatbot with Personality Visualization")
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Chat display
        chat_display = scrolledtext.ScrolledText(root, state='disabled', width=60, height=20, wrap=tk.WORD)
        chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # User input
        user_input = tk.StringVar()
        input_entry = tk.Entry(root, textvariable=user_input, width=50)
        input_entry.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        input_entry.focus_set()  # Set focus on startup

        def send_message(event=None):
            print('[DEBUG] send_message called')  # Debug print
            msg = user_input.get().strip()
            if not msg:
                input_entry.focus_set()
                return
            chat_display.config(state='normal')
            chat_display.insert(tk.END, f'You: {msg}\n')
            chat_display.config(state='disabled')
            chat_display.see(tk.END)
            user_input.set("")
            input_entry.focus_set()  # Set focus after sending
            # Handle commands
            if msg.lower().startswith("/switch"):
                parts = msg.split()
                if len(parts) > 1:
                    try:
                        bot.switch_personality(parts[1])
                        response = f"Switched to {parts[1]}"
                    except ValueError as e:
                        response = str(e)
                    visualizer.update_history()
                    display_response(response)
                    return
            if msg.lower().startswith("/hybrid"):
                parts = msg.split()
                if len(parts) > 1:
                    weights = {}
                    for pair in parts[1].split(","):
                        try:
                            name, w = pair.split(":")
                            weights[name] = float(w)
                        except:
                            response = f"Invalid format: {pair}. Use Name:Weight"
                            display_response(response)
                            return
                    try:
                        bot.set_weighted_hybrid(weights)
                        response = f"Weighted hybrid active: {', '.join([f'{k}({v})' for k,v in weights.items()])}"
                    except ValueError as e:
                        response = str(e)
                    visualizer.update_history()
                    display_response(response)
                    return
            if msg.lower() in ["quit", "exit"]:
                root.quit()
                return
            response = bot.get_response(msg)
            print(f'[DEBUG] Sylvia response: {response}')  # Debug print
            display_response(f"{', '.join(bot.personality.active_profiles)} AI: {response}")
            visualizer.update_history()

        def display_response(response):
            chat_display.config(state='normal')
            chat_display.insert(tk.END, f'{response}\n')
            chat_display.config(state='disabled')
            chat_display.see(tk.END)

        input_entry.bind('<Return>', send_message)
        send_button = tk.Button(root, text="Send", command=send_message)
        send_button.grid(row=1, column=1, padx=5, pady=5)

        # Matplotlib Figure embedding
        canvas = FigureCanvasTkAgg(visualizer.fig, master=root)
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky='nsew')
        root.grid_columnconfigure(2, weight=0)
        root.grid_rowconfigure(1, weight=0)
        visualizer.ani = visualizer.fig.canvas.new_timer(interval=1000)
        def update_plot():
            visualizer.animate(0)
            canvas.draw()
            root.after(1000, update_plot)
        update_plot()

        root.mainloop()
