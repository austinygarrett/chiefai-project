import { AuthLayout } from '@/components/layouts/auth-layout';
import { LoginRegisterForm } from '@/features/auth/components/login-register-form';
export const LoginRoute = () => {
  return (
    <AuthLayout>
      <LoginRegisterForm onSuccess={() => {}} />
    </AuthLayout>
  );
};
