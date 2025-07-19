import { paths } from '@/config/paths';

export const NotFoundRoute = () => {
  return (
    <div>
      <h1>404 - Not Found</h1>
      <p>Sorry, the page you are looking for does not exist.</p>
      <a href={paths.home.getHref()}>Go to Home</a>
    </div>
  );
};
