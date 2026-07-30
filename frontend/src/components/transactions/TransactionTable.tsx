import { Link } from 'react-router'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import type { Transaction } from '@/types/transaction'

interface TransactionTableAction {
  label: string
  to: string
}

interface TransactionTableProps {
  action?: TransactionTableAction
  description: string
  title: string
  transactions: Transaction[]
}

function TransactionTable({
  action,
  description,
  title,
  transactions,
}: TransactionTableProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <h2>{title}</h2>
        </CardTitle>
        <CardDescription>{description}</CardDescription>
        {action ? (
          <CardAction>
            <Button
              nativeButton={false}
              render={<Link to={action.to} />}
              size="sm"
              variant="outline"
            >
              {action.label}
            </Button>
          </CardAction>
        ) : null}
      </CardHeader>

      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead scope="col">Transaction ID</TableHead>
              <TableHead scope="col">Type</TableHead>
              <TableHead className="text-right" scope="col">
                Amount
              </TableHead>
              <TableHead scope="col">Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {transactions.length > 0 ? (
              transactions.map((transaction) => (
                <TableRow key={transaction.id}>
                  <TableCell>{transaction.id}</TableCell>
                  <TableCell>
                    <Badge
                      variant={
                        transaction.type === 'Deposit' ? 'secondary' : 'outline'
                      }
                    >
                      {transaction.type}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right font-medium">
                    {transaction.amount}
                  </TableCell>
                  <TableCell>{transaction.date}</TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell className="h-24 text-center" colSpan={4}>
                  No transactions yet.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}

export default TransactionTable
