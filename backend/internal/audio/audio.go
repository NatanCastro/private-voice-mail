package audio

import (
	"errors"
	"fmt"
	"os"
)

type Audio struct {
	Id        int    `json:"id"`
	Name      string `json:"name"`
	Extension string `json:"-"`
	MimeType  string `json:"-"`
	Size      int    `json:"-"` // size of the audio in bytes
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
