
# Host discovery
Ci sono molte opzioni di nmap per determinare quali host sono attivi. La piu efficace è utilizzare icmp echo requests.
- nmap ip/mask -sn -oA tnet | grep for | cut -d" " -f5: -sn disabilita port scanning -oA scrive output su tnet file
- nmap -sn -oA tnet -iL hosts.lst: -iL scansioni verso i target forniti in hosts.lst, gli host in output sono quelli attivi il resto degli host sono spenti.
- map -sn -oA tnet 10.129.2.18 10.129.2.19 10.129.2.20: scansione di ip multipli
- nmap 10.129.2.18 -sn -oA host -PE --packet-trace: -PE è icmp echo requests, ci aspettiamo un icmp reply, ma in realta prima di tutto cio viene inviato un arp ping-arp reply e lo si puo vedere con l'opzione --packet-trace che consente di vedere i pacchetti inviati/ricevuti. Per assicurare l'invio di icmp echo request si specifica l'opzione -PE
- nmap 10.129.2.18 -sn -oA host -PE --reason: --reason mostra il motivo di un certo risultato
- nmap 10.129.2.18 -sn -oA host -PE --packet-trace --disable-arp-ping:  disabilita arp requests e scansiona host con icmp echo requests

# Host and port scanning
6 stati diversi per le port scansionate:
1. open
2. closed: il pacchetto di risposta contiene la flag RST
3. filtered: nmap non capisce se la porta scansionata è aperta o chiusa perche non riceve nessuna risposta
4. unfiltered: capita durante TCP-ACK scan, significa che la porta è accessibile ma non determina se è aperta o chiusa
5. open | filtered: indica con firewall potrebbe filtrare o proteggere la porta
6. closed | filtered: capita nel IP ID idle scans, indica che è impossibile determinare se la porta è chiusa o filtrata dal firewall

- nmap 10.129.2.28 --top-ports=10: scansione top 10 porte, con opzione -sS di default solo in root mode perche socket permissions richiedono di creare raw tcp packets. Altrimenti tcp scan -sT di default. Con -F top 100 porte, -p- tutte le porte tcp
- nmap 10.129.2.28 -p 21 --packet-trace -Pn -n --disable-arp-ping: osservo pacchetti inviati/ricevuti con packet trace, disabilito icmp echo request, disabilito arp ping, disabilito dns resolution
- nmap 10.129.2.28 -p 443 --packet-trace --disable-arp-ping -Pn -n --reason -sT: opzione -sT completa three way tcp handshake, consente di determinare lo stato preciso della porta, non è stealth come le altre modalità
- nmap 10.129.2.28 -F -sU: UDP scan -F top 100 ports, questo tipo di scansione è molto piu lenta di -sS tcp scan
- nmap -sV: service scan

More information about port scanning techniques we can find at: [scanning techniques](https://nmap.org/book/man-port-scanning-techniques.html)

# Saving the result
## Different format
3 different format:
- -oN: normal output with .nmap extension
- -oG: grepable output with .gnmap ext
- -oX: xml output with .xml ext
- -oA: save results in all formats

## Style sheets
To convert the stored results from XML format to HTML, we can use the tool xsltproc.
- xsltproc target.xml -o target.html

# Service enumeration
Essenziale determinare la versione delle applicazioni in us nel modo piu accurato possibile. Quick port scan -sV, causa poco traffico in rete. L'opzione --stats-every=5s oppure 5m per i minuti consente di mostrare lo stato della scansione, posso aumentare la verbosita con -v oppure -vv, per mostrare direttamente le porte appena vengono scoperte. In primis, nmap guarda ai banner delle porte scansionate e printa. Se non riesce a identificare la versione con i banner allora tenta un signature-based matching system. </br> Svantaggio: la scansione puo tralasciare info importanti perche nmap non sa come gestirle. Possiamo intercettare quello che nmap non ci mostra tramire tcpdump e poi con nc per grab the banner.
- sudo tcpdump -i eth0 host 10.10.14.2 and 10.129.2.28: attende messaggi da 10.129.2.28
- nc -nv 10.129.2.28 25 (server smtp): mi connetto a quell'ip cosi tcpdump cattura i messaggi fra host e target

# Nmap scripting engine
Totale 14 categorie in cui possiamo dividere gli script:
- auth --Determination of authentication credentials.
- broadcast --	Scripts, which are used for host discovery by broadcasting and the discovered hosts, can be automatically added to the remaining scans.
- brute --	Executes scripts that try to log in to the respective service by brute-forcing with credentials.
- default	 --Default scripts executed by using the -sC option.
- discovery --	Evaluation of accessible services.
- dos --	 These scripts are used to check services for denial of service vulnerabilities and are used less as it harms the services.
- exploit --	This category of scripts tries to exploit known vulnerabilities for the scanned port.
- external --     Scripts that use external services for further processing.
- fuzzer --	This uses scripts to identify vulnerabilities and unexpected packet handling by sending different fields, which can take much time.
- intrusive --	Intrusive scripts that could negatively affect the target system.
- malware --	Checks if some malware infects the target system.
- safe --	Defensive scripts that do not perform intrusive and destructive access.
- version --	Extension for service detection.
- vuln --	Identification of specific vulnerabilities.</br>

Modi per definire script in nmap:
- sudo nmap \<target> -sC
- sudo nmap \<target> --script \<category>
- nmap \<target> --script \<script-name>,\<script-name>,...
- nmap 10.129.2.28 -p 80 -A: con -A scansiono con le opzioni -sV, .O (os detection), traceroute(--traceroute) e con script di default inclusi in -sC.

# Performance
## Timeouts
Quando nmap invia pacchetti, aspetta tempo per riceverli (rtt), si puo settare quel tempo con ---min-rtt-timeout yyms (nmap parte con 100ms) e con --max-rtt-timeout xxms

## Max retries
Specificare il retry rate dei pacchetti inviati con --max-retires x (default è 10).
- sudo nmap 10.129.2.0/24 -F --max-retries 0 | grep "/tcp" | wc -l

## Rates
Se conosciamo la banda di rete, possiamo modificare il tasso di invio dei pacchetti con --min-rate \<num>

## Timing
nmap offre sei diversi timing templates da usare -T \<0-5>, determinano il livello di aggressivita della scansione, se troppo aggressivo il sistema potrebbe bloccarci a causa dell'elevato traffico prodotto in rete (dafault -T 3)

#  Firewall and IDS/IPS Evasion
Nmap fornisce molti modi per evadere regole dei firewall e ids/ips.
- Firewall: controllail traffico di rete, e decide come gestire il traffico in base alle sue regole di input, output e forward (drop, accept, queue, return0)
- IDS: scans the network for potential attacks, analyzes them, and reports any detected attacks. 
- IPS complements IDS by taking specific defensive measures if a potential attack should have been detected. 

The analysis of such attacks is based on pattern matching and signatures. If specific patterns are detected, such as a service detection scan, IPS may prevent the pending connection attempts.

## Determine Firewalls and their rules
Pachetti possono essere dropped o rejected. I dropped sono ignorati senza risposto dal host. I pacchetti rejected mostrano che c'è una specifica regola nel firewall del host: pacchetti TCP ritorna un RST flag, mente ICMP contengono diversi tipo di codici di errore:
- net unreachable
- net prohibited
- host enreachable
- host prohibited
- port unreachable
- proto unreachable

Scansione con  -sA è piu difficile da identificare per il firewall e sistemi IDS/IPS, rispetto a scansioni con -sS o -sT, perche -sA invia pacchetti con solo ACK flag. Per le connessioni incoming, anche se il firewall blocca tutto quello che entra, i pacchetti ack li fa passare perche non riesce a riconoscere se la connessione è stata stabilita dall'interno della rete oppure no.

## Detect IDS/IPS
Detection ids/ips piu difficile, perche sono sistemi passivi di monitoraggio del traffico. Sistemi IDS esaminano tutte le connessioni fra host, se trovano pacchetti che rispettano certe specifiche, l'amministratore viene notificato ed esegue le opportune azioni.</br> Sistemi IPS, prendono misure configurate dall'amministratore per prevenire potenziali attacchi automatici.</br> Per determinare se questi sistemi sono presenti sulla rete target si utilizzadno molti VPS (virtual private servers) durante un pen test.

- I sistemi IDS servono generalmente ad aiutare gli amministratori a rilevare potenziali attacchi alla rete. In questo modo, possono decidere come gestire tali connessioni. Possiamo attivare determinate misure di sicurezza da parte di un amministratore, ad esempio eseguendo una scansione aggressiva di una singola porta e del relativo servizio. In base all'attivazione di specifiche misure di sicurezza, possiamo rilevare se sulla rete sono presenti applicazioni di monitoraggio.

- Un metodo per determinare se un sistema IPS è presente nella rete target consiste nell'eseguire una scansione da un singolo host (VPS). Se in qualsiasi momento questo host risulta bloccato e non ha accesso alla rete target, sappiamo che l'amministratore ha adottato delle misure di sicurezza. Di conseguenza, possiamo continuare il nostro penetration test con un altro VPS (quindi con un altro ip).

## Decoys
Puo capitare che l'amministratore blocchi specifiche subnet da diverse zone del mondo, per prevenire accessi alla rete target. Questo è un altro esempio di IPS bloccante.</br> Decoy scanning method è la scelta giusta, nmap genera vari ip dentro l'header per cammuffare l'origine del pacchetto inviato, opzione -D RND:5  per dire di generare cinque ip causali. Decoys possono essere usati con syn, ack, icmp scans e os detection. Con -S possiamo specificare manualmente ip addr.

## DNS proxying
Di default nmapp esegue dns resolution a meno che non si specifichi il contrario. Le query dns passano in quesi tutti i casi perche il web server puo essere trovato e visitato. DNS queries fatte sulla porta udp 53. Nmap specifica dns server con --dns-server \<ns>. Possiamo usare porta 53 come sorgente (--source-port 53) per la scansione. Trovato che il firewall accetta pacchetti dalla porta 53 ci connettiamo a quella porta con nc: ncat -nv --source-port 53 10.129.2.28 50000

To find out what program or service is occupying a specific port, choose the appropriate tool based on your operating system.

Per trovare quale programma o servizio è occupato da una porta specifica, ci sono comandi specifici:
- sudo ss -lnpt 'sport = :pnr'
- sudo lsof -n -i :pnr | grep pnr
- sudo netstat -nlp | grep :pnr