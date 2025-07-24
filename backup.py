import os
from ssh_manager import SSHManager

def backup_ssh_config():
    manager = SSHManager()
    result = manager.backup_config()
    if "Errore" in result:
        return result
    return f"Backup eseguito con successo: {result}"
