package main

import (
	"fmt"
	"net/http"

	"github.com/NatanCastro/private-voice-mail/backend/audio"
)

func main() {
	audio.CreateAudioFolder()
	defer (func() {
		err := recover()
		fmt.Printf("ERROR: %v\n", err)
	})()
	mux := http.NewServeMux()

	audioController := audio.NewAudioController(audio.NewAudioStore())

	audio.BindAudioRoutes(audioController, mux)

	fmt.Println("INFO: starting server at http://localhost:8000")
	http.ListenAndServe("localhost:8000", mux)
}
