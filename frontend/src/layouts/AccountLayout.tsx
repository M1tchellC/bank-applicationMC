import { Outlet } from 'react-router'
import AccountNavigation from '@/components/account/AccountNavigation'

function AccountLayout() {
  // Add the backend session check here later. If the user is not logged in,
  // redirect to paths.login instead of rendering the Outlet.
  return (
    <div className="flex min-h-screen flex-col bg-background text-foreground">
      <AccountNavigation />

      <Outlet />
    </div>
  )
}

export default AccountLayout
