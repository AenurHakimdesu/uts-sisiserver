# Anggota Kelompok

Masahiro Benz Soeryo (A11.2022.14628)

Hikmal Rifqi Perdana (A11.2022.14630)

Aenur Hakim Maulia (A11.2022.14639)

# Manajemen Inventaris

Proyek ini merupakan aplikasi manajemen inventaris yang bertujuan untuk memudahkan pengelolaan stok, pemantauan persediaan, serta memberikan akses informasi inventaris secara real-time. Aplikasi ini dibangun dengan menggunakan Framework Django, PostgreSQL, dan Docker untuk mempermudah penyebaran dan pengelolaan layanan yang terintegrasi.

# Fitur

1. Dashboard Ringkasan Sistem (Kategori, Item, Suppliers, Laporan stok minimal)
2. Manajemen Kategori (Create, Edit, Delete)
3. Manajemen Item (Create, Edit, Delete)
4. Manajemen Suppliers (Create, Edit, Delete)

# Teknologi

1. Django
2. PostgreSQL
3. HTML dan Bootstrap CSS
4. Docker

# Cara Menjalankan Proyek

1. Pastikan Anda memiliki Docker Desktop yang sudah terinstal di komputer Anda dan juga instal ekstensi Docker dan PostgreSQL di VSC Anda.

2. Clone Repository ini

3. Jalankan perintah berikut untuk membangun dan menjalankan kontainer. Sesuaikan dengan port Anda yang masih kosong (ubah bagian kiri port, misalnya 8000:8000 menjadi 8001:8000): <pre>docker compose up -d --build</pre>

4. Pada ekstensi PostgreSQL di VSC Anda, Anda dapat membuat koneksi database yang digunakan sesuai dengan informasi database yang berada pada docker-compose.yml seperti Username, Nama Database, Port Database, dan Password.

5. Mulai ulang kontainer docker
   <pre>docker compose restart</pre>

6. Akses Aplikasi

   - Untuk mengakses dashboard, Anda dapat mengunjungi http://localhost:8000 (Tergantung port yang diatur) dengan cara klik kanan containers uts_server_django-web dan klik open in browser.
   - Untuk dapat menambahkan kategori, item, dan suppliers Anda harus masuk ke halaman Admin dan melakukan login.

7. Masuk ke halaman Admin

   - Saat sudah masuk ke halaman dashboard, ganti halaman http://localhost:8000 menjadi http://localhost:8000/admin
   - Masuk menggunakan akun Admin yang tersedia di table auth_user ataupun di Admins.csv
   - Setelah login Anda bisa klik pada view site untuk beralih ke halaman dashboard.
   - Sekarang Anda dapat menambahkan item, kategori, dan juga supplier.
