package audio

import (
	"context"
	"fmt"
	"strings"

	"github.com/NatanCastro/private-voice-mail/backend/internal/config"
	"github.com/NatanCastro/private-voice-mail/backend/internal/database"
	"github.com/NatanCastro/private-voice-mail/backend/internal/files"
	"github.com/NatanCastro/private-voice-mail/backend/internal/rabbitmq"
	"github.com/google/uuid"
)

type AudioService struct {
	RabbitMQClient  *rabbitmq.RabbitClient
	FileService     *files.FileService
	EnvService      *config.EnvService
	DatabaseQueries *database.Queries
}

func NewAudioService(
	rabbitMQClient *rabbitmq.RabbitClient,
	fileService *files.FileService,
	envService *config.EnvService,
	databaseQueries *database.Queries,
) *AudioService {
	return &AudioService{
		RabbitMQClient:  rabbitMQClient,
		FileService:     fileService,
		EnvService:      envService,
		DatabaseQueries: databaseQueries,
	}
}

func (as *AudioService) Save(fileName, mimeType string, audioData []byte) (int, error) {
	ID := uuid.New()

	as.DatabaseQueries.InsertAudio(context.Background(), database.InsertAudioParams{})

	fileId := as.NextId
	fileParts := strings.Split(fileName, ".")
	fileExtention := fileParts[len(fileParts)-1]
	newFileName := fmt.Sprintf("%d.%s", fileId, fileExtention)

	path, err := as.FileService.Save("http", "files", newFileName, audioData)

	if err != nil {
		return -1, err
	}

	as.Audios[as.NextId] = Audio{
		Id:        fileId,
		Name:      fileName,
		Extension: fileExtention,
		MimeType:  mimeType,
		Path:      path,
	}

	as.NextId++

	return fileId, nil
}

func (as *AudioService) FindOne(id int) (*Audio, error) {
	audio, ok := as.Audios[id]
	if !ok {
		return nil, fmt.Errorf("Could not find audio with Id %d", id)
	}

	return &audio, nil
}

func (as *AudioService) SendAudioToStt(id int, language string) (string, error) {
	audio, err := as.FindOne(id)
	if err != nil {
		return "", fmt.Errorf("Could not send audio to stt: %v", err)
	}

	exchange := as.EnvService.SttRequestExchange
	routingKey := as.EnvService.SttRequestRoutingKey
	queue := as.EnvService.SttRequestQueue
	message := fmt.Sprintf("%d,%s,%s", id, audio.Path, language)
	as.RabbitMQClient.PublishMessage(exchange, routingKey, queue, []byte(message))

	return "Audio sent to stt, the result will come soon", nil
}
