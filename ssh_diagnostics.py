import subprocess
import datetime
import os

class SSHDiagnostics:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, "ssh_diagnostics.log")

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def check_ssh_service(self):
        try:
            result = subprocess.run(
                ["systemctl", "status", "ssh"], capture_output=True, text=True, check=True
            )
            self.log("Controllo stato ssh.service eseguito con successo.")
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.log(f"Errore nel controllo stato ssh.service: {e}")
            return f"Errore nel controllo stato ssh.service: {e}"

    def check_ssh_port(self):
        try:
            result = subprocess.run(
                ["ss", "-tuln"], capture_output=True, text=True, check=True
            )
            listening = ":22" in result.stdout and "LISTEN" in result.stdout
            self.log(f"Controllo porta 22: {'attiva' if listening else 'non attiva'}.")
            return listening
        except subprocess.CalledProcessError as e:
            self.log(f"Errore nel controllo porta 22: {e}")
            return False

    def check_sshd_config(self, config_path="/etc/ssh/sshd_config"):
        try:
            with open(config_path, "r") as f:
                config = f.read()
            self.log("Lettura sshd_config eseguita con successo.")
            return config
        except Exception as e:
            self.log(f"Errore lettura sshd_config: {e}")
            return None

    def run_all(self):
        report = {}
        report["ssh_service_status"] = self.check_ssh_service()
        report["ssh_port_open"] = self.check_ssh_port()
        report["sshd_config"] = self.check_sshd_config()
        return report
