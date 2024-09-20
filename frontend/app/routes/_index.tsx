import type { MetaFunction } from '@remix-run/node'
import { AudioRecorder } from '~/components/audio-recorder'

export const meta: MetaFunction = () => {
  return [
    { title: 'Voice mail' },
    { name: 'description', content: 'record your voice here and save it for later' },
  ]
}

export default function Index() {
  return (
    <div className="bg-zinc-800 h-screen grid place-items-center">
      <AudioRecorder />
    </div>
  )
}
