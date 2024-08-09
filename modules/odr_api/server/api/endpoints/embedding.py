from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from odr_core.utils import pil_image_from_base64, download_image_from_url

from odr_core.schemas.embedding import (
    EmbeddingEngine,
    EmbeddingEngineType,
    EmbeddingEngineCreate,
    EmbeddingEngineUpdate,
    AnnotationEmbedding,
    AnnotationEmbeddingCreate,
    AnnotationEmbeddingUpdate,
    ContentEmbedding,
    ContentEmbeddingCreate,
    ContentEmbeddingUpdate,
    TextEmbeddingGenerate,
    ImageEmbeddingGenerate,
    EmbeddingTextQuery,
    EmbeddingVectorQuery,
)
from odr_core.schemas.content import ContentType

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
    get_annotation_embeddings,
    update_annotation_embedding,
    delete_annotation_embedding,
    create_content_embedding,
    get_content_embedding,
    get_content_embeddings,
    update_content_embedding,
    delete_content_embedding,
    query_annotation_embedding,
    query_content_embedding,
)
from odr_core.crud.content import get_content
from odr_core.crud.annotation import get_annotation

from odr_core.database import get_db

from ..auth.auth_provider import AuthProvider


router = APIRouter(tags=["embedding"])


@router.post("/embedding/engines/", response_model=EmbeddingEngine)
def create_embedding_engine_endpoint(
    embedding_engine: EmbeddingEngineCreate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider(superuser=True)),
):
    return create_embedding_engine(db=db, embedding_engine=embedding_engine)


@router.get("/embedding/engines/{embedding_engine_id}", response_model=EmbeddingEngine)
def read_embedding_engine_endpoint(
    embedding_engine_id: int, db: Session = Depends(get_db)
):
    db_embedding_engine = get_embedding_engine(
        db, embedding_engine_id=embedding_engine_id
    )
    if db_embedding_engine is None:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")
    return db_embedding_engine


@router.get("/embedding/engines/", response_model=List[EmbeddingEngine])
def read_embedding_engines_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    embedding_engines = get_embedding_engines(db, skip=skip, limit=limit)
    return embedding_engines


@router.put("/embedding/engines/{embedding_engine_id}", response_model=EmbeddingEngine)
def update_embedding_engine_endpoint(
    embedding_engine_id: int,
    embedding_engine: EmbeddingEngineUpdate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider(superuser=True)),
):
    db_embedding_engine = update_embedding_engine(
        db,
        embedding_engine_id=embedding_engine_id,
        embedding_engine_update=embedding_engine,
    )
    if db_embedding_engine is None:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")
    return db_embedding_engine


@router.delete("/embedding/engines/{embedding_engine_id}", response_model=bool)
def delete_embedding_engine_endpoint(
    embedding_engine_id: int,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider(superuser=True)),
):
    success = delete_embedding_engine(db, embedding_engine_id=embedding_engine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")
    return success


@router.post("/embedding/generate/image", response_model=List[float])
def generate_image_embedding_endpoint(
    embedding: ImageEmbeddingGenerate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    try:
        image = pil_image_from_base64(embedding.base64_image)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid image data")
    return generate_image_embedding(
        db=db, image=image, embedding_engine_id=embedding.embedding_engine_id
    )


@router.post("/embedding/generate/text", response_model=List[float])
def generate_text_embedding_endpoint(
    embedding: TextEmbeddingGenerate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    return generate_text_embedding(
        db=db, embedding_engine_id=embedding.embedding_engine_id, text=embedding.text
    )


@router.post(
    "/embedding/generate/annotation/{annotation_id}", response_model=AnnotationEmbedding
)
def generate_embedding_for_annotation_endpoint(
    annotation_id: int,
    engine_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthProvider()),
):
    annotation = get_annotation(db, annotation_id=annotation_id)
    if annotation is None:
        raise HTTPException(status_code=404, detail="Annotation not found")

    try:
        annotation_embedding = generate_text_embedding(
            db, annotation.annotation, engine_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    annotation = AnnotationEmbeddingCreate(
        annotation_id=annotation_id,
        embedding=annotation_embedding,
        embedding_engine_id=engine_id,
        from_user_id=current_user.id,
    )

    return create_annotation_embedding(db=db, annotation_embedding=annotation)


@router.post(
    "/embedding/generate/content/{content_id}", response_model=ContentEmbedding
)
def generate_embedding_for_content_endpoint(
    content_id: int,
    engine_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(AuthProvider()),
):
    print(f"Generating embedding for content {content_id} using engine {engine_id}")

    content = get_content(db, content_id=content_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")

    engine = get_embedding_engine(db, embedding_engine_id=engine_id)
    if engine is None:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")

    if content.type.value != engine.type.value:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid content type for embedding engine. Expected {engine.type.value}, got {content.type.value}",
        )

    if content.type == ContentType.IMAGE:
        try:
            image = download_image_from_url(content.url[0])
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        embedding = generate_image_embedding(
            db=db, image=image, embedding_engine_id=engine_id
        )
    # elif content.type == ContentType.TEXT:
    #     embedding = generate_text_embedding(db=db, text=content.meta["text"], embedding_engine_id=engine_id)
    else:
        raise HTTPException(status_code=400, detail="Unsupported content type")

    content_embedding = ContentEmbeddingCreate(
        content_id=content_id,
        embedding=embedding,
        embedding_engine_id=engine_id,
        from_user_id=current_user.id,
    )

    return create_content_embedding(db=db, content_embedding=content_embedding)


@router.post("/embedding/annotation/", response_model=AnnotationEmbedding)
def create_annotation_embedding_endpoint(
    annotation_embedding: AnnotationEmbeddingCreate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    return create_annotation_embedding(db=db, annotation_embedding=annotation_embedding)


@router.get(
    "/embedding/annotation/{annotation_embedding_id}",
    response_model=AnnotationEmbedding,
)
def read_annotation_embedding_endpoint(
    annotation_embedding_id: int, db: Session = Depends(get_db)
):
    db_annotation_embedding = get_annotation_embedding(
        db, annotation_embedding_id=annotation_embedding_id
    )
    if db_annotation_embedding is None:
        raise HTTPException(status_code=404, detail="Annotation Embedding not found")
    return db_annotation_embedding


@router.get("/embedding/annotation/", response_model=List[AnnotationEmbedding])
def read_annotation_embeddings_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_annotation_embeddings(db, skip=skip, limit=limit)


# query for annotations embeddings by vector
@router.get(
    "/embedding/annotation/query/vector", response_model=List[AnnotationEmbedding]
)
def query_annotation_embedding_endpoint(
    query: EmbeddingVectorQuery,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return query_annotation_embedding(db, query, skip, limit)


# query for annotations embeddings by text
@router.get(
    "/embedding/annotation/query/text", response_model=List[AnnotationEmbedding]
)
def query_annotation_embedding_text_endpoint(
    engine_id: int,
    text: str,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    engine = get_embedding_engine(db, embedding_engine_id=engine_id)
    if engine is None:
        raise HTTPException(status_code=404, detail="Embedding Engine not found")

    if not engine.supported:
        raise HTTPException(status_code=400, detail="Embedding Engine not supported")

    if engine.type.value != EmbeddingEngineType.TEXT.value:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid engine type. Expected {EmbeddingEngineType.TEXT.value}, got {engine.type.value}",
        )

    try:
        embedding = generate_text_embedding(db, text, engine_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    query = EmbeddingVectorQuery(embedding=embedding, embedding_engine_id=engine_id)

    try:
        return query_annotation_embedding(db, query, skip, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/embedding/annotation/{annotation_embedding_id}",
    response_model=AnnotationEmbedding,
)
def update_annotation_embedding_endpoint(
    annotation_embedding_id: int,
    annotation_embedding: AnnotationEmbeddingUpdate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    db_annotation_embedding = update_annotation_embedding(
        db,
        annotation_embedding_id=annotation_embedding_id,
        annotation_embedding_update=annotation_embedding,
    )
    if db_annotation_embedding is None:
        raise HTTPException(status_code=404, detail="Annotation Embedding not found")
    return db_annotation_embedding


@router.delete("/embedding/annotation/{annotation_embedding_id}", response_model=bool)
def delete_annotation_embedding_endpoint(
    annotation_embedding_id: int,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    success = delete_annotation_embedding(
        db, annotation_embedding_id=annotation_embedding_id
    )
    if not success:
        raise HTTPException(status_code=404, detail="Annotation Embedding not found")
    return success


@router.post("/embedding/content/", response_model=ContentEmbedding)
def create_content_embedding_endpoint(
    content_embedding: ContentEmbeddingCreate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    return create_content_embedding(db=db, content_embedding=content_embedding)


@router.get(
    "/embedding/content/{content_embedding_id}", response_model=ContentEmbedding
)
def read_content_embedding_endpoint(
    content_embedding_id: int, db: Session = Depends(get_db)
):
    db_content_embedding = get_content_embedding(
        db, content_embedding_id=content_embedding_id
    )
    if db_content_embedding is None:
        raise HTTPException(status_code=404, detail="Content Embedding not found")
    return db_content_embedding


@router.get("/embedding/content/", response_model=List[ContentEmbedding])
def read_content_embeddings_endpoint(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return get_content_embeddings(db, skip=skip, limit=limit)


# query for content embeddings by vector
@router.post(
    "/embedding/content/query/embedding", response_model=List[ContentEmbedding]
)
def query_content_embedding_endpoint(
    query: EmbeddingVectorQuery,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return query_content_embedding(db, query, skip, limit)


@router.put(
    "/embedding/content/{content_embedding_id}", response_model=ContentEmbedding
)
def update_content_embedding_endpoint(
    content_embedding_id: int,
    content_embedding: ContentEmbeddingUpdate,
    db: Session = Depends(get_db),
    _=Depends(AuthProvider()),
):
    db_content_embedding = update_content_embedding(
        db,
        content_embedding_id=content_embedding_id,
        content_embedding_update=content_embedding,
    )
    if db_content_embedding is None:
        raise HTTPException(status_code=404, detail="Content Embedding not found")
    return db_content_embedding


@router.delete("/embedding/content/{content_embedding_id}", response_model=bool)
def delete_content_embedding_endpoint(
    content_embedding_id: int, db: Session = Depends(get_db), _=Depends(AuthProvider())
):
    success = delete_content_embedding(db, content_embedding_id=content_embedding_id)
    if not success:
        raise HTTPException(status_code=404, detail="Content Embedding not found")
    return success
