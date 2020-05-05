<h2>TorGen</h2>
 Improvvisamente ti senti Dora l'esploratrice e vuoi navigare negli abissi?
 TorGen fa a caso tuo. 
 Genera URL .onion e li testa restituendo un codice di risposta.
 I link generati vengono salvati nel file "links/links.txt",
 i link generati e funzionanti li trovi in "links/working_links.txt".

<h2>Uso</h2>
 Avvia TorGen con
 <h6>python torgen.py -g [NUM] [-t, --test] [-f [FILE]]</h6>
 Genera i link con l'argomento '-g':
 <h6>-g [NUM]</h6>
 Usa '-t' o '--test' per testare i link:
 <h6>-t, --test</h6>
 Puoi anche dare un file in input per testare i link:
 <h6>-f [FILE]</h6>
 <br>
 Testato su Ubuntu 18.04.

<h2>Changelog</h2><br>
*v1.1<br>
    * Corretto un problema per la quale i link non venivano testati<br>
    * Aggiunto comando '-f [FILE]'<br>
    * Interfaccia migliorata<br>
*v1.0<br>
    * Release iniziale<br>

