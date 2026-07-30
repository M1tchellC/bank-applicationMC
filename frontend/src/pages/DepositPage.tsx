import type { FormEvent } from 'react'
import { useNavigate } from 'react-router'
import MoneyForm from '@/components/transactions/MoneyForm'
import { paths } from '@/routes/paths'

function DepositPage() {
  const navigate = useNavigate()

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    // Later: POST the amount to /accounts/{accountId}/deposit first.
    navigate(paths.account)
  }

  return (
    <main className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center px-6 py-10">
      <MoneyForm action="deposit" onSubmit={handleSubmit} />
    </main>
  )
}

export default DepositPage
