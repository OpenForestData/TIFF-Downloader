# Tiff Downloader

## Struktura rozwiązania
Wykorzystane obrazy dockerowe:
- Traefik edge router ➤ traefik:v2.2
- tiff_iipimages (Ubuntu 18.04, obraz z IIPImageServer oraz OpenJPG) ➤ registry.gitlab.whiteaster.com/openforestdata/backend/iipimageserver-with-openjpg:master  
 (https://gitlab.whiteaster.com/openforestdata/backend/iipimageserver-with-openjpg )
- tiff_downloader (Python 3.8 Alpine) ➤ Budowanie lokalne rozwiązanie
  
Dostępne ścieżki (z założeniem, że zmienna URL to localhost):  
- https://localhost/fcgi-bin/iipsrv.fcgi ➤ IIPImageServer
- https://localhost/fcgi-bin/tiff? ➤ Tiff Downloader
  
Traefik został skonfigurowany aby domyślnie dostarczał certyfikat SSL Let's Encrypt wraz z automatycznym przkierowaniem na port 443.

## Deployment
### Wymagania
Do uruchomienia aplikacji wymagane jest posiadanie zainstalowanego rozwiążania Docker oraz Docker Compose.  
Instalacja Windows/macOS ➤ https://docs.docker.com/desktop/  
Instalacja GNU/Linux ➤ https://docs.docker.com/engine/install/  
Instalacja Docker Compose ➤ https://docs.docker.com/compose/  

### Uruchomienie rozwiązania (GNU/Linux, macOS)
Adres "localhost" należy zamienić w przypadku deployment na dowolny na którym aplikacja ma zostać wystawiona.

Należy przejść do folderu projektu apa-plot/deployment a następnie:

```
$ docker login registry.gitlab.whiteaster.com
$ URL="localhost" docker-compose pull
$ URL="localhost" docker-compose build
$ URL="localhost" docker-compose up -d
```

### Uruchomienie rozwiązania (Windows)
Adres "localhost" należy zamienić w przypadku deployment na dowolny na którym aplikacja ma zostać wystawiona.

Należy przejść do folderu projektu apa-plot/deployment a następnie:

```
$ docker login registry.gitlab.whiteaster.com
$ $env:URL="localhost"; docker-compose pull
$ $env:URL="localhost"; docker-compose build
$ $env:URL="localhost"; docker-compose up -d
```