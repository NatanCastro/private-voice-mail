package config

import "os"

type EnvService struct {
	FileServer         string
	FileServerUser     string
	FileServerPassword string

	// rabbitmq variables
	SttRequestExchange    string
	SttRequestRoutingKey  string
	SttRequestQueue       string
	SttResponseExchange   string
	SttResponseRoutingKey string
	SttResponseQueue      string
}

func getEnvOrDefault(variable, defaultValue string) string {
	if env, ok := os.LookupEnv(variable); ok {
		return env
	}
	return defaultValue
}

func NewEnvService() *EnvService {
	return &EnvService{
		FileServer:         getEnvOrDefault("FILE_SERVER", "localhost:8080"),
		FileServerUser:     getEnvOrDefault("FILE_SERVER_USER", "upload_user"),
		FileServerPassword: getEnvOrDefault("FILE_SERVER_PASSWORD", "pass"),

		SttRequestExchange:    getEnvOrDefault("STT_REQUEST_EXCHANGE", "stt_request_exchange"),
		SttRequestRoutingKey:  getEnvOrDefault("STT_REQUEST_ROUTINGKEY", "request"),
		SttRequestQueue:       getEnvOrDefault("STT_REQUEST_QUEUE", "sst_request"),
		SttResponseExchange:   getEnvOrDefault("STT_RESPONSE_EXCHANGE", "stt_reponse_exchange"),
		SttResponseRoutingKey: getEnvOrDefault("STT_RESPONSE_ROUTINGKEY", "response"),
		SttResponseQueue:      getEnvOrDefault("STT_RESPONSE_QUEUE", "sst_response"),
	}
}
