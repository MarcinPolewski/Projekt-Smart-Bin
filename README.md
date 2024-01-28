# Śmieci

## Setup projektu
```
npm install
```

### Tryb developerski (tego używamy przy tworzeniu)
```
npm run serve
```

### Build (to będzie stało na serwerze)
```
npm run build
```

# Dokumentacja

## Frontend

### Wprowadzenie

Frontend naszej aplikacji został w pełni zrealizowany przy użyciu reaktywnego frameworku do JavaScripta - Vue.js. To zaawansowane narzędzie umożliwia tworzenie dynamicznych i interaktywnych interfejsów użytkownika. Nasza strona internetowa jest zoptymalizowana jako interfejs do obsługi naszego REST API, co pozwala na efektywną komunikację z serwerem. Strona jest responsywna - dostosowuje się zarówno do wielkości monitora komputera, jak i ekranu telefonu.

### Struktura Projektu

Projekt jest podzielony na widoki, które reprezentują logicznie wydzielone podstrony. Dostęp do poszczególnych widoków uzyskuje się poprzez wykorzystanie drzewa linków dostarczanego przez Vue Router.

Każdy komponent (widok) składa się z trzech głównych części:

    HTML: Definiuje strukturę i układ elementów na stronie.
    JavaScript (Vue.js): Odpowiada za logikę komponentu, interakcję z danymi i dynamiczną aktualizację interfejsu.
    SCSS (kaskadowy arkusz stylów): Zawiera style, które definiują wygląd i układ komponentu.

### Struktura Plików

Najważniejszy folder zawierający frontend to /src. Zawiera on kluczowe elementy, takie jak:

    Assety: Zasoby, takie jak obrazy, ikony, itp.
    Komponenty: Moduły Vue.js, reprezentujące poszczególne części strony.
    Czcionki: Folder zawierający używane czcionki.
    Style: Arkusze stylów w formie plików SCSS.
    Vue Router: Struktura drzewa linków do nawigacji między komponentami.

### Wersja Vue.js

Frontend został zbudowany przy użyciu Vue.js w wersji 3.3.12. Wykorzystanie najnowszej wersji frameworku pozwala na korzystanie z najnowszych funkcji.

### Rozbudowa Projektu

Całość została stworzona z myślą o łatwej rozbudowie w przyszłości. Modułowa struktura projektu i zastosowanie Vue.js jako frameworka reaktywnego ułatwiają dodawanie nowych funkcji i komponentów.

## Backend

### Wprowadzenie
Backend został zrobiony w django rest framework. Pozwala nam na komunikację pomiędzy bazą danych, płytką i stroną. Udostępnia dane w formacie JSON.

### Struktura Plików
Najważniejsze pliki w projekcie to
models.py - plik w którym znajdują się klasy odpowiadające tabelom z bazy danych.
serializers.py - plik w którym znajdują się serializatory danych z modeli
views.py - plik w którym wykorzystywane są modele i serializatory do obsługi zapytań do api i logiki

### Funkcjonalność
Backend, oprócz swojej bazowej funkcjonalności pozwala też na wysyłanie maili użytkownikom po każdym wyniesieniu kosza. Dodaje też akutalne daty do tabel w bazie danych, żeby zminimalizować ilość zadań jakie musi wykonywać płytka. Można z nim "rozmawiać" poprzez klasyczne pythonowe requesty, ale też przeglądać dane po wpisaniu {url strony}:8001 w przeglądarke.

## Serwer HTTPS na Linux Mint z Nginx (Vue) i Daphne (Django)
### Opis Projektu

Projekt obejmuje implementację serwera HTTPS na systemie Linux Mint, z dwiema głównymi częściami: front-end obsługiwany przez Nginx z frameworkiem Vue, oraz back-end obsługiwany przez Daphne z frameworkiem Django.
### Komponenty Projektu
1. Front-end (Nginx + Vue)

    Nginx: Jeden z najpopularniejszych serwerów HTTP, pełniący rolę reverse proxy. Zainstalowany na systemie Linux Mint, konfigurowany jako interfejs pomiędzy zewnętrznymi zapytaniami HTTP a serwerem Vue.

    Vue: Framework JavaScript do budowania interfejsów użytkownika. Działa na porcie 8000 i jest odpowiedzialny za obsługę warstwy front-end.

2. Back-end (Daphne + Django)

    Daphne: Serwer HTTP dla aplikacji Django. Uruchamia się na porcie socketa, obsługując zapytania asynchronicznie.

    Django: Framework webowy oparty na języku Python. Obsługuje zapytania od Daphne, stanowiąc warstwę back-end projektu.

## Implementacja HTTPS na Linux Mint
1. Nginx (Vue)

    Instalacja Nginx na Linux Mint: Nginx został zainstalowany na systemie Linux Mint przy użyciu menedżera pakietów. Konfiguracja Nginx obejmuje obsługę ruchu na porcie 8001 oraz przekierowanie na aplikację Vue.

    Konfiguracja Nginx z SSL: Certyfikat SSL uzyskano za pomocą Certbota, umożliwiając obsługę zabezpieczonego połączenia HTTPS na Linux Mint.

2. Daphne (Django)

    Instalacja Daphne na Linux Mint: Daphne został zainstalowany jako serwer HTTP do obsługi aplikacji Django na systemie Linux Mint.

    Konfiguracja Daphne: Skonfigurowano Daphne do obsługi aplikacji Django, a Nginx został skonfigurowany jako reverse proxy, przekierowując zapytania na port socketa obsługiwanego przez Daphne.

## Struktura Projektu

Struktura projektu jest zorganizowana w sposób umożliwiający łatwe zarządzanie i utrzymanie zarówno front-endu, jak i back-endu. Każda z części (Vue i Django) jest odseparowana, co ułatwia rozwijanie i skalowanie projektu.
## Monitorowanie i Testowanie

Po skonfigurowaniu HTTPS, należy regularnie monitorować dostępność obu części projektu. Testowanie powinno obejmować zarówno część front-end, jak i back-end, aby upewnić się, że obie funkcje są dostępne i działają zgodnie z oczekiwaniami.
## Zakończenie

Dokumentacja informacyjna zawiera podstawowe informacje dotyczące projektu, opisując główne komponenty, sposób implementacji HTTPS na systemie Linux Mint, oraz strukturę projektu. Dla dokładnych instrukcji dotyczących instalacji i konfiguracji, proszę skonsultować się z dokumentacją instruktażową projektu.