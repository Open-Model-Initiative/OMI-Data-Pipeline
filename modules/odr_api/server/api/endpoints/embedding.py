from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from odr_core.schemas.embedding import (
    EmbeddingEngine, 
    EmbeddingEngineCreate, 
    EmbeddingEngineUpdate, 
    AnnotationEmbedding, 
    AnnotationEmbeddingCreate, 
    AnnotationEmbeddingUpdate, 
    ContentEmbedding, 
    ContentEmbeddingCreate, 
    ContentEmbeddingUpdate
    )

from odr_core.crud.embedding import (
    create_embedding_engine, 
    get_embedding_engine, 
    get_embedding_engines, 
    update_embedding_engine, 
    delete_embedding_engine,

    generate_image_embedding,
    generate_text_embedding,

    create_annotation_embedding,
    get_annotation_embedding,
    update_annotation_embedding,
    delete_annotation_embedding,

    create_content_embedding,
    get_content_embedding,
    update_content_embedding,
    delete_content_embedding,
    )

from odr_core.database import get_db

from ..auth.auth_provider import AuthProvider

router = APIRouter(tags=["embedding"])


@router.post("/embedding/engines/", response_model=EmbeddingEngine)
def create_embedding_engine_endpoint(embedding_engine: EmbeddingEngineCreate, db: Session = Depends(get_db), _ = Depends(AuthProvider(superuser=True))):
    return create_embedding_engine(db=db, embedding_engine=embedding_engine)


@router.get("/embedding/engines/{embedding_engine_id}", response_model=EmbeddingEngine)
def read_embedding_engine_endpoint(embedding_engine_id: int, db: Session = Depends(get_db)):
    db_embedding_engine = get_embedding_engine(db, embedding_engine_id=embedding_engine_id)
    if db_embedding_engine is None:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")
    return db_embedding_engine


@router.get("/embedding/engines/", response_model=List[EmbeddingEngine])
def read_embedding_engines_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    embedding_engines = get_embedding_engines(db, skip=skip, limit=limit)
    return embedding_engines


@router.put("/embedding/engines/{embedding_engine_id}", response_model=EmbeddingEngine)
def update_embedding_engine_endpoint(embedding_engine_id: int, embedding_engine: EmbeddingEngineUpdate, db: Session = Depends(get_db), _ = Depends(AuthProvider(superuser=True))):
    db_embedding_engine = update_embedding_engine(db, embedding_engine_id=embedding_engine_id, embedding_engine_update=embedding_engine)
    if db_embedding_engine is None:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")
    return db_embedding_engine


@router.delete("/embedding/engines/{embedding_engine_id}", response_model=bool)
def delete_embedding_engine_endpoint(embedding_engine_id: int, db: Session = Depends(get_db), _ = Depends(AuthProvider(superuser=True))):
    success = delete_embedding_engine(db, embedding_engine_id=embedding_engine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")
    return success


@router.post("/embedding/generate/image", response_model=ContentEmbedding)
def generate_image_embedding_endpoint(content_embedding: ContentEmbeddingCreate, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    return generate_image_embedding(db=db, content_embedding=content_embedding)


@router.post("/embedding/generate/text", response_model=ContentEmbedding)
def generate_text_embedding_endpoint(content_embedding: ContentEmbeddingCreate, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    return generate_text_embedding(db=db, content_embedding=content_embedding)


@router.post("/embedding/generate/annotation/{annotation_id}", response_model=AnnotationEmbedding)
def generate_embedding_for_annotation_endpoint(annotation_id: int, engine_id: int,  db: Session = Depends(get_db), current_user = Depends(AuthProvider())):
    annotation = get_annotation_embedding(db, annotation_embedding_id=annotation_id)
    if annotation is None:
        raise HTTPException(status_code=404, detail="Annotation not found")
    
    try:
        annotation_embedding = generate_text_embedding(annotation.annotation, engine_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    annotation = AnnotationEmbeddingCreate(
        annotation_id=annotation_id,
        embedding=annotation_embedding,
        embedding_engine_id=engine_id,
        from_user_id=current_user.id
    )

    return create_annotation_embedding(db=db, annotation_embedding=annotation)

@router.post("/embedding/annotation/", response_model=AnnotationEmbedding)
def create_annotation_embedding_endpoint(annotation_embedding: AnnotationEmbeddingCreate, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    return create_annotation_embedding(db=db, annotation_embedding=annotation_embedding)


@router.get("/embedding/annotation/{annotation_embedding_id}", response_model=AnnotationEmbedding)
def read_annotation_embedding_endpoint(annotation_embedding_id: int, db: Session = Depends(get_db)):
    db_annotation_embedding = get_annotation_embedding(db, annotation_embedding_id=annotation_embedding_id)
    if db_annotation_embedding is None:
        raise HTTPException(status_code=404, detail="Annotation Embedding not found")
    return db_annotation_embedding


@router.put("/embedding/annotation/{annotation_embedding_id}", response_model=AnnotationEmbedding)
def update_annotation_embedding_endpoint(annotation_embedding_id: int, annotation_embedding: AnnotationEmbeddingUpdate, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    db_annotation_embedding = update_annotation_embedding(db, annotation_embedding_id=annotation_embedding_id, annotation_embedding_update=annotation_embedding)
    if db_annotation_embedding is None:
        raise HTTPException(status_code=404, detail="Annotation Embedding not found")
    return db_annotation_embedding


@router.delete("/embedding/annotation/{annotation_embedding_id}", response_model=bool)
def delete_annotation_embedding_endpoint(annotation_embedding_id: int, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    success = delete_annotation_embedding(db, annotation_embedding_id=annotation_embedding_id)
    if not success:
        raise HTTPException(status_code=404, detail="Annotation Embedding not found")
    return success


@router.post("/embedding/content/", response_model=ContentEmbedding)
def create_content_embedding_endpoint(content_embedding: ContentEmbeddingCreate, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    return create_content_embedding(db=db, content_embedding=content_embedding)


@router.get("/embedding/content/{content_embedding_id}", response_model=ContentEmbedding)
def read_content_embedding_endpoint(content_embedding_id: int, db: Session = Depends(get_db)):
    db_content_embedding = get_content_embedding(db, content_embedding_id=content_embedding_id)
    if db_content_embedding is None:
        raise HTTPException(status_code=404, detail="Content Embedding not found")
    return db_content_embedding


@router.put("/embedding/content/{content_embedding_id}", response_model=ContentEmbedding)
def update_content_embedding_endpoint(content_embedding_id: int, content_embedding: ContentEmbeddingUpdate, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    db_content_embedding = update_content_embedding(db, content_embedding_id=content_embedding_id, content_embedding_update=content_embedding)
    if db_content_embedding is None:
        raise HTTPException(status_code=404, detail="Content Embedding not found")
    return db_content_embedding


@router.delete("/embedding/content/{content_embedding_id}", response_model=bool)
def delete_content_embedding_endpoint(content_embedding_id: int, db: Session = Depends(get_db), _ = Depends(AuthProvider())):
    success = delete_content_embedding(db, content_embedding_id=content_embedding_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content Embedding not found")
    return success


