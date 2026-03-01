import os
import httpx
from mcp.server.fastmcp import FastMCP

# 1. Inisialisasi Server MCP
mcp = FastMCP("Regional Indonesia API")

# Base URL berdasarkan dokumentasi goapi.io
BASE_URL = "https://api.goapi.io/regional"

def get_api_key() -> str:
    """Mengambil API Key dari environment variable untuk keamanan (Bonus Poin)."""
    api_key = os.environ.get("GOAPI_KEY")
    if not api_key:
        raise ValueError("Error: GOAPI_KEY environment variable belum di-set!")
    return api_key

async def make_request(endpoint: str, params: dict = None) -> str:
    """Fungsi helper untuk melakukan HTTP request dengan Error Handling yang anggun."""
    if params is None:
        params = {}
    
    # Memasukkan API Key ke dalam parameter request
    params['api_key'] = get_api_key()
    url = f"{BASE_URL}/{endpoint}"

    try:
        # Menggunakan timeout 10 detik agar tidak hang
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
            # Menangani Rate Limit 
            if response.status_code == 429:
                return "Error: Batas rate limit API tercapai. Mohon tunggu sebentar sebelum mencoba lagi."
            
            # Akan melemparkan error jika status code bukan 200 OK
            response.raise_for_status()
            
            data = response.json()
            
            # Menangani jika hasil dari API kosong
            if data.get('status') == 'success' and not data.get('data'):
                return "Pencarian berhasil, namun tidak ada data yang ditemukan."
                
            # Mengembalikan data dalam bentuk string (format yang dimengerti MCP)
            return str(data.get('data', []))

    except httpx.TimeoutException:
        return "Error: Request ke API Regional Indonesia mengalami Timeout."
    except httpx.HTTPStatusError as e:
        return f"Error: Request gagal dengan status HTTP {e.response.status_code}."
    except Exception as e:
        return f"Error: Terjadi kesalahan sistem internal: {str(e)}"

# 2. Mendefinisikan Tools untuk AI
@mcp.tool()
async def get_provinsi() -> str:
    """
    Mengambil daftar seluruh provinsi di Indonesia beserta ID-nya.
    Gunakan tool ini untuk mencari ID dari suatu provinsi.
    """
    return await make_request("provinsi")

@mcp.tool()
async def get_kota(provinsi_id: str) -> str:
    """
    Mengambil daftar seluruh kabupaten/kota di suatu provinsi.
    Membutuhkan 'provinsi_id' yang didapatkan dari tool get_provinsi.
    """
    return await make_request("kota", params={"provinsi_id": provinsi_id})

# Jalankan server
if __name__ == "__main__":
    mcp.run()