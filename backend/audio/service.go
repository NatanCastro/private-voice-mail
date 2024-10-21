package audio

import (
	"errors"
	"fmt"
	"os"
	"strings"
	"sync"
)

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

func (as *AudioStore) Save(fileName string, audioData []byte) (int, error) {
	as.Lock()

	file_id := as.NextId
	new_file_name := fmt.Sprintf("%d.%s", file_id, strings.Split(fileName, ".")[1])
	file_path := fmt.Sprintf("%s/%s", "audios", new_file_name)

	err := os.WriteFile(file_path, audioData, os.ModePerm)
	if err != nil {
		fmt.Printf("ERROR: %v\n", err)
		return -1, errors.New("Could not save file")
	}

	as.Audios[as.NextId] = Audio{
		Id:   file_id,
		Name: fileName,
	}

	as.NextId++

	return file_id, nil
}
