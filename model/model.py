from database.impianto_DAO import ImpiantoDAO
import copy

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

# funzione che prende gli impianti (presi tramite impianto_DAO) e li memorizza
    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

# funzione che restituisce la media dei consumi su un mese scelto dall'utente
    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # lista contenenti le tuple richieste (nome impianto, media)
        lista_tuple = []
        for impianto in self._impianti:
            # creo la lista di oggetti contenenti i consumi ricavati dal database
            consumi_impianto = impianto.get_consumi()
            totale_kwh_mese = 0
            giorni = 0

            for consumo in consumi_impianto:
                # controllo i vari consumi
                if consumo.data.month == mese:
                    totale_kwh_mese += consumo.kwh
                    giorni += 1

            if giorni > 0:
                media = totale_kwh_mese / giorni
                lista_tuple.append((impianto.nome, media))
        return lista_tuple


# funzione che restituisce la sequenza di dati richiesta
    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo


# funzione di RICORSIONE
    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # condizione di uscita
        if giorno == 8:
            if self.__costo_ottimo == -1 or costo_corrente <= self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = copy.deepcopy(sequenza_parziale)
                return
        # condizione di ricorsione
        else:
            # iterazione su entrambi gli impianti
            for impianto_selezionato in consumi_settimana.keys():
                # costo dei consumi
                costo_consumo = consumi_settimana[impianto_selezionato][giorno - 1]
                costo_spostamento = 0

                # considero il costo spostamento (definito nel problema)
                if ultimo_impianto is not None and ultimo_impianto != impianto_selezionato:
                    costo_spostamento = 5

                # definzione del nuovo costo
                nuovo_costo = costo_corrente + costo_consumo + costo_spostamento
                sequenza_parziale.append(impianto_selezionato)
                self.__ricorsione(sequenza_parziale, giorno + 1, impianto_selezionato, nuovo_costo, consumi_settimana)

                # backtracking
                sequenza_parziale.pop()



# funzione per i consumi della prima settimana del mese
    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        dizionario = dict()
        for impianto in self._impianti:
            # creo la lista di oggetti contenenti i consumi ricavati dal database
            consumi_impianto = impianto.get_consumi()
            costo_giornaliero = []
            # prendo i primi sette giorni
            for consumo in consumi_impianto:
                if consumo.data.month == mese and len(costo_giornaliero) < 7:
                    costo_giornaliero.append(consumo.kwh)
            dizionario[impianto.id] = costo_giornaliero
        return dizionario

