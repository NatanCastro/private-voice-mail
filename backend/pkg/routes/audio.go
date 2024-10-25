package routes

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"

	"github.com/NatanCastro/private-voice-mail/backend/internal/audio"
)

func BindAudioRoutes(ac *AudioController, mux *http.ServeMux) {
	mux.HandleFunc("POST /audio", ac.SaveAudio)
	mux.HandleFunc("GET /audio/file/{id}", ac.GetAudio)
}

type AudioController struct {
	store *audio.AudioService
}

func NewAudioController(s *audio.AudioService) *AudioController {
	as := &AudioController{
		store: s,
	}
	return as
}

func (ac *AudioController) SaveAudio(w http.ResponseWriter, r *http.Request) {
	if r.Header.Get("Content-Type") == "" || !isMultipartFormData(r.Header.Get("Content-Type")) {
		http.Error(w, "request Content-Type isn't multipart/form-data", http.StatusBadRequest)
		log.Println("ERROR: request Content-Type isn't multipart/form-data")
		return
	}

	err := r.ParseMultipartForm(10 << 20)
	if err != nil {
		http.Error(w, "Unable to parse form data", http.StatusBadRequest)
		log.Printf("ERROR: Failed to parse form data: %v\n", err)
		return
	}

	file, file_header, err := r.FormFile("audio")
	if err != nil {
		log.Printf("ERROR: Could not read audio file from form: %v\n", err)
		http.Error(w, "Could not read audio file from form", http.StatusBadRequest)
		return
	}
	defer file.Close()

	buf := bytes.NewBuffer(nil)
	if _, err := io.Copy(buf, file); err != nil {
		log.Printf("ERROR: Could not read file content: %v\n", err)
		http.Error(w, "Something went wrong while reading the file", http.StatusInternalServerError)
		return
	}

	file_id, err := ac.store.Save(file_header.Filename, string(file_header.Header["Content-Type"][0]), buf.Bytes())
	if err != nil {
		log.Printf("ERROR: Something went wrong while saving file: %v\n", err)
		http.Error(w, "Something went wrong while saving file", http.StatusInternalServerError)
		return
	}

	response, err := json.Marshal(audio.Audio{Id: file_id, Name: file_header.Filename})
	if err != nil {
		log.Printf("ERROR: Failed to create response JSON: %v", err)
		http.Error(w, "Something went wrong", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(http.StatusCreated)
	w.Write(response)
}

func isMultipartFormData(contentType string) bool {
	return strings.Contains(contentType, "multipart/form-data")
}

func (ac *AudioController) GetAudio(w http.ResponseWriter, r *http.Request) {
	audio_id, err := strconv.Atoi(r.PathValue("id"))
	if err != nil {
		http.Error(w, "Invalid audio Id format", http.StatusBadRequest)
		return
	}

	audio_data, err := ac.store.Get(audio_id)
	if err != nil {
		re, ok := err.(*audio.ReadingFileError)

		if ok {
			response, err := json.Marshal(re)
			if err != nil {
				http.Error(w, "somethign went wrong", http.StatusInternalServerError)
			}
			switch re.ErrorCode {
			case 1:
				w.WriteHeader(http.StatusBadRequest)
				w.Write(response)
				return
			case 2:
				w.WriteHeader(http.StatusInternalServerError)
				w.Write(response)
				return
			}
		}
	}

	w.Header().Set("Content-Type", audio_data.MimeType)
	w.Write(audio_data.Data)
}
