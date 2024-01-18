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

## Dokumentacja

### Frontend i Vue.js

Frontend jest w całości wykonany w reaktywnym frameworku do JavaScripta - Vue.js. Strona jest napisana jako interfejs do obsługi naszego REST API. Została podzielona na komponenty - logicznie wydzielone podstrony, do których dostęp uzyskuje się poprzez drzewo linków Vue Router.

Każdy z komponentów zawiera część ze strukturą w HTML, skryptem w JavaScripct Vue.js i kaskadowym arkuszem stylów SCSS.

Projekt jest podzielony na foldery z różnymi plikami - najważniejszy jest /src. Są w nim assety, komponenty, czcionki, style i drzewo Vue ROutera.

Całość powstała w Vue.js 3.3.12 i juest swtorzona tak, żeby w przyszłości była możliwa łatwa rozbudowa.