import React, { useState, useRef } from 'react'
import { pipe } from 'fp-ts/lib/function'
import { isSome, none, some, match as opMatch, Option } from 'fp-ts/lib/Option'
import { Button } from './ui/button'

export const AudioRecorder: React.FC = () => {
  const [isRecording, setIsRecording] = useState<boolean>(false)
  const [audioURL, setAudioURL] = useState<Option<string>>(none)
  const [mediaRecorder, setMediaRecorder] =
    useState<Option<MediaRecorder>>(none)
  const [_error, setError] = useState<Option<string>>(none)
  const audioChunksRef = useRef<Blob[]>([])

  const handleDataAvailable = (event: BlobEvent) => {
    audioChunksRef.current.push(event.data)
  }

  const handleStopRecording = () => {
    const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
    const audioUrl = URL.createObjectURL(audioBlob)
    setAudioURL(some(audioUrl))
    audioChunksRef.current = []
  }

  const startRecording = async () => {
    try {
      setError(none)
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)

      recorder.ondataavailable = handleDataAvailable
      recorder.onstop = handleStopRecording

      recorder.start()
      setMediaRecorder(some(recorder))
      setIsRecording(true)
    } catch (error) {
      setError(
        some('Failed to access microphone. Please check your permissions.')
      )
    }
  }

  const stopRecording = () => {
    pipe(
      mediaRecorder,
      opMatch(
        () => { },
        (mr) => {
          mr.stop()
          setIsRecording(false)
          setMediaRecorder(none)
        }
      )
    )
  }

  const saveAudio = () => {
    // TODO: implement saving audio to the cloud
    window.alert('saving audio to the cloud is not implemented')
  }

  const toggleRecording = () => {
    isRecording ? stopRecording() : startRecording()
  }

  return (
    <div className='w-svw h-svh flex flex-col items-center justify-between p-4 text-white'>
      <h1 className="text-4xl text-zinc-50">Audio Recorder</h1>

      <main className='flex flex-col items-center gap-8'>
        <Button
          onClick={toggleRecording}
          variant={isRecording ? 'destructive' : 'default'}
          size={'lg'}
          className='rounded-2xl'
        >
          {isRecording ? (
            'Stop Recording'
          ) : (
            'Start Recording'
          )}
        </Button>

        {isSome(audioURL) && (
          <div className='flex flex-col gap-8 items-center'>
            <audio controls src={audioURL.value}></audio>
            <div className='flex justify-between gap-4'>
              <Button className='rounded-2xl' size={'lg'} variant={'secondary'}>
                <a href={audioURL.value} download="recording.wav" className='float-right'>
                  Download Recording
                </a>
              </Button>
              <Button className='rounded-2xl' size={'lg'} onClick={saveAudio}>
                save audio
              </Button>
            </div>
          </div>
        )}
      </main>

      <footer className='w-svw px-4 text-justify'>
        Lorem ipsum dolor, sit amet consectetur adipisicing elit. Ipsum blanditiis repellendus et eligendi cumque eos mollitia, consectetur ea labore illo quae. Sequi inventore ullam doloremque? Tenetur numquam quaerat rerum ratione?
        Nam alias rerum deserunt, consectetur architecto dolorum eveniet possimus non dignissimos esse enim vel incidunt odit nulla porro rem delectus culpa saepe similique expedita animi, sed vitae? Dolores, architecto sapiente!
      </footer>
    </div>
  )
}
