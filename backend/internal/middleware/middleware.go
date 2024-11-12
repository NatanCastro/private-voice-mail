package middleware

import "net/http"

type Middleware func(http.Handler) http.Handler

func CreateStack(middlewares ...Middleware) Middleware {
	return func(next http.Handler) http.Handler {
		for i := len(middlewares) - 1; i >= 0; i-- {
			middleware := middlewares[i]
			next = middleware(next)
		}
		return next
	}
}

type WrappedWritter struct {
	http.ResponseWriter
	statusCode int
}

func (w *WrappedWritter) WriteHeader(statusCode int) {
	w.ResponseWriter.WriteHeader(statusCode)
	w.statusCode = statusCode
}
