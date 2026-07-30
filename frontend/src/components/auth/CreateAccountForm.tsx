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
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { paths } from '@/routes/paths'

const accountTypes = [
  { label: 'Checking', value: 'CHECKING' },
  { label: 'Savings', value: 'SAVINGS' },
]

interface CreateAccountFormProps {
  onSubmit: FormEventHandler<HTMLFormElement>
}

function CreateAccountForm({ onSubmit }: CreateAccountFormProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <h1>Create an account</h1>
        </CardTitle>
        <CardDescription>
          Enter your information and choose an account type.
        </CardDescription>
      </CardHeader>

      <form className="flex flex-col gap-6" onSubmit={onSubmit}>
        <CardContent>
          <FieldGroup className="gap-4">
            <Field>
              <FieldLabel htmlFor="name">Full name</FieldLabel>
              <Input
                id="name"
                name="name"
                type="text"
                autoComplete="name"
                required
              />
            </Field>

            <Field>
              <FieldLabel htmlFor="email">Email address</FieldLabel>
              <Input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
              />
            </Field>

            <Field>
              <FieldLabel htmlFor="account-type">Account type</FieldLabel>
              <Select items={accountTypes} name="accountType" required>
                <SelectTrigger className="w-full" id="account-type">
                  <SelectValue placeholder="Select an account type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    {accountTypes.map((accountType) => (
                      <SelectItem key={accountType.value} value={accountType.value}>
                        {accountType.label}
                      </SelectItem>
                    ))}
                  </SelectGroup>
                </SelectContent>
              </Select>
            </Field>
          </FieldGroup>
        </CardContent>

        <CardFooter className="flex-col gap-3">
          <Button className="w-full" size="lg" type="submit">
            Create account
          </Button>
          <Button
            className="w-full"
            nativeButton={false}
            render={<Link to={paths.login} />}
            size="lg"
            variant="outline"
          >
            Back to login
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}

export default CreateAccountForm
