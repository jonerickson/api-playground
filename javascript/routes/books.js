const ApiError = require("../lib/apiError.js");
const { z } = require("zod");
const express = require('express');
const { PrismaClient } = require("./../generated/prisma");

const router = express.Router();
const prisma = new PrismaClient();

const Book = z.object({
  title: z.string().min(1, "Title is required."),
  author: z.string().min(1, "Author is required."),
})

// GET ALL
router.get('/', async function(req, res, next) {
  const books = await prisma.books.findMany();
  res.json(books)
});

 // GET BY ID
router.get('/:bookId', async function(req, res, next) {
  const book = await prisma.books.findUnique({
    where: {
      id: parseInt(req.params.bookId)
    }
  });

  if (!book) return next(new ApiError("The book could not be found.", 404));

  res.json(book)
});

// CREATE
router.post('/', async function(req, res, next) {
  try {
    Book.parse(req.body);
    const book = await prisma.books.create({data: req.body});
    res.status(201).json(book)
  } catch (err) {
    if (err instanceof z.ZodError) {
      return next(new ApiError('The request validation failed.', 422, err.flatten()));
    }
    return next(new ApiError(err.message, 400));
  }
})

// UPDATE
router.put('/:bookId', async function(req, res, next) {
  const book = await prisma.books.findUnique({
    where: {
      id: parseInt(req.params.bookId)
    }
  });

  if (!book) return next(new ApiError("The book could not be found.", 404));

  try {
    Book.partial().parse(req.body);
    const book = await prisma.books.update({
      where: {
        id: parseInt(req.params.bookId)
      },
      data: req.body
    });
    res.json(book)
  } catch (err) { 
    if (err instanceof z.ZodError) {
      return next(new ApiError('The request validation failed.', 422, err.flatten()));
    }
    return next(new ApiError(err.message, 400));
  }
});

// DELETE
router.delete('/:bookId', async function(req, res, next) {
  const book = await prisma.books.findUnique({
    where: {
      id: parseInt(req.params.bookId)
    }
  });

  if (!book) return next(new ApiError("The book could not be found.", 404));

  try {
    const book = await prisma.books.delete({
      where: {
        id: parseInt(req.params.bookId)
      }
    });
    res.status(204).json()
  } catch (err) {
    return next(new ApiError(err.message, 400));
  }
});

module.exports = router;
