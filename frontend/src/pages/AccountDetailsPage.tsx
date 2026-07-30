import AccountSummaryCard from '@/components/account/AccountSummaryCard'
import PageHeader from '@/components/layout/PageHeader'
import TransactionTable from '@/components/transactions/TransactionTable'
import { recentTransactions } from '@/data/sampleTransactions'
import { paths } from '@/routes/paths'

function AccountDetailsPage() {
  return (
    <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-8 px-6 py-10">
      <PageHeader eyebrow="Welcome back" title="Jordan Lee" />

      <AccountSummaryCard
        accountId={1001}
        accountType="Checking"
        balance="$4,280.16"
      />

      <TransactionTable
        action={{ label: 'View transactions', to: paths.transactions }}
        description="The newest account activity appears first."
        title="Recent transactions"
        transactions={recentTransactions}
      />

      <p className="text-sm text-muted-foreground">
        Sample account data is shown until authentication is connected.
      </p>
    </main>
  )
}

export default AccountDetailsPage
