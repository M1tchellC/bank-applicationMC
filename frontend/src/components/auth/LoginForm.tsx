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

interface LoginFormProps {
  onSubmit: FormEventHandler<HTMLFormElement>
}

function LoginForm({ onSubmit }: LoginFormProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <h1>Welcome back</h1>
        </CardTitle>
        <CardDescription>Log in to view your bank account.</CardDescription>
      </CardHeader>

      <form className="flex flex-col gap-6" onSubmit={onSubmit}>
        <CardContent>
          <FieldGroup className="gap-4">
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
              <FieldLabel htmlFor="password">Password</FieldLabel>
              <Input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
              />
            </Field>
          </FieldGroup>
        </CardContent>

        <CardFooter className="flex-col gap-3">
          <Button className="w-full" size="lg" type="submit">
            Log in
          </Button>
          <Button
            className="w-full"
            nativeButton={false}
            render={<Link to={paths.createAccount} />}
            size="lg"
            variant="outline"
          >
            Create an account
          </Button>
        </CardFooter>
      </form>
    </Card>
  )
}

export default LoginForm
