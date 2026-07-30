import PageHeader from '@/components/layout/PageHeader'
import TransactionTable from '@/components/transactions/TransactionTable'
import { sampleTransactions } from '@/data/sampleTransactions'
import { paths } from '@/routes/paths'

function TransactionHistoryPage() {
  return (
    <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-6 px-6 py-10">
      <PageHeader
        action={{ label: 'Back to account', to: paths.account }}
        description="Transactions for checking account 1001, newest first."
        title="Transaction history"
      />

      <TransactionTable
        description="All account activity is listed from newest to oldest."
        title="All transactions"
        transactions={sampleTransactions}
      />
    </main>
  )
}

export default TransactionHistoryPage
