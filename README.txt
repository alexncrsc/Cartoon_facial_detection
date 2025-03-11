Versiuni care trebuie incarcate pentru a rula programul

pip install numpy==1.19.5
pip install scikit-learn==0.24.1
pip install scikit-image==0.18.1
pip install matplotlib==3.3.4
pip install opencv-python==4.5.2

In arhiva se gasesc fisierul cu prezentarea codului, modelul antrenat best_svm.sav, notebook-ul cu codul intreg si README.

Trebuie rulate toate casutele cu functii, atunci cand se ajunge la casuta cu clasa Parameters trebuie schimbat path-ul
self.dir_test_examples cu path-ul unde sunt imaginile de test

Apoi se ruleaza casuta care calculeaza detectii, scoruri si file_names si cea care le salveaza, trebuie schimbat path-ul unde se salveaza. Casutele cu comentariul #NU SE RULEAZA LA TESTARE trebuie sa nu fie rulate.

Link-ul de baza pentru dataset:
https://www.dropbox.com/scl/fo/4mnzu3mfj14k6awwbm7kl/AGOMcb8o_F9MXH9G2zY3VBU?rlkey=v4ytfq006m381uri24izm07b6&e=1&st=wvfwsq9r&dl=0
