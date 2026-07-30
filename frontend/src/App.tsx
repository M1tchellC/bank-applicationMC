import { Navigate, Route, Routes } from 'react-router'
import AccountLayout from '@/layouts/AccountLayout'
import AccountDetailsPage from '@/pages/AccountDetailsPage'
import CreateAccountPage from '@/pages/CreateAccountPage'
import DepositPage from '@/pages/DepositPage'
import LoginPage from '@/pages/LoginPage'
import TransactionHistoryPage from '@/pages/TransactionHistoryPage'
import WithdrawPage from '@/pages/WithdrawPage'
import { paths } from '@/routes/paths'

function App() {
  return (
    <Routes>
      <Route path={paths.login} element={<LoginPage />} />
      <Route path={paths.createAccount} element={<CreateAccountPage />} />

      <Route path={paths.account} element={<AccountLayout />}>
        <Route index element={<AccountDetailsPage />} />
        <Route path="deposit" element={<DepositPage />} />
        <Route path="withdraw" element={<WithdrawPage />} />
        <Route path="transactions" element={<TransactionHistoryPage />} />
      </Route>

      <Route path="*" element={<Navigate to={paths.login} replace />} />
    </Routes>
  )
}

export default App
