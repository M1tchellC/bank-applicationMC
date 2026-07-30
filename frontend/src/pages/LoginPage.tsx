import type { FormEvent } from 'react'
import { useNavigate } from 'react-router'
import LoginForm from '@/components/auth/LoginForm'
import { paths } from '@/routes/paths'

function LoginPage() {
  const navigate = useNavigate()

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    // Later: call the backend login service and navigate only on success.
    navigate(paths.account)
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-md flex-col justify-center gap-6 px-6 py-10">
      <LoginForm onSubmit={handleSubmit} />

      <p className="text-sm text-muted-foreground">
        Login authentication will be connected to the backend later.
      </p>
    </main>
  )
}

export default LoginPage
