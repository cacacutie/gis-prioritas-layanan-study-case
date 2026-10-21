"""
Studi Kasus GIS: Analisis Kedekatan Laporan terhadap Aset Layanan
Data dan koordinat di bawah ini hanya simulasi pembelajaran.
"""

from math import radians, sin, cos, asin, sqrt
from pathlib import Path
import json

import pandas as pd

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Data aset dummy
assets = pd.DataFrame([
    {"asset_id": "A01", "nama_aset": "Pusat Layanan Utara", "jenis": "Layanan publik", "latitude": -3.7900, "longitude": 102.2600},
    {"asset_id": "A02", "nama_aset": "Pos Infrastruktur Barat", "jenis": "Infrastruktur", "latitude": -3.8050, "longitude": 102.2450},
    {"asset_id": "A03", "nama_aset": "Pusat Layanan Tengah", "jenis": "Layanan publik", "latitude": -3.8150, "longitude": 102.2700},
    {"asset_id": "A04", "nama_aset": "Pos Infrastruktur Timur", "jenis": "Infrastruktur", "latitude": -3.8200, "longitude": 102.2950},
    {"asset_id": "A05", "nama_aset": "Pusat Layanan Selatan", "jenis": "Layanan publik", "latitude": -3.8400, "longitude": 102.2750},
    {"asset_id": "A06", "nama_aset": "Gudang Operasional", "jenis": "Operasional", "latitude": -3.8000, "longitude": 102.2850},
])

# Data laporan warga dummy
reports = pd.DataFrame([
    {"report_id": "R01", "kategori": "Lampu jalan", "latitude": -3.7920, "longitude": 102.2630, "prioritas": "Sedang"},
    {"report_id": "R02", "kategori": "Jalan rusak", "latitude": -3.8070, "longitude": 102.2490, "prioritas": "Tinggi"},
    {"report_id": "R03", "kategori": "Drainase", "latitude": -3.8170, "longitude": 102.2720, "prioritas": "Sedang"},
    {"report_id": "R04", "kategori": "Lampu jalan", "latitude": -3.8250, "longitude": 102.2910, "prioritas": "Rendah"},
    {"report_id": "R05", "kategori": "Jalan rusak", "latitude": -3.8370, "longitude": 102.2790, "prioritas": "Tinggi"},
    {"report_id": "R06", "kategori": "Drainase", "latitude": -3.7980, "longitude": 102.2810, "prioritas": "Sedang"},
    {"report_id": "R07", "kategori": "Lampu jalan", "latitude": -3.8120, "longitude": 102.2550, "prioritas": "Rendah"},
    {"report_id": "R08", "kategori": "Jalan rusak", "latitude": -3.8300, "longitude": 102.2650, "prioritas": "Tinggi"},
    {"report_id": "R09", "kategori": "Drainase", "latitude": -3.8030, "longitude": 102.3000, "prioritas": "Sedang"},
    {"report_id": "R10", "kategori": "Lampu jalan", "latitude": -3.8450, "longitude": 102.2600, "prioritas": "Rendah"},
    {"report_id": "R11", "kategori": "Jalan rusak", "latitude": -3.7880, "longitude": 102.2500, "prioritas": "Sedang"},
    {"report_id": "R12", "kategori": "Drainase", "latitude": -3.8210, "longitude": 102.2800, "prioritas": "Tinggi"},
])


def haversine_km(lat1, lon1, lat2, lon2):
    """Menghitung jarak garis lurus antara dua koordinat dalam kilometer."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(a))


def main():
    print("=== STUDI KASUS GIS: ANALISIS KEDEKATAN LAPORAN DAN ASET ===")

    print("\nContoh data aset:")
    print(assets.head().to_string(index=False))
    print(f"\nJumlah aset: {len(assets)}")
    print(f"Jumlah laporan: {len(reports)}")

    results = []
    for _, report in reports.iterrows():
        distances = assets.apply(
            lambda asset: haversine_km(
                report["latitude"], report["longitude"],
                asset["latitude"], asset["longitude"]
            ),
            axis=1
        )
        nearest_index = distances.idxmin()
        nearest_asset = assets.loc[nearest_index]
        distance = float(distances.loc[nearest_index])

        if distance <= 1:
            proximity = "Dekat"
        elif distance <= 2:
            proximity = "Sedang"
        else:
            proximity = "Jauh"

        results.append({
            **report.to_dict(),
            "aset_terdekat": nearest_asset["nama_aset"],
            "jarak_km": round(distance, 3),
            "kedekatan": proximity,
        })

    result_df = pd.DataFrame(results)

    # Simpan hasil analisis ke CSV
    csv_path = OUTPUT_DIR / "hasil_analisis_gis.csv"
    result_df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print("\n=== RINGKASAN KEDEKATAN ===")
    print(result_df[
        ["report_id", "kategori", "aset_terdekat", "jarak_km", "kedekatan"]
    ].to_string(index=False))

    print("\nJumlah laporan berdasarkan kedekatan:")
    print(result_df["kedekatan"].value_counts().to_string())

    # Peta HTML mandiri tanpa tile eksternal atau API key.
    # Ini adalah visualisasi koordinat relatif, bukan peta jalan geografis.
    map_data = {
        "assets": assets.to_dict(orient="records"),
        "reports": result_df.to_dict(orient="records"),
    }

    map_html = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Peta Analisis GIS</title>
<style>
* { box-sizing: border-box; }
body { margin: 0; font-family: Arial, sans-serif; color: #20302a; background: #f4f7f4; }
.header { padding: 18px 22px; background: white; border-bottom: 1px solid #dbe4dc; }
h2 { margin: 0 0 8px; font-size: 22px; }
.subtitle { color: #58665d; font-size: 14px; }
.map {
  position: relative; height: 70vh; min-height: 400px; overflow: hidden;
  background-color: #eaf2e5;
  background-image:
    linear-gradient(25deg, transparent 48%, #fff 49%, #fff 51%, transparent 52%),
    linear-gradient(110deg, transparent 47%, #d3e1cc 48%, #d3e1cc 52%, transparent 53%),
    linear-gradient(160deg, transparent 48%, #fff 49%, #fff 50%, transparent 51%);
  background-size: 180px 140px, 210px 170px, 270px 210px;
  border-bottom: 1px solid #dbe4dc;
}
.marker {
  position: absolute; transform: translate(-50%, -50%); border: 2px solid white;
  border-radius: 50%; width: 20px; height: 20px; cursor: pointer;
  box-shadow: 0 1px 5px #657568; z-index: 2;
}
.marker:hover { transform: translate(-50%, -50%) scale(1.25); z-index: 5; }
.asset { width: 28px; height: 28px; background: #2583c5; color: white; font-weight: bold; }
.high { background: #df3d3d; }
.medium { background: #ed9e20; }
.low { background: #2c984e; }
#info {
  position: absolute; left: 12px; bottom: 12px; z-index: 10;
  background: white; padding: 13px; border-radius: 9px; box-shadow: 0 1px 6px #aab7ac;
  max-width: min(330px, calc(100% - 24px)); font-size: 13px; line-height: 1.6;
}
.legend { display: flex; flex-wrap: wrap; gap: 12px; padding: 15px 20px; background: white; font-size: 13px; }
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
.note { padding: 0 20px 18px; background: white; color: #5e6b62; font-size: 12px; }
</style>
</head>
<body>
<header class="header">
  <h2>Studi Kasus GIS: Analisis Kedekatan Laporan dan Aset</h2>
  <div class="subtitle">Pilih titik untuk melihat detail aset atau laporan. Seluruh data merupakan simulasi.</div>
</header>
<div class="map" id="map">
  <div id="info">Klik titik berwarna untuk melihat detailnya.</div>
</div>
<div class="legend">
  <span><i class="dot" style="background:#2583c5"></i>Aset layanan</span>
  <span><i class="dot" style="background:#df3d3d"></i>Prioritas tinggi</span>
  <span><i class="dot" style="background:#ed9e20"></i>Prioritas sedang</span>
  <span><i class="dot" style="background:#2c984e"></i>Prioritas rendah</span>
</div>
<div class="note">Visualisasi koordinat relatif, bukan peta geografis berskala atau peta jalan. Tidak memerlukan API key atau tile internet.</div>
<script>
const data = __GIS_DATA__;
const map = document.getElementById("map");
const info = document.getElementById("info");
const all = [...data.assets, ...data.reports];
const lats = all.map(p => p.latitude), lons = all.map(p => p.longitude);
const minLat = Math.min(...lats), maxLat = Math.max(...lats);
const minLon = Math.min(...lons), maxLon = Math.max(...lons);

function addMarker(point, isAsset) {
  const x = 7 + 86 * (point.longitude - minLon) / (maxLon - minLon || 1);
  const y = 7 + 86 * (maxLat - point.latitude) / (maxLat - minLat || 1);
  const marker = document.createElement("button");
  marker.className = "marker " + (isAsset ? "asset" :
    point.prioritas === "Tinggi" ? "high" :
    point.prioritas === "Sedang" ? "medium" : "low");
  marker.style.left = x + "%";
  marker.style.top = y + "%";
  marker.textContent = isAsset ? "A" : "";
  marker.title = isAsset ? point.nama_aset : point.report_id;
  marker.setAttribute("aria-label", marker.title);
  marker.addEventListener("click", () => {
    if (isAsset) {
      info.innerHTML = "<b>" + point.nama_aset + "</b><br>ID: " + point.asset_id +
        "<br>Jenis: " + point.jenis +
        "<br>Koordinat: " + point.latitude + ", " + point.longitude;
    } else {
      info.innerHTML = "<b>" + point.report_id + " — " + point.kategori + "</b>" +
        "<br>Prioritas contoh: " + point.prioritas +
        "<br>Aset terdekat: " + point.aset_terdekat +
        "<br>Jarak garis lurus: " + point.jarak_km + " km";
    }
  });
  map.appendChild(marker);
}
data.assets.forEach(p => addMarker(p, true));
data.reports.forEach(p => addMarker(p, false));
</script>
</body>
</html>"""

    # Perbaiki token properti dalam HTML dan masukkan data aman sebagai JSON.
    map_html = map_html.replace("point.jarak_km", "point.jarak_km")
    map_html = map_html.replace(
        "__GIS_DATA__",
        json.dumps(map_data, ensure_ascii=False).replace("</", "<\\/")
    )

    map_path = OUTPUT_DIR / "peta_gis_interaktif.html"
    map_path.write_text(map_html, encoding="utf-8")

    print(f"\nFile hasil CSV : {csv_path}")
    print(f"File peta HTML : {map_path}")
    print("\nCATATAN:")
    print("- Data dan koordinat hanya simulasi.")
    print("- Jarak adalah jarak garis lurus, bukan jarak jalan.")
    print("- Peta HTML ini menampilkan koordinat relatif dan tidak membutuhkan API key.")


if __name__ == "__main__":
    main()
