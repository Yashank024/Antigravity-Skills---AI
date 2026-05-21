const { execSync } = require('child_process');

console.log('Running test suite in watch mode...');
try {
  // Checks if the project uses vitest or jest, defaulting to npm run test
  execSync('npm run test -- --watch', { stdio: 'inherit' });
} catch (error) {
  console.error('Test execution failed. Ensure testing dependencies are installed.');
  process.exit(1);
}
