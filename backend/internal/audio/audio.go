package audio

import (
	"errors"
	"fmt"
	"os"

	"github.com/google/uuid"
)

type Audio struct {
	Id        uuid.UUID `json:"id"`
	Name      string    `json:"name"`
	Extension string    `json:"extention"`
	MimeType  string    `json:"mime_type"`
	Path      string    `json:"path"`
}

func CreateAudioFolder() {
	_, err := os.Stat("audios")
	if errors.Is(err, os.ErrNotExist) {
		err = os.Mkdir("audios", os.ModePerm)
		if err != nil {
			fmt.Printf("ERROR: %v\n", err)
			os.Exit(1)
		}
	}
}
