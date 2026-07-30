import { Link } from 'react-router'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { paths } from '@/routes/paths'

interface AccountSummaryCardProps {
  accountId: number
  accountType: string
  balance: string
}

function AccountSummaryCard({
  accountId,
  accountType,
  balance,
}: AccountSummaryCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <h2>Account overview</h2>
        </CardTitle>
        <CardDescription>
          Your current account information and available actions.
        </CardDescription>
      </CardHeader>

      <CardContent className="flex flex-col gap-6">
        <div className="flex flex-col gap-1">
          <p className="text-sm text-muted-foreground">Current balance</p>
          <p className="font-heading text-4xl font-semibold">{balance}</p>
        </div>

        <dl className="grid gap-3 text-sm">
          <div className="flex items-center justify-between gap-4">
            <dt className="text-muted-foreground">Account ID</dt>
            <dd className="font-medium">{accountId}</dd>
          </div>
          <div className="flex items-center justify-between gap-4">
            <dt className="text-muted-foreground">Account type</dt>
            <dd>
              <Badge variant="secondary">{accountType}</Badge>
            </dd>
          </div>
        </dl>
      </CardContent>

      <CardFooter className="flex-col items-stretch gap-3 sm:flex-row">
        <Button
          nativeButton={false}
          render={<Link to={paths.deposit} />}
          size="lg"
        >
          Deposit
        </Button>
        <Button
          nativeButton={false}
          render={<Link to={paths.withdraw} />}
          size="lg"
          variant="outline"
        >
          Withdraw
        </Button>
      </CardFooter>
    </Card>
  )
}

export default AccountSummaryCard
