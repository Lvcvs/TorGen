<h2>TorGen</h2>
 Improvvisamente ti senti Dora l'esploratrice e vuoi navigare negli abissi? Ecco a te la soluzione. <br>
 TorGen genera URL .onion e li testa automaticamente.<br>
 I link generati vengono salvati nel file "links/links_[id].txt", i link generati e attivi li puoi trovare in "links/working_links_[id].txt".
 <br>
 Testato su Ubuntu 18.04.

<h2>Uso</h2>
 Avvia TorGen con
 <h6>python3 torgen.py [NUM]</h6><br>
 Puoi dare un file in input a TorGen per testare i link:
 <h6>--file [FILE]</h6><br>
 Puoi verificare se [URL.onion] esiste con '--check':
 <h6>--check [URL]</h6>


<h2>Changelog</h2>
v1.1<br>
    - Corretto un problema per la quale i link non venivano testati<br>
    - Aggiunto comando '-f [FILE]'<br>
    - Interfaccia migliorata<br>
v1.0<br>
    - Release iniziale<br>


