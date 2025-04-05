var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var booksRouter = require('./routes/books');
const responseWrapper = require('./middleware/responseWrapper');
const ApiError = require('./lib/apiError');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(responseWrapper)

app.use('/', indexRouter);
app.use('/books', booksRouter);

app.use(function(err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  const serializeMessage = (msg) => {
    if (typeof msg === 'object') {
      return msg;
    }
    return String(msg);
  };

  const statusCode = err instanceof ApiError ? err.statusCode : err.status || 500;

  res.status(statusCode).json({
    status: 'error',
    message: err.message,
    ...(err.details && { details: err.details }),
  });
});

module.exports = app;
