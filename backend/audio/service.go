package audio

import (
	"bytes"
	"errors"
	"fmt"
	"io"
	"os"
	"strings"
	"sync"
)

type ReadingFileError struct {
	Err       error  `json:"-"`
	ErrorCode int    `json:"error_code"`
	Message   string `json:"message"`
}

type AudioResponse struct {
	Data     []byte
	MimeType string
}

func NewReadingFileError(message string, code int) *ReadingFileError {
	return &ReadingFileError{
		Err:       errors.New(message),
		ErrorCode: code,
		Message:   message,
	}
}

func (rf *ReadingFileError) Error() string {
	return fmt.Sprintf("error code: %d\nmessage: %s", rf.ErrorCode, rf.Err)
}

type AudioStore struct {
	sync.Mutex

	Audios map[int]Audio
	NextId int
}

func NewAudioStore() *AudioStore {
	as := &AudioStore{
		Audios: make(map[int]Audio),
		NextId: 0,
	}
	return as
}

func (as *AudioStore) Save(fileName, mimeType string, audioData []byte) (int, error) {
	as.Lock()

	file_id := as.NextId
	file_ext := strings.Split(fileName, ".")[1]
	new_file_name := fmt.Sprintf("%d.%s", file_id, file_ext)
	file_path := fmt.Sprintf("%s/%s", "audios", new_file_name)

	err := os.WriteFile(file_path, audioData, os.ModePerm)
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		return -1, errors.New("Could not save file")
	}

	as.Audios[as.NextId] = Audio{
		Id:        file_id,
		Name:      fileName,
		Extension: file_ext,
		MimeType:  mimeType,
		Size:      len(audioData),
	}

	as.NextId++

	return file_id, nil
}

func (as *AudioStore) Get(id int) (*AudioResponse, error) {

	if id < 0 || id > as.NextId {
		return nil, NewReadingFileError(fmt.Sprintf("Audio file with the id %d does not exists", id), 1)
	}

	audio_data := as.Audios[id]

	audio_file_path := fmt.Sprintf("audios/%d.%s", id, audio_data.Extension)

	_, err := os.Stat(audio_file_path)
	if err != nil && errors.Is(err, os.ErrNotExist) {
		return nil, NewReadingFileError("Could not find audio file", 1)
	}

	file, err := os.Open(audio_file_path)
	if err != nil {
		return nil, NewReadingFileError("Something went wrong", 2)
	}
	defer file.Close()

	buf := bytes.NewBuffer(nil)
	if _, err := io.Copy(buf, file); err != nil {
		fmt.Printf("ERROR: Could not read file content: %v\n", err)
		return nil, NewReadingFileError("Something went wrong while reading the file", 2)
	}

	response := &AudioResponse{
		Data:     buf.Bytes(),
		MimeType: audio_data.MimeType,
	}

	return response, nil
}
