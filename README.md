# e-Tugas SMKATB 2026

Laman web statik GitHub Pages + sumber Google Sheets CSV. **Data dibina melalui pengekstrakan automatik; BELUM disahkan dan tidak boleh dianggap rekod rasmi sehingga disemak.**

## Cara buka di GitHub Pages
1. Cipta repository baharu di GitHub, contoh `e-tugas-smkatb`.
2. Muat naik `index.html`, `config.json`, `pelantikan.json`, `bidang_tugas.json` (dan `pelantikan.csv` untuk pengurusan).
3. Buka `Settings` → `Pages` → `Deploy from a branch` → `main` → `/(root)` → `Save`.
4. Selepas GitHub Pages aktif, lawat `https://NAMA-PENGGUNA.github.io/e-tugas-smkatb/`.

## Sambungkan Google Sheets
1. Import **pelantikan.csv** ke satu Google Sheets (File → Import → Upload). Pastikan kolum: `nama,bidang,jawatankuasa,jawatan,konteks,muka_surat,halaman_pdf,status`.
2. Semak dan baiki semua pelantikan, terutama baris yang berstatus `PERLU SEMAK`, entri jawatan bersifat umum, ejaan berganda, dan jawatan yang sebenarnya merujuk kepada SEMUA guru dalam sesuatu kategori.
3. Setelah mendapat persetujuan pentadbir untuk data nama pelantikan ini dipaparkan kepada umum, pilih `File → Share → Publish to web` → helaian berkenaan → `Comma-separated values (.csv)` → Publish. **Perhatian: pautan diterbitkan ini boleh diakses oleh sesiapa yang mempunyai pautan dan data berkemungkinan boleh diindeks.** Jangan masukkan maklumat sulit dalam helaian diterbitkan.
4. Salin URL CSV itu ke nilai `google_sheets_csv` dalam `config.json` dan commit fail di GitHub. Halaman kini memuatkan data terus daripada Sheets (Google mungkin cache beberapa minit). Alternatif: guru/pentadbir boleh masukkan URL melalui butang **Sumber data**, tetapi tetapan itu hanya terpakai pada pelayar berkenaan.
5. Jika keperluan ialah akses tertutup untuk guru sahaja, jangan gunakan Publish to web; pilih penyelesaian pengesahan/log masuk dan pangkalan data dengan kawalan akses yang sesuai.

## Semakan ketepatan penting
- Pengekstrak `extract.py` mengesan baris bermula gelaran nama dalam PDF serta tajuk bernombor. Ia **tidak menjamin** padanan tepat untuk sel jadual bercantum, tajuk diteruskan merentas halaman, singkatan nama, jawatan dibekalkan secara tersirat, dan tugas mengikut kelas/unit. Baris automatik mestilah diaudit sebelum sistem digunakan secara rasmi.
- Fail `bidang_tugas.json` mengandungi poin tugas yang dapat dipadankan secara heuristik; potensi tugasan daripada bahagian sebelum/selepas tajuk perlu disahkan.
- `muka_surat` ialah nombor buku (anggaran halaman PDF ditolak tiga); `halaman_pdf` ialah nombor muka surat fail sebenar.
- Nama yang sama dengan ejaan berbeza mungkin menghasilkan beberapa pilihan carian. Normalisasi carian mengabaikan banyak gelaran/bin/binti tetapi tidak menggantikan audit nama.
- Laman tidak menyimpan maklumat identiti sulit atau rekod prestasi guru.
- `extract.py` ialah skrip pembina semula yang memerlukan fail PDF asal dalam direktori asal; ia tidak diperlukan untuk laman web beroperasi.

## Pembetulan
Betulkan terus baris dalam Google Sheets dan tunggu pautan CSV baharu dimuatkan. Tidak perlu edit laman GitHub untuk setiap kemas kini. Fungsi cetak pelayar membolehkan guru simpan PDF portfolio.
