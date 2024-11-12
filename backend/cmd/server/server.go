package main

import (
	"context"
	"fmt"
	"log/slog"
	"net/http"
	"os"

	"github.com/NatanCastro/private-voice-mail/backend/internal/audio"
	"github.com/NatanCastro/private-voice-mail/backend/internal/config"
	"github.com/NatanCastro/private-voice-mail/backend/internal/database"
	"github.com/NatanCastro/private-voice-mail/backend/internal/files"
	"github.com/NatanCastro/private-voice-mail/backend/internal/middleware"
	"github.com/NatanCastro/private-voice-mail/backend/internal/rabbitmq"

	"github.com/jackc/pgx/v5"
	"github.com/streadway/amqp"
)

func main() {
	audio.CreateAudioFolder()
	defer (func() {
		err := recover()
		fmt.Printf("ERROR: %v\n", err)
	})()

	mux := http.NewServeMux()

	middlewareStack := middleware.CreateStack(middleware.Logging)

	envService := config.NewEnvService()

	conn, err := pgx.Connect(context.Background(), envService.DatabaseUrl)
	if err != nil {
		os.Exit(1)
	}
	defer conn.Close(context.Background())
	q := database.New(conn)

	rabbitClient, err := rabbitmq.NewRabbitClient(envService)
	if err != nil {
		panic(fmt.Errorf("Could not connnect to rabbitmq, %v", err))
	}
	defer rabbitClient.Close()

	exchange := envService.SttResponseExchange
	routingKey := envService.SttResponseRoutingKey
	queue := envService.SttResponseQueue

	msgs, err := rabbitClient.ConsumeMessages(exchange, routingKey, queue)
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

	fileService := files.NewFileService(envService)
	audioService := audio.NewAudioService(rabbitClient, fileService, envService, q)
	audioController := audio.NewAudioController(audioService)

	audio.BindAudioRoutes(audioController, mux)

	fmt.Println("INFO: starting server at http://localhost:8000")
	http.ListenAndServe("localhost:8000", middlewareStack(mux))
}
