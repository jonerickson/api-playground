<?php

namespace App\Http\Controllers;

use App\Http\Resources\BookResource;
use App\Models\Book;
use Illuminate\Http\Request;

class BookController extends Controller
{
    public function index()
    {
        return BookResource::collection(Book::all());
    }

    public function show(Book $book)
    {
        return BookResource::make($book);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'title' => 'required|string|max:255',
            'author' => 'required|string|max:255',
        ]);

        $book = Book::create($data);

        return BookResource::make($book);
    }

    public function update(Request $request, Book $book)
    {
        $data = $request->validate([
            'title' => 'string|max:255',
            'author' => 'string|max:255',
        ]);

        $book->update($data);

        return BookResource::make($book);
    }

    public function destroy(Book $book)
    {
        $book->delete();

        return response()->noContent();
    }
}
