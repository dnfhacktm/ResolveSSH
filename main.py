from ssh_diagnostics import SSHDiagnostics
from ssh_manager import SSHManager
from backup import backup_ssh_config

def print_menu():
    print("""
ResolveSSH - Gestione e diagnostica SSH

             Menu Principale              
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Scelta ┃ Funzione                      ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   1    │ Controlla stato servizio SSH  │
│   2    │ Visualizza configurazione SSH │
│   3    │ Modifica configurazione SSH   │
│   4    │ Backup configurazione         │
│   5    │ Diagnostica problemi SSH      │
│   6    │ Visualizza log SSH recenti    │
│   7    │ Esci                          │
└────────┴───────────────────────────────┘
""")

def main():
    diagnostics = SSHDiagnostics()
    manager = SSHManager()

    while True:
        print_menu()
        scelta = input("Seleziona un'opzione > ").strip()

        if scelta == "1":
            print("\nStato servizio SSH:\n")
            print(diagnostics.check_ssh_service())
        elif scelta == "2":
            config = manager.read_config()
            print("\nConfigurazione sshd_config:\n")
            print(config)
        elif scelta == "3":
            print("\nModifica configurazione SSH")
            print("Inserisci la nuova configurazione. Scrivi 'END' su una nuova riga per terminare:\n")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "END":
                    break
                lines.append(line)
            new_config = "\n".join(lines)
            response = manager.write_config(new_config)
            print(response)
        elif scelta == "4":
            result = backup_ssh_config()
            print(result)
        elif scelta == "5":
            print("\nEsecuzione diagnostica SSH...\n")
            report = diagnostics.run_all()
            print("Report diagnostica:")
            for k, v in report.items():
                if isinstance(v, bool):
                    print(f"{k}: {'OK' if v else 'NON OK'}")
                else:
                    print(f"{k}: {str(v)[:500]}...\n")
        elif scelta == "6":
            try:
                with open(diagnostics.log_file, "r") as f:
                    logs = f.read()
                print("\nLog SSH Diagnostics:\n")
                print(logs)
            except Exception as e:
                print(f"Errore nella lettura dei log: {e}")
        elif scelta == "7":
            print("Uscita in corso...")
            break
        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()
