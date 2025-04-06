<?php

use App\Http\Controllers\BookController;
use App\Http\Middleware\ApiResponseWrapper;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return response()->json([
        'status' => 'Okay',
        'language' => 'PHP',
        'framework' => 'Laravel',
    ]);
});

Route::group(['as' => 'api.', 'middleware' => ApiResponseWrapper::class], function () {
    Route::apiResource('/books', BookController::class);
});
