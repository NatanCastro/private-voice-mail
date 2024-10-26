package files

import (
	"bytes"
	"fmt"
	"net/http"
	"net/url"
	"time"

	"github.com/NatanCastro/private-voice-mail/backend/internal/config"
)

type FileService struct {
	EnvService *config.EnvService
}

func NewFileService(envService *config.EnvService) *FileService {
	return &FileService{
		EnvService: envService,
	}
}

func (fs *FileService) Save(schema string, path string, fileName string, data []byte) (string, error) {
	savedFilePath := fmt.Sprintf("%s://%s/%s/%s", schema, fs.EnvService.FileServer, path, fileName)

	userInfo := url.UserPassword(fs.EnvService.FileServerUser, fs.EnvService.FileServerPassword)
	url := url.URL{
		Scheme: schema,
		Host:   fs.EnvService.FileServer,
		Path:   fmt.Sprintf("%s/%s", "files", fileName),
		User:   userInfo,
	}

	uploadUrl := url.String()
	bodyReader := bytes.NewReader(data)
	resquest, err := http.NewRequest(http.MethodPut, uploadUrl, bodyReader)

	client := http.Client{
		Timeout: 30 * time.Second,
	}

	if err != nil {
		return "", err
	}

	response, err := client.Do(resquest)

	fmt.Printf("%v\n", response)

	if err != nil {
		return "", err
	}

	return savedFilePath, nil
}
