# smieci

## setup projektu
```
npm install
```

### tryb developerski (tego używamy przy tworzeniu)
```
npm run serve
```

### build (to będzie stało na serwerze)
```
npm run build
```

# Dokumentacja

## Frontend

### Wprowadzenie

Frontend naszej aplikacji został w pełni zrealizowany przy użyciu reaktywnego frameworku do JavaScripta - Vue.js. To zaawansowane narzędzie umożliwia tworzenie dynamicznych i interaktywnych interfejsów użytkownika. Nasza strona internetowa jest zoptymalizowana jako interfejs do obsługi naszego REST API, co pozwala na efektywną komunikację z serwerem.

### Struktura Projektu

Projekt jest podzielony na komponenty, które reprezentują logicznie wydzielone podstrony. Dostęp do poszczególnych komponentów uzyskuje się poprzez wykorzystanie drzewa linków dostarczanego przez Vue Router.

Każdy komponent składa się z trzech głównych części:

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