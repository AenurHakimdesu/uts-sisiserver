# Anggota Kelompok

Masahiro Benz Soeryo (A11.2022.14628)

Hikmal Rifqi Perdana (A11.2022.14630)

Aenur Hakim Maulia (A11.2022.14639)

# Manajemen Inventaris

Proyek ini merupakan aplikasi manajemen inventaris yang bertujuan untuk memudahkan pengelolaan stok, pemantauan persediaan, serta memberikan akses informasi inventaris secara real-time. Aplikasi ini dibangun dengan menggunakan Framework Django, PostgreSQL, dan Docker untuk mempermudah penyebaran dan pengelolaan layanan yang terintegrasi.

# Fitur

1. Dashboard Ringkasan Sistem (Kategori, Item, Suppliers, Laporan stok minimal)
2. Manajemen Kategori (Create, Read) 
3. Manajemen Item (Create, Read)
4. Manajemen Suppliers (Create, Read)

# Teknologi

1. Django
2. PostgreSQL
3. HTML dan Bootstrap CSS
4. Docker

# Cara Menjalankan Proyek

1. Pastikan Anda memiliki Docker Desktop yang sudah terinstal di komputer Anda dan juga instal ekstensi Docker dan PostgreSQL di VSC Anda.

2. Clone Repository ini

3. Hapus Folder postgres_data

4. Jalankan perintah berikut untuk membangun dan menjalankan kontainer. Sesuaikan dengan port Anda yang masih kosong (ubah bagian kiri port, misalnya 8000:8000 menjadi 8001:8000): <pre>docker compose up -d --build</pre>

5. Pada ekstensi PostgreSQL di VSC Anda, Anda dapat membuat koneksi database yang digunakan sesuai dengan informasi database yang berada pada docker-compose.yml seperti Username, Nama Database, Port Database, dan Password.

6. Masuk ke shell menggunakan ekstensi Docker pada VSC dengan klik kanan pada bagian container uts_server_django_final-web kemudian klik attach shell.

7. Jalankan perintah berikut untuk melakukan migrasi:
   <pre>python manage.py makemigrations</pre> 
   <pre>python manage.py migrate</pre>

9. Kemudian, jalankan perintah berikut untuk melakukan import database csv ke database PostgreSQL:
    <pre>python importer.py</pre>

5. Mulai ulang container docker dengan menjalankan perintah berikut:
   <pre>docker-compose restart</pre>

7. Akses Aplikasi

   - Untuk mengakses dashboard, Anda dapat mengunjungi http://localhost:8000 (Tergantung port yang diatur) dengan cara klik kanan pada container uts_server_django-web dan klik open in browser.
   - Untuk dapat menambahkan kategori, item, dan suppliers Anda harus masuk ke halaman Admin dan melakukan login.

7. Masuk ke halaman Admin
   
   - Klik Login pada menu navbar
   - Login menggunakan akun Admin yang tersedia di table auth_user ataupun di Admins.csv
   - Setelah login Anda bisa klik pada view site untuk beralih ke halaman dashboard.
   - Sekarang Anda dapat menambahkan item, kategori, dan juga supplier.
