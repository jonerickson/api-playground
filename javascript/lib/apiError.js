class ApiError extends Error {
    constructor(message, statusCode, details = null) {
        super(typeof message === 'string' ? message : 'An error occurred.');
        this.statusCode = statusCode;
        this.details = typeof message === 'object' ? message : details;
    }
}

module.exports = ApiError;