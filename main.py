from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import engine, Base, get_db
from models import BookModel
from schemas import BookCreate, BookResponse

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Crud de livros com FastAPI")

#cria um novo livro
@app.post('/books/', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = BookModel(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book


# 4. UPDATE (Atualizar um livro existente)
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    book_query = db.query(BookModel).filter(BookModel.id == book_id)
    book = book_query.first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    book_query.update(book_data.model_dump(), synchronize_session=False)
    db.commit()
    return book_query.first()


# 5. DELETE (Remover um livro)
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_query = db.query(BookModel).filter(BookModel.id == book_id)
    book = book_query.first()

    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    book_query.delete(synchronize_session=False)
    db.commit()
    return None