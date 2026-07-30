import { Link } from 'react-router'
import { Button } from '@/components/ui/button'
import { paths } from '@/routes/paths'

function AccountNavigation() {
  return (
    <header className="border-b">
      <div className="mx-auto flex w-full max-w-5xl flex-wrap items-center justify-between gap-4 px-6 py-4">
        <Button
          nativeButton={false}
          render={<Link to={paths.account} />}
          variant="link"
        >
          Bank Application
        </Button>

        <nav aria-label="Account navigation">
          <ul className="flex flex-wrap items-center gap-1">
            <li>
              <Button
                nativeButton={false}
                render={<Link to={paths.account} />}
                variant="ghost"
              >
                Account
              </Button>
            </li>
            <li>
              <Button
                nativeButton={false}
                render={<Link to={paths.transactions} />}
                variant="ghost"
              >
                Transactions
              </Button>
            </li>
            <li>
              <Button
                nativeButton={false}
                render={<Link to={paths.login} />}
                variant="ghost"
              >
                Return to login
              </Button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  )
}

export default AccountNavigation
