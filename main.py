import customtkinter
import os
import subprocess
import threading
import shutil
import time
import re

customtkinter.set_appearance_mode("dark")

class GuardianApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("PC GUARDIAN v1.0 | by STOCK")
        self.geometry("600x650")
        self.configure(fg_color="#050505")

        # --- HEADER ---
        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(40, 10))

        self.logo_label = customtkinter.CTkLabel(self.header_frame, text="PC GUARDIAN", font=("Segoe UI", 32, "bold"), text_color="#00FF66")
        self.logo_label.pack(side="left")
        
        self.sub_label = customtkinter.CTkLabel(self, text="OPTIMIZATION & NETWORK TOOL", font=("Segoe UI", 12), text_color="#333333")
        self.sub_label.pack(pady=(0, 30))

        # --- КНОПКИ ДЕЙСТВИЙ ---
        self.btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10, padx=60, fill="x")

        self.dns_btn = self.create_action_btn("⚡ FLUSH NETWORK", self.flush_dns)
        self.temp_btn = self.create_action_btn("🗑️ DEEP SYSTEM CLEAN", self.clean_temp)
        self.ping_btn = self.create_action_btn("🎮 TEST GAMING PING", self.check_ping)

        # --- PROGRESS BAR ---
        self.progress = customtkinter.CTkProgressBar(self, fg_color="#121212", progress_color="#00FF66", height=10)
        self.progress.pack(pady=30, padx=60, fill="x")
        self.progress.set(0)

        # --- LOG BOX ---
        self.log = customtkinter.CTkTextbox(self, height=200, fg_color="#0a0a0a", border_width=1, border_color="#1a1a1a", text_color="#00FF66", font=("Consolas", 12))
        self.log.pack(pady=10, padx=40, fill="both", expand=True)
        
        self.add_log("System Ready. All modules online.")

    def create_action_btn(self, txt, cmd):
        btn = customtkinter.CTkButton(
            self.btn_frame, 
            text=txt, 
            height=50, 
            font=("Segoe UI", 14, "bold"), 
            fg_color="#0d0d0d", 
            border_width=1, 
            border_color="#1a1a1a", 
            hover_color="#00FF66",
            text_color="white"
        )
        btn.configure(command=cmd)
        btn.pack(pady=10, fill="x")
        return btn

    def add_log(self, text):
        self.log.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.log.see("end")

    def flush_dns(self):
        def run():
            self.progress.set(0.3)
            self.after(0, self.add_log, "Starting network reset...")
            try:
                subprocess.run("ipconfig /flushdns", shell=True, check=True, capture_output=True)
                time.sleep(0.5)
                self.progress.set(1.0)
                self.after(0, self.add_log, "SUCCESS: DNS Cache cleared.")
            except:
                self.after(0, self.add_log, "ERROR: Run as Administrator!")
            time.sleep(1)
            self.progress.set(0)
        threading.Thread(target=run, daemon=True).start()

    def clean_temp(self):
        def run():
            self.after(0, self.add_log, "Searching for junk files...")
            temp_path = os.environ.get('TEMP')
            try:
                files = os.listdir(temp_path)
                total = len(files)
                cleaned = 0
                if total == 0:
                    self.after(0, self.add_log, "System is already clean.")
                    return
                for i, file in enumerate(files):
                    try:
                        path = os.path.join(temp_path, file)
                        if os.path.isfile(path) or os.path.islink(path):
                            os.unlink(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                        cleaned += 1
                    except: continue
                    self.progress.set((i + 1) / total)
                self.after(0, self.add_log, f"CLEANUP DONE: {cleaned} objects removed.")
            except Exception as e:
                self.after(0, self.add_log, f"Error: {str(e)}")
            time.sleep(1)
            self.progress.set(0)
        threading.Thread(target=run, daemon=True).start()

    def check_ping(self):
        def run():
            self.progress.set(0.5)
            self.after(0, self.add_log, "Pinging Valve Servers (EU)...")
            target = "146.66.152.1" 
            try:
                res = subprocess.run(f"ping {target} -n 3", shell=True, capture_output=True, text=True, errors='ignore')
                
                match = re.search(r"(\d+)ms", res.stdout) or re.search(r"=\s*(\d+)", res.stdout)
                
                if match:
                    ping_val = match.group(1)
                    self.after(0, self.add_log, f"GAMING PING: {ping_val}ms (Stable)")
                else:
                    self.after(0, self.add_log, "TIMEOUT: Server did not respond.")
            except Exception as e:
                self.after(0, self.add_log, f"EXECUTION ERROR: {str(e)}")
            
            self.progress.set(1.0)
            time.sleep(1)
            self.progress.set(0)
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    app = GuardianApp()
    app.mainloop()