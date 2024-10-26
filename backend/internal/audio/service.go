package audio

import (
	"fmt"
	"strings"
	"sync"

	"github.com/NatanCastro/private-voice-mail/backend/internal/files"
	"github.com/NatanCastro/private-voice-mail/backend/pkg/rabbitmq"
)

type AudioService struct {
	sync.Mutex

	Audios map[int]Audio
	NextId int

	RabbitMQClient *rabbitmq.RabbitClient
	FileService    *files.FileService
}

func NewAudioService(rabbitMQClient *rabbitmq.RabbitClient, fileService *files.FileService) *AudioService {
	return &AudioService{
		Audios:         make(map[int]Audio),
		NextId:         0,
		RabbitMQClient: rabbitMQClient,
		FileService:    fileService,
	}
}

func (as *AudioService) Save(fileName, mimeType string, audioData []byte) (int, error) {
	as.Lock()
	defer as.Unlock()

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
	_, err := as.FindOne(id)
	if err != nil {
		return "", fmt.Errorf("Could not send audio to stt: %v", err)
	}

	return "", nil
}
