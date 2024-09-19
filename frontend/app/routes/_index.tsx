import type { MetaFunction } from '@remix-run/node'
import { AudioRecorder } from '~/components/audio-recorder'

export const meta: MetaFunction = () => {
  return [
    { title: 'New Remix App' },
    { name: 'description', content: 'Welcome to Remix!' },
  ]
}

export default function Index() {
  return (
    <div className="bg-zinc-800 h-screen grid place-items-center">
      <AudioRecorder />
    </div>
  )
}
