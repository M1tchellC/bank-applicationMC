import type { FormEvent } from 'react'
import { useNavigate } from 'react-router'
import CreateAccountForm from '@/components/auth/CreateAccountForm'
import { paths } from '@/routes/paths'

function CreateAccountPage() {
  const navigate = useNavigate()

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    // Later: create the user, create their account, then navigate on success.
    navigate(paths.account)
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-xl flex-col justify-center px-6 py-10">
      <CreateAccountForm onSubmit={handleSubmit} />
    </main>
  )
}

export default CreateAccountPage
