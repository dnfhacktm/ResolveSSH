import os
import shutil

class SSHManager:
    def __init__(self, config_path="/etc/ssh/sshd_config", backup_dir="backup"):
        self.config_path = config_path
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup_config(self):
        try:
            backup_file = os.path.join(
                self.backup_dir,
                f"sshd_config_backup_{self._timestamp()}.bak"
            )
            shutil.copy2(self.config_path, backup_file)
            return backup_file
        except Exception as e:
            return f"Errore nel backup: {e}"

    def _timestamp(self):
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def read_config(self):
        try:
            with open(self.config_path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Errore lettura configurazione: {e}"

    def write_config(self, new_content):
        try:
            with open(self.config_path, "w") as f:
                f.write(new_content)
            return "Configurazione aggiornata con successo."
        except Exception as e:
            return f"Errore scrittura configurazione: {e}"
