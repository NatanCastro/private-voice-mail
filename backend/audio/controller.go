package audio

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"net/http"
	"strings"
)

type AudioController struct {
	store *AudioStore
}

func NewAudioController(s *AudioStore) *AudioController {
	as := &AudioController{
		store: s,
	}
	return as
}

func (as *AudioController) SaveAudio(w http.ResponseWriter, r *http.Request) {
	if r.Header.Get("Content-Type") == "" || !isMultipartFormData(r.Header.Get("Content-Type")) {
		http.Error(w, "request Content-Type isn't multipart/form-data", http.StatusBadRequest)
		log.Println("ERROR: request Content-Type isn't multipart/form-data")
		return
	}

	err := r.ParseMultipartForm(10 << 20) // 10 MB limit
	if err != nil {
		http.Error(w, "Unable to parse form data", http.StatusBadRequest)
		log.Printf("ERROR: Failed to parse form data: %v\n", err)
		return
	}

	file, fileHeader, err := r.FormFile("audio")
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

	fileID, err := as.store.Save(fileHeader.Filename, buf.Bytes())
	if err != nil {
		log.Printf("ERROR: Something went wrong while saving file: %v\n", err)
		http.Error(w, "Something went wrong while saving file", http.StatusInternalServerError)
		return
	}

	response, err := json.Marshal(Audio{Id: fileID, Name: fileHeader.Filename})
	if err != nil {
		log.Printf("ERROR: Failed to create response JSON: %v", err)
		http.Error(w, "Something went wrong", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(http.StatusOK)
	w.Write(response)
}

func isMultipartFormData(contentType string) bool {
	return strings.Contains(contentType, "multipart/form-data")
}
