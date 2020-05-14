# StereoVision

<h4> 1. Spiegazione risultati raggiunti </h4>
<br>
<p>
Progetto realizzato per il laboratorio di Meccatronica presso l'Università politecnica delle Marche 
corso di laurea Ing. Informatica e dell'Automazione.
Il prototipo del misuratore è stato costruito con una StereoCamera collegata tramite USB alla Raspberry Pi 3.
I due elementi sono poi stati fissati ad un supporto metallico per consentire una maggiore stabilità in fase di misurazione.
<br>
<img src="https://github.com/GiuseppeCannata/StereoVision/blob/master/imgs/Prototipo.PNG" Hspace="320" Vspace="0">
<br>
Per quanto riguarda il processo che ha portato allo sviluppo del software ci si è basati sui seguenti passaggi:

<dl>
<dt>-Calibrazione</dt>
<dd>
Le matrici ottenute non sono state confrontate con gli effettivi parametri della StereoCamera a causa di mancaza di Datasheets.
Per maggiore affidabilità dei risultati è stata quindi condatta una calibrazione anche con il toolboox di MatLab.
</dd>
  
<dt>-Rettificazione</dt>
<dd>
Le immagini sono state in seguito rettificate affinchè punti omologhi potessero trovarsi sulla stessa line epipolare (linea in giallo in figura).
<br>
<img src="https://github.com/GiuseppeCannata/StereoVision/blob/master/imgs/Rettificazione_Imgs.PNG" Hspace="230" Vspace="0">
</dd>

<dt>-Detect del laser</dt>
<dd>
La ricerca del PUNTATORE laser avviene utilizzando lo spazio di colori RGB; In particolra il range di ricerca è tra il rosso puro e il bianco, quest'ultimo dovuto alla lucentezza del puntatore.
Per limitare disturbi derivanti dalla scena la ricerca è stata coinata in una ROI(Region of interest).
<br>
<img src="https://github.com/GiuseppeCannata/StereoVision/blob/master/imgs/ROI_Laser.PNG" Hspace="250" Vspace="0">
</dd>

<dt>-Distanza</dt>
<dd>
Dalla teoria sappiamo che la distanza di un punto P della scena, viene calocolata per tringolazione attraverso la seguente formula:
<br><br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp;
                                             distance(P) = B*f / disp    (form 1)
<br><br>
<ul>
<li>B = è la baseline cioè la distanza tra i centri ottici delle due fotocamere</li>
<li>f = distanza focale</li>
<li>disp = valore di disparity cioè la differenza tra le coordinate x dei punti omologhi nell immagine di destra e sinistra.</li>
</ul>
Non avendo i dati B e f per mancaza di Datasheets relativi alla fotocamera, e per l incertezza dei parametri ottenuti con la calibrazione, si è deciso di stimare il rapporto B*f. Procedura:
<ul>
  <li>Trovato il puntatore laser sia nell immagine di destra che in quella di sinistra sono state considerate le cordinate                    xR e XL.
  </li>
  <li>Successivamente è stata calcolata la differenza tra le due coordinate, il valore ottenuto raffigura la disparity tra                    punti omologhi:
                                                  disp = |xL - xR|
  </li>
  <li>ripetendo questi passaggi per distanze su un range da 20cm a 80cm , è stato poi overfittato generando il polinomio     
         specifico.
  </li>
</ul>
        
Cosi facendo è stato generato il valore  5253.
Questo ha permesso di riscrivere la form 1 (vista sopra) in questo modo:  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp;  

                                                   distance(P) =  5253 / disp.  
<br><br>
<img src="https://github.com/GiuseppeCannata/StereoVision/blob/master/imgs/Distanza.PNG" Hspace="240" Vspace="0">
</dd>
</dl>

Il software è stato scritto interamente in linguaggio python
</p>
<br>
<h4> 2. Istallazione software </h4>
<p>
Per poter utilizzare l'applicativo è necessario scaricare la cartella Ranspberry e avviare il file Ranspberry/Misuratore/Main.py.
<br><br>
<b>Attenzione!</b>
<br><br>
L'applicativo richiama le matrici di calibrazione e rettificazione della StereoCamera connessa alla raspberry.
<br>
Nella cartella qui pushata ci sono i file .npy relativi alla <b>StereoCamera da me utilizzata</b>.
<br>
<i>(Possiamo trovarli rispettivamente nella cartella Ranspberry/ResultCalib  e Ranspberry/ResultRect)</i>
<br><br>
Per cui per poter utilizzare il software con una StereoCamera differente è bene generare le matrici di calibrazione e rettificazione ad hoc.
<br>
Per poterlo fare è possibile utilizzare i tools <i>Ottieni_matrici_calibrazione.py</i> e <i>Ottieni_matrici_rettificazione.py</i>, e seguire le varie istruzioni presentate nella parte GESTIONE.
</p>
<br>
<h4> 3. Documentazione </h4>
<ol>
  <li><a href="https://github.com/GiuseppeCannata/StereoVision/blob/master/Documentazione/Report%20finale.pdf">Relazione</a> </li>
</ol>

