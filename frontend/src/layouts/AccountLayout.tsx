import { Outlet } from 'react-router'
import AccountNavigation from '@/components/account/AccountNavigation'
import { BankProvider } from '@/context/BankContext'

function AccountLayout() {
  return (
    <BankProvider>
      <div className="app-shell min-h-screen text-foreground">
        <div className="app-frame"><AccountNavigation /><Outlet /></div>
      </div>
    </BankProvider>
  )
}

export default AccountLayout
