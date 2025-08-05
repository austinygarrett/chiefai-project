import {
  Button,
  Paper,
  PasswordInput,
  Stack,
  TextInput,
  Text,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { useState } from 'react';

// eslint-disable-next-line import/no-restricted-paths
import { useLogin, loginInputSchema, useRegister } from '@/lib/auth';
import logo from '@/assets/images/chiefai-logo-inverse.png';
import './login-register.scss';
type LoginFormProps = {
  onSuccess: () => void;
  tier?: string;
  period?: string;
  coderef?: string;
  hideHeaderText?: boolean;
};

export const LoginRegisterForm = ({
  onSuccess,
  tier,
  period,
  coderef,
  hideHeaderText,
  ...props
}: LoginFormProps) => {
  const login = useLogin({
    onSuccess: (data) => {
      if (!data) {
        setLoginError(true);
      }
    },
  });

  const [loginError, setLoginError] = useState(false);
  const form = useForm({
    initialValues: {
      email: '',
      password: '',
    },
    validate: (values) => {
      // Parse the entire object with our Zod schema
      const result = loginInputSchema.safeParse(values);

      // If the parse fails, gather errors and return them in Mantine's format
      if (!result.success) {
        const errors: Record<string, string> = {};

        for (const issue of result.error.issues) {
          // If any issue is found for the password field, set a single error message
          if (issue.path[0] === 'password') {
            errors.password = 'Password does not meet the requirements';
          }

          // Similarly for email
          if (issue.path[0] === 'email') {
            errors.email = issue.message;
          }
        }

        return errors;
      }

      return {};
    },
  });

  return (
    <Paper
      className="login-register-container"
      radius="md"
      p="xl"
      withBorder
      {...props}
    >
      <img src={logo} style={{ maxHeight: '50px' }} alt="Workflow" />

      <h1 className="intro-text">Technical Project</h1>

      {loginError && (
        <Text className="login-error-text">Invalid username or password</Text>
      )}
      <form
        onSubmit={form.onSubmit((values) => {
          login.mutate(values);
        })}
      >
        <Stack style={{ width: '100%' }}>
          <TextInput
            size="md"
            required
            label="Email"
            placeholder="Email"
            value={form.values.email}
            onChange={(event) =>
              form.setFieldValue('email', event.currentTarget.value)
            }
            error={form.errors.email && 'Invalid email'}
            radius="md"
          />

          <PasswordInput
            size="md"
            required
            label="Password"
            placeholder="Your password"
            value={form.values.password}
            onChange={(event) =>
              form.setFieldValue('password', event.currentTarget.value)
            }
            radius="md"
          />
          <Button size="md" className="submit-button" type="submit">
            Login
          </Button>
        </Stack>
      </form>
    </Paper>
  );
};
