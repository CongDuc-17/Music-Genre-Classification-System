# Music Genre Classification - Django Web App

Ung dung Django dung model Keras de phan tich the loai nhac tu file audio. Du an nay duoc cau hinh de chay local bang Conda environment:

```text
D:\CondaEnvs\tensorflow_env
```

Khong dung lenh `python` mac dinh neu no tro toi `C:\msys64\ucrt64\bin\python.exe`, vi environment do khong co TensorFlow/librosa.

## Cau truc chinh

```text
project/
  manage.py
  config/                    # settings, urls, wsgi/asgi
  apps/
    dashboard/               # giao dien web Django templates
    classification/          # upload, luu audio, ket qua phan tich
    analytics/               # thong ke
    authentication/          # JWT API
  ai/
    preprocessing/           # librosa mel-spectrogram
    inference/               # load model va predict
  templates/
  static/
  media/                     # file audio upload local
  requirements.txt
  requirements-postgres.txt
  docker-compose.yml
```

Model va config mac dinh nam o thu muc goc repo:

```text
AI/third_genre_classification_model.h5
AI/preprocessing_config.json
```

## Kiem tra environment

Chay tu thu muc goc repo:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" --version
& "D:\CondaEnvs\tensorflow_env\python.exe" -c "import librosa, tensorflow as tf; print(librosa.__version__); print(tf.__version__)"
```

Ket qua mong doi:

```text
Python 3.10.x
librosa 0.10.1
tensorflow 2.10.0
```

## Cai dependencies

Neu env da co san thu vien thi co the bo qua. Neu can cai lai:

```powershell
cd "D:\University\Ki_2_25-26\LapTrinhPython\Music_Genre_Classification_System"
& "D:\CondaEnvs\tensorflow_env\python.exe" -m pip install -r project\requirements.txt
```

Neu dung PostgreSQL local/Docker qua `DATABASE_URL`, cai them:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" -m pip install -r project\requirements-postgres.txt
```

## Chay local bang SQLite

Day la cach don gian nhat. Database nam trong:

```text
project/db.sqlite3
```

Lenh chay:

```powershell
cd "D:\University\Ki_2_25-26\LapTrinhPython\Music_Genre_Classification_System\project"
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py migrate
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py createsuperuser
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py runserver 127.0.0.1:8000
```

Hoac dung script da tao o thu muc goc:

```powershell
cd "D:\University\Ki_2_25-26\LapTrinhPython\Music_Genre_Classification_System"
.\runserver_tensorflow_env.ps1
```

Mo ung dung:

```text
http://127.0.0.1:8000/
```

## Cac lenh quan trong

Chay server:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py runserver 127.0.0.1:8000
```

Migrate database:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py migrate
```

Tao admin:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py createsuperuser
```

Kiem tra loi cau hinh Django:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py check
```

Mo Django shell:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py shell
```

Xoa va tao lai SQLite database local:

```powershell
Remove-Item .\db.sqlite3
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py migrate
```

## Upload va phan tich audio

Dang nhap vao web, vao `Upload`, chon file `wav`, `mp3`, hoac `ogg`.

Luu y:

- File ngan hon 4 giay se duoc lap lai de du model input.
- MP3 tren Windows co the can FFmpeg trong PATH. Neu MP3 loi decode, thu file WAV truoc.
- File upload local duoc luu trong `project/media/audio/...`.

## Xem database bang DBeaver

### Truong hop 1: Dang dung SQLite local

Neu khong cau hinh `DATABASE_URL`, app dung SQLite:

```text
project/db.sqlite3
```

Trong DBeaver:

1. Chon `New Database Connection`.
2. Chon `SQLite`.
3. O `Database file`, chon file:

```text
D:\University\Ki_2_25-26\LapTrinhPython\Music_Genre_Classification_System\project\db.sqlite3
```

4. Bam `Finish`.

Bang quan trong:

- `classification_audiofile`: file audio da upload.
- `classification_classificationresult`: ket qua phan tich.
- `classification_genre`: danh sach genre.
- `analytics_useractivity`: log hanh dong nguoi dung.
- `auth_user`: user Django.

### Truong hop 2: Dung PostgreSQL bang Docker Compose

File `docker-compose.yml` tao Postgres voi thong tin:

```text
Host: localhost
Port: 5432
Database: genrelab
Username: genrelab
Password: genrelab
```

Hien tai compose chua expose port Postgres ra host. Neu muon DBeaver ket noi duoc, them `ports` vao service `db`:

```yaml
db:
  image: postgres:16-alpine
  ports:
    - "5432:5432"
  environment:
    POSTGRES_USER: genrelab
    POSTGRES_PASSWORD: genrelab
    POSTGRES_DB: genrelab
```

Sau do chay:

```powershell
cd "D:\University\Ki_2_25-26\LapTrinhPython\Music_Genre_Classification_System\project"
docker compose up -d db
```

Trong DBeaver:

1. Chon `New Database Connection`.
2. Chon `PostgreSQL`.
3. Nhap:

```text
Host: localhost
Port: 5432
Database: genrelab
Username: genrelab
Password: genrelab
```

4. Bam `Test Connection`, neu thieu driver thi cho DBeaver download.
5. Bam `Finish`.

## Chay bang Docker Desktop

Tu thu muc `project/`:

```powershell
cd "D:\University\Ki_2_25-26\LapTrinhPython\Music_Genre_Classification_System\project"
docker compose up --build
```

Docker compose se:

- Build web app.
- Chay PostgreSQL container.
- Mount model:
  - `../AI/third_genre_classification_model.h5`
  - `../AI/preprocessing_config.json`
- Chay migration luc container web khoi dong.

Mo web:

```text
http://127.0.0.1:8000/
```

Xem container trong Docker Desktop:

1. Mo Docker Desktop.
2. Vao tab `Containers`.
3. Tim project compose cua app.
4. Xem logs cua service `web` neu upload/predict loi.
5. Xem service `db` de kiem tra Postgres dang chay.

## API nhanh

Dang ky/dang nhap:

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
```

Phan tich va lich su:

```text
POST /api/classify/upload/
POST /api/classify/predict/
GET  /api/classify/history/?search=&genre=
DELETE /api/classify/history/<id>/
GET  /api/analytics/stats/
```

## Loi thuong gap

### Bao loi No module named 'librosa'

Server dang chay sai Python. Dung lenh nay:

```powershell
& "D:\CondaEnvs\tensorflow_env\python.exe" manage.py runserver 127.0.0.1:8000
```

Neu message hien `Current Python: C:\msys64\ucrt64\bin\python.exe`, hay tat server cu va chay lai bang `tensorflow_env`.

### Canh bao CUDA cua TensorFlow

Neu khong dung GPU, co the bo qua cac canh bao nhu:

```text
Could not load dynamic library 'cudart64_110.dll'
Skipping registering GPU devices...
```

TensorFlow se chay CPU.

### Audio sau phan tich khong phat

Kiem tra file co ton tai trong:

```text
project/media/audio/
```

Voi local dev, setting `SERVE_MEDIA_FILES=true` mac dinh se serve `/media/...`.
