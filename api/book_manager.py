import os
import boto3

from datetime import date
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import List
from boto3.dynamodb.conditions import Key

app = FastAPI()
handler = Mangum(app)


class Book(BaseModel):
    title: str
    isbn: str
    authors: str
    languages: List[str]
    countries: List[str]
    number_of_pages: int
    release_date: date


@app.post('/books')
async def create_book(book: Book):
    book = {
        'title': book.title,
        'isbn': book.isbn,
        'authors': book.authors,
        'languages': book.languages,
        'countries': book.countries,
        'number_of_pages': book.number_of_pages,
        'release_date': book.release_date.isoformat()
    }

    table = _get_table()
    table.put_item(Item=book)
    return {'book': book}


@app.get('/books/{isbn}')
async def get_book_by_isbn(isbn: str):
    table = _get_table()
    response = table.get_item(Key={'isbn': isbn})
    item = response.get('Item')

    if not item:
        raise HTTPException(status_code=404, detail=f'Book with [isbn:{isbn}] not found')
    return item


@app.get('/books')
async def get_all_books():
    table = _get_table()
    response = table.scan()
    books = response.get('Items')
    return {'books': books}


@app.get('/search')
async def search_books(authors: str, title: str = None):
    table = _get_table()

    if title:
        response = table.query(
            IndexName='authorIndex',
            KeyConditionExpression=Key('authors').eq(authors) & Key('title').begins_with(title),
            ScanIndexForward=False,
            Limit=10,
        )
    else:
        response = table.query(
            IndexName='authorIndex',
            KeyConditionExpression=Key('authors').eq(authors),
            ScanIndexForward=False,
            Limit=10,
        )

    books = response.get('Items')
    return {'books': books}


@app.put('/books')
async def update_book_by_isbn(book: Book):
    table = _get_table()

    table.update_item(
        Key={'isbn': book.isbn},
        UpdateExpression="""
            SET title = :title,
                authors = :authors,
                languages = :languages,
                countries = :countries,
                number_of_pages = :number_of_pages,
                release_date = :release_date
        """,
        ExpressionAttributeValues={
            ':title': book.title,
            ':authors': book.authors,
            ':languages': book.languages,
            ':countries': book.countries,
            ':number_of_pages': book.number_of_pages,
            ':release_date': book.release_date.isoformat()
        },
        ReturnValues='ALL_NEW',
    )

    return {'updated_book_isbn': book.isbn}


@app.delete('/books/{isbn}')
async def get_book_by_isbn(isbn: str):
    table = _get_table()
    response = table.delete_item(Key={'isbn': isbn})

    return {'deleted_book_isbn': isbn}


def _get_table():
    table_name = os.environ.get('TABLE_NAME')
    return boto3.resource('dynamodb').Table(table_name)
