package audio

import (
	"errors"
	"fmt"
	"net/http"
	"os"
)

type Audio struct {
	Id   int    `json:"id"`
	Name string `json:"name"`
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

func BindAudioRoutes(ac *AudioController, mux *http.ServeMux) {
	mux.HandleFunc("POST /audio", ac.SaveAudio)
}
