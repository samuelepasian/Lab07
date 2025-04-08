from database.meteo_dao import MeteoDao
from model.situazione import Situazione
import copy


class Model:
    def __init__(self):
        self.lista_sequenze=[]

    def get_allSituazioni(self):
        return MeteoDao.get_all_situazioni()

    def filtra_mese(self, mese):
        lista_filtrata=[]
        situazioni=self.get_allSituazioni()
        for i in situazioni:
            if i.data.month==mese and i.data.day<16:
                lista_filtrata.append(i)
        return lista_filtrata

    def filtra_giorno(self,parziale, situazioni):
        giorno=len(parziale)+1
        lista_filtrate=[]
        for i in situazioni:
            if i.data.day==giorno:
                lista_filtrate.append(i)
        return lista_filtrate

    def accettabile(self, candidato, parziale):
        accettabile=True
        count=0
        for i in parziale:
            if candidato.localita==i.localita:
                count=count+1
        if count>5:
            accettabile=False

        if (len(parziale)==1 or len(parziale)==2) and candidato.localita!=parziale[-1].localita:
            accettabile=False
        if len(parziale)>2:
            if (parziale[-3].localita==parziale[-2].localita and parziale[-2].localita!=parziale[-1].localita
                    and candidato.localita!=parziale[-1].localita):
                accettabile=False
            if (parziale[-3].localita!=parziale[-2].localita and parziale[-2].localita==parziale[-1].localita
                    and candidato.localita!=parziale[-1].localita):
                accettabile=False
        return accettabile

    def get_sequenza(self,parziale,rimanenti):
        #RICORDA!!! come rimanenti devi mettere filtra_mese(mese)
        if len(parziale)==15:
            self.lista_sequenze.append(copy.deepcopy(parziale))
        else:
            candidati=self.filtra_giorno(parziale, rimanenti)
            for i in candidati:
                if self.accettabile(i,parziale):
                    parziale.append(i)
                    self.get_sequenza(parziale,rimanenti)
                    parziale.pop()

    def calcola_sequenza(self, mese):
        lista=self.filtra_mese(mese)
        self.get_sequenza([],lista)
        i=1
        costo=self.calcola_costo(self.lista_sequenze[0])
        sequenza=self.lista_sequenze[0]
        while i<len(self.lista_sequenze):
            if self.calcola_costo(self.lista_sequenze[i])<costo:
                costo=self.calcola_costo(self.lista_sequenze[i])
                sequenza=self.lista_sequenze[i]
            i=i+1
        stringa=f"La sequenza ottima ha costo: {costo}\n"
        for i in sequenza:
            stringa=stringa+f"{i}\n"
        return stringa

    def calcola_costo(self, lista):
        costo=0
        i=0
        while i<len(lista):
            costo=costo+lista[i].umidita
            if i>0 and lista[i].localita!=lista[i-1].localita:
                costo=costo+100
            i=i+1
        return costo
if __name__==("__main__"):
  print(Model().calcola_sequenza(2))