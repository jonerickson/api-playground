var express = require('express');
var router = express.Router();

const { PrismaClient } = require("./../generated/prisma");
const prisma = new PrismaClient();

/* GET books listing. */
router.get('/', async function(req, res, next) {
  const books = await prisma.books.findMany();
  res.json(books)
});

module.exports = router;
