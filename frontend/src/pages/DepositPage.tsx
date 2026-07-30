import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router'
import { toast } from 'sonner'
import MoneyForm from '@/components/transactions/MoneyForm'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { useBank } from '@/context/BankContext'
import { paths } from '@/routes/paths'

const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' })

function DepositPage() {
  const { selectedAccount, moveMoney } = useBank()
  const navigate = useNavigate(); const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  async function handleSubmit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); setError(''); setBusy(true); const form = new FormData(event.currentTarget)
    try { const amount = Number(form.get('amount')); await moveMoney('deposit', amount); toast.success(`${money.format(amount)} deposited`); navigate(paths.account) }
    catch (caught) { setError(caught instanceof Error ? caught.message : 'Deposit failed.') } finally { setBusy(false) }
  }
  return <main className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center px-5 py-12">{error && <Alert className="mb-4" variant="destructive"><AlertDescription>{error}</AlertDescription></Alert>}<MoneyForm action="deposit" balance={selectedAccount ? money.format(selectedAccount.balance) : undefined} busy={busy} onSubmit={handleSubmit} /></main>
}
export default DepositPage
