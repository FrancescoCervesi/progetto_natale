import random


class Giocatore:
    def __init__(self, nome="Eroe"):
        self.nome = nome
        self.salute = 100
        self.attacco = 20
        self.difesa = 5
        self.livello = 1
        self.esperienza = 0
        self.oggetti = []
        self.salute_massima = 100

    def subire_danno(self, danno):
        danno_reale = max(0, danno - self.difesa)
        self.salute -= danno_reale
        print(f"{self.nome} subisce {danno_reale} danni! Salute rimanente: {self.salute}")
        if self.salute <= 0:
            print(f"{self.nome} è morto!")
            return True
        return False

    def attaccare_nemico(self, nemico):
        danno = self.attacco
        print(f"{self.nome} attacca {nemico.nome} per {danno} danni!")
        if nemico.subire_danno(danno):
            self.guadagnare_esperienza(10)
            return True
        return False

    def guadagnare_esperienza(self, quantita):
        self.esperienza += quantita
        print(f"{self.nome} guadagna {quantita} esperienza!")
        if self.esperienza >= 100:
            self.salire_livello()

    def salire_livello(self):
        print(f"{self.nome} è salito al livello {self.livello + 1}!")
        self.livello += 1
        self.attacco += 5
        self.difesa += 2
        self.salute_massima += 10
        self.salute = self.salute_massima 
        print(f"Statistiche dopo il livello-up:\nAttacco: {self.attacco}\nDifesa: {self.difesa}\nSalute: {self.salute}")

        
        self.scelta_abilita()

    def scelta_abilita(self):
        print("Scegli un'abilità da migliorare:")
        print("1: Attacco")
        print("2: Difesa")
        print("3: Salute")
        scelta = input("Scegli l'abilità da migliorare (1/2/3): ")

        if scelta == '1':
            self.attacco += 5
            print(f"{self.nome} ha migliorato l'attacco! Nuovo attacco: {self.attacco}")
        elif scelta == '2':
            self.difesa += 2
            print(f"{self.nome} ha migliorato la difesa! Nuova difesa: {self.difesa}")
        elif scelta == '3':
            self.salute_massima += 10
            self.salute = self.salute_massima 
            print(f"{self.nome} ha migliorato la salute! Nuova salute: {self.salute}")
        else:
            print("Scelta non valida, nessuna abilità migliorata.")

    def guarire(self, oggetto):
        self.salute = min(self.salute_massima, self.salute + oggetto.ammontare_guarigione)
        print(f"{self.nome} usa {oggetto.nome} e guadagna {oggetto.ammontare_guarigione} salute. Salute totale: {self.salute}")

    def aggiungi_oggetto(self, oggetto):
        self.oggetti.append(oggetto)
        print(f"{self.nome} ha raccolto {oggetto.nome}!")

    def mostra_inventario(self):
        print(f"Inventario di {self.nome}:")
        for oggetto in self.oggetti:
            print(f"- {oggetto.nome}")



class Nemico:
    def __init__(self, nome, salute, attacco, difesa):
        self.nome = nome
        self.salute = salute
        self.attacco = attacco
        self.difesa = difesa

    def subire_danno(self, danno):
        danno_reale = max(0, danno - self.difesa)
        self.salute -= danno_reale
        print(f"{self.nome} subisce {danno_reale} danni! Salute rimanente: {self.salute}")
        if self.salute <= 0:
            print(f"{self.nome} è stato sconfitto!")
            return True
        return False

    def attaccare_giocatore(self, giocatore):
        danno = self.attacco
        print(f"{self.nome} attacca {giocatore.nome} per {danno} danni!")
        if giocatore.subire_danno(danno):
            return True
        return False



class Oggetto:
    def __init__(self, nome, ammontare_guarigione=0):
        self.nome = nome
        self.ammontare_guarigione = ammontare_guarigione



class Gioco:
    def __init__(self):
        self.giocatore = Giocatore()
        self.nemico = None
        self.fine_gioco = False
        self.oggetti = [Oggetto("Pozione", 30), Oggetto("Scudo", 0)] 

    def generare_nemico(self):
        
        livello = self.giocatore.livello
        nome = f"Nemico {livello}"
        salute = random.randint(30, 50) + livello * 10
        attacco = random.randint(10, 20) + livello * 2
        difesa = random.randint(5, 10) + livello
        self.nemico = Nemico(nome, salute, attacco, difesa)
        print(f"Un nuovo nemico è apparso: {self.nemico.nome}")

    def battaglia(self):
        while not self.fine_gioco:
            print(f"\n{self.giocatore.nome} VS {self.nemico.nome}")
            print(f"Salute del giocatore: {self.giocatore.salute} | Salute del nemico: {self.nemico.salute}")

            
            print("\nScegli un'azione:")
            print("1: Attacca")
            print("2: Difendi")
            print("3: Usa un oggetto")
            print("4: Scappa")
            scelta = input("Scelta: ")

            if scelta == '1':
                if self.giocatore.attaccare_nemico(self.nemico):
                    print(f"{self.giocatore.nome} ha vinto la battaglia!")
                    break
            elif scelta == '2':
                print(f"{self.giocatore.nome} si difende!")
                self.giocatore.difesa += 5  
                if self.nemico.attaccare_giocatore(self.giocatore):
                    print(f"{self.nemico.nome} ha vinto la battaglia!")
                    break
                self.giocatore.difesa -= 5  
            elif scelta == '3':
                self.usa_oggetto()
            elif scelta == '4':
                print(f"{self.giocatore.nome} tenta di scappare dalla battaglia!")
                if random.choice([True, False]):
                    print(f"{self.giocatore.nome} è riuscito a scappare!")
                    break
                else:
                    print(f"{self.giocatore.nome} non riesce a scappare!")
            else:
                print("Scelta non valida.")

            if self.nemico.attaccare_giocatore(self.giocatore):
                print(f"{self.nemico.nome} ha vinto la battaglia!")
                break

    def usa_oggetto(self):
        if len(self.giocatore.oggetti) == 0:
            print("Non hai oggetti nel tuo inventario!")
            return

        print("Oggetti nel tuo inventario:")
        for idx, oggetto in enumerate(self.giocatore.oggetti, 1):
            print(f"{idx}: {oggetto.nome}")

        scelta = int(input("Scegli un oggetto da usare: "))
        if 1 <= scelta <= len(self.giocatore.oggetti):
            oggetto = self.giocatore.oggetti[scelta - 1]
            self.giocatore.guarire(oggetto)
            self.giocatore.oggetti.remove(oggetto)
        else:
            print("Scelta non valida.")

    def inizia(self):
        print("Benvenuto in Battaglia Eterna!")
        while not self.fine_gioco:
            self.generare_nemico()
            self.battaglia()


if __name__ == "__main__":
    gioco = Gioco()
    gioco.inizia()