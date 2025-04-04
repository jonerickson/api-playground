const { z } = require("zod");
const express = require('express');
const { PrismaClient } = require("./../generated/prisma");

const router = express.Router();
const prisma = new PrismaClient();

const Book = z.object({
  title: z.string().min(1, "Title is required."),
  author: z.string().min(1, "Author is required."),
})

router.get('/', async function(req, res, next) {
  const books = await prisma.books.findMany();
  res.json(books)
});

router.get('/:bookId', async function(req, res, next) {
  const book = await prisma.books.findUnique({
    where: {
      id: parseInt(req.params.bookId)
    }
  });

  if (!book) return res.status(404).json({ error: "The book could not be found." });

  res.json(book)
});

router.post('/', async function(req, res, next) {
  try {
    Book.parse(req.body);
    const book = await prisma.books.create({data: req.body});
    res.status(201).json(book)
  } catch (err) {
    return res.status(422).json({ error: err });
  }
})

router.put('/:bookId', async function(req, res, next) {
  const book = await prisma.books.findUnique({
    where: {
      id: parseInt(req.params.bookId)
    }
  });

  if (!book) return res.status(404).json({ error: "The book could not be found." });

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
    return res.status(422).json({ error: err });
  }
});

router.delete('/:bookId', async function(req, res, next) {
  const book = await prisma.books.findUnique({
    where: {
      id: parseInt(req.params.bookId)
    }
  });

  if (!book) return res.status(404).json({ error: "The book could not be found." });

  try {
    const book = await prisma.books.delete({
      where: {
        id: parseInt(req.params.bookId)
      }
    });
    res.status(204).json()
  } catch (err) {
    return res.status(422).json({ error: err });
  }
});

module.exports = router;
