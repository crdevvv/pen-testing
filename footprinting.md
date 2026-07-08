# Indice
- [Metodologia di enumerazione](#metodologia-di-enumerazione)
  - [Layer1: internet presence](#layer1-internet-presence)
  - [Layer2: gateway](#layer2-gateway)
  - [Layer3: accessible services](#layer3-accessible-services)
  - [Layer4: processes](#layer4-processes)
  - [Layer5: privileges](#layer5-privileges)
  - [Layer6: os setup](#layer6-os-setup)
- [Domain information](#domain-information)
  - [Online presence](#online-presence)
    - [Ricognizione passiva](#ricognizione-passiva)
    - [Certificate transparency](#certificate-transparency)
    - [Identificazione server aziendali](#identificazione-server-aziendali)
    - [Analisi record dns](#analisi-record-dns)

Pen testing and also enumeration are dynamic processes. Metodologia strutturata su 6 livelli e rappresenta i confini che cerchiamo di superare con il processo di enumerazione. Il processo di enumerazione è diviso in tre livelli a partire dal piu esterno:
1. infrastructure-based enumeration (primi due livelli della metodologia)
2. host-based enumeration (successivi due livelli)
3. os-based enumeration (ultimi due livelli piu interni)

Per ogni layer abbimo due sottolivelli (partiamo da infrastructure-based):
1. internet presence
2. gateway 
3. accessible services
4. processes
5. privileges
6. OS setup

![Image](/fprinting.png "tab")

## Layer1: internet presence
Trovare traget su cui investigare. **Obiettivo**: identificare tutti i sistemi target e interfacce da poter testare

## Layer2: gateway
Capire l'interfaccio del target, come è protetta e dove è localizzata. **Obiettivo**: capire con cosa abbiamo a che fare e a cosa dobbiamo fare attenzione.

## Layer3: accessible services
**Obiettivo**:  mira a comprendere la ragione dell'esistenza e la funzionalità del sistema target e ad acquisire le conoscenze necessarie per comunicare con esso e sfruttarlo efficacemente per i nostri scopi.

## Layer4: processes
**Obiettivo**: capire quali processi si attivano e identificare le dipendenze fra loro

## Layer5: privileges
Ogni servizio gira sotto uno specifico utente o gruppo con autorizzazioni e privilegi concessi dall'amministratore del sistema. **Obiettivo**: fondamentale identificarli e comprendere cosa è possibile e cosa non è possibile con questi privilegi.

## Layer6: os setup
Collezionare info riguardanti il so e il suo setup. **Obiettivo**: scoprire come l'amministratore gestire i sistemi e quali info sensibili possiamo ricavarne

# Domain information
Raccogliere info e capire le tecnologie e la stuttura necessarie per i servizi. Info raccolte in modo passivo, navigare mascherati da clienti.</br> Raccolta passiva: servizi di terze parti per capire la compagnia, vedere il sito principale, ricordando quali tecnologie e strutture servono per determinati servizi offerti. Combinazione di quello che vediamo e di quello che non vediamo

## Online presence
Dopo aver compreso le basi della azienda e i suoi servizi, cerchiamo una  prima traccia della sua presenza in internet. Per esempio attraverso il suo certificato ssl che possiamo esaminare a partire dal suo sito web.

### Ricognizione passiva
La ricognizione passiva consiste nel raccogliere informazioni sfruttando servizi di terze parti ed esaminando il sito web principale comportandosi come normali visitatori o clienti.

- Perché si fa: Evita di generare allarmi nei sistemi difensivi (IDS/IPS) del bersaglio.
- L'Approccio dello Sviluppatore: Per capire la struttura invisibile dell'azienda, bisogna guardare i servizi attivi dal punto di vista di chi li ha creati, associando ogni servizio alle sue necessità tecniche sottostanti.

### Certificate transparency
Un punto di partenza fondamentale è lo studio dei certificati SSL/TLS della ditta. Lo standard (RFC 6962) impone alle autorità di certificazione (come Let's Encrypt) di registrare pubblicamente ogni certificato emesso in registri chiamati Certificate Transparency Logs. *crt.sh*: È un motore di ricerca web che interroga questi log storici.
Utilità: Permette di scoprire sottodomini dimenticati o nascosti (es. matomo.inlanefreight.com, smartfactory.inlanefreight.com) semplicemente leggendo la cronologia dei vecchi certificati richiesti dall'azienda.

### Identificazione server aziendali 
Una volta ottenuta una lista di sottodomini, il testo mostra un ciclo for in Bash per identificare quali host appartengano all'infrastruttura diretta dell'azienda e quali a terze parti (es. AWS). Non è consentito testare server di terze parti senza autorizzazione. Con comando *host* troviamo ip del dominio, poi possiamo usare shodan per trovare eventuali port aperte di quel ip

- Shodan: È un motore di ricerca per dispositivi connessi a Internet (IoT, server, router).
- Utilità: Invece di fare una scansione attiva con Nmap (che verrebbe intercettata), si interroga Shodan inserendo gli IP trovati. Shodan restituisce le porte aperte, i banner dei software (es. nginx, Apache httpd) e le versioni memorizzate nei suoi database durante le sue scansioni globali quotidiane.

### Analisi record dns
Il comando dig any inlanefreight.com interroga il server DNS per ottenere tutti i record disponibili in un colpo solo. Il testo si concentra sul valore strategico dei TXT Records. I record TXT contengono stringhe di testo usate per la verifica del dominio o per la sicurezza delle e-mail (SPF, DMARC). Dall'analisi di questi record, l'attaccante scopre quali servizi esterni usa l'azienda, aprendo nuovi scenari di attacco. </br>
Let us look at what we have learned here and come back to our principles. We see an IP record, some mail servers, some DNS servers, TXT records, and an SOA record.
- A records: We recognize the IP addresses that point to a specific (sub)domain through the A record. Here we only see one that we already know.
- MX records: The mail server records show us which mail server is responsible for managing the emails for the company. Since this is handled by google in our case, we should note this and skip it for now.
- NS records: These kinds of records show which name servers are used to resolve the FQDN to IP addresses. Most hosting providers use their own name servers, making it easier to identify the hosting provider.
- TXT records: this type of record often contains verification keys for different third-party providers and other security aspects of DNS, such as SPF, DMARC, and DKIM, which are responsible for verifying and confirming the origin of the emails sent. Here we can already see some valuable information if we look closer at the results.

## Cloud Resources
Anche se il provider del cloud rendono sicura la loro infrastruttura conetralmente, non significa che le compagnie che usano il cloud lo siano, dipende dalla configurazione dell'amministratore. Partiamo da s3 bucket (amazon), blobs (Azure micr), cloud storage (gcp), che possono essere accessi senza autenticazione se configurati male.
- for i in $(cat subdomainlist);do host $i | grep "has address" | grep inlanefreight.com | cut -d" " -f1,4;done
- combinare google search con google dorks, per esempio *inurl:amazonaws.com/blob.core.windows.net* e *intext:* per raffinare la ricerca
- provider di terze parti come [domain.glass](https://domain.glass/) ci dicono molto sull'infrastruttura della compagnia.
- un altro provider utile è [grayhatwarfare](https://buckets.grayhatwarfare.com/), scopre aws, azure, gcp cloud storage

## Staff
La ricerca e l'identificazione dei dipendenti sulle piattaforme di social media possono rivelare molto sull'infrastruttura e la composizione dei team. Questo, a sua volta, può permetterci di individuare le tecnologie, i linguaggi di programmazione e persino le applicazioni software utilizzate. In larga misura, saremo anche in grado di valutare l'attenzione di ciascun individuo in base alle sue competenze.
- tramite linkedin, Xing, analizziamo i linguaggi richiesti, le repo github