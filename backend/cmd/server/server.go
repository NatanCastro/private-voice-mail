package main

import (
	"fmt"
	"log/slog"
	"net/http"

	"github.com/NatanCastro/private-voice-mail/backend/internal/audio"
	"github.com/NatanCastro/private-voice-mail/backend/pkg/rabbitmq"
	"github.com/NatanCastro/private-voice-mail/backend/pkg/routes"
	"github.com/streadway/amqp"
)

func main() {
	audio.CreateAudioFolder()
	defer (func() {
		err := recover()
		fmt.Printf("ERROR: %v\n", err)
	})()
	mux := http.NewServeMux()

	rabbitClient, err := rabbitmq.NewRabbitClient("amqp://user:password@localhost:5672/")
	if err != nil {
		panic(fmt.Errorf("Could not connnect to rabbitmq, %v", err))
	}
	defer rabbitClient.Close()

	msgs, err := rabbitClient.ConsumeMessages("stt_response_exchange", "response", "stt_response")
	if err != nil {
		slog.Error("Failed to consume messages", slog.String("error", err.Error()))
		return
	}

	go func() {
		for d := range msgs {
			go func(delivery amqp.Delivery) {
				fmt.Printf("response: %s", string(delivery.Body))
				delivery.Ack(false)
			}(d)
		}
	}()

	rabbitMQData := audio.NewRabbitMQData(rabbitClient, "stt_request_exchange", "request", "stt_request")
	audioService := audio.NewAudioService(rabbitMQData)
	audioController := routes.NewAudioController(audioService)

	routes.BindAudioRoutes(audioController, mux)

	fmt.Println("INFO: starting server at http://localhost:8000")
	http.ListenAndServe("localhost:8000", mux)
}
