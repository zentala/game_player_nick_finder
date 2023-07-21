
Bedziemy pisac apliakcje webowa oparta o django i sqllite.  Apliakcja nazywa sie Player Finder i sluzy do znajdowania starych znajomych z gier. 

(jako user - gosc) wchodze na storne aplikacji i widze pole tekstowe, w ktorym wpisuje w formularzu nicki starych znajomych z gier. (moge je sobie wyszukac, 1 albo wiecej na raz), 

po wyszukaniu pojawia mi sie strona z wynikiem wyszukiwania ktora tez zacheca do rejesteacji. wynik wyszukiwania to moze byc zero (nicki tych graczy nie zostaly znalezione ale zarejestruj sie aby oni mogli Ciebie znalexc) albo wiecej (znaleziono gracza X albo X graczy odpowiadajacym wyszikiwaniu; zarejestruj sie aby uzyskac ich dane kontaktowe). 

podczas rejestracji user zostawia swoj nick (to bedzie unikalna wartosc, login do konta), imie, naziwsko, email, facebook, twicha.

dalej podczas rejestracji definiuje sobie postacie pod jakimi gralem. postacie moga miec nicki ktorych nazwy nie sa unikalne. postac ma nick, orietacyjny zakres dat kiedy gralem (mozna wybrac zakres), opis postaci (np palladyn level 60), nazwa gry oraz widocznosc moich danych (switch: dane kontaktowe widoczne albo ukryte)

chce z Toba przedyskutowac model bazy danych (strukture, table). mysle aby zrobic tak ze mamy jedna tablę z nazwami gier, jedna z postaciami (id to uuid), jedna z uzytkownikami. 

to znaczy na pewno chce aby mozna bylo zawezac tak ze wyszukuje sie w konkretne grze dany nick i chce aby tworzac postac pojawiala sie lista dostepnych gier, a jesli nie ma taga gry to tworzy sie nowy. 

dodatkowo chce aby byla funkcjonalnosc notyfikacji email oraz wiadomosci. uzytkownicy moga wysylac wiadomosci do innych uzytkownikow. czyli jak znalazlem jakas postac starego znajomego, to moge wyslac do uzytkowniaka ktory posiada te postac wiadomosc. i jesli to zrobie to do uzytkowaniaka ktory otrzymal wiuadomosc zostanie wyslana notyfikacja email - powiadomienie o wiadomosci od nowego uzytkownika. tylko pierwza wiadomosc jak nowa osoba sie ze mna skontaktuje. 

zaproponuj mi szczegolnowa stutkroe bazy danych i endpointow do tej apliackji

poprawki bazy danych: 
* users tez na UUID a nie number
* gra jeszcze dodatkowo dobrze aby miala ikone, aby bylo pole na nia

poprawki do endpointow:
* search - bbedzie mial parametry: nick, data (konkrtna data ktora musi sie miescic w przedziale), gra, przy czym tyllko nick jest obowiazkowy, pozostale sa opcjonalne. dodatkowo nick zawsze przychodzi jako tablica ktora moze zawierac 1 lub wiecej nickow. tak ze moge wyszukiac np 5 znajomnych z danej gry ktory danego dnia za mna grali w gre. search results powinien miec paginacje. domyslnie 20 wynikow na strone. ustawienia mozna bedzie zmienic w configu aplikcacji. co do zwracajnych danych to rejestracja bedzie zawsze obowiazkowa, zle mnie zrozumiales. po prostu raz bede zachecal do rejestacji aby skontaktowac sie ze znaleziomym graczem, a raz by oinni jego starzy znajomi mogli sie skontaktowac z uzytkoniwkiem kiedy oni trafia na te strone. wiec registration required jest nie potrzebne. jesli chodzi o found players to chce aby zwracalo array z postacmi. z zaloznia niezalogowanym userom bedziemy pokazywac tylko ilosc znalezionych osob i zachecac do resjestacji aby sie skontaktowac. natomiast zalogowanym wyslemy cala liste postaci.
* uzytkownik przy tworzseniu potrzebuje jeszcze pola z haslem
* postacie przeciez mialy miec UUID jaki inentyfiaktor a nie integer

