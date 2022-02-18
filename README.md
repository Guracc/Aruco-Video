# Seagull AR

### OBIETTIVO E APPLICAZIONE:

    - L’obiettivo e applicazione del progetto nella vita quotidiana:
    - Il nostro progetto prevede la sistemazione di aruco marker in luoghi come musei, acquari, e così via, con uno scopo educativo, per mostrare immagini o video supplementari alle     descrizioni già presenti.
    - Noi in particolare abbiamo simulato l'implementazione di tutto questo in un acquario.


### MODIFICHE FATTE AL CODICE:

    - Contatore di FPS (con colore variabile)
    - Input video via webcam in real time
    - Ridimensionamento immagine direttamente proporzionale alla distanza
    - Caching per stabilizzazione output video
    - Immagini variabili in base all’ID Aruco
    - Utilizzo di un singolo Aruco marker come sorgente

   
 ### DIFFICOLTÀ E OSTACOLI

    - Abbiamo provato a implementare il multithreading per il codice però è risultato particolarmente complesso e sarebbe servito più tempo per svilupparlo
    - L’idea alla base sarebbe stata quella di rendere compatibile il programma con i dispositivi mobile, ovviamente il tempo e le nostre conoscenze non sono bastate per raggiungere questo obiettivo
    - Difficoltà all’approccio con la libreria cv2
    - Difficoltà di risorse (fps troppo bassi senza multithread)

![This is an image](https://drive.google.com/file/d/1VfAuxH26U5YRXMvLBfcXsjBT1Rrch90f/preview)
    
### Link per la presentazione progetto:
#### https://docs.google.com/presentation/d/1rHU3AESDdcaIuzwY0FAkXYkTqgOhvyEIYkXv9lDDB1s/edit?usp=sharing
