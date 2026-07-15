# Indice

- [Pentesting process](#pentesting-process)
  - [Pre-engagement](#pre-engagement)
  - [Information gathering](#information-gathering)
  - [Vulnerability assessment](#vulnerability-assessment)
  - [Exploitation](#exploitation)
  - [Post-exploitation](#post-exploitation)
  - [Lateral movement](#lateral-movement)
  - [Proof of concept](#proof-of-concept)
  - [Post-engagement](#post-engagement)
- [Penetration testing overview](#penetration-testing-overview)
- [Law and regulations](#law-and-regulations)
- [Pre-engagement](#pre-engagement-1)
  - [Scoping questionnaire](#scoping-questionnaire)
  - [Pre-engagement meeting](#pre-engagement-meeting)
  - [Kick-off meeting](#kick-off-meeting)
  - [Contractors agreement](#contractors-agreement)
- [Information gathering](#information-gathering-1)
  - [Open-source intelligence (OSINT)](#open-source-intelligence-osint)
  - [Infrastructure enumeration](#infrastructure-enumeration)
  - [Service enumeration](#service-enumeration)
  - [Host enumeration](#host-enumeration)
  - [Pillaging](#pillaging)
- [Vulnerability assessment](#vulnerability-assessment-1)
  - [Vulnerability research and analysis](#vulnerability-research-and-analysis)
  - [Assessment of Possible Attack Vectors](#assessment-of-possible-attack-vectors)
  - [The return](#the-return)
- [Exploitation](#exploitation-1)
  - [Prioritization of Possible Attacks](#prioritization-of-possible-attacks)
  - [Preparation for the Attack](#preparation-for-the-attack)
- [Post-exploitation](#post-exploitation-1)
  - [Evasive testing](#evasive-testing)
  - [Information gathering](#information-gathering-2)
  - [Pillaging](#pillaging-1)
  - [Persistence](#persistence)
  - [Vulnerability assessment](#vulnerability-assessment-2)
  - [Privilege escalation](#privilege-escalation)
  - [Data exfiltration](#data-exfiltration)
- [Lateral movement](#lateral-movement-1)
- [Proof-of-concept](#proof-of-concept-1)
- [Post-engagement](#post-engagement-1)
  - [Cleanup](#cleanup)
  - [Documentation and reporting](#documentation-and-reporting)
  - [Report review meeting](#report-review-meeting)
  - [Deliverable acceptance](#deliverable-acceptance)
  - [Post-remediation testing](#post-remediation-testing)
  - [Role of the Pentester in Remediation](#role-of-the-pentester-in-remediation)
  - [Data retention](#data-retention)
  - [Close out](#close-out)

![Image](/img.png "grafo")

# Pentesting process

## Pre-engagement

Documentati per iscritto gli impegni principali, i compiti, l'ambito, i limiti e gli accordi correlati. Durante questa fase, vengono redatti i documenti contrattuali e vengono scambiate le informazioni essenziali rilevanti sia per i penetration tester che per il cliente, a seconda del tipo di valutazione. Da questo nodo si va solo verso **information gathering**. </br> In questa fase è importante avere skill in linux e windows fundamentals, networking, web app, web requests, js deobfuscation, active directory.

## Information gathering

Nodo verso vulnerability assessement. </br>
Le conclusioni che traiamo e le azioni che intraprendiamo si basano sulle informazioni disponibili, queste informazioni devono essere reperite da qualche parte, quindi è fondamentale sapere come recuperarle e sfruttarle al meglio in base ai nostri obiettivi di valutazione. Questa fase richiede tempo e pazienza. Non andare subito verso l'exploiting di una potenziale vulnerabilità per evitare di perdere altro tempo. Nmap , footprinting, osint, ...

## Vulnerability assessment

Fase divisa in due parti: scan for knowing vulnerabilities with automated tools, e analisi di potenziali vulnerabilità tramite le informazioni trovate. In primis possiamo fare exploitation, oppure post exploitation, la terza opzione è lateral movement in cui ci si muove dal sistema rotto ad un altro. Infine possiamo fare di nuovo info gathering in mancanza di info.

## Exploitation

Attacco verso un sistema basato sulle vulnerabilità trovate. Vengono usate le info raccolte per preparare l'attacco. Quattro punti verso cui possiamo andare: info gathering sul sistema locale, post exploitation per fare privileges escalation, lateral movement, proof of concept. </br> Questa fase include tutti gli attacchi comunica a password, porte, web, sql, xss, ecc.

## Post-exploitation

Principalmente fare privileges escalation. Possiamo prendere quatto strade: info gathering per avere un overview del sistema attaccato, expoloitation with higher privileges, lateral movement per trovare cose che prima non erano visibili, proof of concept.

## Lateral movement

Muoversi in una rete, tre percorsi possibili: vulnerability assessment per capire quali servizi che potrebbero essere exploitati stanno girando, info gathering, proof of concept.

## Proof of concept

Prova che la vulnerablità trovata esiste. Consegna report e dimostrazione giocattolo che funziona. Gli amministratori devono garantire che nessun altro sistema venga influenzato negativamente dall'introduzione di una modifica.

## Post-engagement

Documentation and reporting.

# Penetration testing overview

- Concetto di risk management per una azienda, identificare, valutare e mitigare potenziali rishi.
- Vulnerability assessment, include vulnerability or security assessments and penetration tests. Vuln ass viene fatto con tool automatici.
- Testing methods:
  - External pen test fatto da prospettiva di un utente esterno o anonim.
  - Internal pen test fatto all' interno della rete aziendale.
- Tipi di penetration testing (quante informazioni sono disponibili all'attaccante, in ordine crescente):
  - blackbox
  - greybox
  - whitebox
  - red teaming: combinaizone con uno dei tipi sopra, include test fisici e social engineering.
  - purple teaming: lavorare a contatto con i difensori.

# Law and regulations

Each country has specific laws to protect individuals from unauthorized access and exploitation of their data and to ensure thei privacy.

- EU: gdpr, nisd 2, e-privacy directive.
- USA: cisa, cfaa, dmca, ecpa, hipaa, coppa.
- UK ..
- India ..
- Cina ..

# Pre-engagement

Composto da tre fasi:

1. scoping questionnaire
2. pre-engagement meeting
3. kick-off meeting

Prima di queste fasi bisogna discutere un non-disclosure agreement NDA signed by all parties (unilateral, bilateral, multilateral NDA).</br> Essenziale capire che nell'azienda può richiedere un pen test (solo C-level staff e a volte IT seniors).
Questa fase richiede la preparazione di 7 documenti prima di fare il pen test, che devono essere firmati dal client e vengono compilati prima/dopo/durante una delle tre fasi del pre-engagement:

1. NDA
2. scoping questionnaire
3. scoping document
4. pen testing proposal (contract/Sow)
5. RoE
6. contractors agreement
7. reports

## Scoping questionnaire

Inviato al cliente, per capire di cosa ha bisogno. Chiedere di che servizio ha bisogno, internal/external vulnerability assessm/pen test,..., chiedere anche quanti host attivi, quanti ip, quanti domini o subdomains, quante applicazioni mobili,etc. Chiedere se pen test è black/grey/white box, chiedere invasività del test (non, hybrid, fully) --> tutte queste info sono raccolte nel ***scoping document***.

## Pre-engagement meeting

Discute le componenti necessarie prima del pen test al client. Raccolte nel *Contract/SoW*. Si discute quindi il contract/Sow e le rules of engagement (RoE).

## Kick-off meeting

Lo scopo è consentire al cliente di valutare internamente il rischio e determinare se il problema richieda un intervento di emergenza. Avvisare il client riguardo potenziali rischi durante il pen tes: log entries and alarms, lock some users, negative impact on the net.

## Contractors agreement

Se il penetration test include anche test fisici, è necessario un ulteriore accordo con il contraente. Poiché non si tratta solo di un ambiente virtuale ma anche di un'intrusione fisica, si applicano leggi completamente diverse.

# Information gathering

Questa è la fase in cui raccogliamo tutte le informazioni disponibili sull'azienda, i suoi dipendenti e l'infrastruttura. Fase più frequente e vitale dell'intero processo di penetration testing.
Si ottengono info rilevanti in diversi modi, divisi in 4 categorie:

1. Open-source intelligence
2. Infrastructure enumeration
3. Service enumeration
4. Host enumeration

Ogni fase dovrebbe essere percorsa in ogni pen test.

## Open-source intelligence (OSINT)

Processo per trovare info pubbliche su un target. Usa info da risorse diponibili gratuitamente. Trova anche info sensibili su aziende e suoi dipendenti (chiavi private ssh per es).

## Infrastructure enumeration

Mapping dell'infrastruttura della compagnia (servers, hosts). Inoltre determinare le misure di sicurezza della azienda.

## Service enumeration

Identificare servizi che permettono di interagire con gli host o server sulla rete. Versione del servizio, quale info da, e motivo dell'utilizzo.

## Host enumeration

Esaminare ogni singolo host all'interno dell'infrastruttura nello scoping document. Quale so gira sul host o server, quali servizi usa e che versione, ecc. Determinare il ruolo svolto da ciascun host o server e i componenti di rete con cui comunica. Inoltre, dobbiamo identificare i servizi che utilizza e le porte su cui sono configurati. Si ripete anche dopo un exploitation di una o piu vulnerabilità.

## Pillaging

After post-exploitation, per raccogliere info locali sensibili su host exploitati. In sé non è una fase o una sottocategoria, ma parte integrante delle fasi di raccolta di informazioni e di escalation dei privilegi, che vengono eseguite localmente sui sistemi bersaglio.

# Vulnerability assessment

Esaminare e analizzare info raccolte nella fase di info gathering. Un'analisi è una esaminazione di un evento o di un processo, che ne descrive l'origine e l'impatto e che può essere innescato per favorire o prevenire il ripetersi. Quattro tipi di analisi:

1. Descrittiva: descrive dataset in base a caratteristiche individuali
2. Diagnostica: chiarisce cause, effetti e interazioni delle condizioni
3. Predittiva: valuazioni dati passati e presenti, questo tipo di analisi crea un modello predittivo, basato su analisi descrittiva e diagnistica
4. Prescrittiva: mira a descrivere quali azioni eseguire per elimiare o prevenire un problema futuro o per triggerare un processo specifico

## Vulnerability research and analysis

Parte dell'analisi descrittiva. Si identificano i componenti del sistema o della rete su cui stiamo investigando. In questa fase si cercano vulnerabilità, exploits e security holes già scoperti in passato e analizzati (common vuln and exposures aka CVE). Trovata la vuln entrano in gioco analisi diagnostica e predittiva, per determinare cosa ha causato quella vuln.

## Assessment of Possible Attack Vectors

Vuln assessment include anche il testing, parte dell'**analisi predittiva**. Analisi info passati e combinazione con info correnti scoperte.

## The return

Supponiamo di non riuscire a rilevare o identificare potenziali vulnerabilità nell'analisi. In tal caso, torneremo alla fase di raccolta delle informazioni e cercheremo informazioni più approfondite di quelle raccolte finora.</br> IMPORTANTE: le fasi di info gathering e vulnerability assessment spesso si interecciano e si ripetono ciclicamente finchè si non si ottengono info concrete.

# Exploitation

Si cercano modi per adattare queste vulnerabilità al nostro caso d'uso al fine di ottenere il ruolo desiderato (ad esempio, un punto d'appoggio, privilegi elevati, ecc.). Se vogliamo ottenere una reverse shell, dobbiamo modificare il PoC per eseguire il codice, in modo che il sistema target si connetta a noi tramite una connessione (idealmente) crittografata a un indirizzo IP da noi specificato.

## Prioritization of Possible Attacks

Trovate una o piu vulnerabilità durante la fase di vuln assessment, possiamo prioritizzare gli attacchi al target, in base a:

- probabilità di successo: CVSS Scoring fa questo
- complessità: time, effort, e ricerca sono richiesti per eseguire con successo l'attacco
- probabilità di danno: causata dall'exploit, bisogna evitare ogni danno al target, no dos attack in genere

Tabella con le vuln in colonna e nell rige prob succ, complessita e prob di danno.

## Preparation for the Attack

A volte ci imbattiamo in situazioni in cui non riusciamo a trovare codice exploit PoC funzionante e di alta qualità. Pertanto, potrebbe essere necessario ricostruire l'exploit localmente su una macchina virtuale che rappresenti il ​​nostro host di destinazione per capire con precisione cosa deve essere adattato e modificato. Terminato il setup con tutte le componenti installate per simulare fedelmente il sistema target, si inizia a preparare l'exploit seguendo gli step previsti. Dopo aver con successo exploitato un target e ottenuto l'accesso, ci muoviamo verso la fase di post-exploitation.

# Post-exploitation

Si assuma che l'exploitation abbia avuto successo. Considerare se usare o meno ***evasive testing***. Questa fase mira a ottenere info sensibili e security-relevant e business-relevant. Componenti richieste:

- evasive tasting
- pillaging
- privilege escalation
- data exfiltration
- info gathering
- vulnerability assessment
- persistence

## Evasive testing

Diviso in tre categorie:

- evasive: see if security measures can identifiy and respond to the actions performed.
- hybrid evasive: test specific components and sec measures.
- non-evasive: for intrusive pen test.

## Information gathering

Grazie alla fase di exploitation siamo in un nuovo ambiente e quindi bisogna raccogliere le nuove info del sistema. Quindi attraversiamo di nuovo le fasi di info gathering e vulnerability assessment da una prospettiva interna.

## Pillaging

Fase in cui esaminiamo il ruolo degli host nella rete. Analizziamo le configurazioni di rete, tra cui: interfacce, routing, DNS, servizi, ARP, VPN, IP, sottoreti, condivisioni e traffico di rete. Ricerca anche di dati sensibili come password on shares, config files, mail, documenti vari, ecc. Obiettio: dimostrare l'impatto di uno exploit riuscito e, se non abbiamo ancora raggiunto l'obiettivo dell'assessment, trovare dati aggiuntivi come le password che possono essere input per altre fasi come il movimento laterale.

## Persistence

Fasi di mantenimentodell'accesso agli host exploitati.

## Vulnerability assessment

Premesso che venga mantenuto l'accesso al sistema, ripetiamo il vulner assessment, questa volta dall'interno. Obiettivo: privilege escalation.

## Privilege escalation

Ottenere i privilegi più elevati possibili sul sistema o sul dominio è spesso fondamentale. Pertanto, puntiamo ad ottenere i privilegi di root (sui sistemi basati su Linux) o di amministratore di dominio/amministratore locale/SYSTEM (sui sistemi basati su Windows), poiché ciò ci consentirà spesso di muoverci liberamente nell'intera rete senza restrizioni.

## Data exfiltration

Provare ad estrarre informazioni confidenziali e dati vari. Trasferimento dal target al nostro sistema. DLP e EDR aiutano a trovare e prevenire data exfiltration. Per noi, il tipo di dati non ha molta importanza, ma lo sono i controlli necessari, per simulare data exfiltration from the net come proof of concept della sua fattibilità. Dovremmo verificare con il cliente che i suoi sistemi siano progettati per intercettare il tipo di dati fittizi che tentiamo di esfiltrare in caso di successo, in modo da non fornire informazioni errate nel nostro rapporto.

# Lateral movement

Se siamo riusciti a penetrare con successo nella rete (Exploitation), a raccogliere informazioni archiviate localmente e ad elevare i nostri privilegi (Post-Exploitation), passiamo alla fase di Movimento Laterale. L'obiettivo qui è testare cosa potrebbe fare un attaccante all'interno dell'intera rete. Esempio: ransomware, blocca tutti i sistemi con metodi di encyption, rendendoli inutilizzabili. 6 fasi per andare a fondo dal'interno del sistema:

1. pivoting: access inaccessible systems via an intermediary system, sfruttare host exploitato per fare scansioni dalla macchina attaccante
2. evasive testing
3. information gathering
4. vulnerability assessment
5. exploitation
6. post-exploitation

# Proof-of-concept

Prova che un progetto è ammissibile. Per dimostrare l'esistenza di un problema di sicurezza, in modo che possa essere convalidato, riprodotto, e per valutarne l'impatto e testare le soluzioni adottate. Uno degli esempi più comuni utilizzati per dimostrare le vulnerabilità del software è l'esecuzione della calcolatrice sul sistema target. Una PoC può assumere diverse forme. Ad esempio, la documentazione delle vulnerabilità riscontrate, oppure uno script o un codice che sfrutta le vulnerabilità individuate.

# Post-engagement

## Cleanup

## Documentation and reporting

## Report review meeting

## Deliverable acceptance

## Post-remediation testing

## Role of the Pentester in Remediation

## Data retention

## Close out