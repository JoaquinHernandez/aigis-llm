import asyncio
import httpx
from sentence_transformers import SentenceTransformer
from app.db.session import AsyncSessionLocal
from app.db.models import ThreatDocument

# BGE-Large generates 1024-dimensional embeddings matching our pgvector schema
EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
MITRE_STIX_URL = "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json"

async def fetch_mitre_data() -> dict:
    """Downloads the latest MITRE ATT&CK Enterprise STIX 2.1 dataset."""
    print("[*] Downloading MITRE ATT&CK STIX dataset...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(MITRE_STIX_URL)
        response.raise_for_status()
        return response.json()

def extract_techniques(stix_data: dict) -> list[dict]:
    """Parses STIX JSON to extract technique names, descriptions, and IDs."""
    techniques = []
    for obj in stix_data.get("objects", []):
        if obj.get("type") == "attack-pattern" and not obj.get("revoked") and not obj.get("x_mitre_deprecated"):
            
            # Extract the T-Code (e.g., T1059)
            ext_id = next((ref["external_id"] for ref in obj.get("external_references", []) if ref.get("source_name") == "mitre-attack"), None)
            
            if ext_id:
                content = f"Technique: {obj.get('name')}\nID: {ext_id}\nDescription: {obj.get('description', '')}"
                techniques.append({
                    "source_name": "MITRE ATT&CK",
                    "content": content
                })
    return techniques

async def ingest_to_pgvector(techniques: list[dict]):
    """Generates embeddings and stores them in Postgres via pgvector."""
    print(f"[*] Loading Embedding Model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    print(f"[*] Generating embeddings for {len(techniques)} techniques. (This utilizes CPU/GPU)...")
    texts = [t["content"] for t in techniques]
    
    # Generate vectors as NumPy arrays
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

    print("[*] Saving vectors to PostgreSQL...")
    async with AsyncSessionLocal() as session:
        for idx, tech in enumerate(techniques):
            doc = ThreatDocument(
                source_name=tech["source_name"],
                content=tech["content"],
                embedding=embeddings[idx].tolist()  # Convert NumPy array to standard Python list for pgvector
            )
            session.add(doc)
        
        await session.commit()
    print("[+] MITRE ATT&CK Ingestion Complete.")

async def main():
    stix_data = await fetch_mitre_data()
    techniques = extract_techniques(stix_data)
    await ingest_to_pgvector(techniques)

if __name__ == "__main__":
    asyncio.run(main())
