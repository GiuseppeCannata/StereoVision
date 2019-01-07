# StereoVision

<p>
Progetto realizzato per il laboratorio di Meccatronica presso l'Università politecnica delle Marche 
corso di laurea Ing. Informatica e dell'Automazione.

Il prototipo del misuratore è stato costruito con una StereoCamera collegata tramite USB alla Raspberry Pi 3.
I due elementi sono poi stati fissati ad un supporto metallico per consentire una maggiore stabilità in fase di misurazione.

Per quanto riguarda il processo che ha portato allo sviluppo del software ci si è basati sui seguenti passaggi:

-CALIBRAZIONE
Le matrici ottenute non sono state confrontate con gli effettivi parametri della StereoCamera a causa di mancaza di Datasheets.
Per maggiore affidabilità dei risultati è stata quindi condatta una calibrazione anche con il toolboox di MatLab.

-RETTIFICAZIONE
Le immagini sono state in seguito rettificate affinchè punti omologhi potessero trovarsi sulla stessa line epipolare (linea in giallo in figura).
<br>
<img src="https://github.com/GiuseppeCannata/StereoVision/blob/master/imgs/Rettificazione_Imgs.PNG">

-DETECT DEL LASER
La ricerca del PUNTATORE laser avviene utilizzando lo spazio di colori RGB; In particolra il range di ricerca è tra il rosso puro e il bianco, quest'ultimo dovuto alla lucentezza del puntatore.
Per limitare disturbi derivanti dalla scena la ricerca è stata coinata in una ROI(Region of interest).
<br>
<img src="https://github.com/GiuseppeCannata/StereoVision/blob/master/imgs/ROI_Laser.PNG">
<br>
<br>
Il software è stato scritto interamente in linguaggio python
</p>

