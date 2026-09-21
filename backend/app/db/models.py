import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Alert(Base):
    """Stores incoming alerts from Splunk, Elastic, and Sentinel."""
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, index=True, nullable=False)
    severity = Column(String, index=True, nullable=False)
    raw_log = Column(JSONB, nullable=False)
    status = Column(String, default="Open", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ThreatDocument(Base):
    """Stores MITRE ATT&CK, CVEs, and runbooks for RAG retrieval."""
    __tablename__ = "threat_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name = Column(String, index=True) # e.g., "MITRE", "NVD", "Internal"
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1024)) # Dimension size for BGE-large-en
