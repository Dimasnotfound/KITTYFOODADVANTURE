
# Kitty's Food Adventure

Kitty's Food Adventure adalah game berbasis Python yang mengimplementasikan algoritma Knapsack Problem dalam mekanisme permainannya. Dalam game ini, pemain mengendalikan seekor kucing yang harus menemukan kombinasi makanan yang tepat untuk mencapai nilai "fullness" maksimal dengan batasan berat tertentu.

## Fitur Utama
- **Algoritma Knapsack**: Menggunakan algoritma knapsack untuk menentukan kombinasi makanan terbaik berdasarkan nilai kenyang dan berat.
- **Gameplay Dinamis**: Pemain menggerakkan kucing untuk mengambil makanan yang tersebar di berbagai area sambil menghindari area terlarang.
- **Level yang Menantang**: Setiap level memiliki batasan berat dan tantangan tersendiri. Jika kombinasi makanan yang dipilih sesuai dengan solusi algoritma, pemain naik level; jika tidak, pemain kehilangan kesempatan.
- **Antarmuka Grafis**: Menggunakan pygame-ce dan pygame_gui untuk tampilan grafis dan UI yang menarik.
- **Leaderboard**: Skor tertinggi disimpan dalam file CSV, sehingga pemain dapat melihat peringkat terbaik.

## Persyaratan
Pastikan sistem Anda telah menginstal:
- Python 3.x
- pygame-ce
- pygame_gui
- pandas

## Instalasi

### Clone Repository
Clone repository ini ke komputer Anda:

```bash
git clone https://github.com/username/kitty-food-adventure.git
```

### Pindah ke Direktori Proyek

```bash
cd kitty-food-adventure
```

### Instal Dependensi
Instal modul yang dibutuhkan dengan perintah:

```bash
pip install pygame-ce pygame_gui pandas
```

## Struktur Proyek

```plaintext
kitty-food-adventure/
├── main.py
├── data/
│   └── data_user.csv
├── audio/
│   ├── background_music.mp3
│   ├── button_sound.wav
│   ├── failure.wav
│   ├── levelup.mp3
│   └── catsound/
├── food/
│   └── (gambar makanan)
├── img/
│   ├── bg_game.png
│   ├── background.png
│   ├── background1.png
│   ├── logo.png
│   ├── start_button.png
│   ├── exit_button.png
│   ├── leaderboard_button.png
│   ├── table_background1.png
│   └── character/
│       ├── walking/
│       └── sitting_down/
└── font/
    └── StardewValley.otf
```

## Cara Bermain

### Memulai Game:
Jalankan file `main.py` dengan perintah:

```bash
python main.py
```

### Input Nama:
Masukkan nama pemain pada menu awal.

### Kontrol Karakter:
Gunakan tombol panah (↑, ↓, ←, →) untuk menggerakkan kucing.

### Mengambil Makanan:
Kucing akan mengambil makanan saat bersentuhan dengan objek makanan, dengan batasan berat sesuai level.

### Memasuki Chamber:
Saat kucing berada di area chamber, tekan tombol SPACE untuk memeriksa kombinasi makanan yang telah dipilih. Jika kombinasi sesuai dengan solusi algoritma knapsack, pemain naik level; jika tidak, kesempatan akan berkurang.

### Game Over & Leaderboard:
Game berakhir ketika kesempatan habis atau semua level telah diselesaikan. Skor akhir akan disimpan dan dapat dilihat pada menu leaderboard.

## Catatan
- Pastikan seluruh folder (audio, img, font, food, data) tersedia di direktori proyek agar game berjalan dengan lancar.
- Jika terjadi error terkait pygame-ce atau pygame_gui, periksa urutan import di file `main.py` dan pastikan versi modul yang digunakan kompatibel.

## Kontribusi
Kontribusi sangat diterima! Jika Anda menemukan bug atau memiliki saran perbaikan, silakan buka issue atau kirim pull request di repository ini.

## Lisensi
Project ini dilisensikan di bawah MIT License.
