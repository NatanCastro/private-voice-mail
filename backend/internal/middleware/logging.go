package middleware

import (
	"log"
	"net/http"
	"time"
)

func Logging(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		wrappedWritter := &WrappedWritter{
			ResponseWriter: w,
			statusCode:     http.StatusOK,
		}
		next.ServeHTTP(wrappedWritter, r)

		log.Println(wrappedWritter.statusCode, r.Method, r.URL.Path, time.Since(start))
	})
}
