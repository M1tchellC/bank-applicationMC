import type { FormEventHandler } from 'react'
import { Link } from 'react-router'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Field, FieldGroup, FieldLabel } from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { paths } from '@/routes/paths'

const moneyFormCopy = {
  deposit: {
    description: 'Enter the amount you want to add to your account.',
    fieldLabel: 'Deposit amount',
    submitLabel: 'Submit deposit',
    title: 'Deposit money',
  },
  withdraw: {
    description: 'Enter the amount you want to remove from your account.',
    fieldLabel: 'Withdrawal amount',
    submitLabel: 'Submit withdrawal',
    title: 'Withdraw money',
  },
} as const

export type MoneyAction = keyof typeof moneyFormCopy

interface MoneyFormProps {
  action: MoneyAction
  onSubmit: FormEventHandler<HTMLFormElement>
}

function MoneyForm({ action, onSubmit }: MoneyFormProps) {
  const copy = moneyFormCopy[action]
  const amountId = `${action}-amount`

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <h1>{copy.title}</h1>
        </CardTitle>
        <CardDescription>{copy.description}</CardDescription>
      </CardHeader>

      <form className="flex flex-col gap-6" onSubmit={onSubmit}>
        <CardContent>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor={amountId}>{copy.fieldLabel}</FieldLabel>
              <Input
                id={amountId}
                name="amount"
                type="number"
                inputMode="decimal"
                min="0.01"
                step="0.01"
                placeholder="0.00"
                required
              />
            </Field>
          </FieldGroup>
        </CardContent>

        <CardFooter className="flex-col gap-3">
          <Button className="w-full" size="lg" type="submit">
            {copy.submitLabel}
          </Button>
          <Button
            className="w-full"
            nativeButton={false}
            render={<Link to={paths.account} />}
            size="lg"
            variant="outline"
          >
            Cancel
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}

export default MoneyForm
