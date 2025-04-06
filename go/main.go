package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type book struct {
	ID     string `json:"id"`
	Title  string `json:"title"`
	Author string `json:"author"`
}

var books = []book{
	{ID: "1", Title: "Book 1", Author: "Author 1"},
	{ID: "2", Title: "Book 2", Author: "Author 2"},
	{ID: "3", Title: "Book 3", Author: "Author 3"},
}

func getBooks(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, books)
}

func getBookByID(c *gin.Context) {
	id := c.Param("id")

	for _, book := range books {
		if book.ID == id {
			c.IndentedJSON(http.StatusOK, book)
			return
		}
	}

	c.IndentedJSON(http.StatusNotFound, gin.H{"message": "The book could not found."})
}

func createBook(c *gin.Context) {
	var newBook book

	if err := c.BindJSON(&newBook); err != nil {
		return
	}

	books = append(books, newBook)
	c.IndentedJSON(http.StatusCreated, newBook)
}

func main() {
	router := gin.Default()
	router.GET("/books", getBooks)
	router.GET("/books/:id", getBookByID)
	router.POST("/books", createBook)

	router.Run("localhost:3000")
}
