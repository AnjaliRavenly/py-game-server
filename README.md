# MyGame - serwer gry

Prosty server do gry pozwalający się użytkownikowy zarejestrować,
stworzyć własną postać oraz sprawdzić się w rankingu.

## Jak rozpocząć?

Sprawdź czy masz zainstalowane wszystkie potrzebne narzędzia wymienione w wymaganiach wstępnych, następnie postępuj zgodnie z instrukcją instalacji.

### Wymagania wstępne

| silniki / kompilatory  | wersja    |
| :--------------------- | --------: |
| python                 | ^3.6      |
| mysql / MariaDB        | ^5.6 / 10 |

| wtyczki do pythona     | wersja   |
| :--------------------- | -------: |
| flask                  | ^1.0.2   |
| mysql-connector        | ^8.0.11  |
 
#### Co jak nie mam pythona, mysql?
Linki do instalatorów są [niżej](#links), do pracy z bazą polecam Xamppa.

### Instalacja

Jak już mamy dostęp do bazy i do pythona z linii komend, możemy wziąść się za import niezbędnych danych. W tym celu przechodzimy do folderu [`migrations`](/migrations)

```cmd
cd migrations
```

Tutaj znajdują się pliki `.sql` które należy albo zaimportować do bazy. Pierwszy używająć komendy

```cmd
mysql -u root -p < 000_create_database.sql
```

i potwierdzić za pomocą klawisza `ENTER`.

Kolejne w kolejności rosnącej:

```cmd
mysql -u root -D mygame -p < NAZWA_PLIKU.sql
```
i również potwierdzić za pomocą klawisza `ENTER`.

Na koniec wracamy poziom wyżej
```commandline
cd ..
```
i odpalamy serwer
```commandline
py hello.py
```

Dzięki temu serwer jest dostępny pod adresem `http://127.0.0.1:5000/` gdzie możemy się zalogować / zarejestrować i zacząć tworzyć swoje postacie.

## Deployment

Nie jest zalecane uruchamianie projektu w środowisku produkcjnym.

## Użyte programy <span id="links"></span>

* [PyCharm CE](https://www.jetbrains.com/pycharm/) - IDE do pracy w pythonie.
* [Xampp](https://www.apachefriends.org/pl/index.html) - środowisko do pracy na lokalnym serwerze
* [mysql](https://dev.mysql.com/downloads/connector/python/) - baza danych mysql
* [Python](https://www.python.org/downloads/) - no i sam python ;)

## Autorzy

* **Anna Rakotna** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details