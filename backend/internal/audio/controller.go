package audio

import (
	"bytes"
	"encoding/json"
	"io"
	"log"
	"log/slog"
	"net/http"
	"strconv"
	"strings"
)

func BindAudioRoutes(ac *AudioController, mux *http.ServeMux) {
	mux.HandleFunc("POST /audio", ac.SaveAudio)
	mux.HandleFunc("GET /audio/{id}", ac.GetAudioById)
}

type AudioController struct {
	store *AudioService
}

func NewAudioController(s *AudioService) *AudioController {
	as := &AudioController{
		store: s,
	}
	return as
}

func (ac *AudioController) SaveAudio(w http.ResponseWriter, r *http.Request) {
	if r.Header.Get("Content-Type") == "" || !isMultipartFormData(r.Header.Get("Content-Type")) {
		slog.Error("ERROR: request Content-Type isn't multipart/form-data")
		http.Error(w, "request Content-Type isn't multipart/form-data", http.StatusBadRequest)
		return
	}

	err := r.ParseMultipartForm(10 << 20)
	if err != nil {
		slog.Error("ERROR: Failed to parse form data: ", err)
		http.Error(w, "Unable to parse form data", http.StatusBadRequest)
		return
	}

	file, file_header, err := r.FormFile("audio")
	if err != nil {
		slog.Error("ERROR: Could not read audio file from form: ", err)
		http.Error(w, "Could not read audio file from form", http.StatusBadRequest)
		return
	}
	defer file.Close()

	buf := bytes.NewBuffer(nil)
	if _, err := io.Copy(buf, file); err != nil {
		slog.Error("ERROR: Could not read file content: ", err)
		http.Error(w, "Something went wrong while reading the file", http.StatusInternalServerError)
		return
	}

	file_id, err := ac.store.Save(file_header.Filename, string(file_header.Header["Content-Type"][0]), buf.Bytes())
	if err != nil {
		slog.Error("ERROR: Something went wrong while saving file: ", err)
		http.Error(w, "Something went wrong while saving file", http.StatusInternalServerError)
		return
	}

	response, err := json.Marshal(Audio{Id: file_id, Name: file_header.Filename})
	if err != nil {
		slog.Error("ERROR: Failed to create response JSON: ", err)
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

func (ac *AudioController) GetAudioById(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.Atoi(r.PathValue("id"))

	if err != nil {
		slog.Error("invalid ID ", err)
		http.Error(w, "invalid ID", http.StatusBadRequest)
	}

	ac.store.FindOne(id)
}
