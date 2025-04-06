<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpFoundation\Response;

class ApiResponseWrapper
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        if (! $request->routeIs('api.*')) {
            return $response;
        }

        if (! $response instanceof JsonResponse) {
            return $response;
        }

        $data = $response->getData(true);

        $status = $response->getStatusCode() >= 400 ? 'error' : 'okay';

        $payload = [
            'status' => $status,
        ];

        if ($status === 'okay') {
            $payload['data'] = $data['data'] ?? $data;
        } else {
            $payload['message'] = $data['message'] ?? 'An unexpected error occurred.';
        }

        if ($response->exception instanceof ValidationException) {
            $payload['details'] = $data['errors'] ?? [];
        }

        return response()->json($payload, $response->getStatusCode());
    }
}
